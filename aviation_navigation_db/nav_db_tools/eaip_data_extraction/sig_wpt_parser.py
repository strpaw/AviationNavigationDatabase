"""
sig_wpt_parser.py module
This module provides extracting data operation from text files that contains significant waypoints
in the following format:
<waypoint_ident> <latitude> <longitude>
for example:
TEST1 304522.17N 0215543.45E
To extract data from file:
sgp = SignificantWaypointParser(ctr_iso3='POL') # Create instance of class for country 'POL'
sgp.set_coordinates(AF_DMSH)  # Set coordinates formats in which waypoints are stored
# Extract data from file data_file and insert to database
sgp.sig_point_txt_file_into_database(data_file, host, database, user, password)
"""
import os.path
from aviation_navigation_db.aviation_gis_toolkit.const import *
from aviation_navigation_db.aviation_gis_toolkit.coordinate_predetermined import CoordinatePredetermined
from aviation_navigation_db.nav_db_tools.db_tools.db_tools import DatabaseTools


class SignificantWaypointParser:

    def __init__(self, ctry_iso3):

        self.ctry_iso3 = ctry_iso3
        self.wpt_ident = ''
        self.lon_src = ''
        self.lat_src = ''
        self.lon_dd = ''
        self.lat_dd = ''
        self.err_msg = ''
        self.parsing_result = None
        self._lon = None
        self._lat = None
        self._ang_format = ''

    def set_coordinates(self, ang_format=AF_DMSH_COMP):
        """ Sets coordinates.
        :param: ang_format: const, format of coordinates, e.g. AF_DMSH_COMP
        """
        self._ang_format = ang_format
        self._lon = CoordinatePredetermined(self._ang_format, AT_LON)
        self._lat = CoordinatePredetermined(self._ang_format, AT_LAT)

    def parse_sig_point_line(self, line):
        """ Parses line of data file with significant points to extract data.
        :param line: str: line of  data file
        """
        # Examples of line
        # ABKEM 642855N 0254841E A, D, I L85 EFOU
        self.parsing_result = True
        self.err_msg = ''

        line_parts = line.split()
        if len(line_parts) >= 3:
            self.wpt_ident = line_parts[0]
            self.lat_src = line_parts[1]
            self.lon_src = line_parts[2]
            self.lon_dd = self._lon.coordinate_to_dd(self.lon_src)
            self.lat_dd = self._lat.coordinate_to_dd(self.lat_src)

            # ----------------- Validate parsed data -----------------

            # Check if waypoint name length is maximum 5
            if len(self.wpt_ident) > 5:
                self.parsing_result = False
                self.err_msg = 'Waypoint ident name length is > 5'

            # Check if coordinates match specified format
            if self.lon_dd is None or self.lat_dd is None:
                self.parsing_result = False
                self.err_msg += 'Coordinates are not in given format: {}'.format(self._ang_format)
        else:
            self.parsing_result = False
            self.err_msg = 'Less then three parts in line'

    def insert_sig_point_into_db(self, connection, cursor):
        """ Inserts single significant waypoint into database
        :param connection: connection to database object
        :param cursor: cursor object
        """

        cursor.execute("""INSERT INTO sig_waypoint 
                      (ctry_iso3,
                       wpt_ident,
                       lon_src,
                       lat_src,
                       location)
                       VALUES (%s, %s, %s, %s,
                               ST_GeomFromText('POINT(%s %s)', 4326));""",
                       (self.ctry_iso3,
                        self.wpt_ident,
                        self.lon_src,
                        self.lat_src,
                        self.lon_dd,
                        self.lat_dd))
        connection.commit()

    def sig_point_txt_file_into_database(self, data_file, host, database, user, password):
        """ Imports significant point text file into PostGIS database.
        :param data_file: str, text file with significant points
        :param host: str,
        :param database: str, database name
        :param user: str, user name of database
        :param password: str, password to database
        """
        if data_file.strip() != '':
            # Check if data file exists
            if os.path.isfile(data_file):
                with open(data_file, 'r', encoding='utf-8') as file:
                    # Connect to database
                    db = DatabaseTools(host, database, user, password)
                    conn = db.get_connection()
                    if conn:
                        cur = conn.cursor()
                        line_number = 0
                        for line in file:
                            line_number += 1
                            # Parse line to extract significant point data
                            self.parse_sig_point_line(line)
                            if self.parsing_result:
                                self.insert_sig_point_into_db(conn, cur)
                            else:  # Print errors why data is not parsed correctly
                                print('[Line nr: {}][Error: {}][Line: {}]'.format(line_number, self.err_msg,
                                                                                  line.strip('\n')))

                        cur.close()
                        conn.close()
            else:
                self.err_msg = 'Error: {} not a file.'.format(data_file)
        else:
            self.err_msg = 'Error: Data file name not given'

"""
etod_parser.py module
This module provides extracting data from eTOD csv files text files
"""

import csv
from aviation_navigation_db_tools.nav_db_tools.db_tools.db_tools import DatabaseTools
from aviation_navigation_db_tools.nav_db_tools.eaip_data_extraction.etod_mapping import *
from aviation_navigation_db_tools.aviation_gis_toolkit.coordinate_predetermined import *


class EtodParser:

    def __init__(self, ctry_name, etod_file):
        """
        :param: ctry_name: str, country name that defines rules of mapping fields from CSV file with obstacle attributes
                defined in _obstacle_data dictionary,
        :param: etod_file: str, ful path to CSV with data """

        self.ctry_name = ctry_name
        self.etod_file = etod_file
        self.etod_file_type = None
        self.ctry_iso3 = None
        self.coord_format = None
        self.vert_uom = None
        # self.coord_format = etod_csv_map[self.ctry_name]['COORD_FORMAT']
        self.obstacle_data = {'ctry_iso3': '',
                              'obst_id': '',
                              'obst_type': '',
                              'lon_src': '',
                              'lat_src': '',
                              'amsl': '',
                              'agl': '',
                              'vert_uom': '',
                              'lighting': '',
                              'marking': '',
                              'lon_dd': '',
                              'lat_dd': ''}

    def init_data(self):
        self.etod_file_type = etod_map[self.ctry_name]['file_type']
        self.ctry_iso3 = etod_map[self.ctry_name]['ctry_iso3']
        self.coord_format = etod_map[self.ctry_name]['coord_format']
        self.vert_uom = etod_map[self.ctry_name]['vert_uom']

    def map_csv_fields(self):

        etod_csv_fields = {'obst_id': None,
                           'obst_type': None,
                           'lon_src': None,
                           'lat_src': None,
                           'amsl': None,
                           'agl': None,
                           'lighting': None,
                           'marking': None}

        for field in etod_csv_fields:
            etod_csv_fields[field] = etod_map[self.ctry_name]['fields'][field]

        return etod_csv_fields

    def parse_csv_row(self, mapping_fields, row):
        """ Parse CSV row and extracts obstacle data into _obstacle_data structure
        :param row: str, row of CSV file """
        for key in mapping_fields:
            if mapping_fields[key] is not None:
                self.obstacle_data[key] = row[mapping_fields[key]].strip()
            else:
                self.obstacle_data[key] = 'U'

    def insert_etod_into_db(self, connection, cursor):
        """ Inserts single eTOD into database
        :param connection: connection to database object
        :param cursor: cursor object
        """
        cursor.execute("""
                insert into
                    etod
                    (ctry_iso3, 
                     obst_id, 
                     obst_type, 
                     lon_src, 
                     lat_src, 
                     amsl,
                     agl, 
                     vert_uom, 
                     lighting, 
                     marking, 
                     geo_location)
                    values
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    ST_GeomFromText('POINT(%s %s)', 4326));
                   """,
                       (self.obstacle_data['ctry_iso3'],
                        self.obstacle_data['obst_id'],
                        self.obstacle_data['obst_type'],
                        self.obstacle_data['lon_src'],
                        self.obstacle_data['lat_src'],
                        self.obstacle_data['amsl'],
                        self.obstacle_data['agl'],
                        self.obstacle_data['vert_uom'],
                        self.obstacle_data['lighting'],
                        self.obstacle_data['marking'],
                        self.obstacle_data['lon_dd'],
                        self.obstacle_data['lat_dd']))

        connection.commit()

    def csv_etod_to_postgis(self, host, database, user, password):
        """ Parses CSV eTOD file and insert data into PostGIS database """

        # Map CSV fields with rules before parsing
        mapping_fields = self.map_csv_fields()

        # Connect to database
        db = DatabaseTools(host, database, user, password)
        conn = db.get_connection()

        lon = CoordinatePredetermined(self.coord_format, AT_LON)
        lat = CoordinatePredetermined(self.coord_format, AT_LAT)

        self.obstacle_data['ctry_iso3'] = etod_map[self.ctry_name]['ctry_iso3']
        self.obstacle_data['vert_uom'] = etod_map[self.ctry_name]['vert_uom']

        delimiter = etod_map[self.ctry_name]['fields']['csv_delimiter']
        if conn:
            cur = conn.cursor()
            with open(self.etod_file, 'r', errors='ignore') as data_file:
                reader = csv.DictReader(data_file, delimiter=delimiter)
                for row in reader:
                    self.parse_csv_row(mapping_fields, row)
                    # Calculate coordinate in decimal degrees
                    self.obstacle_data['lon_dd'] = lon.coordinate_to_dd(self.obstacle_data['lon_src'])
                    self.obstacle_data['lat_dd'] = lat.coordinate_to_dd(self.obstacle_data['lat_src'])
                    # Check parsed data
                    if self.obstacle_data['lon_dd'] is not None and self.obstacle_data['lat_dd'] is not None:
                        self.insert_etod_into_db(conn, cur)
                    else:
                        print(row)

                cur.close()
                conn.close()

    def parse_dat_line(self, dat_fields, line):
        """ Extracts data from DAT file line.
        :param line:
        :return:
        """
        for key in dat_fields:
            if len(dat_fields[key]) == 2:
                self.obstacle_data[key] = line[int(dat_fields[key][0]) - 1:int(dat_fields[key][1])].strip()
            if len(dat_fields[key]) == 1:
                self.obstacle_data[key] = line[int(dat_fields[key][0] - 1)].strip()

    def dat_etod_to_postgis(self, host, database, user, password):
        """ Parses CSV eTOD file and insert data into PostGIS database """

        # Get fields from DAT file
        dat_fields = etod_map[self.ctry_name]['fields']

        # Connect to database
        db = DatabaseTools(host, database, user, password)
        conn = db.get_connection()
        lon = CoordinatePredetermined(self.coord_format, AT_LON)
        lat = CoordinatePredetermined(self.coord_format, AT_LAT)

        self.obstacle_data['ctry_iso3'] = etod_map[self.ctry_name]['ctry_iso3']
        self.obstacle_data['vert_uom'] = etod_map[self.ctry_name]['vert_uom']

        if conn:
            cur = conn.cursor()
            line_nr = 0
            with open(self.etod_file, 'r') as data:
                for line in data:
                    line_nr += 1
                    if line_nr < 5:
                        continue
                    else:
                        self.parse_dat_line(dat_fields, line)
                        lon_mod = self.obstacle_data['lon_src'].replace(' ', '')
                        lon_dd = lon.coordinate_to_dd(lon_mod)

                        lat_mod = self.obstacle_data['lat_src'].replace(' ', '')
                        lat_dd = lat.coordinate_to_dd(lat_mod)

                        self.obstacle_data['lon_dd'] = lon_dd
                        self.obstacle_data['lat_dd'] = lat_dd
                        try:
                            self.insert_etod_into_db(conn, cur)
                        except:
                            pass

                cur.close()
                conn.close()

    def etod_to_postgis(self, host, database, user, password):
        self.init_data()
        if self.etod_file_type == 'CSV':
            self.csv_etod_to_postgis(host, database, user, password)
        elif self.etod_file_type == 'DAT':
            self.dat_etod_to_postgis(host, database, user, password)

"""
etod_parser.py module
This module provides extracting data from eTOD csv files text files
"""
import csv
from aviationnavigationdb.aviation_navdb_libs.eaip_data_extraction.etod_mapping import *
from aviationnavigationdb.aviation_gis_toolkit.coordinate_predetermined import *


class EtodParser:
    def __init__(self, ctry_short_name, etod_file):
        self.ctry_short_name = ctry_short_name
        self.etod_file = etod_file
        self.file_format = None
        self.coord_format = None
        self.vert_uom = None
        self.field_map = None  # Map between obstacle columns and fields in source data file
        self.obst_type_map = None
        self.lon = None
        self.lat = None
        self.obstacle_data = {
            'ctry_id': None,
            'obst_identifier': None,
            'obst_name': None,
            'lon_src': None,
            'lat_src': None,
            'agl': None,
            'amsl': None,
            'vert_uom': None,
            'hor_acc': None,
            'hor_acc_uom': None,
            'vert_acc': None,
            'vert_acc_uom': None,
            'obst_type_id': None,
            'lighting': None,
            'marking': None,
            'is_group': None,
            'lon_dd': None,
            'lat_dd': None
        }
        self.marking_map = None
        self.lighting_map = None

    def map_csv_fields(self):
        """ Assigns fields between eTOD CSV file and obstacle data.
        :return: dict
        """
        etod_csv_fields = {
            'ctry_id': None,
            'obst_identifier': None,
            'obst_name': None,
            'lon_src': None,
            'lat_src': None,
            'agl': None,
            'amsl': None,
            'vert_uom': None,
            'hor_acc': None,
            'hor_acc_uom': None,
            'vert_acc': None,
            'vert_acc_uom': None,
            'obst_type': None,
            'lighting': None,
            'marking': None,
            'is_group': None,
        }

        for field in etod_csv_fields:
            try:
                etod_csv_fields[field] = etod_map[self.ctry_short_name]['fields'][field]
            except KeyError:
                etod_csv_fields[field] = None

        self.field_map = etod_csv_fields

    def get_obstacle_type_id(self, obstacle_type):
        """ Gets obstacle type id based on obstacle type specified for given country.
        :param obstacle_type:
        :return: int, obstacle_type_id value from database
        """
        try:
            return self.obst_type_map[obstacle_type]
        except KeyError:
            return 1

    def get_marking_value(self, marking):
        """ Gets marking value (U, Y, N) based on marking form eTOD file. Note specified for given country.
        :param marking:
        :return: str, marking value to be stored in database
        """
        if marking:
            return self.marking_map[marking]
        else:
            return 'U'

    def get_lighting_value(self, lighting):
        """ Gets lighting value (U, Y, N) based on marking form eTOD file. Note specified for given country.
        :param lighting:
        :return: str, lighting value to be stored in database
        """
        if lighting:
            return self.lighting_map[lighting]
        else:
            return 'U'

    def init_parser(self, ctry_id):
        """ Prepares parser for extracting data from source file, e. g.: initialize
        common data for all obstacles, depends on the country such as country_id, vert_uom
        :param ctry_id: int, value taken from country table (ctry_id for given short_name)
        """
        self.obstacle_data["ctry_id"] = ctry_id
        self.file_format = etod_map[self.ctry_short_name]['file_format']
        self.coord_format = etod_map[self.ctry_short_name]['coord_format']
        self.obstacle_data['vert_uom'] = etod_map[self.ctry_short_name]['vert_uom']
        self.lon = CoordinatePredetermined(self.coord_format, AT_LON)
        self.lat = CoordinatePredetermined(self.coord_format, AT_LAT)

        if self.file_format == 'CSV':
            self.map_csv_fields()
            # TODO: Check header of file
            for key in self.field_map:
                if self.field_map[key] is None:
                    if key == 'marking':
                        self.obstacle_data['marking'] = 'U'
                    if key == 'lighting':
                        self.obstacle_data['lighting'] = 'U'
                    if key == 'is_group':
                        self.obstacle_data['is_group'] = False
        elif self.file_format == 'DAT':
            self.field_map = etod_map[self.ctry_short_name]['fields']

        self.marking_map = marking_map[self.ctry_short_name]
        self.lighting_map = lighting_map[self.ctry_short_name]

    def parse_csv_row(self, row):
        """ Parse CSV row and extracts obstacle data into obstacle_data structure
        :param row: str, row of CSV source file
        """

        for key in self.field_map:
            if self.field_map[key] is not None:
                if key == 'marking':
                    self.obstacle_data[key] = self.get_marking_value(row[self.field_map[key]].strip())
                elif key == 'lighting':
                    self.obstacle_data[key] = self.get_lighting_value(row[self.field_map[key]].strip())
                elif key == 'obst_type':
                    self.obstacle_data['obst_type_id'] = self.get_obstacle_type_id(row[self.field_map[key]].strip())
                else:
                    self.obstacle_data[key] = row[self.field_map[key]].strip()

    def get_raw_value_from_dat_file(self, row, field):
        """ Gets raw value from data file.
        :param field: row, str, row of DAT source file
        :param field: str, field of the mapping rule
        :return: str, value of the field from data file
        """
        if len(self.field_map[field]) == 2:
            return row[int(self.field_map[field][0]) - 1:int(self.field_map[field][1])].strip()
        if len(self.field_map[field]) == 1:
            return row[int(self.field_map[field][0] - 1)].strip()

    def parse_dat_row(self, row):
        """ Extracts data from DAT file line.
        :param row: str, row of DAT source file
        """
        self.obstacle_data['is_group'] = False
        for field in self.field_map:
            field_value = self.get_raw_value_from_dat_file(row, field)
            if field == 'marking':
                self.obstacle_data[field] = self.get_marking_value(field_value)
            elif field == 'lighting':
                self.obstacle_data[field] = 'U'
            elif field == 'obst_type':
                self.obstacle_data['obst_type_id'] = 1
            else:
                self.obstacle_data[field] = field_value

    def validate_obstacle_data(self):
        check_result = True

        self.obstacle_data['lon_dd'] = self.lon.coordinate_to_dd(self.obstacle_data['lon_src'].replace(' ', ''))
        self.obstacle_data['lat_dd'] = self.lat.coordinate_to_dd(self.obstacle_data['lat_src'].replace(' ', ''))

        if self.obstacle_data['lon_dd'] is None or self.obstacle_data['lat_dd'] is None:
            check_result = False
        if float(self.obstacle_data['agl']) <= 0:
            check_result = False

        return check_result

    def import_etod_from_csv(self):
        self.init_parser(63)
        delimiter = etod_map[self.ctry_short_name]['csv_delimiter']
        with open(self.etod_file, 'r', errors='ignore') as data_file:
            reader = csv.DictReader(data_file, delimiter=delimiter)
            for row in reader:
                self.parse_csv_row(row)
                print(self.obstacle_data)

    def import_etod_from_dat(self):
        self.init_parser(63)
        with open(self.etod_file, 'r') as data_file:
            counter = 0
            for row in data_file:
                counter += 1
                if counter < 5:
                    continue
                else:
                    self.parse_dat_row(row)
                    self.validate_obstacle_data()
                    print(self.obstacle_data)

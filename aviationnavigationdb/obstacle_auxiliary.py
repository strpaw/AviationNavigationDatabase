import csv
from aviationnavigationdb.aviation_navdb_libs.eaip_data_extraction.etod_mapping import *


def get_unique_list(country_name, field_name, file_name):
    """ Gets unique list for given field. Use this function to get all possible for given field: type, lighting, marking
    :param country_name:
    :param field_name:
    :return:
    """
    values = []
    delimiter = etod_map[country_name]['csv_delimiter']

    with open(file_name, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            value = row[field_name]
            if value not in values:
                values.append(value)
        return values

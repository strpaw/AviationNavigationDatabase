"""
etod_mapping_csv.py provides rules for mapping data from eTOD stored in CSV file
"""
from aviation_navigation_db.aviation_gis_toolkit.const import *

etod_map = {
        'Finland': {
            'file_type': 'CSV',
            'ctry_iso3': 'FIN',
            'coord_format': AF_DMSH_COMP,
            'vert_uom': 'ft',
            'fields': {
                'ctry_iso3': 'FIN',
                'obst_id': 'OBST ID',
                'obst_type': 'TYPE',
                'lon_src': 'CLON',
                'lat_src': 'CLAT',
                'amsl': 'ELEV MSL (FT)',
                'agl': 'HGT AGL (FT)',
                'lighting': 'LGT TYPE',
                'marking': 'MARKINGS',
                'csv_delimiter': ';'
                }
            },  # End of Finland mapping
        'Romania': {
            'file_type': 'CSV',
            'ctry_iso3': 'ROU',
            'coord_format': AF_DMSH_COMP,
            'vert_uom': 'ft',
            'fields': {
                'obst_id': 'Ident',
                'obst_type': 'Type',
                'lon_src': 'Longitude',
                'lat_src': 'Latitude',
                'amsl': 'Elevation',
                'agl': 'Height',
                'lighting': 'LGHT',
                'marking': None,
                'csv_delimiter': ','
                }
            },  # End of Romania mapping
        'Poland': {
            'file_type': 'CSV',
            'ctry_iso3': 'POL',
            'coord_format': AF_DMSH_COMP,
            'vert_uom': 'ft',
            'fields': {
                'obst_id': 'Obstacle Identifier',
                'obst_type': 'Obstacle type',
                'lon_src': 'Latitude',
                'lat_src': 'Longitude',
                'amsl': 'Elevation',
                'agl': 'Height',
                'vert_uom': 'ft',
                'lighting': 'Lighting',
                'marking': 'Marking',
                'COORD_FORMAT': AF_DMSH_COMP,
                'csv_delimiter': ';'
                }
            },  # End of Poland mapping
        'USA': {
            'file_type': 'DAT',
            'ctry_iso3': 'USA',
            'coord_format': AF_DMSH_COMP,
            'vert_uom': 'ft',
            'fields': {
                'obst_id': [4, 9],
                'obst_type': [63, 78],
                'lon_src': [49, 61],
                'lat_src': [36, 47],
                'amsl': [90, 94],
                'agl': [84, 88],
                'lighting': [96],
                'marking': [102]
                }
            }  # End of USA mapping
        }


etod_csv_map = {
                'Spain': {'CSV_FIELDS': {'obst_id': 'Identificador_Identifier',
                                         'obst_type': 'Tipo_Type',
                                         'lon_src': 'Longitud_Longitude',
                                         'lat_src': 'Latitud_Latitude',
                                         'amsl': 'Elevacion_Elevation',
                                         'agl': 'Altura_Height',
                                         'lighting': 'Iluminado_Lighting',
                                         'marking': 'Senalizado_Marking'},
                          'VERT_UOM': 'ft',
                          'COORD_FORMAT': AF_DMSH_COMP}}


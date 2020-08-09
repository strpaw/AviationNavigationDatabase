"""
etod_mapping_csv.py provides rules for mapping data from eTOD stored in CSV file
"""

from aviationnavigationdb.aviation_gis_toolkit.const import *

# Map for country general rules, between CSV file fields and obstacle attributes
etod_map = {
    'Finland': {
        'file_format': 'CSV',
        'csv_delimiter': ';',
        'coord_format': AF_DMSH_COMP,
        'vert_uom': 'ft',
        'fields': {
            'obst_identifier': 'OBST ID',
            'obst_type': 'TYPE',
            'lon_src': 'CLON',
            'lat_src': 'CLAT',
            'amsl': 'ELEV MSL (FT)',
            'agl': 'HGT AGL (FT)',
            'lighting': 'LGT TYPE',
            'marking': 'MARKINGS'
        }
    },
    'Romania': {
        'file_format': 'CSV',
        'csv_delimiter': ',',
        'coord_format': AF_DMSH_COMP,
        'vert_uom': 'ft',
        'fields': {
            'obst_identifier': 'Ident',
            'obst_type': 'Type',
            'lon_src': 'Longitude',
            'lat_src': 'Latitude',
            'amsl': 'Elevation',
            'agl': 'Height',
            'lighting': 'LGHT'
        }
    },
    'Poland': {
        'file_format': 'CSV',
        'csv_delimiter': ';',
        'coord_format': AF_HDMS_COMP,
        'vert_uom': 'ft',
        'fields': {
            'obst_identifier': 'Obstacle Identifier',
            'obst_type': 'Obstacle type',
            'lon_src': 'Longitude',
            'lat_src': 'Latitude',
            'amsl': 'Elevation',
            'agl': 'Height',
            'hor_acc': 'Horizontal Accuracy',
            'hor_acc_uom': 'Horizontal Accuracy Uom',
            'vert_acc': 'Vertical Accuracy',
            'vert_acc_uom': 'Vertical Accuracy Uom',
            'lighting': 'Lighting',
            'marking': 'Marking '
        }
    },
    'Spain': {
        'file_format': 'CSV',
        'csv_delimiter': ';',
        'coord_format': AF_DMSH_COMP,
        'vert_uom': 'm',
        'fields': {
            'obst_identifier': 'Identificador_Identifier',
            'obst_type': 'Tipo_Type',
            'lon_src': 'Longitud_Longitude',
            'lat_src': 'Latitud_Latitude',
            'amsl': 'Elevacion_Elevation',
            'agl': 'Altura_Height',
            'lighting': 'Iluminado_Lighting',
            'marking': 'Señalizado_Marking'
        }
    },
    'United States of America': {
        'file_format': 'DAT',
        'coord_format': AF_DMSH_COMP,
        'vert_uom': 'ft',
        'fields': {
            'obst_identifier': [4, 9],
            'obst_type': [63, 78],
            'lon_src': [49, 61],
            'lat_src': [36, 47],
            'amsl': [90, 94],
            'agl': [84, 88],
            'lighting': [96],
            'marking': [102]
        }
    }
}

# Map between CSV data lighting description and obstacle database description
marking_map = {
    'Finland': {
        'Y': 'Y',
        'NIL': 'N'
    },
    'Romania': None,
    'Poland': {
        'YES': 'Y',
        'NO': 'N'
    },
    'Spain': {
        'No': 'N',
        'Si/Yes': 'Y'
    },
    'United States of America': {
        'P': 'Y',
        'W': 'Y',
        'M': 'Y',
        'F': 'Y',
        'S': 'Y',
        'N': 'N',
        'U': 'U'
    }
}

# Map between CSV data marking description and obstacle database description
lighting_map = {
    'Finland': {
        'F R': 'Y',
        'FLG W': 'Y',
        'FLG R': 'Y',
        'NIL': 'N'
    },
    'Romania': {
        'Red lights': 'Y',
        'Lighted': 'Y',
        'NIL': 'N',
        'Nil': 'N'
    },
    'Poland': {
        'YES': 'Y',
        'NO': 'N'
    },
    'Spain': {
        'No': 'N',
        'Si/Yes': 'Y'
    },
    'United States of America': {
        'R': 'Y',
        'D': 'Y',
        'H': 'Y',
        'M': 'Y',
        'F': 'Y',
        'C': 'Y',
        'W': 'Y',
        'L': 'Y',
        'N': 'N',
        'U': 'U'
    }
}

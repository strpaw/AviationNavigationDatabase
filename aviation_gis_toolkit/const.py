"""
const.py
const module provides common constants as unit of measure, angle types used in aviation_gis_toolkit package.
"""

# Units of measure

UOM_M = 'm'
UOM_KM = 'km'
UOM_NM = 'NM'
UOM_FT = 'ft'
UOM_SM = 'SM'

UOM_LIST = [UOM_M, UOM_KM, UOM_NM, UOM_FT, UOM_SM]

# Angle types
AT_LON = 'AT_LON'
AT_LAT = 'AT_LAT'

# Angle formats

# Degrees, minutes, seconds, hemisphere - compacted formats:
AF_DMSH_COMP = 'AF_DMSH_COMP'  # e.g.: 552243.47N
AF_HDMS_COMP = 'AF_HDMS_COMP'  # e.g.: N552243.47

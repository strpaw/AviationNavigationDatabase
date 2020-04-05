import unittest
from aviation_gis_toolkit.coordinate_predetermined import *
from aviation_gis_toolkit.const import *


class CoordinatePredeterminedTests(unittest.TestCase):

    def test_is_given_format(self):
        # DMSH Longitude check
        ang = ''
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '1732235.41W'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '0430900E'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '0035959.9E'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '0000100.00W'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '0015903.15S'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '1806159.15E'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '002234.15E'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '1812343.15E'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        # DMSH Latitude check
        ang = '732235.41S'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '093259N'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '005959.41N'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '001400S'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '1235959S'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '076352.44N'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '592234.15E'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '912335.15N'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        # HDMS Longitude check
        ang = 'W1732235.41'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'E0430900'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'E0035959.9'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'W0000100.00'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'S0015903.15'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'E1806159.15'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'E002234.15'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'E1812343.15'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        # HDMS Latitude check
        ang = 'S732235.41'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'N093259'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'N005959.41'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'S001400'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'S1235959'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'N076352.44'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'E592234.15'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'N912335.15'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

    def test_get_dms_coordinate_parts(self):

        # DMSH Longitude
        ang = '1233456.211W'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual((123, 34, 56.211, 'W'),
                         CoordinatePredetermined.get_dms_coordinate_parts(ang, regex))

        # DMSH Latitude
        ang = '233456S'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual((23, 34, 56.0, 'S'),
                         CoordinatePredetermined.get_dms_coordinate_parts(ang, regex))

        # HDMS Longitude
        ang = 'E0233456'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual((23, 34, 56.0, 'E'),
                         CoordinatePredetermined.get_dms_coordinate_parts(ang, regex))

        # HDMS Latitude
        ang = 'N233456.011'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual((23, 34, 56.011, 'N'),
                         CoordinatePredetermined.get_dms_coordinate_parts(ang, regex))

    def test_dms_parts_to_dd(self):
        dms_parts = (100, 30, 0.0, 'S')
        self.assertEqual(-100.5, CoordinatePredetermined.dms_parts_to_dd(dms_parts))

        dms_parts = (47, 30, 0.0, 'N')
        self.assertEqual(47.5, CoordinatePredetermined.dms_parts_to_dd(dms_parts))

        dms_parts = (100, 60, 0.0, 'S')
        self.assertEqual(None, CoordinatePredetermined.dms_parts_to_dd(dms_parts))

        dms_parts = (100, 22, 60.0, 'S')
        self.assertEqual(None, CoordinatePredetermined.dms_parts_to_dd(dms_parts))

        dms_parts = (180, 60, 0.0, 'S')
        self.assertEqual(None, CoordinatePredetermined.dms_parts_to_dd(dms_parts))

        dms_parts = (180, 0, 0.0, 'E')
        self.assertEqual(180, CoordinatePredetermined.dms_parts_to_dd(dms_parts))

    def test_dms_to_dd(self):

        ang = CoordinatePredetermined(AF_DMSH_COMP, AT_LON)
        self.assertEqual(-135.5, ang.dms_to_dd('1353000.000W'))

        ang = CoordinatePredetermined(AF_DMSH_COMP, AT_LON)
        self.assertEqual(-135.68944444444446, ang.dms_to_dd('1354122.000W'))

        ang = CoordinatePredetermined(AF_DMSH_COMP, AT_LON)
        self.assertEqual(None, ang.dms_to_dd('1800100.000W'))

        ang = CoordinatePredetermined(AF_DMSH_COMP, AT_LON)
        self.assertEqual(None, ang.dms_to_dd('180000.001E'))

        ang = CoordinatePredetermined(AF_DMSH_COMP, AT_LON)
        self.assertEqual(135.5, ang.dms_to_dd('1353000.000E'))

        ang = CoordinatePredetermined(AF_DMSH_COMP, AT_LAT)
        self.assertEqual(-35.5, ang.dms_to_dd('353000.000S'))

        ang = CoordinatePredetermined(AF_DMSH_COMP, AT_LAT)
        self.assertEqual(35.5, ang.dms_to_dd('353000.000N'))

        ang = CoordinatePredetermined(AF_HDMS_COMP, AT_LAT)
        self.assertEqual(-35.5, ang.dms_to_dd('S353000.000'))

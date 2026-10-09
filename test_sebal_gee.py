import unittest

import sebal_gee


class TestSEBALModule(unittest.TestCase):
    def test_dataset_constants(self):
        self.assertIn("LANDSAT", sebal_gee.LANDSAT8)
        self.assertIn("LANDSAT", sebal_gee.LANDSAT9)
        self.assertEqual(sebal_gee.ERA5_LAND, "ECMWF/ERA5_LAND/HOURLY")
        self.assertEqual(sebal_gee.HYDROSHEDS_7, "WWF/HydroSHEDS/v1/Basins/hybas_7")

    def test_default_outlet(self):
        lon, lat = sebal_gee.DEFAULT_OUTLET
        self.assertTrue(60 < lon < 75)
        self.assertTrue(20 < lat < 30)

    def test_engine_import_status(self):
        ok, message = sebal_gee.earth_engine_status()
        self.assertIsInstance(ok, bool)
        self.assertIsInstance(message, str)


if __name__ == "__main__":
    unittest.main()

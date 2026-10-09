import io
import unittest
import pandas as pd
from sebal_upload_analytics import find_coordinate_columns, valid_spatial_rows, read_uploaded_table

class FakeUpload:
    def __init__(self, name, raw): self.name, self._raw = name, raw
    def getvalue(self): return self._raw

class TestSEBALUploadAnalytics(unittest.TestCase):
    def test_coordinate_aliases(self):
        df = pd.DataFrame({"Latitude (decimal)": [31.5], "Longitude": [74.3]})
        lat, lon = find_coordinate_columns(df)
        self.assertEqual(lat, "Latitude (decimal)")
        self.assertEqual(lon, "Longitude")

    def test_invalid_coordinates_removed(self):
        df = pd.DataFrame({"lat": [31, 100, None], "lon": [74, 20, 71], "ET_mm_day": [4, 5, 6]})
        valid, lat, lon = valid_spatial_rows(df)
        self.assertEqual((lat, lon), ("lat", "lon"))
        self.assertEqual(len(valid), 1)

    def test_csv_upload(self):
        upload = FakeUpload("sample.csv", b"lat,lon,ET_mm_day\n31.5,74.3,4.2\n")
        df = read_uploaded_table(upload)
        self.assertIn("ET_mm_day", df.columns)
        self.assertEqual(len(df), 1)

if __name__ == "__main__": unittest.main()

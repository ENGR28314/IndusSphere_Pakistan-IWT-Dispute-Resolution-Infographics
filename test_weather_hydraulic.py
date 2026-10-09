import unittest
from telemetry_engine import simulate_12_month_telemetry, simulated_live_weather
from weather_hydraulic import hydraulic_hazard, telemetry_with_hazard


class WeatherHydraulicTests(unittest.TestCase):
    def test_all_required_city_basins(self):
        expected = {"Sialkot": "Chenab", "Jhelum": "Jhelum", "Lahore": "Ravi"}
        for city, basin in expected.items():
            df = simulate_12_month_telemetry(city)
            self.assertEqual(len(df), 12)
            self.assertTrue((df["basin"] == basin).all())

    def test_hazard_range(self):
        for city in ("Sialkot", "Jhelum", "Lahore"):
            weather = simulated_live_weather(city)
            result = hydraulic_hazard(weather)
            self.assertGreaterEqual(result["hazard_index"], 0)
            self.assertLessEqual(result["hazard_index"], 100)

    def test_telemetry_has_hazard(self):
        df = telemetry_with_hazard("Sialkot")
        self.assertEqual(len(df), 12)
        self.assertTrue(df["hydraulic_hazard_index"].between(0, 100).all())


if __name__ == "__main__":
    unittest.main()

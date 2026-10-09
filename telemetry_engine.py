"""Simulated 12-month city/basin telemetry for IndusSphere Pakistan.

This module intentionally generates synthetic screening data. It does not claim to
be an observation archive or a substitute for WAPDA/PMD gauge records.
"""
from __future__ import annotations

import hashlib
from datetime import date
import numpy as np
import pandas as pd

CITY_CONFIG = {
    "Sialkot": {
        "basin": "Chenab",
        "rain_peak": 210.0,
        "rain_base": 18.0,
        "discharge_base": 950.0,
        "discharge_amp": 520.0,
        "level_base": 2.6,
        "level_amp": 0.75,
        "temp_base": 25.0,
        "rain_phase": 6.5,
        "discharge_phase": 6.0,
    },
    "Jhelum": {
        "basin": "Jhelum",
        "rain_peak": 190.0,
        "rain_base": 15.0,
        "discharge_base": 1150.0,
        "discharge_amp": 700.0,
        "level_base": 3.0,
        "level_amp": 0.85,
        "temp_base": 23.0,
        "rain_phase": 6.0,
        "discharge_phase": 5.7,
    },
    "Lahore": {
        "basin": "Ravi",
        "rain_peak": 175.0,
        "rain_base": 12.0,
        "discharge_base": 520.0,
        "discharge_amp": 360.0,
        "level_base": 2.1,
        "level_amp": 0.65,
        "temp_base": 26.0,
        "rain_phase": 6.4,
        "discharge_phase": 6.2,
    },
}


def _seed(city: str, period: str) -> int:
    raw = f"IndusSphere|{city}|{period}".encode()
    return int(hashlib.sha256(raw).hexdigest()[:8], 16)


def simulate_12_month_telemetry(city: str, end: date | None = None) -> pd.DataFrame:
    """Generate exactly 12 monthly synthetic telemetry observations."""
    if city not in CITY_CONFIG:
        raise ValueError(f"Unsupported city: {city}")
    cfg = CITY_CONFIG[city]
    end_ts = pd.Timestamp(end or pd.Timestamp.today()).to_period("M")
    months = pd.period_range(end=end_ts, periods=12, freq="M")
    rows = []
    for i, period in enumerate(months):
        month = period.month
        # Seasonal index: high in monsoon months, lower in winter/spring.
        seasonal = max(0.0, np.sin((month - cfg["rain_phase"]) / 12 * 2 * np.pi))
        discharge_season = max(0.0, np.sin((month - cfg["discharge_phase"]) / 12 * 2 * np.pi))
        rng = np.random.default_rng(_seed(city, str(period)))
        rainfall = max(0.0, cfg["rain_base"] + cfg["rain_peak"] * seasonal + rng.normal(0, 10))
        discharge = max(20.0, cfg["discharge_base"] + cfg["discharge_amp"] * discharge_season + rainfall * 1.15 + rng.normal(0, 45))
        level = max(0.2, cfg["level_base"] + cfg["level_amp"] * discharge_season + rainfall / 500 + rng.normal(0, 0.10))
        temperature = cfg["temp_base"] + 10 * np.cos((month - 7) / 12 * 2 * np.pi) + rng.normal(0, 1.2)
        rows.append({
            "date": period.to_timestamp(how="end").normalize(),
            "city": city,
            "basin": cfg["basin"],
            "rainfall_mm": round(float(rainfall), 1),
            "river_discharge_m3s": round(float(discharge), 1),
            "water_level_m": round(float(level), 2),
            "temperature_c": round(float(temperature), 1),
        })
    return pd.DataFrame(rows)


def simulated_live_weather(city: str, now: pd.Timestamp | None = None) -> dict:
    """Generate a deterministic, current-period synthetic weather snapshot."""
    if city not in CITY_CONFIG:
        raise ValueError(f"Unsupported city: {city}")
    now = pd.Timestamp(now or pd.Timestamp.now())
    cfg = CITY_CONFIG[city]
    rng = np.random.default_rng(_seed(city, now.strftime("%Y-%m-%d-%H")))
    month = now.month
    seasonal = max(0.0, np.sin((month - cfg["rain_phase"]) / 12 * 2 * np.pi))
    discharge_season = max(0.0, np.sin((month - cfg["discharge_phase"]) / 12 * 2 * np.pi))
    rainfall_24h = max(0.0, cfg["rain_base"] / 4 + cfg["rain_peak"] * seasonal / 5 + rng.normal(0, 5))
    rainfall_intensity = max(0.0, rainfall_24h / 6 + rng.normal(0, 1.5))
    discharge = max(20.0, cfg["discharge_base"] + cfg["discharge_amp"] * discharge_season + rainfall_24h * 2 + rng.normal(0, 35))
    level = max(0.2, cfg["level_base"] + cfg["level_amp"] * discharge_season + rainfall_24h / 450 + rng.normal(0, 0.08))
    temperature = cfg["temp_base"] + 10 * np.cos((month - 7) / 12 * 2 * np.pi) + rng.normal(0, 1.0)
    humidity = np.clip(48 + rainfall_intensity * 3.2 + seasonal * 20 + rng.normal(0, 4), 20, 98)
    return {
        "timestamp": now,
        "city": city,
        "basin": cfg["basin"],
        "temperature_c": round(float(temperature), 1),
        "rainfall_24h_mm": round(float(rainfall_24h), 1),
        "rainfall_intensity_mm_h": round(float(rainfall_intensity), 1),
        "humidity_pct": round(float(humidity), 1),
        "river_discharge_m3s": round(float(discharge), 1),
        "water_level_m": round(float(level), 2),
    }

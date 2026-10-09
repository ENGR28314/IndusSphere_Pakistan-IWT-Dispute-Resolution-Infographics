"""Simulated live weather/rainfall and hydraulic-hazard screening."""
from __future__ import annotations

import numpy as np
import pandas as pd

from telemetry_engine import CITY_CONFIG, simulated_live_weather, simulate_12_month_telemetry


def hydraulic_hazard(weather: dict) -> dict:
    """Convert simulated rainfall, discharge and water level into a transparent 0-100 screening index."""
    city = weather["city"]
    cfg = CITY_CONFIG[city]
    rainfall_score = np.clip(weather["rainfall_intensity_mm_h"] / 25.0 * 100, 0, 100)
    discharge_ratio = weather["river_discharge_m3s"] / max(cfg["discharge_base"] + cfg["discharge_amp"], 1)
    discharge_score = np.clip(discharge_ratio * 100, 0, 100)
    level_ratio = weather["water_level_m"] / max(cfg["level_base"] + cfg["level_amp"] + 1.0, 1)
    level_score = np.clip(level_ratio * 100, 0, 100)
    index = float(np.clip(0.40 * rainfall_score + 0.40 * discharge_score + 0.20 * level_score, 0, 100))
    risk_class = "Low" if index < 40 else "Moderate" if index < 70 else "High"
    return {
        "hazard_index": round(index, 1),
        "risk_class": risk_class,
        "rainfall_score": round(float(rainfall_score), 1),
        "discharge_score": round(float(discharge_score), 1),
        "water_level_score": round(float(level_score), 1),
        "method": "Illustrative screening index; not a flood warning or calibrated hydraulic model.",
    }


def telemetry_with_hazard(city: str, end: pd.Timestamp | None = None) -> pd.DataFrame:
    df = simulate_12_month_telemetry(city, end=end).copy()
    hazards = []
    for row in df.to_dict("records"):
        weather = {
            "city": city,
            "rainfall_intensity_mm_h": row["rainfall_mm"] / 8.0,
            "river_discharge_m3s": row["river_discharge_m3s"],
            "water_level_m": row["water_level_m"],
        }
        h = hydraulic_hazard(weather)
        hazards.append((h["hazard_index"], h["risk_class"]))
    df["hydraulic_hazard_index"] = [x[0] for x in hazards]
    df["hydraulic_hazard_class"] = [x[1] for x in hazards]
    return df


__all__ = ["CITY_CONFIG", "simulated_live_weather", "simulate_12_month_telemetry", "hydraulic_hazard", "telemetry_with_hazard"]

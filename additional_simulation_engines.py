"""Lightweight engineering screening engines used by the Streamlit simulator.

These are transparent screening models, not substitutes for calibrated professional
hydraulic, hydrologic or environmental design software.
"""
from __future__ import annotations
import math
import pandas as pd


def groundwater_balance(initial_storage, recharge, pumping, natural_discharge=0.0, periods=12):
    storage = float(initial_storage)
    rows = []
    for i in range(1, int(periods) + 1):
        storage = max(0.0, storage + float(recharge) - float(pumping) - float(natural_discharge))
        rows.append({"Period": i, "Recharge": float(recharge), "Pumping": float(pumping), "Natural discharge": float(natural_discharge), "End storage": storage})
    return pd.DataFrame(rows)


def drought_index(precip_mm, normal_mm, temperature_anomaly_c=0.0, demand_pressure=50.0):
    p = max(0.0, float(precip_mm)); n = max(1e-9, float(normal_mm))
    rainfall_deficit = max(0.0, 1.0 - p / n)
    heat_factor = max(0.0, float(temperature_anomaly_c)) / 4.0
    demand_factor = max(0.0, min(100.0, float(demand_pressure))) / 100.0
    index = min(100.0, 100.0 * (0.55 * rainfall_deficit + 0.25 * heat_factor + 0.20 * demand_factor))
    label = "Low" if index < 30 else "Moderate" if index < 60 else "High" if index < 80 else "Very High"
    return {"index": index, "class": label, "rainfall_deficit": rainfall_deficit, "heat_factor": heat_factor, "demand_factor": demand_factor}


def sediment_load(discharge_m3s, sediment_concentration_mg_l, duration_hours):
    # mg/L × m3/s × seconds -> kg, then tonnes.
    mass_tonnes = float(discharge_m3s) * float(sediment_concentration_mg_l) * float(duration_hours) * 3600 / 1e6
    return {"sediment_mass_tonnes": max(0.0, mass_tonnes), "duration_hours": float(duration_hours)}


def water_quality_index(ph, turbidity_ntu, tds_mg_l, dissolved_oxygen_mg_l, nitrate_mg_l):
    def clamp(x): return max(0.0, min(100.0, x))
    ph_score = clamp(100 - abs(float(ph) - 7.5) * 22)
    turb_score = clamp(100 - float(turbidity_ntu) * 3)
    tds_score = clamp(100 - max(0.0, float(tds_mg_l) - 300) / 12)
    do_score = clamp(float(dissolved_oxygen_mg_l) / 8 * 100)
    nitrate_score = clamp(100 - float(nitrate_mg_l) * 4)
    score = 0.20 * ph_score + 0.20 * turb_score + 0.20 * tds_score + 0.20 * do_score + 0.20 * nitrate_score
    label = "Good" if score >= 80 else "Moderate" if score >= 60 else "Poor" if score >= 40 else "Very Poor"
    return {"index": score, "class": label, "pH score": ph_score, "Turbidity score": turb_score, "TDS score": tds_score, "DO score": do_score, "Nitrate score": nitrate_score}


def irrigation_schedule(et0_mm, crop_coefficient, effective_rain_mm, efficiency, area_ha):
    net_mm = max(0.0, float(et0_mm) * float(crop_coefficient) - float(effective_rain_mm))
    gross_mm = net_mm / max(0.01, float(efficiency))
    volume_m3 = gross_mm * float(area_ha) * 10.0
    return {"ETc_mm": float(et0_mm) * float(crop_coefficient), "Net irrigation_mm": net_mm, "Gross irrigation_mm": gross_mm, "Gross volume_m3": volume_m3}


def socio_agro_projection(df, metric_col, growth_rate_pct, years):
    rows = []
    for _, row in df.iterrows():
        base = float(row[metric_col])
        for year in range(0, int(years) + 1):
            rows.append({"province/region": row["province/region"], "year": year, metric_col: base * (1 + float(growth_rate_pct) / 100) ** year})
    return pd.DataFrame(rows)

"""Hydrology and river-reservoir simulation engines for IndusSphere Pakistan.
All engines are deterministic and input-driven; they are educational screening models,
not substitutes for calibrated hydrologic/hydraulic studies.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def monthly_water_balance(inflow, demand, storage0, capacity, evaporation=0.0):
    inflow = np.asarray(inflow, dtype=float)
    demand = np.asarray(demand, dtype=float)
    if inflow.size != demand.size:
        raise ValueError("inflow and demand must have the same length")
    storage = float(np.clip(storage0, 0, capacity))
    rows = []
    for i, (qin, qdem) in enumerate(zip(inflow, demand), 1):
        available = storage + max(qin, 0)
        evap = min(max(evaporation, 0), available)
        after_evap = available - evap
        release = min(after_evap, max(qdem, 0))
        spill = max(after_evap - release - capacity, 0)
        end = np.clip(after_evap - release, 0, capacity)
        shortage = max(qdem - release, 0)
        rows.append({"Period": i, "Inflow": qin, "Demand": qdem, "Evaporation": evap,
                     "Release": release, "Shortage": shortage, "Spill": spill,
                     "End storage": end})
        storage = float(end)
    return pd.DataFrame(rows)


def reservoir_rule_curve(inflow, demand, capacity, storage0=None, target_fraction=0.6, evaporation=0.0):
    """Simple target-storage reservoir operation with spill and shortage accounting."""
    target = capacity * float(np.clip(target_fraction, 0, 1))
    if storage0 is None:
        storage0 = target
    df = monthly_water_balance(inflow, demand, storage0, capacity, evaporation)
    df["Target storage"] = target
    df["Storage deviation"] = df["End storage"] - target
    return df

"""Small input-driven utilities for telecommunication-network analysis."""
import math
import pandas as pd


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2-lat1)
    dl = math.radians(lon2-lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*r*math.asin(math.sqrt(a))


def pairwise_distance_table(nodes: pd.DataFrame) -> pd.DataFrame:
    required = {"name", "latitude", "longitude"}
    if not required.issubset(nodes.columns):
        raise ValueError(f"nodes must contain {sorted(required)}")
    rows = []
    for i, a in nodes.reset_index(drop=True).iterrows():
        for j in range(i+1, len(nodes)):
            b = nodes.iloc[j]
            rows.append({"from": a["name"], "to": b["name"], "distance_km": haversine_km(float(a["latitude"]), float(a["longitude"]), float(b["latitude"]), float(b["longitude"]))})
    return pd.DataFrame(rows)


def network_summary(nodes: pd.DataFrame) -> dict:
    return {
        "nodes": int(len(nodes)),
        "with_coordinates": int(nodes[["latitude", "longitude"]].notna().all(axis=1).sum()) if {"latitude", "longitude"}.issubset(nodes.columns) else 0,
    }

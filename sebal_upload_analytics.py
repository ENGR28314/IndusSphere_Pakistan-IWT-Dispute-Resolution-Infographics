"""Upload-driven analytics for the IndusSphere SEBAL page.

CSV/XLSX/XLS data can be inspected and mapped without Earth Engine credentials.
These visualizations do not calculate satellite SEBAL ET unless a real ET field
is already present in the uploaded data or the Earth Engine workflow is run.
"""
from __future__ import annotations
import io
import re
import pandas as pd

LAT_ALIASES = {"lat", "latitude", "y", "lat_dd", "latitude_dd", "decimal_latitude", "latitude_decimal", "lat_decimal", "gps_latitude"}
LON_ALIASES = {"lon", "lng", "long", "longitude", "x", "lon_dd", "longitude_dd", "decimal_longitude", "longitude_decimal", "lon_decimal", "gps_longitude"}
DATE_ALIASES = {"date", "datetime", "timestamp", "time", "acquisition_date", "sample_date", "observation_date"}


def read_uploaded_table(uploaded_file) -> pd.DataFrame:
    """Read supported tabular uploads and normalize column labels."""
    name = str(uploaded_file.name).lower()
    raw = uploaded_file.getvalue()
    if name.endswith(".csv"):
        errors = []
        for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
            try:
                df = pd.read_csv(io.BytesIO(raw), encoding=encoding)
                break
            except Exception as exc:
                errors.append(str(exc))
        else:
            raise ValueError("Could not read CSV: " + "; ".join(errors[-2:]))
    elif name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(io.BytesIO(raw))
    else:
        raise ValueError("Upload a CSV, XLSX, or XLS table.")
    df = df.copy()
    df.columns = [re.sub(r"\s+", " ", str(c)).strip() or f"column_{i+1}" for i, c in enumerate(df.columns)]
    df = df.dropna(axis=0, how="all").dropna(axis=1, how="all")
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].map(lambda v: v.strip() if isinstance(v, str) else v)
    return df


def _norm(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def find_coordinate_columns(df: pd.DataFrame) -> tuple[str | None, str | None]:
    normalized = {_norm(c): c for c in df.columns}
    lat = next((normalized[a] for a in LAT_ALIASES if a in normalized), None)
    lon = next((normalized[a] for a in LON_ALIASES if a in normalized), None)
    if lat is None:
        lat = next((c for n, c in normalized.items() if n.startswith("lat_") or n.endswith("_latitude")), None)
    if lon is None:
        lon = next((c for n, c in normalized.items() if n.startswith(("lon_", "lng_", "long_")) or n.endswith(("_longitude", "_long"))), None)
    return lat, lon


def valid_spatial_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, str | None, str | None]:
    lat, lon = find_coordinate_columns(df)
    if not lat or not lon:
        return pd.DataFrame(), lat, lon
    out = df.copy()
    out[lat] = pd.to_numeric(out[lat].astype(str).str.replace(",", "", regex=False), errors="coerce")
    out[lon] = pd.to_numeric(out[lon].astype(str).str.replace(",", "", regex=False), errors="coerce")
    out = out.dropna(subset=[lat, lon])
    out = out[out[lat].between(-90, 90) & out[lon].between(-180, 180)]
    return out, lat, lon

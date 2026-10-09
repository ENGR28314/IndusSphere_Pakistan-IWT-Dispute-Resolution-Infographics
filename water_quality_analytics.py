"""Water-quality and telemetry analytics for IndusSphere Pakistan."""
from __future__ import annotations

import re
from typing import Iterable

import pandas as pd


BASIN_ALIASES = [
    "river basin", "basin", "river_basin", "catchment", "watershed", "river system"
]

TELEMETRY_HINTS = (
    "telemetry", "sensor", "gauge", "flow", "discharge", "level", "stage",
    "velocity", "rainfall", "temperature", "pressure", "ec", "conductivity"
)

WATER_QUALITY_INDEXES = {
    "Dissolved Oxygen (DO)": ["do", "dissolved oxygen", "dissolved_oxygen", "oxygen"],
    "pH": ["ph"],
    "Turbidity": ["turbidity"],
    "TDS": ["tds", "total dissolved solids", "total_dissolved_solids"],
    "Conductivity": ["conductivity", "ec", "electrical conductivity"],
    "Temperature": ["temperature", "water temperature", "water_temperature"],
    "Nitrate": ["nitrate", "no3", "no3-n", "nitrate-n"],
    "BOD": ["bod", "biochemical oxygen demand"],
    "COD": ["cod", "chemical oxygen demand"],
    "Coliform": ["coliform", "e. coli", "ecoli", "fecal coliform"],
}


def _norm(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()


def find_column(df: pd.DataFrame, aliases: Iterable[str]) -> str | None:
    normalized = {_norm(c): c for c in df.columns}
    aliases_n = [_norm(a) for a in aliases]
    for alias in aliases_n:
        if alias in normalized:
            return normalized[alias]
    for c in df.columns:
        nc = _norm(c)
        if any(alias in nc for alias in aliases_n):
            return c
    return None


def detect_basin_column(df: pd.DataFrame) -> str | None:
    return find_column(df, BASIN_ALIASES)


def detect_water_quality_columns(df: pd.DataFrame) -> dict[str, str]:
    found: dict[str, str] = {}
    for label, aliases in WATER_QUALITY_INDEXES.items():
        col = find_column(df, aliases)
        if col:
            found[label] = col
    return found


def detect_telemetry_columns(df: pd.DataFrame, exclude: Iterable[str] = ()) -> list[str]:
    excluded = set(exclude)
    result = []
    for col in df.columns:
        if col in excluded:
            continue
        normalized = _norm(col)
        if any(h in normalized for h in TELEMETRY_HINTS):
            result.append(col)
    return result


def coerce_numeric_columns(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        out[col] = pd.to_numeric(
            out[col].astype(str).str.replace(",", "", regex=False).str.replace("%", "", regex=False),
            errors="coerce",
        )
    return out


def telemetry_variance_by_basin(
    df: pd.DataFrame,
    basin_col: str,
    telemetry_cols: list[str],
) -> pd.DataFrame:
    """Return each basin's average sample variance across telemetry variables."""
    if not telemetry_cols:
        return pd.DataFrame(columns=[basin_col, "average_telemetry_variance", "observations"])

    work = coerce_numeric_columns(df, telemetry_cols)
    rows = []
    for basin, group in work.groupby(basin_col, dropna=False):
        variances = group[telemetry_cols].var(ddof=1, skipna=True)
        valid = variances.dropna()
        rows.append({
            basin_col: "Unknown" if pd.isna(basin) else basin,
            "average_telemetry_variance": float(valid.mean()) if len(valid) else float("nan"),
            "observations": int(len(group)),
            "telemetry_variables_used": int(len(valid)),
        })
    return pd.DataFrame(rows).sort_values("average_telemetry_variance", ascending=False, na_position="last")


def water_quality_summary(df: pd.DataFrame, basin_col: str, quality_cols: dict[str, str]) -> pd.DataFrame:
    """Calculate basin-level means for detected water-quality indexes."""
    if not quality_cols:
        return pd.DataFrame()
    work = coerce_numeric_columns(df, quality_cols.values())
    agg = {col: "mean" for col in quality_cols.values()}
    result = work.groupby(basin_col, dropna=False).agg(agg).reset_index()
    return result.rename(columns={v: k for k, v in quality_cols.items()})


def generate_visualization_script(
    basin_col: str,
    telemetry_cols: list[str],
    quality_cols: dict[str, str],
) -> str:
    """Create a standalone pandas/Plotly script tailored to the detected columns."""
    telemetry_repr = repr(telemetry_cols)
    quality_repr = repr(list(quality_cols.values()))
    return f'''# IndusSphere Pakistan — River Basin Telemetry Variance + Water Quality\nimport pandas as pd\nimport plotly.express as px\n\ndf = pd.read_csv("your_water_data.csv")\nbasin_col = {basin_col!r}\ntelemetry_cols = {telemetry_repr}\nwater_quality_cols = {quality_repr}\n\nfor col in telemetry_cols + water_quality_cols:\n    df[col] = pd.to_numeric(df[col], errors="coerce")\n\nvariance = (df.groupby(basin_col)[telemetry_cols]\n              .var(ddof=1)\n              .mean(axis=1)\n              .sort_values(ascending=False)\n              .rename("average_telemetry_variance")\n              .reset_index())\n\nfig = px.bar(variance, x=basin_col, y="average_telemetry_variance",\n             title="Average Telemetry Data Variance by River Basin",\n             labels={{"average_telemetry_variance": "Average variance"}})\nfig.show()\n\n# Optional water-quality analysis — including dissolved oxygen (DO) when present.\nif water_quality_cols:\n    quality = df.groupby(basin_col)[water_quality_cols].mean().reset_index()\n    print(quality)\n'''

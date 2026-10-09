import pandas as pd

METRICS = [
    "Cultivated area (ha)", "Crop production (tonnes)", "Employment (persons)",
    "Honey production (tonnes)", "Aquaculture production (tonnes)"
]
GRAPH_TYPES = ["Bar chart", "Pie chart", "Scatter plot", "Line chart"]

def validate_input(df):
    required = ["Province / Region", *METRICS]
    return [c for c in required if c not in df.columns]

def clean_input(df):
    out = df.copy()
    for c in METRICS:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out

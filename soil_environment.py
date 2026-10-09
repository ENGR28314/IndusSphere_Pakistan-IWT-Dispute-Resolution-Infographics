import pandas as pd

SOIL_ANALYTICS = pd.DataFrame([
 ["EMI Survey of Indus Delta","Survey / field data","Use uploaded observations to examine spatial/temporal patterns."],
 ["Interpolated EC","Electrical conductivity","Can indicate salinity patterns when units and interpolation method are documented."],
 ["pH","Soil reaction","Analyze distribution and relationship with salinity indicators."],
 ["ESP","Exchangeable sodium percentage","Useful for sodicity assessment when laboratory methods are documented."],
 ["Soil salinity","Salinity indicator","Map by coordinates or administrative/geographic units when location fields are available."],
 ["Soil sampling from Indus Delta","Sampling observations","Preserve sampling date, location, depth and laboratory metadata."],
], columns=["topic","parameter","analytics_note"])

def detect_spatial_columns(df):
    lat = next((c for c in df.columns if str(c).strip().lower() in {"lat","latitude","y"}), None)
    lon = next((c for c in df.columns if str(c).strip().lower() in {"lon","lng","longitude","x"}), None)
    return lat, lon

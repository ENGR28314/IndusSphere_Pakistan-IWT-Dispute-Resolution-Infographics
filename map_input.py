import pandas as pd
import plotly.express as px
from soil_environment import detect_spatial_columns

def map_uploaded_data(df, color=None, hover=None, title="Uploaded spatial data"):
    lat, lon = detect_spatial_columns(df)
    if not lat or not lon:
        return None, "Latitude/longitude columns were not detected. Add columns such as latitude/longitude or lat/lon."
    d = df.copy()
    d[lat] = pd.to_numeric(d[lat], errors="coerce")
    d[lon] = pd.to_numeric(d[lon], errors="coerce")
    d = d.dropna(subset=[lat, lon])
    if d.empty:
        return None, "No valid coordinate rows were found."
    color_col = color if color in d.columns else None
    hover_cols = [c for c in (hover or []) if c in d.columns]
    fig = px.scatter_geo(d, lat=lat, lon=lon, color=color_col, hover_data=hover_cols,
                         title=title, scope="asia")
    fig.update_geos(center=dict(lat=30.5, lon=70.5), projection_scale=5.0,
                    showcountries=True, showland=True, showocean=True)
    fig.update_layout(height=600, margin=dict(l=0,r=0,t=45,b=0))
    return fig, None

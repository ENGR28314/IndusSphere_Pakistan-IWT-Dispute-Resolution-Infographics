import plotly.graph_objects as go
from coordinates import POINTS

def water_map(rivers,dams,barrages,confluences):
    fig=go.Figure()
    paths={
    "Indus":[(35.9,74.58),(34.08,72.70),(33.99,72.24),(32.44,71.39),(30.70,70.65),(28.43,69.74),(27.71,68.86),(25.38,68.31)],
    "Jhelum":[(34.37,73.47),(33.15,73.65),(32.77,73.45),(31.24,72.12)],
    "Chenab":[(32.67,74.46),(32.41,73.75),(32.22,73.75),(31.24,72.12),(29.35,71.05)],
    "Ravi":[(32.67,74.20),(31.22,73.84),(30.49,72.21),(29.35,71.05)],
    "Sutlej":[(30.66,73.08),(29.91,72.26),(29.35,71.05)],
    "Kabul":[(34.15,71.78),(33.99,72.24)]
    }
    selected=set(rivers["name"]) if len(rivers) else set(paths)
    for name,pts in paths.items():
        if name not in selected: continue
        fig.add_trace(go.Scattergeo(lat=[p[0] for p in pts],lon=[p[1] for p in pts],
            mode="lines",name=name,line=dict(width=3)))
    def points(df,label,symbol):
        if df.empty:return
        lat=[];lon=[];txt=[]
        for _,r in df.iterrows():
            p=POINTS.get(r["name"],(30.5,70.5));lat.append(p[0]);lon.append(p[1]);txt.append(r["name"])
        fig.add_trace(go.Scattergeo(lat=lat,lon=lon,mode="markers+text",text=txt,
            textposition="top center",name=label,marker=dict(size=9,symbol=symbol)))
    points(dams,"Dams","circle")
    points(barrages,"Barrages","square")
    points(confluences,"Confluences","diamond")
    fig.update_geos(scope="asia",center=dict(lat=30.5,lon=70.5),projection_scale=5.2,
                    showland=True,landcolor="rgb(235,235,235)",showocean=True)
    fig.update_layout(height=650,margin=dict(l=0,r=0,t=10,b=0))
    return fig


def parks_map(parks, selected_name=None):
    """Interactive representative-location map for parks.

    Coordinates are intended for visualization only; they are not park boundaries.
    """
    from coordinates import PARK_POINTS, POINTS
    fig = go.Figure()
    names, lats, lons, focus = [], [], [], []
    park_coord_cache = {}
    for _, row in parks.iterrows():
        name = row.get("name", row.get("Park", ""))
        p = PARK_POINTS.get(name)
        if not p:
            region = row.get("province_region", row.get("region", ""))
            p = POINTS.get(str(region))
        if not p:
            # Stable visualization fallback: do not drop the selected park merely because
            # a detailed point has not yet been added to the curated coordinate inventory.
            p = (30.5, 70.5)
        park_coord_cache[name] = p
        names.append(name)
        lats.append(p[0]); lons.append(p[1])
        focus.append(row.get("focus", row.get("Focus", "Protected/recreational area")))

    if names:
        fig.add_trace(go.Scattergeo(
            lat=lats, lon=lons, mode="markers+text",
            text=names, textposition="top center",
            customdata=focus,
            hovertemplate="<b>%{text}</b><br>%{customdata}<extra></extra>",
            name="Parks", marker=dict(size=9, symbol="circle")
        ))

    if selected_name in park_coord_cache:
        lat, lon = park_coord_cache[selected_name]
        fig.add_trace(go.Scattergeo(
            lat=[lat], lon=[lon], mode="markers",
            name="Selected park", marker=dict(size=18, symbol="star")
        ))

    fig.update_geos(
        scope="asia", center=dict(lat=30.5, lon=70.5), projection_scale=5.0,
        showland=True, showocean=True,
        showcountries=True,
    )
    fig.update_layout(height=600, margin=dict(l=0, r=0, t=10, b=0),
                      legend=dict(orientation="h"))
    return fig

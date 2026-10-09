import pandas as pd
import plotly.graph_objects as go

# Representative coordinates for visualization. They are not survey-grade GIS boundaries.
LAKE_POINTS = {
    "Attabad Lake": (36.333, 74.826), "Saiful Muluk": (34.881, 73.694),
    "Sheosar Lake": (35.133, 75.561), "Satpara Lake": (35.213, 75.207),
    "Upper Kachura Lake": (35.466, 75.414), "Rama Lake": (35.430, 74.694),
    "Manchar Lake": (26.420, 67.870), "Keenjhar Lake": (24.806, 67.447),
    "Haleji Lake": (24.800, 67.560), "Hanna Lake": (30.262, 67.040),
    "Rawal Lake": (33.693, 73.127), "Khanpur Lake": (33.817, 72.930),
    "Chotiari Reservoir": (26.150, 68.700),
}

GLACIER_POINTS = {
    "Baltoro Glacier": (35.720, 76.310), "Biafo Glacier": (35.950, 75.780),
    "Hispar Glacier": (36.000, 75.800), "Batura Glacier": (36.520, 74.760),
    "Passu Glacier": (36.470, 74.890), "Siachen Glacier": (35.430, 77.150),
    "Chhota Shigri / northern cryosphere zone": (35.300, 76.900),
}

FOREST_POINTS = {
    "Changa Manga": (31.080, 73.970), "Ziarat Juniper Forest": (30.380, 67.720),
    "Ushu Forest": (35.550, 72.550), "Dir Forests": (35.200, 71.880),
    "Soon Valley Forests": (32.480, 72.260), "Mukshpuri Forest": (34.350, 73.390),
    "Rama Meadows / Forest": (35.430, 74.690), "Kalam Forests": (35.490, 72.580),
    "Chitral Forests": (35.850, 71.780), "Margalla Hills": (33.740, 73.020),
}

# Representative coordinates for the requested 17-project dashboard dataset.
INDIA_PROJECT_COORDS = {
    "Uri-I": (34.090, 74.060), "Uri-II": (34.090, 74.040),
    "Lower Jhelum": (34.160, 73.760), "Upper Sindh-II & Extension": (34.000, 75.180),
    "Kishenganga": (34.630, 74.850), "Dulhasti": (33.350, 75.760),
    "Salal I & II": (33.130, 74.830), "Baglihar-I": (33.160, 75.020),
    "Baglihar-II": (33.150, 75.030), "Sewa-II": (32.770, 75.480),
    "Pakal Dul": (33.430, 76.000), "Parnai": (33.850, 75.650),
    "Kiru": (33.450, 75.970), "Ratle": (33.370, 75.650),
    "Kwar": (33.470, 75.900), "Uri-I Stage-II": (34.090, 74.020),
    "Dulhasti Stage-II": (33.360, 75.770),
}

WESTERN_RIVER_PROJECTS = {
    "Uri-I", "Uri-II", "Lower Jhelum", "Upper Sindh-II & Extension", "Kishenganga",
    "Dulhasti", "Salal I & II", "Baglihar-I", "Baglihar-II", "Pakal Dul", "Parnai",
    "Kiru", "Ratle", "Kwar", "Uri-I Stage-II", "Dulhasti Stage-II"
}

# River paths are simplified display paths, not engineering centerlines.
RIVER_PATHS = {
    "Indus": [(35.90,74.58),(35.62,73.62),(34.08,72.70),(33.99,72.24),(32.44,71.39),(30.70,70.65),(28.43,69.74),(27.71,68.86),(25.38,68.31)],
    "Jhelum": [(34.37,73.47),(34.15,73.76),(33.15,73.65),(32.77,73.45),(31.24,72.12)],
    "Chenab": [(32.67,74.46),(32.41,73.75),(32.22,73.75),(31.24,72.12),(29.35,71.05)],
    "Ravi": [(32.67,74.20),(31.22,73.84),(30.49,72.21),(29.35,71.05)],
    "Sutlej": [(30.66,73.08),(29.91,72.26),(29.35,71.05)],
    "Kabul": [(34.15,71.78),(33.99,72.24)],
    "Swat": [(35.00,72.25),(34.45,71.95),(34.15,71.78)],
    "Kurram": [(33.80,69.95),(33.60,70.55),(33.40,71.20)],
    "Gomal": [(32.90,69.40),(32.65,70.25),(32.45,71.20)],
    "Hingol": [(27.60,65.70),(26.80,65.60),(25.55,65.50)],
    "Hub": [(26.60,66.70),(25.95,66.40),(24.90,66.75)],
}

LINK_PATHS = {
    "Chashma-Jhelum Link": [(32.44,71.39),(32.55,72.00),(32.75,72.75),(32.77,73.45)],
    "Rasul-Qadirabad Link": [(32.77,73.45),(32.55,73.70),(32.40,73.80)],
    "Marala-Ravi Link": [(32.67,74.46),(32.40,74.05),(31.90,73.90)],
    "Qadirabad-Balloki Link": [(32.40,73.80),(31.90,73.80),(31.40,73.80),(31.22,73.84)],
    "Balloki-Sulemanki Link": [(31.22,73.84),(30.70,73.40),(30.30,73.10)],
    "Trimmu-Sidhnai Link": [(31.24,72.12),(30.80,72.10),(30.49,72.21)],
    "Sidhnai-Melsi-Bahawalpur": [(30.49,72.21),(30.20,71.80),(29.80,71.60)],
    "Taunsa-Panjnad Link": [(30.70,70.65),(30.20,70.85),(29.35,71.05)],
}

CONFLUENCE_POINTS = {
    "Indus + Kabul (Attock)": (33.99,72.24),
    "Neelum + Jhelum (Muzaffarabad)": (34.37,73.47),
    "Jhelum + Chenab (Trimmu/Jhang system)": (31.24,72.12),
    "Sutlej + Chenab (Panjnad)": (29.35,71.05),
    "Panjnad + Indus (Mithankot)": (28.94,70.58),
    "Swat + Kabul": (34.15,71.78),
    "Gilgit + Indus": (35.90,74.58),
}


def _df_points(df, coord_dict, name_col="name"):
    if df is None or df.empty:
        return pd.DataFrame(columns=["name","lat","lon","info"])
    rows = []
    for _, r in df.iterrows():
        name = str(r.get(name_col, ""))
        p = coord_dict.get(name)
        if p:
            info = " | ".join(f"{k}: {v}" for k, v in r.items() if k != name_col and pd.notna(v))
            rows.append({"name": name, "lat": p[0], "lon": p[1], "info": info})
    return pd.DataFrame(rows)


def pakistan_water_map(
    rivers_df=None, dams_df=None, barrages_df=None, confluences_df=None,
    lakes_df=None, forests_df=None, india_df=None, solar_df=None,
    show_rivers=True, show_canals=True, show_dams=True, show_barrages=True,
    show_confluences=True, show_lakes=True, show_forests=True,
    show_glaciers=True, show_india_projects=True, show_western_projects=True, show_solar_projects=True,
    show_solar_labels=False, solar_highlight_project=None, show_labels=True, center=(30.5, 70.5), projection_scale=5.2,
):
    fig = go.Figure()

    if show_rivers:
        for name, pts in RIVER_PATHS.items():
            fig.add_trace(go.Scattergeo(
                lat=[p[0] for p in pts], lon=[p[1] for p in pts],
                mode="lines", name=f"River — {name}",
                line=dict(width=2.6), hoverinfo="name"
            ))

    if show_canals:
        for name, pts in LINK_PATHS.items():
            fig.add_trace(go.Scattergeo(
                lat=[p[0] for p in pts], lon=[p[1] for p in pts],
                mode="lines", name=f"Link canal — {name}",
                line=dict(width=1.4, dash="dash"), hoverinfo="name"
            ))

    def add_inventory(df, coord_map, label, symbol, size=9):
        p = _df_points(df, coord_map)
        if p.empty:
            return
        fig.add_trace(go.Scattergeo(
            lat=p.lat, lon=p.lon, mode="markers" + ("+text" if show_labels else ""),
            text=p.name if show_labels else None,
            textposition="top center", customdata=p["info"],
            hovertemplate="<b>%{text}</b><br>%{customdata}<extra></extra>",
            name=label, marker=dict(size=size, symbol=symbol)
        ))

    # Curated coordinate maps from the project's existing inventories.
    dam_coords = {
        "Tarbela Dam": (34.08,72.70), "Diamer Basha Dam": (35.62,73.62),
        "Dasu Hydropower Project": (35.25,73.55), "Mohmand Dam": (34.70,71.85),
        "Warsak Dam": (34.16,71.56), "Mangla Dam": (33.15,73.65),
        "Nai Gaj Dam": (27.65,67.50), "Naulong Dam": (29.35,67.65),
    }
    barrage_coords = {
        "Nowshera Headworks": (34.01,72.00), "Chashma Barrage": (32.44,71.39),
        "Rasul Barrage": (32.77,73.45), "Marala Headworks": (32.67,74.46),
        "Khanki Barrage": (32.38,73.82), "Qadirabad Barrage": (32.27,73.71),
        "Trimmu Barrage": (31.24,72.12), "Balloki Headworks": (31.22,73.84),
        "Sidhnai Barrage": (30.49,72.21), "Sulemanki Barrage": (29.93,73.03),
        "Islam Barrage": (29.85,72.32), "Panjnad Barrage": (29.35,71.05),
        "Taunsa Barrage": (30.70,70.65), "Guddu Barrage": (28.43,69.74),
        "Sukkur Barrage": (27.71,68.86), "Kotri Barrage": (25.38,68.31),
    }

    if show_dams:
        add_inventory(dams_df, dam_coords, "Dams / hydropower", "circle", 10)
    if show_barrages:
        add_inventory(barrages_df, barrage_coords, "Barrages / headworks", "square", 9)

    if show_confluences:
        lat = [p[0] for p in CONFLUENCE_POINTS.values()]
        lon = [p[1] for p in CONFLUENCE_POINTS.values()]
        fig.add_trace(go.Scattergeo(
            lat=lat, lon=lon, mode="markers" + ("+text" if show_labels else ""),
            text=list(CONFLUENCE_POINTS), textposition="bottom center",
            name="Confluences", marker=dict(size=10, symbol="diamond"),
            hovertemplate="<b>%{text}</b><extra></extra>"
        ))

    if show_lakes:
        p = _df_points(lakes_df, LAKE_POINTS)
        if p.empty:
            p = pd.DataFrame([{"name":n,"lat":v[0],"lon":v[1],"info":"Representative lake location"} for n,v in LAKE_POINTS.items()])
        fig.add_trace(go.Scattergeo(
            lat=p.lat, lon=p.lon, mode="markers" + ("+text" if show_labels else ""), text=p.name if show_labels else None,
            customdata=p["info"], textposition="top center", name="Lakes / reservoirs",
            marker=dict(size=8, symbol="circle"), hovertemplate="<b>%{text}</b><br>%{customdata}<extra></extra>"
        ))

    if show_forests:
        p = _df_points(forests_df, FOREST_POINTS)
        if p.empty:
            p = pd.DataFrame([{"name":n,"lat":v[0],"lon":v[1],"info":"Representative forest location"} for n,v in FOREST_POINTS.items()])
        fig.add_trace(go.Scattergeo(
            lat=p.lat, lon=p.lon, mode="markers" + ("+text" if show_labels else ""), text=p.name if show_labels else None,
            textposition="bottom center", name="Forests", marker=dict(size=9, symbol="triangle-up"),
            hovertemplate="<b>%{text}</b><br>%{customdata}<extra></extra>"
        ))

    if show_glaciers:
        lat=[v[0] for v in GLACIER_POINTS.values()]; lon=[v[1] for v in GLACIER_POINTS.values()]
        fig.add_trace(go.Scattergeo(
            lat=lat, lon=lon, mode="markers" + ("+text" if show_labels else ""), text=list(GLACIER_POINTS) if show_labels else None,
            textposition="top center", name="Glaciers / cryosphere", marker=dict(size=9, symbol="triangle-down"),
            hovertemplate="<b>%{text}</b><extra></extra>"
        ))

    if show_solar_projects and solar_df is not None and not solar_df.empty:
        s = solar_df.copy()
        required = {"project", "latitude", "longitude"}
        if required.issubset(s.columns):
            s = s.dropna(subset=["latitude", "longitude"]).copy()
            if not s.empty:
                cap = s["capacity_mw"].apply(lambda x: "Not specified" if pd.isna(x) else f"{float(x):,.3g} MW") if "capacity_mw" in s.columns else pd.Series("Not specified", index=s.index)
                custom = []
                for i, r in s.iterrows():
                    custom.append([
                        str(r.get("project", "")),
                        str(r.get("province_region", "")),
                        str(r.get("district_area", "")),
                        str(r.get("status", "")),
                        str(r.get("solar_type", "")),
                        cap.loc[i],
                        str(r.get("source_note", "")),
                        str(r.get("source_url", "")),
                    ])
                # Do not permanently print every project name.  Dense Pakistani
                # project clusters (especially Punjab/Sindh) otherwise produce
                # overlapping Plotly labels.  Full names remain available on hover.
                fig.add_trace(go.Scattergeo(
                    lat=s["latitude"], lon=s["longitude"],
                    mode="markers",
                    customdata=custom,
                    name="Pakistan — Solar projects / programs",
                    marker=dict(size=11, symbol="star-diamond"),
                    hovertemplate=(
                        "<b>%{customdata[0]}</b><br>Province/Region: %{customdata[1]}"
                        "<br>Area: %{customdata[2]}<br>Status: %{customdata[3]}"
                        "<br>Type: %{customdata[4]}<br>Capacity: %{customdata[5]}"
                        "<br><i>%{customdata[6]}</i><extra></extra>"
                    )
                ))

                # Optional single-project label: one label can never collide with
                # the whole inventory.  The selected project is also emphasized.
                if show_solar_labels and solar_highlight_project:
                    h = s[s["project"].astype(str) == str(solar_highlight_project)]
                    if not h.empty:
                        hr = h.iloc[0]
                        hcap = "Not specified" if pd.isna(hr.get("capacity_mw")) else f"{float(hr.get('capacity_mw')):,.3g} MW"
                        fig.add_trace(go.Scattergeo(
                            lat=[hr["latitude"]], lon=[hr["longitude"]],
                            mode="markers+text",
                            text=[str(hr["project"])],
                            textposition="top center",
                            name="Selected solar project",
                            showlegend=False,
                            marker=dict(size=15, symbol="star-diamond"),
                            hovertemplate=(
                                f"<b>{str(hr['project'])}</b><br>Province/Region: {str(hr.get('province_region',''))}"
                                f"<br>Area: {str(hr.get('district_area',''))}<br>Status: {str(hr.get('status',''))}"
                                f"<br>Type: {str(hr.get('solar_type',''))}<br>Capacity: {hcap}<extra></extra>"
                            )
                        ))

    if india_df is not None and not india_df.empty:
        all_rows=[]
        western_rows=[]
        for _, r in india_df.iterrows():
            name=str(r.get("project","")); p=INDIA_PROJECT_COORDS.get(name)
            if not p: continue
            row=(name,p[0],p[1],str(r.get("status","")),float(r.get("capacity_mw",0)),str(r.get("river","")))
            all_rows.append(row)
            if name in WESTERN_RIVER_PROJECTS:
                western_rows.append(row)
        if show_india_projects and all_rows:
            fig.add_trace(go.Scattergeo(
                lat=[x[1] for x in all_rows], lon=[x[2] for x in all_rows],
                mode="markers" + ("+text" if show_labels else ""),
                text=[x[0] for x in all_rows] if show_labels else None,
                textposition="top center",
                customdata=[[x[3],x[4],x[5]] for x in all_rows],
                name="India — 17-project dataset",
                marker=dict(size=10, symbol="star"),
                hovertemplate="<b>%{text}</b><br>Status: %{customdata[0]}<br>Capacity: %{customdata[1]} MW<br>River: %{customdata[2]}<extra></extra>"
            ))
        if show_western_projects and western_rows:
            fig.add_trace(go.Scattergeo(
                lat=[x[1] for x in western_rows], lon=[x[2] for x in western_rows],
                mode="markers" + ("+text" if show_labels else ""),
                text=[x[0] for x in western_rows] if show_labels else None,
                textposition="bottom center",
                customdata=[[x[3],x[4],x[5]] for x in western_rows],
                name="India — Western Rivers / IWT technical context",
                marker=dict(size=15, symbol="star-open"),
                hovertemplate="<b>%{text}</b><br>Status: %{customdata[0]}<br>Capacity: %{customdata[1]} MW<br>River: %{customdata[2]}<br><i>Project-level treaty status should be checked against primary records.</i><extra></extra>"
            ))

    fig.update_geos(
        scope="asia", center=dict(lat=center[0],lon=center[1]), projection_scale=projection_scale,
        showland=True, landcolor="rgb(241,239,230)", showocean=True, oceancolor="rgb(221,236,245)",
        showcountries=True, countrycolor="rgb(105,105,105)", countrywidth=0.8,
        showcoastlines=True, coastlinecolor="rgb(75,75,75)", coastlinewidth=0.8,
        showlakes=True, lakecolor="rgb(200,225,240)",
        lonaxis=dict(showgrid=True, gridcolor="rgba(100,100,100,.15)"),
        lataxis=dict(showgrid=True, gridcolor="rgba(100,100,100,.15)"),
    )
    fig.update_layout(
        height=760, margin=dict(l=0,r=0,t=5,b=0),
        legend=dict(orientation="v", x=1.01, y=1, xanchor="left", yanchor="top",
                    bgcolor="rgba(255,255,255,.90)", bordercolor="rgba(80,80,80,.3)", borderwidth=1),
        hoverlabel=dict(align="left"),
    )
    return fig

import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import *
from expanded_inventory import *
from development_framework import sdg_table, mdg_table, vision_table, crosswalk_table, DEVELOPMENT_DOMAINS
from data_analytics import load_uploaded_file, coerce_numeric, chart_candidates
from water_quality_analytics import (
    detect_basin_column, detect_telemetry_columns, detect_water_quality_columns,
    telemetry_variance_by_basin, water_quality_summary, generate_visualization_script,
)
from socio_agro_inputs import (
    CROP_SEASONS, RABI, KHARIF, MAJOR_CROP_SEASONS, APICULTURE, AQUACULTURE,
    APICULTURE_INDICATORS, AQUACULTURE_INDICATORS, DEFAULT_SOCIO_AGRO_DATA,
    SOCIO_AGRO_METRICS, GRAPH_TYPES
)
from desert_data import DESERTS as DESERT_CATALOG
from esg_framework import ESG, ISO_STANDARDS
from indian_projects import PROJECTS as INDIAN_PROJECTS, TECHNICAL_POINTS, INTER_BASIN
from india_indus_hydropower import PROJECTS_DF as INDIA_INDUS_HYDRO, TOTAL_CAPACITY_MW, OPERATIONAL_CAPACITY_MW, UNDER_CONSTRUCTION_CAPACITY_MW, SOURCE_URLS as INDIA_HYDRO_SOURCES, MAP_NOTE
from india_hydropower_map import india_indus_projects_map
from soil_environment import SOIL_ANALYTICS
from map_input import map_uploaded_data
from solar_projects import PROJECTS_DF as SOLAR_PROJECTS, known_capacity_by_region, source_urls as solar_source_urls
import map_view
from map_view import water_map
from interactive_pakistan_map import pakistan_water_map
from telecommunication import WESTERN_RIVERS, EASTERN_RIVERS, APPROX_COORDS, SOURCE_DOCUMENTS, SOURCE_NOTE
from network_view import river_network
from hydraulic_model import scenario_summary
from weather_hydraulic import CITY_CONFIG, simulated_live_weather, hydraulic_hazard, telemetry_with_hazard
from sebal_gee import (
    EE_AVAILABLE, GEEMAP_IMPORT_ERROR, GEOPANDAS_IMPORT_ERROR,
    earth_engine_status, initialize_ee, indus_basin_geodataframe,
    monthly_sebal, sebal_image, zonal_statistics, geemap_map,
)
from sebal_upload_analytics import read_uploaded_table, valid_spatial_rows
from iwt_treaty_reference import render as render_iwt_reference
def _safe_sebal_bar_chart(df, key="sebal_et24_chart"):
    """Render SEBAL ET24 summary without Streamlit auto-inference failures.

    Streamlit's st.bar_chart auto-detects x/y columns. SEBAL summary tables often
    contain mixed text and numeric fields, so we explicitly select the label and
    numeric ET column before plotting.
    """
    import numpy as np
    import plotly.express as px

    if df is None or df.empty:
        st.info("No SEBAL ET24 data are available for the chart.")
        return

    work = df.copy()
    # Prefer the common SEBAL ET24 naming variants.
    et_candidates = [
        "ET24", "et24", "ET24_mm", "et24_mm", "ET24 (mm/day)",
        "ET24_mm_day", "et24_mm_day", "ET_24", "et_24"
    ]
    et_col = next((c for c in et_candidates if c in work.columns), None)
    if et_col is None:
        # Fall back to a numeric column whose name contains ET.
        numeric_cols = work.select_dtypes(include="number").columns.tolist()
        et_like = [c for c in numeric_cols if "et" in str(c).lower()]
        et_col = et_like[0] if et_like else None

    if et_col is None:
        st.warning("SEBAL ET24 chart skipped because no numeric ET24 field was found.")
        return

    label_candidates = ["zone", "Zone", "land_cover", "landcover", "class", "label", "description"]
    label_col = next((c for c in label_candidates if c in work.columns), None)
    if label_col is None:
        label_col = work.columns[0]

    chart_df = work[[label_col, et_col]].copy()
    chart_df[et_col] = pd.to_numeric(chart_df[et_col], errors="coerce")
    chart_df = chart_df.replace([np.inf, -np.inf], np.nan).dropna(subset=[et_col])
    chart_df[label_col] = chart_df[label_col].astype(str)

    if chart_df.empty:
        st.warning("SEBAL ET24 chart skipped because all ET24 values are missing or non-numeric.")
        return

    # Plotly receives exactly one categorical and one numeric column, avoiding
    # st.bar_chart's mixed-column inference problem.
    fig = px.bar(
        chart_df, x=label_col, y=et_col,
        title="SEBAL 24-hour evapotranspiration (ET24)",
        labels={label_col: "SEBAL zone", et_col: "ET24 (mm/day)"},
        hover_data={et_col: ":.3f"},
    )
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True, key=key)

try:
    from streamlit_folium import st_folium
except Exception as _st_folium_exc:
    st_folium = None
from simulation_engine import ENGINES
from simulation_registry import SIMULATION_CATALOG
from additional_simulation_engines import (
    groundwater_balance, drought_index, sediment_load, water_quality_index,
    irrigation_schedule, socio_agro_projection
)
from hydrology_engine import monthly_water_balance, reservoir_rule_curve
from flood_engine import flood_scenario, rainfall_sweep
from crop_water_engine import crop_comparison, CROP_COEFFICIENTS
from climate_engine import climate_stress, sensitivity_table
from monte_carlo_engine import monte_carlo_risk, summarize
from iwt_compliance_engine import ExchangeRecord, compliance_matrix, gap_score, ARTICLE_BASELINE
from iwt_data_exchange_engine import normalize_exchange_df, compare_dataset_coverage, empty_template
from iwt_timeline_engine import timeline_df
from iwt_dispute_resolution_engine import pathway
from iwt_evidence_engine import evidence_ledger
from iwt_scenario_engine import scenario_matrix

st.set_page_config(
    page_title="IndusSphere Pakistan",
    page_icon="🇵🇰",
    layout="wide",
    initial_sidebar_state="expanded",
)

CREATOR = "Engr. Syed Hassan Iqbal Shah"

# ---------------------------------------------------------------------------
# Visual styling — modeled on the classic Pakistan Water/Terrain Explorer
# layout: branded sidebar navigation, wide content area, cards and tables.
# ---------------------------------------------------------------------------
st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
[data-testid="stSidebar"] {min-width: 285px; max-width: 320px;}
.hero {
    padding: 1.1rem 1.35rem; border-radius: 14px; margin-bottom: 1rem;
    border: 1px solid rgba(49,51,63,.15);
    background: linear-gradient(135deg, rgba(27,94,32,.10), rgba(25,118,210,.08));
}
.hero h1 {margin-bottom:.2rem;}
.small-note {font-size:.86rem; opacity:.75;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def filter_df(df, province="All", search=""):
    x = df.copy()
    if province != "All" and not x.empty:
        cols = [c for c in ["province_region", "region", "province", "territory", "area"] if c in x.columns]
        if cols:
            mask = pd.Series(False, index=x.index)
            for c in cols:
                mask = mask | x[c].astype(str).str.contains(province, case=False, na=False)
            x = x[mask]
    if search.strip() and not x.empty:
        q = search.strip()
        mask = x.astype(str).apply(lambda col: col.str.contains(q, case=False, na=False)).any(axis=1)
        x = x[mask]
    return x


def show_table(df, columns=None):
    x = df.copy()
    if columns:
        columns = [c for c in columns if c in x.columns]
        if columns:
            x = x[columns]
    st.dataframe(x, use_container_width=True, hide_index=True)


# ---------------------------------------------------------------------------
# Sidebar — intentionally mirrors the reference explorer's navigation model.
# ---------------------------------------------------------------------------
SECTIONS = [
    "🏠 Overview",
    "🗺️ Interactive Pakistan Water Map",
    "☀️ Pakistan Solar Projects",
    "🗺️ Provinces & Territories",
    "🌊 Rivers",
    "🚧 Dams & Barrages",
    "🔀 Link Canals",
    "🌡️ Climatic Regions",
    "⛰️ Mountain Ranges",
    "🏞️ Lakes",
    "🏜️ Deserts",
    "⚠️ Disaster Risk Context",
    "📈 Socio-Economic & Agro-Economic",
    "🗺️ Geo-Political & Strategic",
    "🇨🇳 China Hydropower (CPEC)",
    "📐 India Upstream Dam Disputes",
    "🗺️ India Indus-Basin Hydropower (17 Projects)",
    "⚖️ IWT Legal & Data Exchange",
    "1960 Dam Design",
    "Western Rivers Pakistan",
    "IWT Main points",
    "Impact on Transboundary Water Cooperation",
    "The IWT Treaty",
    "Article XII(3) Modification by Consent",
    "🌲 Forests & Parks",
    "🌍 SDGs / MDGs / Vision 2030",
    "🌦️ Simulated Weather & Hydraulic Hazard",
    "🛰️ SEBAL Evapotranspiration (GEE)",
    "🧮 Interactive Hydraulic Models",
    "⚙️ Simulation Engines",
    "📡 WAPDA Telecommunication Networks",
    "🇮🇳 Chenab Projects & IWT Flow Concerns",
    "🌍 ESG / ISO / SDG / MDG / Vision 2030",
    "📊 Data Analytics & Graphs",
    "🧭 Regional Profiles",
    "📚 Sources",
]

with st.sidebar:
    st.markdown("# 🇵🇰 IndusSphere")
    st.caption("Pakistan Water, Terrain, Climate & Strategic Explorer")
    st.markdown(f"**Creator:** {CREATOR}")
    st.divider()
    choice = st.radio("Go to section", SECTIONS, label_visibility="collapsed")
    st.divider()
    st.header("🔎 Global Filters")
    province = st.selectbox("Province / Region", ["All"] + list(PROVINCES))
    search = st.text_input("Search inventory", placeholder="river, dam, lake, forest...")
    st.divider()
    st.header("🧮 Scenario Inputs")
    exposure = st.slider("Exposure", 0, 100, 60)
    vulnerability = st.slider("Population vulnerability", 0, 100, 55)
    sensitivity = st.slider("Sensitivity", 0, 100, 55)
    adaptive = st.slider("Adaptive capacity", 0, 100, 50)
    criticality = st.slider("Asset / service criticality", 0, 100, 65)
    scenario = st.selectbox("Scenario", ["Baseline", "Medium", "Worst-Case"])
    st.divider()
    st.caption("Built with Streamlit · Pandas · Plotly")

st.markdown(f"""
<div class="hero">
<h1>🇵🇰 IndusSphere Pakistan</h1>
<div>Integrated Water, Terrain, Climate, Disaster-Risk, Socio-Economic & Strategic Intelligence Explorer</div>
<div class="small-note">Creator: {CREATOR}</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
if choice == "🏠 Overview":
    st.title("Pakistan Water, Terrain & Integrated Intelligence Explorer")
    st.write("Interactive national-scale exploration of Pakistan's water systems, terrain, climate, hazards, economy, agriculture and strategic infrastructure.")
    cols = st.columns(6)
    metrics = [
        ("Regions", len(PROVINCES)), ("Rivers", len(RIVERS)),
        ("Dams", len(DAMS)), ("Barrages", len(BARRAGES)),
        ("Lakes", len(LAKES) + len(EXTRA_LAKES)), ("Parks", len(NATIONAL_PARKS) + len(EXTRA_PARKS)),
    ]
    for col, (label, value) in zip(cols, metrics): col.metric(label, value)
    st.subheader("National water and terrain view")
    st.caption("Use the dedicated Interactive Pakistan Water Map section for detailed layer controls, legends and India/IWT project overlays.")
    overview_lakes = pd.concat([LAKES, EXTRA_LAKES], ignore_index=True).drop_duplicates(subset=["name"])
    overview_fig = pakistan_water_map(
        rivers_df=RIVERS, dams_df=DAMS, barrages_df=BARRAGES, confluences_df=CONFLUENCES,
        lakes_df=overview_lakes, forests_df=FORESTS, india_df=INDIA_INDUS_HYDRO,
        show_rivers=True, show_canals=True, show_dams=True, show_barrages=True,
        show_confluences=True, show_lakes=True, show_forests=True, show_glaciers=True,
        show_india_projects=True, show_western_projects=True, show_solar_projects=True, show_labels=False,
        center=(30.5,70.5), projection_scale=5.2
    )
    st.plotly_chart(overview_fig, use_container_width=True, config={"scrollZoom": True, "displaylogo": False, "responsive": True})
    st.subheader("Regional overview")
    show_table(filter_df(REGIONAL_PROFILE, province, search))
    st.info("Map points are curated visualization coordinates. Verify authoritative GIS, engineering and survey data before professional use.")

elif choice == "🗺️ Interactive Pakistan Water Map":
    st.title("🗺️ Interactive Pakistan Water, Terrain & IWT Map")
    st.caption("National-scale interactive visualization. Coordinates and simplified river/canal paths are for visualization; verify authoritative GIS/survey data before engineering use.")

    c1,c2,c3,c4 = st.columns(4)
    with c1:
        show_rivers = st.checkbox("🌊 Rivers", True)
        show_canals = st.checkbox("🔀 Link canals", True)
        show_lakes = st.checkbox("🏞️ Lakes", True)
        show_glaciers = st.checkbox("❄️ Glaciers", True)
    with c2:
        show_dams = st.checkbox("🚧 Dams", True)
        show_barrages = st.checkbox("🟦 Barrages", True)
        show_confluences = st.checkbox("◆ Confluences", True)
        show_forests = st.checkbox("🌲 Forests", True)
    with c3:
        show_india = st.checkbox("🇮🇳 India 17 projects", True)
        show_western = st.checkbox("Western-river projects", True)
        show_solar = st.checkbox("☀️ Solar projects", True)
        show_labels = st.checkbox("Labels", True)
        map_zoom = st.slider("Map detail / zoom", 3.8, 7.0, 5.2, 0.1)
    with c4:
        focus = st.selectbox("Map focus", ["Pakistan", "Northern Pakistan", "Indus Plain", "Sindh / Delta", "Western & Northern rivers"])

    focus_cfg = {
        "Pakistan": ((30.5,70.5), map_zoom),
        "Northern Pakistan": ((34.5,74.0), max(map_zoom,5.5)),
        "Indus Plain": ((30.5,71.0), max(map_zoom,5.3)),
        "Sindh / Delta": ((26.7,68.0), max(map_zoom,5.5)),
        "Western & Northern rivers": ((32.8,71.5), max(map_zoom,5.3)),
    }
    center, scale = focus_cfg[focus]
    lakes_all = pd.concat([LAKES, EXTRA_LAKES], ignore_index=True).drop_duplicates(subset=["name"])
    forest_map = FORESTS.copy() if "FORESTS" in globals() else pd.DataFrame()

    fig = pakistan_water_map(
        rivers_df=filter_df(RIVERS, province, search),
        dams_df=filter_df(DAMS, province, search),
        barrages_df=filter_df(BARRAGES, province, search),
        confluences_df=filter_df(CONFLUENCES, province, search),
        lakes_df=filter_df(lakes_all, province, search),
        forests_df=filter_df(forest_map, province, search),
        india_df=INDIA_INDUS_HYDRO,
        solar_df=SOLAR_PROJECTS,
        show_rivers=show_rivers, show_canals=show_canals, show_dams=show_dams,
        show_barrages=show_barrages, show_confluences=show_confluences, show_lakes=show_lakes,
        show_forests=show_forests, show_glaciers=show_glaciers, show_india_projects=show_india,
        show_western_projects=show_western, show_solar_projects=show_solar, show_labels=show_labels, center=center, projection_scale=scale
    )
    st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True, "displaylogo": False, "responsive": True})

    left,right = st.columns([3,1])
    with right:
        st.markdown("### Map Legend")
        legend = [
            ("🌊", "Rivers", "Main river systems and tributaries"),
            ("🔀", "Link canals", "Simplified inter-river transfer routes"),
            ("🚧", "Dams / hydropower", "Major Pakistani dams/projects"),
            ("🟦", "Barrages / headworks", "Major diversion/control structures"),
            ("◆", "Confluences", "Selected river junctions"),
            ("🏞️", "Lakes / reservoirs", "Representative lake locations"),
            ("🌲", "Forests", "Selected forest locations"),
            ("❄️", "Glaciers / cryosphere", "Representative glacier locations"),
            ("☀️", "Solar projects / programs", "Officially documented solar projects and solarization programs"),
            ("🇮🇳", "India projects", "17-project dashboard dataset"),
            ("⚠️", "Western-river IWT context", "India projects associated with Western Rivers in the project dataset"),
        ]
        for icon,name,desc in legend:
            st.markdown(f"**{icon} {name}**  \\n{desc}")
        st.info("The term 'disputed' is not used as a blanket legal classification: project-level treaty objections, stakeholder positions and formal adjudicative findings can differ.")
    with left:
        st.subheader("Layer notes")
        st.write("The map combines the project's curated inventories with representative coordinates and simplified display paths. The uploaded Indus Waters Treaty map identifies the major rivers, named barrages and link canals used as a source reference.")
        st.write("For water-body completeness, the national Water Body Inventory describes an interactive inventory covering dams, rivers, lakes, canals and other surface-water resources. The current app can be extended with that dataset when licensed/available for integration.")
        st.write("Natural Earth provides general-purpose physical layers including rivers/lake centerlines, lakes/reservoirs and glaciated areas; these are suitable as a geographic base layer but are not a substitute for Pakistan's authoritative engineering GIS.")

elif choice == "🗺️ Provinces & Territories":
    st.title("Provinces & Territories of Pakistan")
    show_table(filter_df(REGIONAL_PROFILE, province, search))
    st.subheader("Major cities / service centres")
    show_table(filter_df(MAJOR_CITIES, province, search))

elif choice == "🌊 Rivers":
    st.title("Rivers of Pakistan")
    st.plotly_chart(river_network(), use_container_width=True)
    show_table(filter_df(RIVERS, province, search), ["name","river_system","province_region","upstream","downstream","confluences","notes"])
    st.download_button("⬇️ Download rivers CSV", filter_df(RIVERS, province, search).to_csv(index=False).encode(), "indussphere_rivers.csv", "text/csv")
    st.subheader("River confluences")
    show_table(filter_df(CONFLUENCES, province, search))

elif choice == "🚧 Dams & Barrages":
    st.title("Dams, Barrages & Hydropower Projects")
    st.subheader("Dams / hydropower structures")
    show_table(filter_df(DAMS, province, search))
    st.subheader("Barrages / headworks")
    show_table(filter_df(BARRAGES, province, search))
    st.subheader("Upstream / downstream relationships")
    rel = pd.concat([filter_df(DAMS, province, search), filter_df(BARRAGES, province, search)], ignore_index=True)
    show_table(rel, ["name","river","province_region","upstream","downstream","status","notes"])

elif choice == "🔀 Link Canals":
    st.title("Link Canals — Indus Basin Irrigation System (IBIS)")
    st.write("Link canals redistribute water between river systems and irrigation commands within the Indus Basin network.")
    show_table(filter_df(LINK_CANALS, province, search))

elif choice == "🌡️ Climatic Regions":
    st.title("Climatic Regions of Pakistan")
    show_table(pd.DataFrame(CLIMATE_REGIONS))
    if "region" in pd.DataFrame(CLIMATE_REGIONS).columns:
        region_options = pd.DataFrame(CLIMATE_REGIONS)["region"].dropna().tolist()
        if region_options:
            selected = st.selectbox("Climate region detail", region_options)
            row = pd.DataFrame(CLIMATE_REGIONS)
            st.dataframe(row[row["region"] == selected], use_container_width=True, hide_index=True)

elif choice == "⛰️ Mountain Ranges":
    st.title("Mountain Ranges of Pakistan")
    m = filter_df(MOUNTAINS, province, search)
    show_table(m)
    if not m.empty and "name" in m.columns:
        selected = st.selectbox("Select mountain range", m["name"].tolist())
        row = m[m["name"] == selected].iloc[0]
        st.subheader(selected)
        a,b = st.columns(2)
        for i,(k,v) in enumerate(row.items()):
            (a if i % 2 == 0 else b).markdown(f"**{k.replace('_',' ').title()}:** {v}")

elif choice == "🏞️ Lakes":
    st.title("Lakes of Pakistan")
    lakes = pd.concat([LAKES, EXTRA_LAKES], ignore_index=True).drop_duplicates(subset=["name"])
    lakes = filter_df(lakes, province, search)
    st.metric("Inventory entries", len(lakes))
    show_table(lakes)
    st.download_button("⬇️ Download lakes CSV", lakes.to_csv(index=False).encode(), "indussphere_lakes.csv", "text/csv")

elif choice == "🏜️ Deserts":
    st.title("Deserts of Pakistan")
    deserts = filter_df(DESERT_CATALOG, province, search)
    show_table(deserts)
    if not deserts.empty:
        st.subheader("Desert locations")
        # Representative visualization points; not official boundaries.
        desert_points = {
            "Thar Desert": (24.9, 70.2), "Cholistan Desert": (29.4, 71.6),
            "Thal Desert": (32.0, 71.1), "Kharan Desert": (28.6, 65.2),
            "Katpana Cold Desert": (35.3, 75.6), "Sarfaranga Cold Desert": (35.3, 75.7),
        }
        import plotly.graph_objects as go
        pts = [(n, *desert_points[n]) for n in deserts["name"] if n in desert_points]
        if pts:
            fig = go.Figure(go.Scattergeo(lat=[x[1] for x in pts], lon=[x[2] for x in pts],
                text=[x[0] for x in pts], mode="markers+text", textposition="top center",
                marker=dict(size=10), name="Deserts"))
            fig.update_geos(scope="asia", center=dict(lat=30.5,lon=70.5), projection_scale=5.0,
                            showcountries=True, showland=True, showocean=True)
            fig.update_layout(height=560, margin=dict(l=0,r=0,t=10,b=0))
            st.plotly_chart(fig, use_container_width=True)

elif choice == "⚠️ Disaster Risk Context":
    st.title("National Disaster Risk Context")
    t1,t2,t3,t4,t5 = st.tabs(["Hydro-meteorological","Tectonic","Climatological / Emerging","Anthropogenic","Exposure & Vulnerability"])
    with t1:
        items = HAZARDS.get("Hydro-meteorological", [])
        show_table(pd.DataFrame(items))
    with t2:
        show_table(pd.DataFrame(HAZARDS.get("Tectonic", [])))
    with t3:
        show_table(pd.DataFrame(HAZARDS.get("Climatological / Emerging", [])))
        show_table(EMERGING_CLIMATE)
    with t4:
        show_table(pd.DataFrame(HAZARDS.get("Anthropogenic", [])))
    with t5:
        show_table(DISASTER_VULNERABILITY)
    st.subheader("Scenario definitions")
    show_table(SCENARIO_DETAIL)

elif choice == "📈 Socio-Economic & Agro-Economic":
    st.title("Socio-Economic & Agro-Economic Domains")
    a,b = st.tabs(["Socio-Economic","Agro-Economic"])
    with a:
        for k,v in SOCIO_ECONOMIC.items(): st.markdown(f"**{k}:** {v}")
    with b:
        for k,v in AGRO_ECONOMIC.items(): st.markdown(f"**{k}:** {v}")
        st.subheader("Major crop seasons")
        st.dataframe(MAJOR_CROP_SEASONS, use_container_width=True, hide_index=True)
        season = st.selectbox("Season", ["Rabi", "Kharif"], key="agro_season")
        season_df = RABI if season == "Rabi" else KHARIF
        st.dataframe(season_df[["season", "crop", "typical_window", "engineering_water_note"]], use_container_width=True, hide_index=True)
        st.subheader("Apiculture")
        st.dataframe(pd.DataFrame(APICULTURE_INDICATORS), use_container_width=True, hide_index=True)
        st.subheader("Aquaculture")
        st.dataframe(pd.DataFrame(AQUACULTURE_INDICATORS), use_container_width=True, hide_index=True)

    st.subheader("Input-driven socio/agro data")
    st.caption("Edit the values below. Charts are calculated from the current table, so replacing the demonstration values with your own province/region dataset changes the outputs immediately.")
    edited = st.data_editor(
        DEFAULT_SOCIO_AGRO_DATA.copy(), num_rows="dynamic", use_container_width=True,
        column_config={
            "province/region": st.column_config.TextColumn("province/region"),
            "cultivated area": st.column_config.NumberColumn("cultivated area", min_value=0),
            "crop production": st.column_config.NumberColumn("crop production", min_value=0),
            "employment": st.column_config.NumberColumn("employment", min_value=0),
            "honey production": st.column_config.NumberColumn("honey production", min_value=0),
            "aquaculture production": st.column_config.NumberColumn("aquaculture production", min_value=0),
        }, key="socio_agro_editor")
    edited = edited.dropna(subset=["province/region"]).copy()
    for col in SOCIO_AGRO_METRICS.values():
        edited[col] = pd.to_numeric(edited[col], errors="coerce").fillna(0)

    graph_type = st.selectbox("Graph type", GRAPH_TYPES, key="socio_agro_graph_type")
    metric_label = st.selectbox("Metric", list(SOCIO_AGRO_METRICS), key="socio_agro_metric")
    metric_col = SOCIO_AGRO_METRICS[metric_label]
    if graph_type == "Scatter plot":
        x_label = st.selectbox("X metric", list(SOCIO_AGRO_METRICS), index=0, key="socio_agro_x")
        y_label = st.selectbox("Y metric", list(SOCIO_AGRO_METRICS), index=min(1, len(SOCIO_AGRO_METRICS)-1), key="socio_agro_y")
        fig = px.scatter(edited, x=SOCIO_AGRO_METRICS[x_label], y=SOCIO_AGRO_METRICS[y_label], hover_name="province/region", title=f"{y_label} vs {x_label}")
    elif graph_type == "Bar chart":
        fig = px.bar(edited, x="province/region", y=metric_col, title=metric_label)
    elif graph_type == "Pie chart":
        fig = px.pie(edited, names="province/region", values=metric_col, title=metric_label)
    else:
        fig = px.line(edited, x="province/region", y=metric_col, markers=True, title=metric_label)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Input-driven projection")
    projection_growth = st.slider("Annual growth / change assumption (%)", -10.0, 20.0, 3.0, 0.5, key="socio_agro_growth")
    projection_years = st.slider("Projection years", 1, 20, 5, key="socio_agro_years")
    proj = socio_agro_projection(edited, metric_col, projection_growth, projection_years)
    st.plotly_chart(px.line(proj, x="year", y=metric_col, color="province/region", markers=True, title=f"Projected {metric_label}"), use_container_width=True)
    st.dataframe(proj, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Download edited socio/agro data", edited.to_csv(index=False).encode(), "socio_agro_input_data.csv", "text/csv", key="download_socio_agro")
    st.download_button("⬇️ Download projection CSV", proj.to_csv(index=False).encode(), "socio_agro_projection.csv", "text/csv", key="download_socio_agro_projection")

elif choice == "🗺️ Geo-Political & Strategic":
    st.title("Geo-Political & Strategic Domains")
    for k,v in GEO_STRATEGIC.items():
        with st.expander(k, expanded=False): st.write(v)
    st.warning("The dashboard presents documented issues and competing claims neutrally. It does not rank political positions or decide disputed questions.")

elif choice == "☀️ Pakistan Solar Projects":
    st.title("☀️ Pakistan Solar Projects & Solarization Programs")
    st.caption("National solar inventory covering Punjab, Sindh, Khyber Pakhtunkhwa, Balochistan, Gilgit-Baltistan, Azad Jammu & Kashmir and Islamabad Capital Territory. Capacity is shown only where the cited source provides an aggregate value.")

    region_options = ["All"] + sorted(SOLAR_PROJECTS["province_region"].dropna().unique().tolist())
    r1, r2, r3 = st.columns(3)
    with r1:
        solar_region = st.selectbox("Province / region", region_options, key="solar_region")
    with r2:
        solar_status = st.selectbox("Status", ["All"] + sorted(SOLAR_PROJECTS["status"].dropna().unique().tolist()), key="solar_status")
    with r3:
        solar_type = st.selectbox("Solar type", ["All"] + sorted(SOLAR_PROJECTS["solar_type"].dropna().unique().tolist()), key="solar_type")

    sdf = SOLAR_PROJECTS.copy()
    if solar_region != "All": sdf = sdf[sdf.province_region == solar_region]
    if solar_status != "All": sdf = sdf[sdf.status == solar_status]
    if solar_type != "All": sdf = sdf[sdf.solar_type == solar_type]

    known = sdf["capacity_mw"].dropna()
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Records", len(sdf))
    k2.metric("Known capacity", f"{known.sum():,.2f} MW")
    k3.metric("Regions represented", sdf["province_region"].nunique())
    k4.metric("Capacity records", len(known))

    st.subheader("Interactive Pakistan solar map")
    st.caption("Solar project names are shown on hover to keep every province readable. Permanent labels are limited to one selected project so labels never overwrite one another.")
    highlight_options = ["None"] + sdf["project"].astype(str).tolist()
    highlight = st.selectbox("Highlight one solar project", highlight_options, key="solar_highlight_project")
    show_selected_label = st.checkbox("Show selected project label", value=True, key="solar_show_selected_label")

    solar_map = pakistan_water_map(
        rivers_df=RIVERS, dams_df=DAMS, barrages_df=BARRAGES, confluences_df=CONFLUENCES,
        lakes_df=pd.concat([LAKES, EXTRA_LAKES], ignore_index=True).drop_duplicates(subset=["name"]),
        forests_df=FORESTS, india_df=INDIA_INDUS_HYDRO, solar_df=sdf,
        show_rivers=True, show_canals=True, show_dams=True, show_barrages=True,
        show_confluences=False, show_lakes=False, show_forests=False, show_glaciers=False,
        show_india_projects=False, show_western_projects=False, show_solar_projects=True,
        show_solar_labels=show_selected_label and highlight != "None", solar_highlight_project=highlight if highlight != "None" else None,
        show_labels=False, center=(30.5,70.5), projection_scale=5.0
    )
    st.plotly_chart(solar_map, use_container_width=True, config={"scrollZoom": True, "displaylogo": False, "responsive": True})

    st.subheader("Solar inventory")
    display_cols = ["project","province_region","district_area","status","solar_type","capacity_mw","latitude","longitude","source_note"]
    st.dataframe(sdf[display_cols], use_container_width=True, hide_index=True)

    st.subheader("Known capacity by province / region")
    summary = known_capacity_by_region(sdf)
    if not summary.empty:
        st.bar_chart(summary.set_index("province_region")["capacity_mw"], use_container_width=True)
    else:
        st.info("No capacity values are available for the selected filters.")

    st.info("Important: solarization programs and project pipelines are not equivalent to commissioned utility-scale plants. Records without an official aggregate MW figure are retained with capacity marked as not specified rather than estimated.")
    st.download_button("⬇️ Download Pakistan solar project/program CSV", sdf.to_csv(index=False).encode("utf-8"), "pakistan_solar_projects.csv", "text/csv", key="dl_pakistan_solar")
    st.subheader("Sources")
    for url in solar_source_urls():
        st.markdown(f"- {url}")

elif choice == "🇨🇳 China Hydropower (CPEC)":
    st.title("The Financial Footprint of China's Investments in Pakistan's Hydropower")
    show_table(CHINA_HYDRO)
    st.caption("Project status and financing details are time-sensitive; verify against the linked primary institutional sources.")

elif choice == "🗺️ India Indus-Basin Hydropower (17 Projects)":
    st.title("🗺️ India Indus River System — 17 Hydropower Projects")
    st.info("Separate map and inventory for the 17-project grouping supplied for this dashboard. The map is informational and uses approximate visualization coordinates.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Projects", len(INDIA_INDUS_HYDRO))
    c2.metric("Total capacity", f"{TOTAL_CAPACITY_MW:,.1f} MW")
    c3.metric("Operational", f"{OPERATIONAL_CAPACITY_MW:,.1f} MW")
    c4.metric("Under construction", f"{UNDER_CONSTRUCTION_CAPACITY_MW:,.1f} MW")

    st.plotly_chart(india_indus_projects_map(), use_container_width=True)

    st.subheader("Operational Projects (10)")
    st.dataframe(INDIA_INDUS_HYDRO[INDIA_INDUS_HYDRO.status == "Operational"].drop(columns=["latitude", "longitude"]), use_container_width=True, hide_index=True)

    st.subheader("Under-Construction Projects (7)")
    st.dataframe(INDIA_INDUS_HYDRO[INDIA_INDUS_HYDRO.status == "Under Construction"].drop(columns=["latitude", "longitude"]), use_container_width=True, hide_index=True)

    st.subheader("Capacity by river system")
    basin_summary = INDIA_INDUS_HYDRO.groupby(["basin", "status"], as_index=False)["capacity_mw"].sum()
    st.dataframe(basin_summary, use_container_width=True, hide_index=True)
    st.plotly_chart(px.bar(basin_summary, x="basin", y="capacity_mw", color="status", barmode="group", title="Installed / listed capacity by Indus-basin river system"), use_container_width=True)

    st.subheader("Source and data-quality notes")
    st.write("The Central Electricity Authority hydro profile confirms the project names, river associations and installed-capacity figures used for the listed projects. NHPC independently lists Pakal Dul, Kiru, Ratle, Kwar, Uri-I Stage-II and Dulhasti Stage-II as under construction. The 17-project operational/under-construction grouping is retained as the dashboard dataset requested by the user; it should not be interpreted as the complete CEA inventory for Jammu & Kashmir.")
    for label, url in INDIA_HYDRO_SOURCES.items():
        st.markdown(f"- [{label}]({url})")
    st.caption(MAP_NOTE)
    st.download_button("⬇️ Download 17-project India Indus hydropower CSV", INDIA_INDUS_HYDRO.to_csv(index=False).encode(), "india_indus_17_hydropower_projects.csv", "text/csv", key="dl_india_indus_17")

elif choice == "📐 India Upstream Dam Disputes":
    st.title("India Upstream Projects — Technical Issues, Flow Concerns & IWT")
    st.warning("This section presents documented party positions, engineering issues and adjudicative records neutrally. A reported concern is not treated as an independently established fact unless supported by a cited source or uploaded dataset.")
    st.subheader("Pakal Dul (1,000 MW) and Ratle (850 MW)")
    show_table(INDIAN_PROJECTS)
    st.subheader("Technical points raised by Pakistan in the IWT proceedings")
    show_table(TECHNICAL_POINTS)
    st.subheader("Head Marala / crop-impact issue")
    st.info("The dashboard records reported concerns about reduced Chenab flows at Head Marala and potential consequences for irrigation and crops as stakeholder claims, rather than asserting a causal crop-loss estimate without a hydrological dataset.")
    st.subheader("Court of Arbitration (PCA) timeline")
    st.markdown("Selected procedural milestones are shown in the IWT Legal & Data Exchange section. The PCA case page currently records awards/orders through 31 August 2026, including an Award on Treaty Status and an Order on Interim Measures.")
    st.subheader("Reported inter-basin transfer concepts")
    show_table(INTER_BASIN)
    st.subheader("Current evidence workspace")
    st.write("Upload hydrological records in Data Analytics & Graphs to test flow, discharge, crop-water and Head Marala relationships quantitatively. The app does not infer causation from narrative claims alone.")

elif choice == "⚖️ IWT Legal & Data Exchange":
    st.title("⚖️ Indus Waters Treaty — Legal Baseline & Data-Exchange Explorer")
    st.write("An evidence-driven research and simulation workspace for examining IWT data-exchange records, institutional channels, timelines and dispute-resolution pathways. It does not determine whether a treaty violation occurred.")
    st.warning("Legal-status outputs are descriptive screening indicators. Treaty interpretation and compliance conclusions should be taken from the treaty text, applicable awards/orders, and verified evidence.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Legal Baseline", "Exchange Audit", "Timeline", "Resolution Pathways", "Evidence & Scenarios"])
    with tab1:
        st.subheader("Core treaty provisions")
        st.dataframe(pd.DataFrame([{"Provision":k,"Baseline":v} for k,v in ARTICLE_BASELINE.items()]), use_container_width=True, hide_index=True)
        st.markdown("**Key analytical principle:** examine the content of information, reporting frequency, and institutional channel separately before drawing any conclusion.")
        st.info("The app deliberately distinguishes treaty text, party positions, adjudicative findings, observed hydrological records and model-generated indicators.")

    with tab2:
        st.subheader("Hydrological data-exchange audit")
        st.caption("Enter documented events or upload a prepared exchange CSV. The resulting flags identify documentation gaps; they are not legal findings.")
        mode=st.radio("Input mode", ["Manual record", "CSV upload"], horizontal=True)
        if mode == "Manual record":
            c=st.columns(3)
            date=c[0].text_input("Date", "2026-09-01")
            river=c[1].text_input("River", "Chenab")
            dataset=c[2].text_input("Dataset", "Gauge / discharge")
            c=st.columns(4)
            frequency=c[0].selectbox("Frequency", ["Daily","Monthly","More frequently on request","Ad hoc","Unknown"])
            channel=c[1].selectbox("Transmission channel", ["PIC / Commissioners","Diplomatic channel","Other / unspecified"])
            notice=c[2].selectbox("Prior notice", ["Yes","No","Unknown"])
            source=c[3].text_input("Evidence/source", "User-provided record")
            rec=ExchangeRecord(date,river,dataset,frequency,channel,notice,source)
            result=pd.DataFrame(compliance_matrix([rec]))
            st.dataframe(result, use_container_width=True, hide_index=True)
            st.metric("Documentation-gap indicator", gap_score(rec))
            st.caption("Higher values mean more fields require documentary review; this is not a probability or legal-compliance score.")
        else:
            up=st.file_uploader("Upload exchange records", type=["csv","xlsx","xls"])
            if up:
                try:
                    if up.name.lower().endswith('.csv'): df=pd.read_csv(up)
                    else: df=pd.read_excel(up)
                    norm=normalize_exchange_df(df)
                    st.dataframe(norm,use_container_width=True,hide_index=True)
                    st.subheader("Dataset coverage")
                    cov=compare_dataset_coverage(norm)
                    st.dataframe(cov,use_container_width=True,hide_index=True)
                    st.download_button("Download normalized exchange CSV",norm.to_csv(index=False).encode(),"iwt_exchange_normalized.csv","text/csv")
                except Exception as e: st.error(f"Could not read file: {e}")
            else:
                st.download_button("Download blank exchange template",empty_template().to_csv(index=False).encode(),"iwt_exchange_template.csv","text/csv")

    with tab3:
        st.subheader("IWT research timeline")
        tl=timeline_df()
        st.plotly_chart(px.scatter(tl,x="date",y="category",text="event",hover_data=["source"],title="Selected treaty and arbitration events"),use_container_width=True)
        st.dataframe(tl,use_container_width=True,hide_index=True)
        st.caption("The timeline contains selected documented milestones; it is not an exhaustive chronology.")

    with tab4:
        st.subheader("Descriptive dispute-resolution pathways")
        issue=st.selectbox("Issue type", ["Data exchange","Technical design issue","Treaty interpretation"])
        rows=[{"Stage":a,"Description":b} for a,b in pathway(issue)]
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
        st.info("The appropriate pathway depends on the treaty provisions and characterization of the particular matter; the app does not select a legal forum as a recommendation.")

    with tab5:
        st.subheader("Evidence hierarchy")
        st.dataframe(evidence_ledger(),use_container_width=True,hide_index=True)
        st.subheader("Data-channel scenarios")
        st.dataframe(scenario_matrix(),use_container_width=True,hide_index=True)
        st.subheader("Primary current arbitration record")
        st.markdown("The PCA case record includes the 27 June 2025 Supplemental Award on Competence, 8 August 2025 Award on General Interpretation, 15 May 2026 Maximum Pondage Award, and 31 August 2026 Award on Treaty Status plus Order on Interim Measures.")

elif choice in {
    "1960 Dam Design",
    "Western Rivers Pakistan",
    "IWT Main points",
    "Impact on Transboundary Water Cooperation",
    "The IWT Treaty",
    "Article XII(3) Modification by Consent",
}:
    render_iwt_reference(choice)

elif choice == "🌲 Forests & Parks":
    st.title("Forests, National Parks & Recreational Areas")
    st.subheader("Forest types")
    show_table(FOREST_TYPES)
    st.subheader("Notable forests — location, area, history/origin, wildlife, attractions and recreation")
    forest_view = filter_df(FORESTS, province, search)
    show_table(forest_view)
    st.caption("Where covered-area or historical details are not present in the curated inventory, upload authoritative forestry records through Data Analytics rather than treating missing values as estimates.")

    st.subheader("National parks / protected / recreational areas")
    parks = pd.concat([NATIONAL_PARKS, EXTRA_PARKS], ignore_index=True).drop_duplicates(subset=["name"])
    parks_filtered = filter_df(parks, province, search)

    park_tab1, park_tab2 = st.tabs(["🗺️ Parks Map", "📍 Select a park for details"])
    with park_tab1:
        st.plotly_chart(map_view.parks_map(parks_filtered), use_container_width=True)
        st.caption("Park markers show representative locations for visualization; they are not official park boundaries.")
        show_table(parks_filtered)

    with park_tab2:
        park_names = parks_filtered["name"].tolist()
        if park_names:
            selected_park = st.selectbox("Select a park for details", park_names)
            selected_row = parks_filtered.loc[parks_filtered["name"] == selected_park].iloc[0]
            st.subheader(selected_park)
            c1, c2, c3 = st.columns(3)
            c1.metric("Region", selected_row.get("province_region", selected_row.get("region", "—")))
            c2.metric("Location", selected_row.get("location", "—"))
            c3.metric("Type / Focus", selected_row.get("focus", "—"))
            st.plotly_chart(map_view.parks_map(parks_filtered, selected_name=selected_park), use_container_width=True)
            st.caption("The star identifies the selected park. The marker is a representative map point, not a surveyed boundary.")
            st.dataframe(pd.DataFrame([selected_row]), use_container_width=True, hide_index=True)
        else:
            st.info("No parks match the current Province/Region or search filters.")

elif choice == "🌍 SDGs / MDGs / Vision 2030":
    st.title("UN SDGs / MDGs / Pakistan Vision 2030")
    view = st.selectbox("Framework", ["SDGs","MDGs","Vision 2030","Crosswalk","Development Domains"])
    if view == "SDGs": show_table(sdg_table())
    elif view == "MDGs": show_table(mdg_table())
    elif view == "Vision 2030": show_table(vision_table())
    elif view == "Crosswalk": show_table(crosswalk_table())
    else: show_table(pd.DataFrame({"Development domain": DEVELOPMENT_DOMAINS}))

elif choice == "🌦️ Simulated Weather & Hydraulic Hazard":
    st.title("🌦️ Simulated Live Weather, Rainfall & Hydraulic Hazard")
    st.write("A transparent screening workspace for three linked city–river-basin locations: Sialkot–Chenab, Jhelum–Jhelum and Lahore–Ravi.")
    st.warning("All weather, rainfall and telemetry values in this section are simulated. They are not live observations and must not be used as an operational flood warning or engineering design dataset.")

    city = st.selectbox("City / river basin", ["Sialkot", "Jhelum", "Lahore"], key="weather_city")
    cfg = CITY_CONFIG[city]
    current = simulated_live_weather(city)
    hazard = hydraulic_hazard(current)

    st.subheader("1. Simulated Live Weather & Rainfall")
    c = st.columns(6)
    c[0].metric("Location", city)
    c[1].metric("Basin", cfg["basin"])
    c[2].metric("Temperature", f"{current['temperature_c']:.1f} °C")
    c[3].metric("Rainfall / 24 h", f"{current['rainfall_24h_mm']:.1f} mm")
    c[4].metric("Rain intensity", f"{current['rainfall_intensity_mm_h']:.1f} mm/h")
    c[5].metric("Humidity", f"{current['humidity_pct']:.1f} %")
    st.caption(f"Simulated timestamp: {current['timestamp'].strftime('%Y-%m-%d %H:%M %Z') or current['timestamp'].strftime('%Y-%m-%d %H:%M')}")

    st.subheader("2. Hydraulic Hazard Screening")
    c = st.columns(5)
    c[0].metric("River discharge", f"{current['river_discharge_m3s']:,.1f} m³/s")
    c[1].metric("Water level", f"{current['water_level_m']:.2f} m")
    c[2].metric("Hazard index", f"{hazard['hazard_index']:.1f}/100")
    c[3].metric("Screening class", hazard["risk_class"])
    c[4].metric("Basin", cfg["basin"])
    hdf = pd.DataFrame({"Component": ["Rainfall intensity", "River discharge", "Water level"], "Score": [hazard["rainfall_score"], hazard["discharge_score"], hazard["water_level_score"]]})
    st.plotly_chart(px.bar(hdf, x="Component", y="Score", range_y=[0,100], title=f"Hydraulic hazard components — {city}"), use_container_width=True)
    st.caption(hazard["method"])

    st.subheader("3. Simulated 12-Month Historical Telemetry")
    telemetry = telemetry_with_hazard(city)
    t1, t2, t3 = st.tabs(["Telemetry trend", "Hazard trend", "Data table"])
    with t1:
        vars_to_plot = st.multiselect("Telemetry variables", ["rainfall_mm", "river_discharge_m3s", "water_level_m", "temperature_c"], default=["rainfall_mm", "river_discharge_m3s"], key="hist_telemetry_vars")
        if vars_to_plot:
            st.plotly_chart(px.line(telemetry, x="date", y=vars_to_plot, markers=True, title=f"12-month simulated telemetry — {city} ({cfg['basin']} basin)"), use_container_width=True)
        st.caption("The 12 observations are generated from city/basin seasonal parameters with deterministic noise so the same project produces reproducible screening data.")
    with t2:
        st.plotly_chart(px.line(telemetry, x="date", y="hydraulic_hazard_index", color="hydraulic_hazard_class", markers=True, title=f"12-month simulated hydraulic hazard — {city}"), use_container_width=True)
        latest = telemetry.iloc[-1]
        st.info(f"Latest simulated month: {latest['date'].strftime('%Y-%m')} · hazard {latest['hydraulic_hazard_index']:.1f}/100 · {latest['hydraulic_hazard_class']}")
    with t3:
        st.dataframe(telemetry, use_container_width=True, hide_index=True)
        st.download_button("⬇️ Download simulated 12-month telemetry CSV", telemetry.to_csv(index=False).encode(), f"{city.lower()}_simulated_12_month_telemetry.csv", "text/csv", key=f"download_telemetry_{city}")

    st.subheader("4. Three-city basin comparison")
    comparison = []
    for location in ["Sialkot", "Jhelum", "Lahore"]:
        w = simulated_live_weather(location)
        hz = hydraulic_hazard(w)
        comparison.append({"City": location, "Basin": CITY_CONFIG[location]["basin"], "Rainfall 24h (mm)": w["rainfall_24h_mm"], "Rain intensity (mm/h)": w["rainfall_intensity_mm_h"], "Discharge (m³/s)": w["river_discharge_m3s"], "Water level (m)": w["water_level_m"], "Hazard index": hz["hazard_index"], "Class": hz["risk_class"]})
    comp_df = pd.DataFrame(comparison)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)
    st.plotly_chart(px.bar(comp_df, x="City", y="Hazard index", color="Basin", range_y=[0,100], title="Simulated hydraulic hazard comparison"), use_container_width=True)

    st.subheader("5. Data provenance and limitations")
    st.markdown("""- **Simulated:** weather, rainfall, discharge, water level, telemetry and hazard index.
- **City-to-basin mapping:** Sialkot → Chenab, Jhelum → Jhelum, Lahore → Ravi.
- **Historical reference:** PMD publishes climate records and Flood Forecasting Division bulletins with rainfall and river-gauge observations; this module does not copy those observations into the simulation.
- **Engineering limitation:** the hazard index is a transparent screening indicator, not a calibrated hydraulic model, flood forecast, warning threshold or design discharge.""")
    st.markdown("PMD climate records: https://weather.gov.pk/cdpc/climate-records  ·  PMD Flood Forecasting Division bulletins: https://ffd.pmd.gov.pk/")

elif choice == "🛰️ SEBAL Evapotranspiration (GEE)":
    st.title("🛰️ SEBAL Evapotranspiration — Indus Basin")
    st.write("Google Earth Engine + geemap + GeoPandas workspace for satellite-based Surface Energy Balance Algorithm for Land (SEBAL) evapotranspiration screening across the Indus Basin.")
    st.warning("This module requires an authenticated Google Earth Engine account/project for satellite SEBAL runs. Uploaded-file analytics and coordinate mapping work independently of Earth Engine. Results are research/screening outputs and require local validation before operational irrigation, water-allocation or engineering decisions.")

    # Upload-driven analytics intentionally appears before the Earth Engine gate,
    # so CSV/XLSX analysis and coordinate maps still work without GEE credentials.
    st.header("📂 A. Upload data — charts, analytics and coordinate map")
    st.caption("Upload one or more CSV/Excel files. This section analyses the uploaded observations; it does not manufacture SEBAL estimates. To calculate satellite ET, use the authenticated Earth Engine section below or upload a file that already contains ET values.")
    sebal_uploads = st.file_uploader(
        "Upload SEBAL, evapotranspiration, weather, soil, irrigation or telemetry tables",
        type=["csv", "xlsx", "xls"], accept_multiple_files=True, key="sebal_data_uploads",
        help="Coordinate mapping supports common fields such as latitude/longitude, lat/lon, lng, x/y, and decimal latitude/longitude."
    )
    if sebal_uploads:
        file_names = [f.name for f in sebal_uploads]
        chosen_upload = st.selectbox("Dataset to analyse", file_names + (["Combine uploaded files (matching columns)"] if len(sebal_uploads) > 1 else []), key="sebal_upload_choice")
        try:
            if chosen_upload == "Combine uploaded files (matching columns)":
                parts = []
                for uf in sebal_uploads:
                    part = read_uploaded_table(uf)
                    part["source_file"] = uf.name
                    parts.append(part)
                df_upload = pd.concat(parts, ignore_index=True, sort=False)
                upload_label = "combined_uploads"
            else:
                selected_upload = next(f for f in sebal_uploads if f.name == chosen_upload)
                df_upload = read_uploaded_table(selected_upload)
                upload_label = selected_upload.name
            if df_upload.empty:
                st.warning("The selected file contains no tabular records.")
            else:
                import numpy as np
                from pandas.api.types import is_numeric_dtype
                st.success(f"Loaded {len(df_upload):,} rows × {len(df_upload.columns):,} columns from {upload_label}.")
                metric_cols = st.columns(4)
                metric_cols[0].metric("Rows", f"{len(df_upload):,}")
                metric_cols[1].metric("Columns", f"{len(df_upload.columns):,}")
                numeric_df = df_upload.copy()
                for _col in numeric_df.columns:
                    if not is_numeric_dtype(numeric_df[_col]):
                        _converted = pd.to_numeric(numeric_df[_col].astype(str).str.replace(",", "", regex=False).str.replace("%", "", regex=False), errors="coerce")
                        if _converted.notna().mean() >= 0.70:
                            numeric_df[_col] = _converted
                numeric_cols = [c for c in numeric_df.columns if is_numeric_dtype(numeric_df[c]) and numeric_df[c].notna().any()]
                category_cols = [c for c in numeric_df.columns if c not in numeric_cols]
                metric_cols[2].metric("Numeric fields", len(numeric_cols))
                spatial_df, lat_col, lon_col = valid_spatial_rows(df_upload)
                metric_cols[3].metric("Valid coordinate rows", f"{len(spatial_df):,}" if lat_col and lon_col else "Not detected")
                with st.expander("Preview and field summary", expanded=False):
                    st.dataframe(df_upload.head(100), use_container_width=True, hide_index=True)
                    st.write({"numeric_columns": numeric_cols, "categorical_or_other_columns": category_cols})

                st.subheader("Interactive chart builder")
                chart_kind = st.selectbox("Chart type", ["Bar chart", "Pie chart", "Scatter plot", "Line chart"], key="sebal_upload_chart_kind")
                if chart_kind == "Scatter plot":
                    if len(numeric_cols) >= 2:
                        cx, cy = st.columns(2)
                        x_col = cx.selectbox("X numeric field", numeric_cols, key="sebal_upload_scatter_x")
                        y_col = cy.selectbox("Y numeric field", [c for c in numeric_cols if c != x_col] or numeric_cols, key="sebal_upload_scatter_y")
                        color_options = ["None"] + category_cols + [c for c in numeric_cols if c not in (x_col, y_col)]
                        color_choice = st.selectbox("Optional color / grouping field", color_options, key="sebal_upload_scatter_color")
                        color_arg = None if color_choice == "None" else color_choice
                        fig = px.scatter(numeric_df, x=x_col, y=y_col, color=color_arg, hover_data=list(df_upload.columns[:6]), title=f"{y_col} vs {x_col}")
                        st.plotly_chart(fig, use_container_width=True, key="sebal_upload_scatter_plot")
                    else:
                        st.info("Scatter plots need at least two numeric columns. Check that the uploaded file contains numeric observations.")
                elif chart_kind == "Pie chart":
                    if numeric_cols and category_cols:
                        pc1, pc2 = st.columns(2)
                        name_col = pc1.selectbox("Category / label", category_cols, key="sebal_upload_pie_name")
                        value_col = pc2.selectbox("Numeric value", numeric_cols, key="sebal_upload_pie_value")
                        pie_df = numeric_df[[name_col, value_col]].dropna().groupby(name_col, as_index=False)[value_col].sum()
                        pie_df = pie_df[pie_df[value_col] > 0].nlargest(15, value_col)
                        if not pie_df.empty:
                            st.plotly_chart(px.pie(pie_df, names=name_col, values=value_col, title=f"{value_col} by {name_col} (top 15 categories)"), use_container_width=True, key="sebal_upload_pie_plot")
                        else:
                            st.info("No valid category/value pairs are available for the pie chart.")
                    else:
                        st.info("Pie charts need at least one numeric field and one category/label field.")
                elif chart_kind == "Bar chart":
                    if numeric_cols:
                        bc1, bc2, bc3 = st.columns(3)
                        x_options = category_cols + numeric_cols
                        x_col = bc1.selectbox("Group / X field", x_options, key="sebal_upload_bar_x")
                        y_col = bc2.selectbox("Numeric value", numeric_cols, key="sebal_upload_bar_y")
                        agg = bc3.selectbox("Aggregation", ["mean", "sum", "count"], key="sebal_upload_bar_agg")
                        if agg == "count":
                            plot_df = numeric_df.groupby(x_col, dropna=False).size().reset_index(name="record_count")
                            y_plot = "record_count"
                        else:
                            plot_df = numeric_df.groupby(x_col, dropna=False)[y_col].agg(agg).reset_index()
                            y_plot = y_col
                        st.plotly_chart(px.bar(plot_df, x=x_col, y=y_plot, title=f"{agg.title()} {y_plot} by {x_col}"), use_container_width=True, key="sebal_upload_bar_plot")
                    else:
                        st.info("Bar charts need at least one numeric field.")
                else:  # Line chart
                    if numeric_cols:
                        lc1, lc2 = st.columns(2)
                        x_col = lc1.selectbox("X / time field", list(numeric_df.columns), key="sebal_upload_line_x")
                        y_col = lc2.selectbox("Numeric value", numeric_cols, key="sebal_upload_line_y")
                        line_df = numeric_df[[x_col, y_col]].copy().dropna()
                        if x_col in {"date", "datetime", "timestamp", "time", "sample_date", "observation_date", "acquisition_date"} or "date" in str(x_col).lower() or "time" in str(x_col).lower():
                            line_df[x_col] = pd.to_datetime(line_df[x_col], errors="coerce")
                            line_df = line_df.dropna(subset=[x_col]).sort_values(x_col)
                        st.plotly_chart(px.line(line_df, x=x_col, y=y_col, markers=True, title=f"{y_col} by {x_col}"), use_container_width=True, key="sebal_upload_line_plot")
                    else:
                        st.info("Line charts need at least one numeric field.")

                st.subheader("🗺️ Map from uploaded latitude/longitude")
                if lat_col and lon_col and not spatial_df.empty:
                    map_color_options = ["None"] + [c for c in spatial_df.columns if c not in (lat_col, lon_col)]
                    map_color = st.selectbox("Optional map colour field", map_color_options, key="sebal_upload_map_color")
                    map_color_arg = None if map_color == "None" else map_color
                    hover_cols = [c for c in spatial_df.columns if c not in (lat_col, lon_col)][:8]
                    fig_map_upload = px.scatter_geo(
                        spatial_df, lat=lat_col, lon=lon_col, color=map_color_arg, hover_data=hover_cols,
                        title=f"Uploaded coordinate map — {upload_label}", scope="world"
                    )
                    # Fit the map to the uploaded points so Pakistan-scale datasets
                    # are not compressed into a tiny cluster on a world map.
                    fig_map_upload.update_geos(
                        showcountries=True, showland=True, showocean=True,
                        fitbounds="locations", showcoastlines=True, showframe=False,
                    )
                    fig_map_upload.update_layout(
                        height=600, margin=dict(l=0, r=0, t=50, b=0),
                        legend_title_text="Uploaded data",
                    )
                    st.plotly_chart(fig_map_upload, use_container_width=True, key="sebal_upload_spatial_map")
                    st.caption(f"Mapped {len(spatial_df):,} rows using latitude field '{lat_col}' and longitude field '{lon_col}'. Rows with missing or out-of-range coordinates were excluded from the map only.")
                    st.download_button("⬇️ Download valid mapped rows", spatial_df.to_csv(index=False).encode("utf-8"), f"{upload_label.rsplit('.', 1)[0]}_mapped_rows.csv", "text/csv", key="sebal_upload_map_download")
                else:
                    st.info("No valid latitude/longitude pair was detected. Use column names such as latitude + longitude, lat + lon, lng, or x + y. Coordinate mapping will appear automatically when valid coordinate fields are found.")
                st.download_button("⬇️ Download analysed dataset as CSV", df_upload.to_csv(index=False).encode("utf-8"), f"{upload_label.rsplit('.', 1)[0]}_analysed.csv", "text/csv", key="sebal_upload_data_download")
        except Exception as exc:
            st.error(f"Could not analyse the uploaded SEBAL dataset: {exc}")
    else:
        st.info("Upload a CSV or Excel file to enable charting and coordinate mapping. You can use the Earth Engine model below separately.")

    st.divider()
    st.header("🛰️ B. Satellite-based SEBAL model (Google Earth Engine)")
    ok, status_msg = earth_engine_status()
    if not ok:
        st.error(status_msg)
        st.info("Install the Earth Engine Python API and geospatial dependencies from requirements.txt, then authenticate with Earth Engine.")
    elif geemap_map is None or st_folium is None:
        st.error("The geemap/streamlit-folium map dependencies are unavailable. Install the project's updated requirements.txt.")
    else:
        st.subheader("1. Earth Engine authentication")
        default_project = ""
        try:
            default_project = str(st.secrets.get("GEE_PROJECT", ""))
        except Exception:
            default_project = ""
        gee_project = st.text_input("Google Cloud / Earth Engine project ID", value=default_project, help="Use a project registered for Earth Engine. For local use, authenticate once with ee.Authenticate(). For deployed apps, use a secure service-account setup rather than committing credentials.")
        init_col1, init_col2 = st.columns([1, 2])
        with init_col1:
            init_clicked = st.button("🔐 Initialize Earth Engine", type="primary")
        with init_col2:
            st.caption("Local/Colab: ee.Authenticate() → ee.Initialize(project='YOUR_PROJECT'). Deployed apps should keep credentials in a secure secret store.")

        if init_clicked:
            try:
                service_account_email = ""
                private_key_json = ""
                try:
                    service_account_email = str(st.secrets.get("GEE_SERVICE_ACCOUNT", ""))
                    private_key_json = str(st.secrets.get("GEE_PRIVATE_KEY_JSON", ""))
                except Exception:
                    pass
                initialize_ee(
                    gee_project.strip() or None,
                    service_account=service_account_email or None,
                    private_key_json=private_key_json or None,
                )
                st.session_state["gee_initialized"] = True
                st.success("Earth Engine initialized successfully.")
            except Exception as exc:
                st.session_state["gee_initialized"] = False
                st.error(f"Earth Engine initialization failed: {exc}")

        if not st.session_state.get("gee_initialized", False):
            st.info("Initialize Earth Engine above to run the Indus Basin SEBAL computation.")
        else:
            st.subheader("2. Indus Basin geometry")
            outlet_col1, outlet_col2 = st.columns(2)
            outlet_lon = outlet_col1.number_input("Indus outlet longitude", value=67.80, format="%.4f", help="HydroSHEDS uses this outlet to identify the upstream MAIN_BAS chain.")
            outlet_lat = outlet_col2.number_input("Indus outlet latitude", value=24.10, format="%.4f")
            try:
                basin_gdf = indus_basin_geodataframe(outlet_lon, outlet_lat)
                st.dataframe(basin_gdf[["main_bas", "area_km2"]], use_container_width=True, hide_index=True)
                st.caption("HydroSHEDS Level-7 basin polygons are used to identify the upstream basin chain. GeoPandas is used for local geometry inspection; Earth Engine retains the analysis geometry.")
            except Exception as exc:
                basin_gdf = None
                st.error(f"Could not build the HydroSHEDS Indus Basin geometry: {exc}")

            st.subheader("3. SEBAL processing")
            mode = st.radio("Processing mode", ["Single Landsat scene", "Monthly composite"], horizontal=True)
            cloud = st.slider("Maximum Landsat cloud cover (%)", 5, 60, 30, 5)
            if mode == "Single Landsat scene":
                process_date = st.date_input("Landsat acquisition window start", value=pd.Timestamp("2025-10-01").date())
                date_str = process_date.strftime("%Y-%m-%d")
                if st.button("▶️ Run SEBAL scene", type="primary"):
                    try:
                        with st.spinner("Querying Landsat + ERA5-Land and computing SEBAL energy balance in Earth Engine…"):
                            image, basin_fc, raw = sebal_image(date_str, outlet_lon=outlet_lon, outlet_lat=outlet_lat, max_cloud_pct=cloud)
                            stats = zonal_statistics(image, basin_fc, scale=1000)
                            m = geemap_map(image, basin_fc, center=(30.5, 70.5), zoom=5)
                        st.success("SEBAL computation completed in Earth Engine.")
                        a, b, c, d = st.columns(4)
                        a.metric("Scene", str(raw.get("LANDSAT_PRODUCT_ID").getInfo())[:30])
                        a.metric("Cloud cover", f"{float(raw.get('CLOUD_COVER').getInfo() or 0):.1f}%")
                        et_mean = stats.loc[stats["variable"] == "et_mm_h", "mean"]
                        ts_mean = stats.loc[stats["variable"] == "ts_k", "mean"]
                        ndvi_mean = stats.loc[stats["variable"] == "ndvi", "mean"]
                        b.metric("Mean ET rate", f"{float(et_mean.iloc[0]):.3f} mm/h" if not et_mean.empty and pd.notna(et_mean.iloc[0]) else "—")
                        c.metric("Mean LST", f"{float(ts_mean.iloc[0]):.1f} K" if not ts_mean.empty and pd.notna(ts_mean.iloc[0]) else "—")
                        d.metric("Mean NDVI", f"{float(ndvi_mean.iloc[0]):.3f}" if not ndvi_mean.empty and pd.notna(ndvi_mean.iloc[0]) else "—")
                        if st_folium is not None:
                            st_folium(m, width=1200, height=650, returned_objects=[])
                        st.subheader("Basin-level SEBAL statistics")
                        st.dataframe(stats, use_container_width=True, hide_index=True)
                        st.download_button("⬇️ Download SEBAL basin statistics", stats.to_csv(index=False).encode(), "indus_basin_sebal_statistics.csv", "text/csv")
                    except Exception as exc:
                        st.error(f"SEBAL processing failed: {exc}")
                        st.info("Try a date with a clear Landsat scene and a higher cloud threshold. Also confirm that your Earth Engine project has access to the required public datasets.")
            else:
                year = st.number_input("Year", min_value=2013, max_value=2026, value=2025, step=1)
                month = st.slider("Month", 1, 12, 6)
                if st.button("▶️ Run monthly SEBAL composite", type="primary"):
                    try:
                        with st.spinner("Processing available Landsat scenes and generating a monthly SEBAL median composite…"):
                            image, basin_fc, scene_count = monthly_sebal(int(year), int(month), outlet_lon=outlet_lon, outlet_lat=outlet_lat, max_cloud_pct=cloud)
                            stats = zonal_statistics(image, basin_fc, scale=1000)
                            m = geemap_map(image, basin_fc, center=(30.5, 70.5), zoom=5)
                        st.success(f"Monthly SEBAL composite completed using {scene_count} Landsat scene(s).")
                        et_mean = stats.loc[stats["variable"] == "et_mm_h", "mean"]
                        st.metric("Mean instantaneous ET rate", f"{float(et_mean.iloc[0]):.3f} mm/h" if not et_mean.empty and pd.notna(et_mean.iloc[0]) else "—")
                        if st_folium is not None:
                            st_folium(m, width=1200, height=650, returned_objects=[])
                        st.dataframe(stats, use_container_width=True, hide_index=True)
                        st.download_button("⬇️ Download monthly SEBAL statistics", stats.to_csv(index=False).encode(), f"indus_basin_sebal_{int(year)}_{int(month):02d}.csv", "text/csv")
                    except Exception as exc:
                        st.error(f"Monthly SEBAL processing failed: {exc}")

            st.subheader("4. Model components")
            st.markdown("**Landsat:** surface reflectance, NDVI, broadband albedo and land-surface temperature. **ERA5-Land:** shortwave/longwave radiation, 2-m air temperature and 10-m wind. **SEBAL:** net radiation → soil heat flux → sensible heat flux → latent heat flux → instantaneous ET rate. **HydroSHEDS + GeoPandas:** basin geometry and local spatial inspection.")
            st.caption("The implementation uses Landsat 8/9 Collection 2 Level-2 and ERA5-Land hourly inputs. It is a transparent SEBAL-style research implementation; hot/cold-pixel selection, aerodynamic resistance and emissivity assumptions should be calibrated/validated for Indus Basin conditions before operational use.")

elif choice == "🧮 Interactive Hydraulic Models":
    st.title("Interactive Hydraulic & Risk Models")
    result = scenario_summary(exposure, vulnerability, sensitivity, adaptive, scenario)
    a,b,c,d = st.columns(4)
    a.metric("Scenario index", result["risk_index"]); b.metric("Risk class", result["risk_class"]); c.metric("Criticality", criticality); d.metric("Scenario factor", result["scenario_factor"])
    comp = pd.DataFrame({"Component":list(result["components"].keys()),"Value":list(result["components"].values())})
    st.plotly_chart(px.bar(comp, x="Component", y="Value", range_y=[0,100], title="Inputs feeding the scenario index"), use_container_width=True)
    st.write(result["explanation"])
    st.dataframe(pd.DataFrame([{"Scenario":scenario,"Exposure":exposure,"Vulnerability":vulnerability,"Sensitivity":sensitivity,"Adaptive capacity":adaptive,"Criticality":criticality,"Scenario index":result["risk_index"],"Risk class":result["risk_class"]}]), use_container_width=True, hide_index=True)

elif choice == "⚙️ Simulation Engines":
    st.title("⚙️ Engineering Simulation Engines")
    st.write("Run transparent, input-driven screening simulations for reservoirs, floods, crop water requirements, climate stress, uncertainty and river/canal routing. Results are generated from the values entered in the interface.")
    st.info("These are educational/screening models. Professional hydraulic design requires calibrated hydrology, surveyed geometry, boundary conditions and validated engineering software.")
    st.subheader("Available Python simulation modules")
    st.dataframe(pd.DataFrame(SIMULATION_CATALOG), use_container_width=True, hide_index=True)
    engine_options = list(ENGINES.keys()) + ["Groundwater Balance", "Drought Stress", "Sediment Load", "Water Quality Index", "Irrigation Schedule", "Socio-Agro Projection"]
    engine = st.selectbox("Select simulation engine", engine_options, key="simulation_engine_selector")
    module_lookup = {row["name"]: row["module"] for row in SIMULATION_CATALOG}
    st.caption(f"Engine module: {module_lookup.get(engine, ENGINES.get(engine, 'built-in'))}")

    if engine == "Reservoir / Water Balance":
        st.subheader("Reservoir mass-balance simulation")
        a,b,c,d=st.columns(4)
        capacity=a.number_input("Reservoir capacity (million m³)",1.0,100000.0,1000.0)
        storage=b.number_input("Initial storage (million m³)", min_value=0.0, max_value=100000.0, value=600.0, key="sim_initial_storage", help="The app checks that initial storage does not exceed the selected capacity.")
        evap=c.number_input("Monthly evaporation loss (million m³)",0.0,10000.0,20.0)
        target=d.slider("Target storage fraction",0.0,1.0,0.60,0.05)
        inflow_text=st.text_input("Monthly inflows (million m³, comma separated)","450,500,650,800,900,750,600,500,420,380,400,430")
        demand_text=st.text_input("Monthly demand (million m³, comma separated)","400,420,450,480,500,520,500,480,450,430,410,400")
        try:
            inflow=[float(x.strip()) for x in inflow_text.split(",") if x.strip()]
            demand=[float(x.strip()) for x in demand_text.split(",") if x.strip()]
            if len(inflow)!=len(demand): st.error("Inflow and demand lists must have equal length.")
            elif storage > capacity:
                st.error("Initial storage cannot exceed reservoir capacity. Increase capacity or reduce initial storage.")
            else:
                res=reservoir_rule_curve(inflow,demand,capacity,storage,target,evap)
                st.plotly_chart(px.line(res,x="Period",y=["End storage","Target storage"],markers=True,title="Reservoir storage trajectory"),use_container_width=True)
                st.plotly_chart(px.bar(res,x="Period",y=["Inflow","Demand","Release","Shortage"],barmode="group",title="Water balance by period"),use_container_width=True)
                st.dataframe(res,use_container_width=True,hide_index=True)
        except ValueError as e: st.error(str(e))

    elif engine == "Flood Screening":
        st.subheader("Rainfall–runoff and channel-capacity screening")
        a,b,c=st.columns(3)
        rainfall=a.number_input("Rainfall event (mm)",0.0,2000.0,150.0)
        area=b.number_input("Catchment area (km²)",1.0,1000000.0,1000.0)
        runoff=c.slider("Runoff coefficient",0.0,1.0,0.45,0.05)
        d,e,f=st.columns(3)
        capacity=d.number_input("Channel capacity (m³/s)",1.0,1000000.0,500.0)
        duration=e.number_input("Event duration (hours)",0.1,168.0,6.0)
        exposure=f.slider("Exposure",0,100,50, key="flood_exposure")
        vulnerability=st.slider("Vulnerability",0,100,50, key="flood_vulnerability")
        criticality=st.slider("Asset/service criticality",0,100,50, key="flood_criticality")
        out=flood_scenario(rainfall,area,runoff,capacity,duration,exposure,vulnerability,criticality)
        cols=st.columns(4); cols[0].metric("Runoff volume",f"{out['runoff_volume_m3']:,.0f} m³"); cols[1].metric("Peak-flow proxy",f"{out['peak_flow_proxy_m3s']:,.1f} m³/s"); cols[2].metric("Capacity ratio",f"{out['capacity_ratio']:.2f}×"); cols[3].metric("Risk index",f"{out['risk_index']:.1f}")
        st.write(f"Screening class: **{out['risk_class']}**")
        rain_range=st.slider("Rainfall sensitivity range (mm)",10,1000,(50,500),10)
        sweep=rainfall_sweep(range(rain_range[0],rain_range[1]+1,max(1,(rain_range[1]-rain_range[0])//20 or 1)),catchment_km2=area,runoff_coefficient=runoff,channel_capacity_m3s=capacity,duration_hours=duration,exposure=exposure,vulnerability=vulnerability,criticality=criticality)
        st.plotly_chart(px.line(sweep,x="Rainfall (mm)",y="Peak flow proxy (m3/s)",markers=True,title="Rainfall sensitivity"),use_container_width=True)

    elif engine == "Crop Water Requirement":
        st.subheader("Rabi / Kharif crop water screening")
        season=st.radio("Season",["Rabi","Kharif"],horizontal=True, key="crop_season")
        default_crops=["Wheat","Gram/Chickpea","Barley","Mustard/Rapeseed","Canola","Lentil"] if season=="Rabi" else ["Rice","Cotton","Maize","Sugarcane"]
        crops=st.multiselect("Crops",list(CROP_COEFFICIENTS),default=[c for c in default_crops if c in CROP_COEFFICIENTS], key="crop_selection")
        a,b,c,d=st.columns(4)
        et0=a.number_input("Reference ET0 (mm/season)",0.0,3000.0,600.0)
        rain=b.number_input("Effective rainfall (mm/season)",0.0,2000.0,150.0)
        area_ha=c.number_input("Area (ha)",0.1,1000000.0,100.0)
        eff=d.slider("Irrigation efficiency",0.10,1.0,0.65,0.05)
        if crops:
            cropdf=crop_comparison(crops,et0,rain,area_ha,eff)
            st.plotly_chart(px.bar(cropdf,x="Crop",y="Gross irrigation volume_m3",title="Estimated gross irrigation volume"),use_container_width=True)
            st.dataframe(cropdf,use_container_width=True,hide_index=True)

    elif engine == "Climate Stress":
        st.subheader("Climate scenario and sensitivity simulation")
        vals={}
        cols=st.columns(5)
        for i,k in enumerate(["Exposure","Vulnerability","Sensitivity","Adaptive capacity","Criticality"]): vals[k.lower().replace(" ","_")]=cols[i].slider(k,0,100,50, key=f"climate_input_{i}")
        scenario=st.selectbox("Scenario",["Baseline","Medium","Worst-Case"], key="climate_scenario")
        horizon=st.selectbox("Horizon",["Near Term","Mid Century","Long Term"], key="climate_horizon")
        out=climate_stress(vals["exposure"],vals["vulnerability"],vals["sensitivity"],vals["adaptive_capacity"],vals["criticality"],scenario,horizon)
        st.metric("Risk index",f"{out['risk_index']:.1f}"); st.write(f"Class: **{out['risk_class']}** · Scenario factor {out['scenario_factor']} · Horizon factor {out['horizon_factor']}")
        parameter=st.selectbox("Sensitivity parameter",["exposure","vulnerability","sensitivity","adaptive_capacity","criticality"], key="climate_parameter")
        base=dict(exposure=vals["exposure"],vulnerability=vals["vulnerability"],sensitivity=vals["sensitivity"],adaptive_capacity=vals["adaptive_capacity"],criticality=vals["criticality"],scenario=scenario,horizon=horizon)
        sens=sensitivity_table(base,parameter,range(0,101,5))
        st.plotly_chart(px.line(sens,x=parameter,y="Risk index",markers=True,title=f"Risk sensitivity to {parameter.replace('_',' ')}"),use_container_width=True)

    elif engine == "Monte Carlo Risk":
        st.subheader("Monte Carlo uncertainty simulation")
        n=st.slider("Simulation runs",500,10000,2000,500, key="mc_runs"); seed=st.number_input("Random seed",0,999999,42, key="mc_seed")
        c=st.columns(5)
        inputs=[c[i].slider(k,0,100,50, key=f"mc_{i}") for i,k in enumerate(["Exposure","Vulnerability","Sensitivity","Adaptive capacity","Criticality"])]
        sim=monte_carlo_risk(n=n,seed=int(seed),exposure=inputs[0],vulnerability=inputs[1],sensitivity=inputs[2],adaptive_capacity=inputs[3],criticality=inputs[4])
        summ=summarize(sim); m=st.columns(5)
        m[0].metric("Mean",f"{summ['mean']:.1f}");m[1].metric("P10",f"{summ['p10']:.1f}");m[2].metric("Median",f"{summ['median']:.1f}");m[3].metric("P90",f"{summ['p90']:.1f}");m[4].metric("≥70",f"{summ['high_pct']:.1f}%")
        st.plotly_chart(px.histogram(sim,x="Risk index",nbins=35,title="Distribution of simulated risk index"),use_container_width=True)
        st.dataframe(sim.head(100),use_container_width=True,hide_index=True)

    elif engine == "Groundwater Balance":
        st.subheader("Groundwater recharge–pumping balance")
        c = st.columns(4)
        initial = c[0].number_input("Initial groundwater storage (million m³)", 0.0, 1e7, 5000.0, key="gw_initial")
        recharge = c[1].number_input("Recharge per period (million m³)", 0.0, 1e6, 450.0, key="gw_recharge")
        pumping = c[2].number_input("Pumping per period (million m³)", 0.0, 1e6, 500.0, key="gw_pumping")
        natural = c[3].number_input("Natural discharge (million m³)", 0.0, 1e6, 50.0, key="gw_natural")
        periods = st.slider("Periods", 1, 60, 12, key="gw_periods")
        out = groundwater_balance(initial, recharge, pumping, natural, periods)
        st.plotly_chart(px.line(out, x="Period", y="End storage", markers=True, title="Groundwater storage trajectory"), use_container_width=True)
        st.dataframe(out, use_container_width=True, hide_index=True)

    elif engine == "Drought Stress":
        st.subheader("Drought stress screening")
        c = st.columns(4)
        precip = c[0].number_input("Observed / scenario precipitation (mm)", 0.0, 5000.0, 450.0, key="drought_precip")
        normal = c[1].number_input("Normal precipitation (mm)", 1.0, 5000.0, 650.0, key="drought_normal")
        temp = c[2].number_input("Temperature anomaly (°C)", -5.0, 10.0, 1.0, key="drought_temp")
        demand = c[3].slider("Water-demand pressure", 0, 100, 50, key="drought_demand")
        out = drought_index(precip, normal, temp, demand)
        st.metric("Drought stress index", f"{out['index']:.1f}")
        st.write(f"Screening class: **{out['class']}**")
        st.dataframe(pd.DataFrame([out]), use_container_width=True, hide_index=True)

    elif engine == "Sediment Load":
        st.subheader("Sediment transport screening")
        c = st.columns(3)
        q = c[0].number_input("Discharge (m³/s)", 0.0, 1e7, 1000.0, key="sed_q")
        conc = c[1].number_input("Suspended sediment concentration (mg/L)", 0.0, 1e6, 500.0, key="sed_conc")
        dur = c[2].number_input("Duration (hours)", 0.1, 10000.0, 24.0, key="sed_duration")
        out = sediment_load(q, conc, dur)
        st.metric("Estimated sediment mass", f"{out['sediment_mass_tonnes']:,.2f} tonnes")
        st.dataframe(pd.DataFrame([out]), use_container_width=True, hide_index=True)

    elif engine == "Water Quality Index":
        st.subheader("Input-driven water quality screening")
        c = st.columns(5)
        ph = c[0].number_input("pH", 0.0, 14.0, 7.2, key="wqi_ph")
        turb = c[1].number_input("Turbidity (NTU)", 0.0, 10000.0, 5.0, key="wqi_turb")
        tds = c[2].number_input("TDS (mg/L)", 0.0, 100000.0, 400.0, key="wqi_tds")
        do = c[3].number_input("Dissolved oxygen (mg/L)", 0.0, 30.0, 6.5, key="wqi_do")
        nitrate = c[4].number_input("Nitrate (mg/L)", 0.0, 1000.0, 5.0, key="wqi_nitrate")
        out = water_quality_index(ph, turb, tds, do, nitrate)
        st.metric("Screening index", f"{out['index']:.1f}")
        st.write(f"Class: **{out['class']}**")
        contribution = pd.DataFrame({"Parameter": list(out.keys())[2:], "Score": list(out.values())[2:]})
        st.plotly_chart(px.bar(contribution, x="Parameter", y="Score", range_y=[0,100], title="Parameter contribution scores"), use_container_width=True)

    elif engine == "Irrigation Schedule":
        st.subheader("ET-based irrigation schedule")
        c = st.columns(5)
        et0 = c[0].number_input("Reference ET0 (mm)", 0.0, 5000.0, 600.0, key="irr_et0")
        kc = c[1].number_input("Crop coefficient (Kc)", 0.0, 2.5, 1.0, key="irr_kc")
        rain = c[2].number_input("Effective rainfall (mm)", 0.0, 3000.0, 100.0, key="irr_rain")
        eff = c[3].slider("Irrigation efficiency", 0.1, 1.0, 0.65, 0.05, key="irr_eff")
        area = c[4].number_input("Area (ha)", 0.1, 1e6, 100.0, key="irr_area")
        out = irrigation_schedule(et0, kc, rain, eff, area)
        st.dataframe(pd.DataFrame([out]), use_container_width=True, hide_index=True)
        st.metric("Gross irrigation volume", f"{out['Gross volume_m3']:,.0f} m³")

    elif engine == "Socio-Agro Projection":
        st.subheader("Socio-agro metric projection engine")
        source = DEFAULT_SOCIO_AGRO_DATA.copy()
        metric_label = st.selectbox("Metric", list(SOCIO_AGRO_METRICS), key="engine_socio_metric")
        metric_col = SOCIO_AGRO_METRICS[metric_label]
        edited = st.data_editor(source, num_rows="dynamic", use_container_width=True, key="engine_socio_editor")
        edited[metric_col] = pd.to_numeric(edited[metric_col], errors="coerce").fillna(0)
        growth = st.slider("Annual growth / change assumption (%)", -10.0, 20.0, 3.0, 0.5, key="engine_socio_growth")
        years = st.slider("Projection years", 1, 20, 5, key="engine_socio_years")
        out = socio_agro_projection(edited, metric_col, growth, years)
        st.plotly_chart(px.line(out, x="year", y=metric_col, color="province/region", markers=True, title=f"Projected {metric_label}"), use_container_width=True)
        st.dataframe(out, use_container_width=True, hide_index=True)

    else:
        st.subheader("River / Link Canal Network Routing")
        st.write("Use this engine for a simplified directed network of rivers, canals, barrages or transfer links.")
        st.code("from network_engine import route_network\n# links: columns from, to, capacity\n# source_inflows={...}")
        st.info("The network engine is available as network_engine.py for extension with your own river/canal topology.")

elif choice == "📡 WAPDA Telecommunication Networks":
    st.title("📡 WAPDA Telecommunication Networks")
    st.write("Network inventory extracted from the user-supplied WAPDA telecommunication diagrams. The source material identifies network locations and river-system groupings; it does not provide GIS coordinates or an explicit link topology.")
    st.info(SOURCE_NOTE)

    t1, t2, t3 = st.tabs(["Western Rivers — HF Radio", "Eastern Rivers — Wireless Network", "Source documents"])
    with t1:
        st.subheader("High Frequency Radio Network — Western Rivers")
        western = pd.DataFrame({"Network area": ["Western Rivers"] * len(WESTERN_RIVERS), "Location / facility": WESTERN_RIVERS})
        st.dataframe(western, use_container_width=True, hide_index=True)
        coords = [{"name": n, "latitude": APPROX_COORDS[n][0], "longitude": APPROX_COORDS[n][1]} for n in WESTERN_RIVERS if n in APPROX_COORDS]
        if coords:
            wdf = pd.DataFrame(coords)
            fig = px.scatter_map(wdf, lat="latitude", lon="longitude", hover_name="name", zoom=4.5, height=560, title="Western Rivers network — visualization-only approximate points")
            fig.update_layout(map_style="open-street-map")
            st.plotly_chart(fig, use_container_width=True)
        st.caption("Approximate map coordinates are visualization aids only and are not contained in the supplied PDF diagrams. No network links are inferred.")

    with t2:
        st.subheader("Wireless Network — Eastern Rivers")
        eastern = pd.DataFrame({"Network area": ["Eastern Rivers"] * len(EASTERN_RIVERS), "Location / facility": EASTERN_RIVERS})
        st.dataframe(eastern, use_container_width=True, hide_index=True)
        coords = [{"name": n, "latitude": APPROX_COORDS[n][0], "longitude": APPROX_COORDS[n][1]} for n in EASTERN_RIVERS if n in APPROX_COORDS]
        if coords:
            edf = pd.DataFrame(coords)
            fig = px.scatter_map(edf, lat="latitude", lon="longitude", hover_name="name", zoom=4.5, height=560, title="Eastern Rivers network — visualization-only approximate points")
            fig.update_layout(map_style="open-street-map")
            st.plotly_chart(fig, use_container_width=True)
        st.caption("The eastern-river diagram lists sites around Ravi, Sutlej, Chenab, Jhelum and Indus systems. Approximate map coordinates are not source-derived.")

    with t3:
        st.subheader("Supplied WAPDA source documents")
        for name in SOURCE_DOCUMENTS:
            st.write(f"• {name}")
        st.write("The two supplied PDFs contain the same three-page diagram set in the uploaded material. The original PDFs are preserved in the project under `source_documents/` for traceability.")
        st.download_button("⬇️ Download Western Rivers inventory CSV", pd.DataFrame({"location": WESTERN_RIVERS}).to_csv(index=False).encode(), "wapda_western_rivers_network.csv", "text/csv", key="dl_western_network")
        st.download_button("⬇️ Download Eastern Rivers inventory CSV", pd.DataFrame({"location": EASTERN_RIVERS}).to_csv(index=False).encode(), "wapda_eastern_rivers_network.csv", "text/csv", key="dl_eastern_network")

elif choice == "🇮🇳 Chenab Projects & IWT Flow Concerns":
    st.title("🇮🇳 Chenab Projects, Flow Concerns & Indus Waters Treaty")
    st.warning("This research tab presents reported proposals, party positions, engineering questions and adjudicative records without adopting contested political characterizations. A party's submission is not treated as an independent legal or factual finding.")

    st.subheader("1. Reported inter-basin water-transfer proposals")
    st.markdown("Media reports from June 2025 described a proposed 113-km canal concept intended to redirect reported surplus flows toward Punjab, Haryana and Rajasthan, with a proposed Chenab–Ravi-Beas-Sutlej connection. These reports describe a feasibility-study stage rather than establishing that the full project has been completed.")
    st.dataframe(pd.DataFrame([
        {"item":"113-km canal concept","reported_scope":"Chenab linked toward the Ravi-Beas-Sutlej system; proposed redistribution toward Punjab, Haryana and Rajasthan","status_note":"Reported proposal / feasibility-study reporting; verify current official project status."},
        {"item":"Ravi-Beas link concept","reported_scope":"Reported proposal to use flows described as surplus/beyond treaty allocations","status_note":"Reported concept; verify against current authoritative Indian project documentation."},
    ]), use_container_width=True, hide_index=True)
    st.caption("Source: reporting dated 16 June 2025, including Times of India / ETInfra coverage. The dashboard records the proposal as reported, not as an independently verified completed project.")

    st.subheader("2. Reported / under-construction hydroelectric projects in the Chenab system")
    show_table(INDIAN_PROJECTS)
    st.caption("Project capacities are presented as project/institutional figures in the dashboard inventory. For current construction status, consult dated government and PCA records.")

    st.subheader("3. Pakistan's stated position on the Court of Arbitration")
    st.markdown("**Pakistan's position:** Pakistan has participated in the PCA process and has argued that the Court of Arbitration is a properly constituted dispute-resolution mechanism under Article IX and Annexure G of the IWT. The PCA case record confirms that the Court was constituted under Annexure G and that the case remains pending.")
    st.markdown("**India's stated position:** India has publicly disputed the constitution/competence of the parallel Court of Arbitration process and has described the Neutral Expert process as the Treaty-consistent mechanism. This is a documented Indian government position, not an independent conclusion of this dashboard.")
    st.markdown("Primary sources: PCA case record — https://pca-cpa.org/en/cases/284/ ; India Ministry of External Affairs statement — https://www.mea.gov.in/press-releases.htm?dtl%2F36761%2FMatters+pertaining+to+the+Indus+Waters+Treaty=")

    st.subheader("4. Court of Arbitration timeline")
    tl = timeline_df()
    st.plotly_chart(px.scatter(tl, x="date", y="category", text="event", hover_data=["source"], title="Selected IWT / PCA procedural milestones"), use_container_width=True)
    st.dataframe(tl, use_container_width=True, hide_index=True)
    st.markdown("**31 August 2026:** The PCA announced an Award on the status of the Indus Waters Treaty and an Order on Interim Measures concerning the Ratle Hydro-Electric Plant. The official PCA case record lists this as the latest published award/order in Case No. 2023-01 in the sources reviewed for this release.")
    st.markdown("**Neutral Expert:** Michel Lino was appointed by the World Bank in 2022 in the separate Neutral Expert proceedings concerning Kishanganga and Ratle. The World Bank describes the Neutral Expert and Court of Arbitration mechanisms as separate processes under the Treaty.")

    st.subheader("Validity of the Court of Arbitration — attributed positions")
    st.markdown("**Pakistan's stated position:** Pakistan actively participates in the PCA process and argues that the Court of Arbitration is a legally sound dispute-resolution body constituted under Article IX / Annexure G of the IWT. This is presented as Pakistan's legal position, not as a dashboard adjudication.")
    st.markdown("**India's stated position:** India has disputed the parallel Court of Arbitration process and has challenged its constitution/competence. This is presented as India's stated position.")
    st.caption("Attribution note: the PCA records that the Court of Arbitration was constituted pursuant to Annexure G and that the proceedings remain pending; Government of India materials state that India considers the Court of Arbitration illegal and does not participate in its proceedings. These are attributed party positions, not a legal conclusion by this dashboard.")

    st.subheader("5. Technical design questions reported in the IWT proceedings")
    show_table(TECHNICAL_POINTS)
    st.markdown("The following numerical values are shown as **reported party positions / historical design comparisons**, not as independent engineering or legal findings:")
    design_df = pd.DataFrame([
        ["Kishanganga", "Pondage", "7.5 MCM reported Indian design", "1 MCM reported Pakistan position", "Party-position comparison; verify against operative PCA/Neutral Expert documents"],
        ["Ratle", "Pondage", "24 MCM reported in supplied material", "8 MCM reported Pakistan position", "Party-position comparison; PCA records should control for adjudicated findings"],
        ["Ratle", "Freeboard", "2 m reported Indian design", "1 m reported Pakistan position", "Party-position comparison"],
        ["Ratle", "Spillway", "Deep / low-level orifice configuration reported", "Higher / surface-gated configuration requested in Pakistan's position", "Engineering-design dispute; exact operative requirements should be read from primary documents"],
        ["Kishanganga / Ratle", "Power intake", "Low intake levels described in supplied material", "Pakistan requested higher intake elevations", "Exact elevations require primary technical documents"],
    ], columns=["project", "metric", "reported design / position", "reported Pakistan position", "evidence note"])
    st.dataframe(design_df, use_container_width=True, hide_index=True)
    st.caption("The dashboard intentionally uses 'reported' and 'party position' language because technical pleadings, awards and engineering documents can contain different values or later determinations.")

    st.subheader("6. Neutral Expert work programme")
    st.info("The user-supplied July 2027 schedule is retained as a research note, but the app does not label every milestone as officially binding unless an authoritative procedural source confirms it. Check the PCA Neutral Expert case page for the latest work programme before relying on dates.")
    st.dataframe(pd.DataFrame([
        ["Nov 2026", "Synthesis Memorandum", "User-supplied research schedule — verify against current PCA record"],
        ["Feb 2027", "7th meeting / hydraulic modelling exercise", "User-supplied research schedule — verify"],
        ["Mar 2027", "Draft technical decision", "User-supplied research schedule — verify"],
        ["Jul 2027", "Final technical determination", "User-supplied research schedule — verify"],
    ], columns=["date", "milestone", "verification status"]), use_container_width=True, hide_index=True)

    st.subheader("7. Interim measures and construction-status evidence")
    st.markdown("The PCA's 31 August 2026 press release confirms that an Order on Interim Measures concerning Ratle was issued. The dashboard does not restate additional construction restrictions or their duration beyond what is established in the operative order; users should consult the primary order for exact elevations, dates and legal effect.")
    st.markdown("Primary PCA case record: https://pca-cpa.org/en/cases/284/")

    st.subheader("8. Evidence workspace")
    st.write("Upload hydrological, crop-water, reservoir or flow datasets in Data Analytics & Graphs to test downstream-flow and agricultural relationships quantitatively. Narrative claims alone are not converted into causal estimates.")

elif choice == "🌍 ESG / ISO / SDG / MDG / Vision 2030":
    st.title("ESG / ISO / UN SDGs / MDGs / Vision 2030")
    view = st.selectbox("Framework", ["ESG","ISO standards","UN SDGs","MDGs","Vision 2030","Crosswalk"] )
    if view == "ESG":
        show_table(ESG)
    elif view == "ISO standards":
        show_table(ISO_STANDARDS)
    elif view == "UN SDGs":
        show_table(sdg_table())
    elif view == "MDGs":
        show_table(mdg_table())
    elif view == "Vision 2030":
        show_table(vision_table())
    else:
        show_table(crosswalk_table())
    st.subheader("Input-driven sustainability assessment")
    st.caption("Upload official indicator data in Data Analytics & Graphs to calculate project- or region-specific charts; framework tables here are reference mappings rather than performance scores.")

elif choice == "📊 Data Analytics & Graphs":
    st.title("Upload Data → Clean → Analyze → Graph")
    st.write("Upload one or multiple CSV, PDF, XLSX or XLS files. The application extracts the data, converts numeric fields where possible, and generates interactive Plotly graphs from the actual uploaded values.")
    st.info("PDF support covers selectable-text PDFs, table PDFs, and scanned/image PDFs when OCR is available. No unreadable values are invented.")
    files = st.file_uploader("Choose CSV, PDF or Excel files", type=["csv","pdf","xlsx","xls"], accept_multiple_files=True)
    if files:
        for file_index, uploaded in enumerate(files):
            file_key = f"file_{file_index}_{uploaded.name}"
            with st.expander(f"📄 {uploaded.name}", expanded=True):
                try:
                    if getattr(uploaded, "size", 0) == 0:
                        st.warning("This file is empty. Please upload a non-empty CSV, PDF or Excel file.")
                        continue
                    loaded, meta = load_uploaded_file(uploaded)
                    df = coerce_numeric(loaded)
                    if df.empty:
                        st.warning("No tabular records could be extracted from this file. Check the file structure or upload a cleaner source.")
                        continue
                    st.success(f"Loaded {len(df):,} rows × {len(df.columns):,} columns")
                    if meta.get("type") == "pdf":
                        st.caption(f"PDF extraction mode: {meta.get('extraction', 'unknown')}")
                        for warning in meta.get("warnings", []):
                            st.warning(warning)
                    st.dataframe(df.head(200), use_container_width=True, hide_index=True)

                    # River-basin telemetry variance + optional water-quality indexes.
                    st.markdown("### 🌊 River Basin Telemetry & Water Quality Analytics")
                    basin_col = detect_basin_column(df)
                    quality_cols = detect_water_quality_columns(df)
                    telemetry_cols = detect_telemetry_columns(df, exclude=[basin_col] if basin_col else [])

                    basin_options = list(df.columns)
                    selected_basin = st.selectbox(
                        "River basin / watershed column",
                        ["Auto-detect"] + basin_options,
                        index=0,
                        key=f"basin_{file_key}",
                    )
                    if selected_basin != "Auto-detect":
                        basin_col = selected_basin

                    numeric_cols = chart_candidates(df)["numeric"]
                    default_telemetry = [c for c in telemetry_cols if c in numeric_cols]
                    selected_telemetry = st.multiselect(
                        "Telemetry variables for variance analysis",
                        numeric_cols,
                        default=default_telemetry,
                        key=f"telemetry_{file_key}",
                        help="Select gauge, discharge, level, flow, sensor or other numeric telemetry fields. The engine calculates sample variance within each basin and then averages the available telemetry variances.",
                    )

                    if basin_col and selected_telemetry:
                        variance_df = telemetry_variance_by_basin(df, basin_col, selected_telemetry)
                        if not variance_df.empty:
                            st.dataframe(variance_df, use_container_width=True, hide_index=True)
                            fig_var = px.bar(
                                variance_df.dropna(subset=["average_telemetry_variance"]),
                                x=basin_col, y="average_telemetry_variance",
                                title="Average Telemetry Data Variance by River Basin",
                                labels={"average_telemetry_variance": "Average telemetry variance", basin_col: "River basin"},
                            )
                            st.plotly_chart(fig_var, use_container_width=True)
                            top = variance_df.dropna(subset=["average_telemetry_variance"]).head(1)
                            if not top.empty:
                                st.success(f"Highest average telemetry variance: **{top.iloc[0][basin_col]}** ({top.iloc[0]['average_telemetry_variance']:.4g}).")
                    else:
                        st.info("To calculate basin-level telemetry variance, provide/select a river-basin column and at least one numeric telemetry variable.")

                    # Dissolved oxygen and additional water-quality indexes.
                    st.markdown("#### 🧪 Optional Water Quality Indexes")
                    detected_quality = list(quality_cols.keys())
                    selected_quality_labels = st.multiselect(
                        "Water-quality parameters",
                        detected_quality,
                        default=["Dissolved Oxygen (DO)"] if "Dissolved Oxygen (DO)" in detected_quality else detected_quality[:1],
                        key=f"quality_{file_key}",
                        help="Dissolved Oxygen (DO) is included when detected. You can also analyze pH, turbidity, TDS, conductivity, temperature, nitrate, BOD, COD and coliform where present.",
                    )
                    if basin_col and selected_quality_labels:
                        selected_quality_cols = {k: quality_cols[k] for k in selected_quality_labels}
                        quality_summary = water_quality_summary(df, basin_col, selected_quality_cols)
                        if not quality_summary.empty:
                            st.dataframe(quality_summary, use_container_width=True, hide_index=True)
                            quality_metric = st.selectbox(
                                "Water-quality index to visualize",
                                selected_quality_labels,
                                key=f"quality_metric_{file_key}",
                            )
                            qplot = quality_summary[[basin_col, quality_metric]].dropna()
                            if not qplot.empty:
                                fig_q = px.bar(
                                    qplot, x=basin_col, y=quality_metric,
                                    title=f"Average {quality_metric} by River Basin",
                                    labels={basin_col: "River basin", quality_metric: quality_metric},
                                )
                                st.plotly_chart(fig_q, use_container_width=True)

                    # Provide a reproducible Python visualization script based on the uploaded columns.
                    if basin_col and selected_telemetry:
                        script_quality = {k: quality_cols[k] for k in selected_quality_labels} if 'selected_quality_labels' in locals() else {}
                        script = generate_visualization_script(basin_col, selected_telemetry, script_quality)
                        with st.expander("🐍 Python visualization script", expanded=False):
                            st.code(script, language="python")
                            st.download_button(
                                "⬇️ Download Python visualization script",
                                script.encode("utf-8"),
                                f"{uploaded.name.rsplit('.',1)[0]}_river_basin_telemetry_visualization.py",
                                "text/x-python",
                                key=f"script_{file_key}",
                            )

                    st.markdown("### 🗺️ Map output from uploaded CSV / PDF / Excel")
                    spatial_color = st.selectbox("Optional map color column", ["None"] + list(df.columns), key=f"map_color_{file_key}")
                    color_arg = None if spatial_color == "None" else spatial_color
                    fig_map, map_msg = map_uploaded_data(df, color=color_arg, hover=list(df.columns[:5]), title=f"Map from {uploaded.name}")
                    if fig_map is not None:
                        st.plotly_chart(fig_map, use_container_width=True)
                        st.success("Spatial map generated from the uploaded coordinate fields.")
                    else:
                        st.info(map_msg)

                    st.markdown("### 🌱 Indus Delta EMI / Soil Salinity Analytics")
                    st.dataframe(SOIL_ANALYTICS, use_container_width=True, hide_index=True)
                    numeric, categorical = chart_candidates(df)
                    if numeric:
                        kind = st.selectbox("Chart", ["Bar chart","Pie chart","Scatter plot","Line chart"], key=f"kind_{file_key}")
                        if kind == "Scatter plot":
                            x = st.selectbox("X numeric column", numeric, key=f"x_{file_key}")
                            y = st.selectbox("Y numeric column", numeric, index=min(1,len(numeric)-1), key=f"y_{file_key}")
                            fig = px.scatter(df, x=x, y=y, hover_data=categorical[:5], title=f"{y} vs {x}")
                        else:
                            metric = st.selectbox("Numeric column", numeric, key=f"metric_{file_key}")
                            group = st.selectbox("Category / time column", categorical or [numeric[0]], key=f"group_{file_key}")
                            if kind == "Bar chart":
                                agg = st.selectbox("Aggregation", ["sum","mean","count"], key=f"agg_{file_key}")
                                if agg == "count":
                                    p = df.groupby(group, dropna=False).size().reset_index(name="count")
                                    fig = px.bar(p, x=group, y="count", title=f"Count by {group}")
                                else:
                                    p = df.groupby(group, dropna=False)[metric].agg(agg).reset_index()
                                    fig = px.bar(p, x=group, y=metric, title=f"{agg.title()} of {metric} by {group}")
                            elif kind == "Pie chart":
                                p = df.groupby(group, dropna=False)[metric].sum().reset_index()
                                fig = px.pie(p, names=group, values=metric, title=f"{metric} by {group}")
                            else:
                                fig = px.line(df, x=group, y=metric, markers=True, title=f"{metric} over {group}")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No numeric columns were detected for quantitative charts.")
                    st.download_button("⬇️ Download cleaned CSV", df.to_csv(index=False).encode(), f"{uploaded.name.rsplit('.',1)[0]}_cleaned.csv", "text/csv", key=f"dl_{file_key}")
                except Exception as e:
                    st.error(f"Could not parse {uploaded.name}: {e}")
                    st.info("Text/table PDFs are supported. Image-only scanned PDFs require OCR software; the app will not invent unreadable values.")
    else:
        st.info("Upload files above to generate graphs from your own data.")

elif choice == "🧭 Regional Profiles":
    st.title("Regional Profiles & Major Cities")
    show_table(filter_df(REGIONAL_PROFILE, province, search))
    st.subheader("Major cities / service centres")
    show_table(filter_df(MAJOR_CITIES, province, search))

elif choice == "📚 Sources":
    st.title("Primary / Supporting Sources")
    for s in SOURCES:
        st.markdown(f"- [{s['title']}]({s['url']})")
    st.markdown("### Current PCA / project-status references")
    current_sources = [
        ("PCA — Indus Waters Western Rivers Arbitration case record", "https://pca-cpa.org/en/cases/284/"),
        ("PPIB — CPEC Projects, as of 30 June 2026", "https://www.ppib.gov.pk/cpec.html"),
        ("CPEC — Energy Projects", "https://www.cpec.gov.pk/energy"),
        ("WAPDA — Diamer Basha Dam", "https://wapda.gov.pk/diamer-basha-dam-project/"),
    ]
    for title,url in current_sources:
        st.markdown(f"- [{title}]({url})")
    st.info("For legal, project-status and engineering claims, consult the linked primary institutional source and its current version.")

st.divider()
st.caption(f"IndusSphere Pakistan · Creator: {CREATOR} · Educational and decision-support visualization. Verify engineering, legal, environmental and statistical inputs before professional use.")

import plotly.express as px
from india_indus_hydropower import PROJECTS_DF, MAP_NOTE


def india_indus_projects_map(df=None, height=650):
    """Return a standalone Plotly map for the 17-project Indus-basin inventory."""
    data = (PROJECTS_DF if df is None else df).copy()
    fig = px.scatter_map(
        data,
        lat="latitude",
        lon="longitude",
        color="status",
        size="capacity_mw",
        size_max=24,
        hover_name="project",
        hover_data={
            "capacity_mw": True,
            "river": True,
            "basin": True,
            "status": True,
            "latitude": False,
            "longitude": False,
        },
        zoom=5.0,
        center={"lat": 33.65, "lon": 75.15},
        height=height,
        title="India Indus River System — 17-project hydropower inventory",
    )
    fig.update_layout(map_style="open-street-map", legend_title_text="Project status")
    fig.add_annotation(
        x=0.01, y=0.01, xref="paper", yref="paper", showarrow=False,
        text=MAP_NOTE, align="left", font={"size": 10}
    )
    return fig

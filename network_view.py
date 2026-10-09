import plotly.graph_objects as go
def river_network():
    nodes={"Gilgit":(74.58,35.90),"Indus":(72.70,34.08),"Kabul":(72.24,33.99),
           "Jhelum":(73.65,33.15),"Chenab":(74.46,32.67),"Ravi":(73.84,31.22),
           "Sutlej":(73.08,30.66),"Panjnad":(71.05,29.35),"Lower Indus":(69.74,28.43),
           "Arabian Sea":(68.31,25.38)}
    edges=[("Gilgit","Indus"),("Kabul","Indus"),("Jhelum","Chenab"),
           ("Chenab","Panjnad"),("Ravi","Panjnad"),("Sutlej","Panjnad"),
           ("Panjnad","Lower Indus"),("Lower Indus","Arabian Sea")]
    f=go.Figure()
    for a,b in edges:
        x1,y1=nodes[a];x2,y2=nodes[b]
        f.add_trace(go.Scatter(x=[x1,x2],y=[y1,y2],mode="lines",
            line=dict(width=3),showlegend=False,hoverinfo="skip"))
    f.add_trace(go.Scatter(x=[v[0] for v in nodes.values()],y=[v[1] for v in nodes.values()],
        mode="markers+text",text=list(nodes.keys()),textposition="top center",
        marker=dict(size=13),name="Network nodes"))
    f.update_layout(height=550,xaxis_title="Longitude",yaxis_title="Latitude",
                    yaxis=dict(scaleanchor="x",scaleratio=1),margin=dict(l=20,r=20,t=20,b=20))
    return f

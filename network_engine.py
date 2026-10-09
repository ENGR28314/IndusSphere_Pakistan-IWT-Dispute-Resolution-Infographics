from __future__ import annotations
import pandas as pd
def route_network(nodes,links,source_inflows=None,losses=None):
    nodes=list(nodes); links=links.copy(); required={'from','to','capacity'}
    if not required.issubset(links.columns): raise ValueError(f'links must contain {sorted(required)}')
    flow={n:float((source_inflows or {}).get(n,0)) for n in nodes}; losses=losses or {}; rows=[]
    for _,r in links.iterrows():
        a,b=r['from'],r['to']; incoming=flow.get(a,0); cap=max(float(r['capacity']),0); routed=min(incoming,cap); loss=max(min(float(losses.get(a,0)),1),0); delivered=routed*(1-loss); flow[b]=flow.get(b,0)+delivered; flow[a]=max(incoming-routed,0)
        rows.append({'From':a,'To':b,'Capacity':cap,'Routed':routed,'Delivered':delivered})
    return pd.DataFrame(rows),pd.DataFrame([{'Node':n,'Remaining flow':v} for n,v in flow.items()])

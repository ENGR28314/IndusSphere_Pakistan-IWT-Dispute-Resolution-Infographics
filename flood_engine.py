from __future__ import annotations
import numpy as np
import pandas as pd

def flood_scenario(rainfall_mm, catchment_km2, runoff_coefficient, channel_capacity_m3s, duration_hours, exposure=50, vulnerability=50, criticality=50):
    rainfall_m=max(float(rainfall_mm),0)/1000; area=max(float(catchment_km2),0)*1_000_000
    volume=rainfall_m*area*np.clip(float(runoff_coefficient),0,1); duration=max(float(duration_hours),.01)*3600
    peak=volume/duration; exceed=max(peak-float(channel_capacity_m3s),0); ratio=peak/max(float(channel_capacity_m3s),1e-9)
    risk=float(np.clip(.45*min(ratio*50,100)+.2*exposure+.2*vulnerability+.15*criticality,0,100))
    return {'runoff_volume_m3':volume,'peak_flow_proxy_m3s':peak,'capacity_exceedance_m3s':exceed,'capacity_ratio':ratio,'risk_index':risk,'risk_class':'Low' if risk<40 else 'Moderate' if risk<70 else 'High'}

def rainfall_sweep(rainfall_values, **kwargs):
    rows=[]
    for r in rainfall_values:
        o=flood_scenario(rainfall_mm=r,**kwargs); rows.append({'Rainfall (mm)':r,'Peak flow proxy (m3/s)':o['peak_flow_proxy_m3s'],'Capacity ratio':o['capacity_ratio'],'Risk index':o['risk_index']})
    return pd.DataFrame(rows)

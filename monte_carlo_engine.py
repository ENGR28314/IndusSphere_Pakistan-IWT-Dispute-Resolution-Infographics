from __future__ import annotations
import numpy as np
import pandas as pd
def monte_carlo_risk(n=2000,seed=42,exposure=50,vulnerability=50,sensitivity=50,adaptive_capacity=50,criticality=50):
    rng=np.random.default_rng(seed); sample=lambda x:np.clip(rng.normal(float(x),10,n),0,100); e,v,s,a,c=map(sample,[exposure,vulnerability,sensitivity,adaptive_capacity,criticality]); risk=np.clip(.25*e+.25*v+.20*s+.20*c+.10*(100-a),0,100); return pd.DataFrame({'Exposure':e,'Vulnerability':v,'Sensitivity':s,'Adaptive capacity':a,'Criticality':c,'Risk index':risk})
def summarize(sim):
    r=sim['Risk index']; return {'mean':float(r.mean()),'p10':float(r.quantile(.10)),'median':float(r.median()),'p90':float(r.quantile(.90)),'high_pct':float((r>=70).mean()*100)}

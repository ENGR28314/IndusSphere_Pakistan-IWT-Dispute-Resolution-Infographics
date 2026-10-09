from __future__ import annotations
import numpy as np
import pandas as pd
SCENARIO_FACTORS={'Baseline':1.0,'Medium':1.15,'Worst-Case':1.35}; HORIZON_FACTORS={'Near Term':1.0,'Mid Century':1.15,'Long Term':1.30}
def climate_stress(exposure,vulnerability,sensitivity,adaptive_capacity,criticality,scenario,horizon):
    sf=SCENARIO_FACTORS.get(scenario,1); hf=HORIZON_FACTORS.get(horizon,1); raw=(.25*exposure+.25*vulnerability+.20*sensitivity+.20*criticality+.10*(100-adaptive_capacity))*sf*hf; idx=float(np.clip(raw/1.30,0,100)); return {'risk_index':idx,'risk_class':'Low' if idx<40 else 'Moderate' if idx<70 else 'High','scenario_factor':sf,'horizon_factor':hf}
def sensitivity_table(base,parameter,values):
    return pd.DataFrame([{parameter:v,'Risk index':climate_stress(**{**base,parameter:v})['risk_index']} for v in values])

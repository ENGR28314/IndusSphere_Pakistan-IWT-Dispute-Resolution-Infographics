from __future__ import annotations
CROP_COEFFICIENTS={'Wheat':1.15,'Rice':1.20,'Cotton':1.10,'Maize':1.05,'Sugarcane':1.25,'Gram/Chickpea':.90,'Barley':1.05,'Mustard/Rapeseed':.95,'Canola':1.00,'Lentil':.90}
def crop_water_requirement(et0_mm,kc,effective_rainfall_mm=0,area_ha=1,efficiency=.65):
    etc=max(float(et0_mm),0)*max(float(kc),0); net=max(etc-max(float(effective_rainfall_mm),0),0); gross=net/max(float(efficiency),.01); vol=gross*max(float(area_ha),0)*10
    return {'ETc_mm':etc,'Net irrigation_mm':net,'Gross irrigation_mm':gross,'Gross irrigation volume_m3':vol}
def crop_comparison(crops,et0_mm,effective_rainfall_mm,area_ha,efficiency):
    import pandas as pd
    return pd.DataFrame([{'Crop':c,'Kc':CROP_COEFFICIENTS.get(c,1.0),**crop_water_requirement(et0_mm,CROP_COEFFICIENTS.get(c,1.0),effective_rainfall_mm,area_ha,efficiency)} for c in crops])

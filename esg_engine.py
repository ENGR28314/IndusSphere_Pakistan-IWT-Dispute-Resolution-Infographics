import pandas as pd

def sustainability_input_template():
    return pd.DataFrame([
        ["Punjab","Food security",0.0,"SDG 2"],
        ["Sindh","Water conservation",0.0,"SDG 6"],
        ["Balochistan","Climate resilience",0.0,"SDG 13"],
    ], columns=["province_region","indicator","value","framework_alignment"])

def summarize_esg(df):
    if df.empty or "indicator" not in df.columns or "value" not in df.columns:
        return pd.DataFrame()
    x=df.copy(); x["value"]=pd.to_numeric(x["value"],errors="coerce")
    return x.groupby("indicator",dropna=False)["value"].mean().reset_index(name="mean_value")

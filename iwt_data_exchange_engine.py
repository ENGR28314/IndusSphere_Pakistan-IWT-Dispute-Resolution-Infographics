"""Data-exchange timeline and audit helpers for IWT research dashboards."""
import pandas as pd

CORE_FIELDS = ["date","river","gauge_discharge","reservoir_releases","canal_withdrawals","channel","frequency","prior_notice","source"]

def empty_template():
    return pd.DataFrame(columns=CORE_FIELDS)

def normalize_exchange_df(df):
    x = df.copy()
    aliases = {
        "Date":"date", "River":"river", "Gauge/Discharge":"gauge_discharge",
        "Reservoir Releases":"reservoir_releases", "Canal Withdrawals":"canal_withdrawals",
        "Channel":"channel", "Frequency":"frequency", "Prior Notice":"prior_notice", "Source":"source"
    }
    x = x.rename(columns={k:v for k,v in aliases.items() if k in x.columns})
    for c in CORE_FIELDS:
        if c not in x.columns: x[c] = ""
    return x[CORE_FIELDS]

def compare_dataset_coverage(df):
    x = normalize_exchange_df(df)
    checks = []
    for _, r in x.iterrows():
        fields = [r.get("gauge_discharge"), r.get("reservoir_releases"), r.get("canal_withdrawals")]
        supplied = sum(bool(str(v).strip()) and str(v).lower() not in {"nan","none"} for v in fields)
        checks.append({"date":r["date"], "river":r["river"], "dataset_fields_supplied":supplied, "coverage":"Partial" if supplied < 3 else "Core fields supplied"})
    return pd.DataFrame(checks)

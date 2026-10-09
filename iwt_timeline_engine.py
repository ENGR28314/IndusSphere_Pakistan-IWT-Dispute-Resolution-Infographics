"""Neutral timeline engine for documented Indus Waters Treaty events."""
import pandas as pd

DEFAULT_EVENTS = [
    {"date":"1960-09-19","event":"Indus Waters Treaty signed","category":"Treaty baseline","source":"Indus Waters Treaty / India MEA text"},
    {"date":"2022-10-17","event":"World Bank appointed Michel Lino as Neutral Expert and Sean Murphy as Chairman of the Court of Arbitration","category":"Institutional appointments","source":"World Bank"},
    {"date":"2025-06-27","event":"PCA Supplemental Award on Competence","category":"Arbitration","source":"PCA"},
    {"date":"2025-08-11","event":"PCA Award on Issues of General Interpretation","category":"Arbitration","source":"PCA"},
    {"date":"2025-11-10","event":"PCA Decision on Pakistan's Request for Clarification","category":"Arbitration","source":"PCA"},
    {"date":"2026-06-05","event":"PCA Supplemental Award concerning Maximum Pondage","category":"Arbitration","source":"PCA"},
    {"date":"2026-08-31","event":"PCA Award on Treaty Status and Order on Interim Measures concerning Ratle","category":"Arbitration","source":"PCA"},
]

def timeline_df():
    return pd.DataFrame(DEFAULT_EVENTS)

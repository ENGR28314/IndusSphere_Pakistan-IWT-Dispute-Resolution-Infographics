"""Evidence ledger separating source types and assertions."""
import pandas as pd

def evidence_ledger():
    return pd.DataFrame([
        {"source_type":"Treaty text","claim_scope":"Treaty provisions","treatment":"Primary legal text"},
        {"source_type":"PCA award/order","claim_scope":"Arbitration findings and procedural decisions","treatment":"Primary adjudicative source"},
        {"source_type":"Pakistan official statement","claim_scope":"Pakistan's position","treatment":"Attributed position"},
        {"source_type":"India official statement","claim_scope":"India's position","treatment":"Attributed position"},
        {"source_type":"Hydrological record","claim_scope":"Observed flows/releases/alerts","treatment":"Technical evidence; verify provenance"},
        {"source_type":"Dashboard calculation","claim_scope":"Model-derived indicator","treatment":"Analytical output, not a legal finding"},
    ])

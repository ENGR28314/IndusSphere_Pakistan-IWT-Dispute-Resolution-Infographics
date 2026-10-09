"""Descriptive IWT dispute-resolution pathway model."""
PATHWAYS = [
    ("Commissioners / PIC", "Bilateral technical and institutional engagement"),
    ("Difference", "Issue may proceed under the treaty's technical difference mechanism depending on characterization"),
    ("Neutral Expert", "Annexure F pathway for matters falling within its scope"),
    ("Court of Arbitration", "Annexure G pathway for matters falling within its scope"),
]

def pathway(issue_type):
    mapping = {
        "Data exchange": [PATHWAYS[0], PATHWAYS[1], PATHWAYS[3]],
        "Technical design issue": [PATHWAYS[0], PATHWAYS[1], PATHWAYS[2]],
        "Treaty interpretation": [PATHWAYS[0], PATHWAYS[3]],
    }
    return mapping.get(issue_type, PATHWAYS)

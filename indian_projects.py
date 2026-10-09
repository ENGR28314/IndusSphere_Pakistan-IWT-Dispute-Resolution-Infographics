import pandas as pd

PROJECTS = pd.DataFrame([
 ["Pakal Dul","1,000 MW","Chenab/Marusudar system","Technical design issues raised by Pakistan include storage/pondage and outlet configuration; legal conclusions should be taken from the PCA/Neutral Expert records."],
 ["Ratle","850 MW","Chenab","Pakistan has raised technical questions concerning pondage, freeboard/dam elevation, intake/outlet configuration and spillways; the proceedings contain the operative findings."],
 ["Kiru","624 MW","Chenab basin","Hydropower project in the Chenab basin; include project status only when supported by a dated authoritative source."],
 ["Kwar","540 MW","Chenab basin","Hydropower project in the Chenab basin; include project status only when supported by a dated authoritative source."],
], columns=["project","capacity","basin","dashboard_note"])

TECHNICAL_POINTS = pd.DataFrame([
 ["Pondage capacity","Live/pondage storage used for daily operational fluctuations","Present party positions separately; do not convert a submission into a legal finding."],
 ["Freeboard / dam elevation","Vertical safety margin and reservoir elevation design","Compare engineering drawings and operative adjudicative decisions."],
 ["Deep-level outlets / gated spillways","Outlet elevation and gate configuration","Use primary proceedings for exact dimensions and binding requirements."],
 ["Power intake submergence","Intake elevation relative to reservoir levels","Record claimed and adjudicated values separately."],
 ["Head Marala / crop-impact issue","Reported concern about Chenab flow conditions and irrigation/crop implications","No causal crop-loss estimate should be asserted without a hydrological dataset."],
], columns=["issue","engineering_description","evidence_rule"])

INTER_BASIN = pd.DataFrame([
 ["Proposed inter-basin canal concept","Reports of proposals involving links among Chenab/Ravi-Beas-Sutlej systems","Treat as a reported proposal and verify against current Indian government/project documentation before treating as an active project."],
 ["Ravi-Beas link concept","Reported objective of managing eastern-river flows","Use dated authoritative documentation for feasibility, construction status and design."],
], columns=["item","description","verification_note"])

import pandas as pd

ESG = pd.DataFrame([
 ["Environment","Water stewardship","Water conservation, efficient irrigation, pollution prevention, groundwater protection"],
 ["Environment","Climate resilience","Flood, drought, heat, GLOF and coastal-risk adaptation"],
 ["Environment","Biodiversity & forests","Forest protection, restoration, habitat and protected-area management"],
 ["Environment","Pollution","Air, water and soil pollution monitoring and mitigation"],
 ["Social","Food security","Reliable water, agriculture, livelihoods and nutrition"],
 ["Social","Community impacts","Resettlement, local development, access to services and stakeholder engagement"],
 ["Social","Worker health & safety","Occupational safety and emergency preparedness"],
 ["Governance","Transparency & data","Traceable datasets, disclosure, monitoring and audit trails"],
 ["Governance","Risk management","Structured identification, assessment, controls and review"],
 ["Governance","Legal & institutional compliance","Applicable treaty, regulatory, environmental and governance requirements"],
], columns=["pillar","topic","IndusSphere application"])

ISO_STANDARDS = pd.DataFrame([
 ["ISO 14001","Environmental management systems","Environmental aspects, controls, continual improvement"],
 ["ISO 14064","Greenhouse-gas quantification/reporting","GHG inventories and reporting"],
 ["ISO 14067","Carbon footprint of products","Product carbon-footprint analysis"],
 ["ISO 31000","Risk management","Risk identification, assessment, treatment and monitoring"],
 ["ISO 50001","Energy management","Energy performance and efficiency"],
 ["ISO 45001","Occupational health and safety","Worker safety management"],
], columns=["standard","theme","dashboard_use"])

def framework_table():
    return ESG.copy()

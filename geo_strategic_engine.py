import pandas as pd

def issue_register():
    return pd.DataFrame([
        ["Hydro-politics of Kashmir","Headwater geography and water management are major bilateral/regional issues."],
        ["Punjab–Sindh water disputes","Documented competing claims concerning allocation, timing, shortages and downstream requirements."],
        ["IRSA / CCI / Article 155","Institutional and constitutional mechanisms for water-related complaints and coordination."],
        ["Maritime trade infrastructure","Karachi Port, Port Qasim and Gwadar connect water/energy systems with maritime trade."],
        ["CPEC hydropower","Project capacity, status and financing should be tracked with dated primary sources."],
        ["Indian Chenab projects","Pakistan's stated technical and flow concerns should be separated from adjudicative findings and hydrological evidence."],
    ], columns=["issue","neutral_description"])

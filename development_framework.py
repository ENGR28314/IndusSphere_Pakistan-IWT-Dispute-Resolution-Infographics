"""UN SDGs, MDGs and Pakistan Vision 2030 thematic framework for IndusSphere Pakistan.

This module stores framework descriptions and a thematic crosswalk. It deliberately
avoids inventing current performance scores; users can upload official indicator data.
"""

SDGS = [
    (1, "No Poverty", "End poverty in all its forms everywhere", "poverty, resilience, social protection"),
    (2, "Zero Hunger", "End hunger, achieve food security and improved nutrition and promote sustainable agriculture", "food security, crops, irrigation, nutrition"),
    (3, "Good Health and Well-being", "Ensure healthy lives and promote well-being for all at all ages", "health, WASH, pollution, disasters"),
    (4, "Quality Education", "Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all", "education, skills, human capital"),
    (5, "Gender Equality", "Achieve gender equality and empower all women and girls", "gender, livelihoods, participation"),
    (6, "Clean Water and Sanitation", "Ensure availability and sustainable management of water and sanitation for all", "rivers, groundwater, irrigation, sanitation, water efficiency"),
    (7, "Affordable and Clean Energy", "Ensure access to affordable, reliable, sustainable and modern energy for all", "hydropower, renewable energy, energy efficiency"),
    (8, "Decent Work and Economic Growth", "Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all", "employment, productivity, rural livelihoods, tourism"),
    (9, "Industry, Innovation and Infrastructure", "Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation", "dams, transport, digital systems, infrastructure resilience"),
    (10, "Reduced Inequalities", "Reduce inequality within and among countries", "regional disparities, access, vulnerable communities"),
    (11, "Sustainable Cities and Communities", "Make cities and human settlements inclusive, safe, resilient and sustainable", "urban flooding, drainage, land use, resilient settlements"),
    (12, "Responsible Consumption and Production", "Ensure sustainable consumption and production patterns", "water conservation, resource efficiency, pollution, waste"),
    (13, "Climate Action", "Take urgent action to combat climate change and its impacts", "GLOFs, floods, droughts, heatwaves, adaptation"),
    (14, "Life Below Water", "Conserve and sustainably use the oceans, seas and marine resources for sustainable development", "coastal Sindh/Balochistan, mangroves, marine pollution"),
    (15, "Life on Land", "Protect, restore and promote sustainable use of terrestrial ecosystems", "forests, mountains, biodiversity, land degradation"),
    (16, "Peace, Justice and Strong Institutions", "Promote peaceful and inclusive societies for sustainable development", "governance, institutions, transparency, dispute mechanisms"),
    (17, "Partnerships for the Goals", "Strengthen the means of implementation and revitalize the global partnership for sustainable development", "finance, data, technology, cooperation"),
]

MDGS = [
    (1, "Eradicate extreme poverty and hunger", "poverty, hunger, livelihoods"),
    (2, "Achieve universal primary education", "education and human capital"),
    (3, "Promote gender equality and empower women", "gender equality"),
    (4, "Reduce child mortality", "child health"),
    (5, "Improve maternal health", "maternal health"),
    (6, "Combat HIV/AIDS, malaria and other diseases", "disease prevention"),
    (7, "Ensure environmental sustainability", "water, sanitation, environment"),
    (8, "Develop a global partnership for development", "international cooperation"),
]

# Thematic representation of Pakistan Vision 2030 for dashboard cross-referencing.
# It is not presented as a live implementation scorecard.
VISION_2030_THEMES = [
    {"theme": "A just and sustainable society", "focus": "poverty reduction, social inclusion, human development, environmental sustainability"},
    {"theme": "Knowledge and human capital", "focus": "education, skills, science, technology and innovation"},
    {"theme": "Economic transformation", "focus": "productive agriculture, industry, services, employment and competitiveness"},
    {"theme": "Water, food and energy security", "focus": "water resources, irrigation, food security, energy availability and efficiency"},
    {"theme": "Infrastructure and connectivity", "focus": "transport, communications, urban development and resilient infrastructure"},
    {"theme": "Environment and climate resilience", "focus": "ecosystems, forests, pollution control, climate risks and natural-resource management"},
    {"theme": "Governance and institutions", "focus": "effective institutions, policy coordination, accountability and long-term planning"},
]

CROSSWALK = [
    ("Food security / Zero Hunger", "SDG 2", "MDG 1", "Vision 2030: economic transformation / water-food-energy security"),
    ("Poverty alleviation", "SDG 1", "MDG 1", "Vision 2030: just and sustainable society"),
    ("Water conservation & WASH", "SDG 6", "MDG 7", "Vision 2030: water, food and energy security"),
    ("Environmental protection", "SDG 12, 13, 14, 15", "MDG 7", "Vision 2030: environment and climate resilience"),
    ("Sustainable agriculture", "SDG 2, 6, 12, 13, 15", "MDG 1, 7", "Vision 2030: economic transformation / natural-resource management"),
    ("Forests & biodiversity", "SDG 13, 15", "MDG 7", "Vision 2030: environment and climate resilience"),
    ("Clean energy", "SDG 7, 9, 13", "MDG 7, 8", "Vision 2030: water, food and energy security"),
    ("Employment & livelihoods", "SDG 1, 8, 10", "MDG 1, 3", "Vision 2030: economic transformation / human capital"),
    ("Disaster resilience", "SDG 1, 9, 11, 13", "MDG 1, 7", "Vision 2030: resilient infrastructure / climate resilience"),
    ("Coastal / marine protection", "SDG 13, 14, 15", "MDG 7", "Vision 2030: environment and climate resilience"),
    ("Sustainable cities", "SDG 11", "MDG 7", "Vision 2030: infrastructure, urban development and environmental sustainability"),
    ("Governance & institutions", "SDG 16", "MDG 8", "Vision 2030: governance, institutional reform and public-sector modernization"),
    ("International partnerships", "SDG 17", "MDG 8", "Vision 2030: regional connectivity, development cooperation and international partnerships"),
]

DEVELOPMENT_DOMAINS = [
    "Poverty alleviation", "Food security / Zero Hunger", "Water conservation & WASH",
    "Environmental protection", "Sustainable agriculture", "Forests & biodiversity",
    "Clean energy", "Employment & livelihoods", "Disaster resilience", "Sustainable cities",
    "Coastal / marine protection", "Governance & institutions", "International partnerships"
]


def sdg_table():
    import pandas as pd
    return pd.DataFrame(SDGS, columns=["Goal", "Name", "Official description", "IndusSphere relevance"])


def mdg_table():
    import pandas as pd
    return pd.DataFrame(MDGS, columns=["MDG", "Goal", "IndusSphere relevance"])


def vision_table():
    import pandas as pd
    return pd.DataFrame(VISION_2030_THEMES)


def crosswalk_table():
    import pandas as pd
    return pd.DataFrame(CROSSWALK, columns=["Development domain", "UN SDG alignment", "MDG alignment", "Vision 2030 thematic alignment"])

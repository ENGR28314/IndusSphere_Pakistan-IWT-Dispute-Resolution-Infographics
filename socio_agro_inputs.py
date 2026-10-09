"""Structured, input-driven socio-economic and agro-economic reference data."""
from __future__ import annotations
import pandas as pd

# The season tables deliberately use the fields requested by the project scope.
RABI = pd.DataFrame([
    ["Rabi", "Wheat", "October–November sowing; March–April harvest", "High-value cool-season crop; irrigation scheduling is important during establishment, tillering and grain filling."],
    ["Rabi", "Gram / Chickpea", "October–November sowing; March–April harvest", "Generally lower water requirement than wheat; avoid excessive late-season irrigation."],
    ["Rabi", "Barley", "October–November sowing; March–April harvest", "Cool-season crop; irrigation requirement varies with rainfall, soil and cultivar."],
    ["Rabi", "Mustard / Rapeseed", "October–November sowing; February–March harvest", "Timely irrigation can support establishment and flowering; avoid waterlogging."],
    ["Rabi", "Canola", "October–November sowing; March–April harvest", "Manage irrigation around establishment and flowering according to soil moisture and weather."],
    ["Rabi", "Lentil", "October–November sowing; March–April harvest", "Moderate water demand; excessive irrigation can increase disease and lodging risk."],
    ["Rabi", "Fodder", "Season-dependent", "Irrigation scheduling should follow the specific fodder species and cutting cycle."],
], columns=["season", "crop", "typical_window", "engineering_water_note"])

KHARIF = pd.DataFrame([
    ["Kharif", "Rice", "May–June transplanting/sowing; September–October harvest", "High seasonal water demand; field-level irrigation and drainage efficiency are key engineering considerations."],
    ["Kharif", "Cotton", "April–June sowing; October–December picking", "Irrigation timing should track crop growth stages and rainfall; avoid prolonged waterlogging."],
    ["Kharif", "Maize", "Spring or summer planting depending on production system", "Water demand rises around vegetative growth, tasseling and grain filling; schedule with ET and soil moisture."],
    ["Kharif", "Sugarcane", "Planting windows vary; crop may occupy fields for much of the year", "Large cumulative water requirement; optimize conveyance, field application and drainage."],
    ["Kharif", "Sorghum", "Spring/summer sowing depending on production system", "Moderate water requirement; irrigation should follow crop stage and rainfall."],
    ["Kharif", "Millet", "Spring/summer sowing", "Relatively drought-tolerant, but irrigation can improve establishment and yield under moisture stress."],
    ["Kharif", "Mung bean", "Spring/summer or monsoon-associated windows", "Short-duration crop; avoid unnecessary late irrigation near maturity."],
    ["Kharif", "Mash bean", "Summer/monsoon window", "Short-duration crop; coordinate irrigation with rainfall and soil water holding capacity."],
], columns=["season", "crop", "typical_window", "engineering_water_note"])

CROP_SEASONS = {
    "Kharif": {"period": "Typically spring/summer to autumn; timing varies by crop and locality.", "crops": KHARIF["crop"].tolist(), "water_focus": "Higher warm-season irrigation demand for many crops; monsoon and canal availability affect scheduling."},
    "Rabi": {"period": "Typically autumn to spring; timing varies by crop and locality.", "crops": RABI["crop"].tolist(), "water_focus": "Winter irrigation demand is important for wheat and other cool-season crops."},
}

MAJOR_CROP_SEASONS = pd.DataFrame([
    ["Rabi", "Cool-season cropping", "Typically Oct–Apr", "Wheat, gram/chickpea, barley, mustard/rapeseed, canola, lentil, fodder"],
    ["Kharif", "Warm-season cropping", "Typically Apr/May–Oct", "Rice, cotton, maize, sugarcane, sorghum, millet, mung bean, mash bean"],
], columns=["season", "description", "typical_window", "representative_crops"])

APICULTURE_INDICATORS = [
    {"indicator": "Honey production", "unit": "tonnes", "description": "Annual honey harvested from managed colonies; useful for agro-economic and livelihood analysis."},
    {"indicator": "Managed colonies", "unit": "colonies", "description": "Number of productive bee colonies under management."},
    {"indicator": "Honey yield", "unit": "kg/colony", "description": "Average honey output per productive colony."},
    {"indicator": "Apiaries", "unit": "sites", "description": "Number of managed apiary locations."},
    {"indicator": "Pollination service", "unit": "ha serviced", "description": "Area benefiting from managed pollination services where records are available."},
]

AQUACULTURE_INDICATORS = [
    {"indicator": "Aquaculture production", "unit": "tonnes", "description": "Harvested fish/aquatic biomass from managed production systems."},
    {"indicator": "Production area", "unit": "ha", "description": "Pond, tank or other managed production area."},
    {"indicator": "Stocking density", "unit": "fish/ha", "description": "Number of stocked fish per unit production area."},
    {"indicator": "Survival rate", "unit": "%", "description": "Share of stocked animals surviving to harvest."},
    {"indicator": "Feed conversion ratio", "unit": "kg feed/kg biomass", "description": "Feed required per unit harvested biomass where records are available."},
]

APICULTURE = {
    "Production system": "Managed honey-bee colonies for honey, beeswax and pollination services.",
    "Common products": "Honey, beeswax and other hive products; pollination is an important agricultural service.",
    "Water/climate link": "Colony health and forage availability depend on flowering calendars, temperature, water access and pesticide management.",
    "Planning indicators": "Colonies, honey yield, apiaries, forage area, mortality/losses, input costs and farm-gate value.",
}
AQUACULTURE = {
    "Production systems": "Pond, tank and other managed aquatic production systems, alongside capture fisheries where relevant.",
    "Key outputs": "Fish biomass/harvest, species mix, feed use, stocking density, survival and farm value.",
    "Water-quality link": "Temperature, dissolved oxygen, pH, turbidity, ammonia and other water-quality variables affect production.",
    "Planning indicators": "Pond area, stocking density, production, feed conversion, mortality, water source and operating costs.",
}

SOCIO_ECONOMIC_INPUT_COLUMNS = [
    "province/region", "cultivated area", "crop production", "employment", "honey production", "aquaculture production"
]
SOCIO_AGRO_METRICS = {
    "Cultivated area (ha)": "cultivated area",
    "Crop production (tonnes)": "crop production",
    "Employment (persons)": "employment",
    "Honey production (tonnes)": "honey production",
    "Aquaculture production (tonnes)": "aquaculture production",
}
GRAPH_TYPES = ["Bar chart", "Pie chart", "Scatter plot", "Line chart"]

# Blank/default editable dataset: values are demonstration inputs only and are intended to be replaced by the user.
DEFAULT_SOCIO_AGRO_DATA = pd.DataFrame([
    ["Punjab", 1000000, 5000000, 2500000, 1200, 18000],
    ["Sindh", 700000, 3200000, 1400000, 700, 24000],
    ["Khyber Pakhtunkhwa", 450000, 1800000, 900000, 500, 6000],
    ["Balochistan", 250000, 600000, 450000, 300, 2500],
    ["Gilgit-Baltistan", 90000, 250000, 160000, 250, 900],
    ["Azad Jammu & Kashmir", 120000, 400000, 220000, 350, 1200],
    ["Islamabad Capital Territory", 12000, 35000, 25000, 20, 100],
], columns=SOCIO_ECONOMIC_INPUT_COLUMNS)

SOCIO_ECONOMIC_INPUTS = [
    "Population / households", "Employment / labor force", "Poverty / income", "Urban growth", "Food security", "Education", "Health access", "Tourism", "Domestic water utility", "Industrial water utility", "Energy access / generation", "Climate vulnerability"
]
AGRO_ECONOMIC_INPUTS = [
    "Cultivated area", "Irrigated area", "Crop yield", "Crop production", "Farm-gate value", "Input costs", "Rural employment", "Livestock", "Fisheries", "Apiculture", "Aquaculture", "Water productivity"
]

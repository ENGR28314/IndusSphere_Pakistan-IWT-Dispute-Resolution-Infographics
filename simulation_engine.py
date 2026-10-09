from hydrology_engine import monthly_water_balance,reservoir_rule_curve
from flood_engine import flood_scenario,rainfall_sweep
from crop_water_engine import crop_water_requirement,crop_comparison,CROP_COEFFICIENTS
from climate_engine import climate_stress,sensitivity_table
from monte_carlo_engine import monte_carlo_risk,summarize
ENGINES={'Reservoir / Water Balance':'hydrology_engine.py','Flood Screening':'flood_engine.py','Crop Water Requirement':'crop_water_engine.py','Climate Stress':'climate_engine.py','Monte Carlo Risk':'monte_carlo_engine.py','River / Canal Network':'network_engine.py'}

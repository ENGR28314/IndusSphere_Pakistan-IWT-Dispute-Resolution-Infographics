import pandas as pd

REGIONAL_PROFILE = pd.DataFrame([
    ["Gilgit-Baltistan","High mountain / alpine","Upper Indus, Gilgit, Hunza, Shyok, Shigar","Karakoram, western Himalaya, Hindu Kush margins","Glaciers, GLOFs, avalanches, landslides, earthquakes, water/energy systems, tourism"],
    ["Khyber Pakhtunkhwa","Highland / temperate to arid transition","Kabul, Swat, Kurram, Gomal, Indus","Hindu Kush, Hindu Raj, Spīn Ghar, western Himalaya margins","Floods, flash floods, landslides, earthquakes, avalanches, drought, urban growth"],
    ["Punjab","Alluvial / semi-arid plains","Indus, Jhelum, Chenab, Ravi, Sutlej, Panjnad","Salt Range, western foothills","Riverine/urban flooding, heat, drought, smog, groundwater stress, irrigation pressure"],
    ["Sindh","Arid / semi-arid plains and coast","Indus, lower delta and coastal drainage","Kirthar Range","Floods, drought, heat, salinity/sea intrusion, cyclones/storm surge, water pollution"],
    ["Balochistan","Arid / highland / coastal","Hingol, Dasht, Hub, Mula and seasonal systems","Sulaiman, Kirthar, Toba Kakar, Chagai/uplands","Drought, flash floods, earthquakes, water scarcity, coastal hazards, sparse-service exposure"],
    ["Azad Jammu & Kashmir","Mountain / temperate","Jhelum, Neelum, Poonch","Himalayan and Pir Panjal systems","Earthquakes, landslides, floods, avalanches, hydropower and slope risks"],
    ["Islamabad Capital Territory","Highland / subtropical","Soan and local drainage","Margalla Hills / foothills","Urban flooding, landslides, heat, air pollution, forest fire and seismic exposure"],
], columns=["region","climate_setting","water_systems","mountain_systems","key_risk_context"])

MAJOR_CITIES = pd.DataFrame([
    ["Gilgit-Baltistan","Gilgit","Gilgit","Upper Indus","Regional administrative and service centre"],
    ["Gilgit-Baltistan","Skardu","Baltistan","Indus/upper tributaries","Tourism, services and gateway to high mountains"],
    ["Khyber Pakhtunkhwa","Peshawar","Peshawar","Kabul","Major urban/service and trade centre"],
    ["Khyber Pakhtunkhwa","Abbottabad","Hazara","Dora/Indus tributary systems","Highland urban and tourism centre"],
    ["Khyber Pakhtunkhwa","Mingora","Swat","Swat","Major Swat valley urban centre"],
    ["Punjab","Lahore","Lahore","Ravi","Major metropolitan, industrial and cultural centre"],
    ["Punjab","Faisalabad","Faisalabad","Ravi-Chenab irrigation command","Industrial/agricultural centre"],
    ["Punjab","Multan","Multan","Chenab/Indus system","Agricultural, industrial and logistics centre"],
    ["Punjab","Rawalpindi","Rawalpindi","Soan/Indus system","Major urban and service centre"],
    ["Sindh","Karachi","Karachi","Coastal drainage","Largest coastal metropolitan and port economy"],
    ["Sindh","Hyderabad","Hyderabad","Lower Indus","Urban/agricultural service centre"],
    ["Sindh","Sukkur","Sukkur","Indus","Barrage and irrigation centre"],
    ["Balochistan","Quetta","Quetta","Local basins","Provincial administrative and service centre"],
    ["Balochistan","Gwadar","Gwadar","Makran coast","Port and coastal development centre"],
    ["Azad Jammu & Kashmir","Muzaffarabad","Muzaffarabad","Jhelum/Neelum","Mountain river confluence and administrative centre"],
    ["Islamabad Capital Territory","Islamabad","Islamabad","Soan/local drainage","National capital and planned urban region"],
], columns=["region","city","district_or_area","water_context","role"])

EXTRA_LAKES = pd.DataFrame([
    ["Borith Lake","Gilgit-Baltistan","Hunza","High-altitude lake","Gojal","Wetland/birding and scenic tourism"],
    ["Naltar Lakes","Gilgit-Baltistan","Gilgit","Glacial lakes","Naltar Valley","Scenic and trekking tourism"],
    ["Rush Lake","Gilgit-Baltistan","Hunza/Nagar","High-altitude lake","Rush Peak area","High-altitude trekking"],
    ["Kachura Lakes","Gilgit-Baltistan","Skardu","Mountain lakes","Skardu","Tourism and recreation"],
    ["Blind Lake","Gilgit-Baltistan","Deosai region","High-altitude lake/wetland","Deosai","Wildlife and trekking"],
    ["Zharba Tso","Gilgit-Baltistan","Khunjerab/Hunza","High-altitude lake","Upper Hunza","Mountain tourism"],
    ["Daral Lake","Khyber Pakhtunkhwa","Swat","High-altitude lake","Upper Swat","Trekking"],
    ["Mahodand Lake","Khyber Pakhtunkhwa","Swat","Glacial lake","Utror/Kalam","Tourism and fisheries"],
    ["Kundol Lake","Khyber Pakhtunkhwa","Swat","High-altitude lake","Swat","Trekking and tourism"],
    ["Ansoo Lake","Khyber Pakhtunkhwa","Kaghan","Glacial lake","Mansehra/Kaghan","Trekking"],
    ["Pyala Lake","Khyber Pakhtunkhwa","Kaghan","Mountain lake","Kaghan","Scenic tourism"],
    ["Dudipatsar Lake","Khyber Pakhtunkhwa","Kaghan","High-altitude lake","Lulusar-Dudipatsar NP","Remote trekking"],
    ["Katora Lake","Khyber Pakhtunkhwa","Upper Dir","Glacial/high-altitude lake","Jahaz Banda","Trekking"],
    ["Saidgai Lake","Khyber Pakhtunkhwa","Swat/Dir","High-altitude lake","Upper mountain valleys","Trekking"],
    ["Keenjhar Lake","Sindh","Thatta","Freshwater lake","Thatta","Water supply, fisheries and recreation"],
    ["Drigh Lake","Sindh","Larkana","Freshwater wetland","Larkana region","Wetland and bird habitat"],
    ["Hadero Lake","Sindh","Thatta","Wetland lake","Thatta","Migratory bird habitat"],
    ["Kinjhar/Haleji wetland complex","Sindh","Thatta","Wetland system","Thatta","Waterbirds and ecological services"],
    ["Banjosa Lake","Azad Jammu & Kashmir","Poonch","Mountain reservoir/lake","Rawalakot","Tourism and recreation"],
    ["Ratti Gali Lake","Azad Jammu & Kashmir","Neelum","Glacial/high-altitude lake","Neelum Valley","Trekking and tourism"],
    ["Chitta Katha Lake","Azad Jammu & Kashmir","Neelum","High-altitude lake","Shounter region","Trekking"],
    ["Shounter Lake","Azad Jammu & Kashmir","Neelum","High-altitude lake","Upper Neelum","Trekking"],
    ["Hanna Lake","Balochistan","Quetta","Reservoir lake","Quetta","Recreation"],
    ["Zangi Nawar","Balochistan","Chagai","Salt/lake wetland","Chagai","Wetland and bird habitat"],
    ["Kallar Kahar Lake","Punjab","Chakwal","Salt/freshwater lake","Salt Range","Tourism and birding"],
    ["Jhelum/Khabbeki wetland systems","Punjab","Khushab","Wetland/lake complex","Soon Valley","Birding and recreation"],
], columns=["name","region","area","type","location","value_or_use"])

EXTRA_PARKS = pd.DataFrame([
    ["City Park Multan","Punjab","Multan","Urban recreation and green space"],
    ["Kashmir Park","Azad Jammu & Kashmir","Muzaffarabad/region","Recreation / landscape park"],
    ["DHA Multan Park","Punjab","Multan","Urban recreational green space"],
    ["Chaman Zar-e-Askari Park","Punjab","Multan","Urban recreation park"],
    ["Jinnah Park","Punjab","Rawalpindi","Urban recreation park"],
    ["Faisal Park Mumtazabad","Punjab","Multan","Urban recreation park"],
    ["Pakistan Park","Islamabad Capital Territory","Islamabad","Urban green/recreation area"],
    ["Rajana Forest Bhagat Wildlife Park","Punjab","Toba Tek Singh / Faisalabad region","Forest/wildlife recreation"],
    ["Mumtazabad/Faisal Park area","Punjab","Multan","Urban green/recreation"],
], columns=["name","region","location","focus"])

DISASTER_VULNERABILITY = pd.DataFrame([
    ["Exposure","Population pressure","Concentration of people and assets can increase consequences when hazards affect settlements."],
    ["Exposure","Diverse terrain","Mountains, plains, deserts and coasts create different hazard pathways and access constraints."],
    ["Exposure","Infrastructure deficits","Weak or aging infrastructure can increase service disruption."],
    ["Social vulnerability","Poverty and inequality","Income and asset differences affect preparedness, recovery resources and ability to relocate."],
    ["Social vulnerability","Access to education/health","Unequal access can affect warning uptake, prevention and recovery."],
    ["Social vulnerability","Mobility / spatial entrapment","Remote or constrained communities may have fewer evacuation and transport options."],
    ["Institutional vulnerability","Delayed decisions","Slow decisions can increase exposure during rapidly evolving events."],
    ["Institutional vulnerability","Coordination gaps","Overlapping responsibilities can create confusion or delayed response."],
    ["Institutional vulnerability","Trust and communication","Poor risk communication can reduce compliance with warnings."],
    ["Institutional vulnerability","Resource misallocation","Limited resources may not match the spatial pattern of risk."],
], columns=["dimension","factor","description"])

EMERGING_CLIMATE = pd.DataFrame([
    ["GLOFs","Cryosphere","Glacial lakes and changing ice/snow conditions can create downstream flood risk."],
    ["Erratic monsoons","Hydro-meteorological","Timing and intensity variability can complicate water, agriculture and flood planning."],
    ["Sea intrusion / coastal salinization","Coastal","Sea-level rise, storm surges, reduced freshwater flows and groundwater pressure can increase salinity risks."],
    ["Heatwaves","Climatological","Extreme heat can affect health, crops, water demand, power systems and urban environments."],
    ["Drought / water stress","Hydro-climatic","Low precipitation and high demand can reduce surface-water and groundwater reliability."],
    ["Compound hazards","Cross-cutting","Flood, heat, drought, landslide, pollution and infrastructure failures can interact."],
], columns=["trend_or_risk","category","description"])

SCENARIO_DETAIL = pd.DataFrame([
    ["Baseline","Near-current conditions","Observed/current exposure, infrastructure and climate variability are represented without an additional stress multiplier."],
    ["Medium","Moderate intensification","Hazard pressure and exposure increase while some adaptation and resilience improvements are assumed."],
    ["Worst-Case","High compound stress","Multiple hazards, infrastructure constraints and socioeconomic vulnerabilities coincide."],
], columns=["scenario","meaning","features"])

FOREST_TYPES = pd.DataFrame([
    ["Coniferous","Northern highlands","Deodar, pine, fir and associated species","Watershed protection, biodiversity, timber and recreation"],
    ["Juniper","Balochistan uplands","Ancient juniper woodlands","Biodiversity, soil/water conservation, heritage"],
    ["Mangrove","Sindh/Balochistan coast","Mangrove communities","Coastal protection, nursery habitat, carbon and fisheries"],
    ["Riverain / Bela","Indus floodplain","Riverain woodland","Bank stabilization, habitat and floodplain functions"],
    ["Tropical thorn / scrub","Dry plains and foothills","Kikar/jand and xeric scrub","Soil protection, grazing and dryland ecology"],
    ["Irrigated / planted","Punjab and other irrigated areas","Shisham, eucalyptus, mulberry, poplar and mixed plantations","Timber, shade, recreation and environmental services"],
], columns=["forest_type","setting","examples","functions"])

CROP_MATRIX = pd.DataFrame([
    ["Kharif","Rice","Apr/May-Oct/Nov","High water demand in irrigated systems; timing varies by agro-ecological zone"],
    ["Kharif","Cotton","Apr/May-Nov","Heat and water availability influence crop performance"],
    ["Kharif","Maize","Spring/summer","Multiple seasons/planting windows occur by region"],
    ["Kharif","Sugarcane","Long-duration","Water-intensive perennial/long-duration crop"],
    ["Kharif","Sorghum","Summer","More drought-tolerant cereal option in some dry zones"],
    ["Kharif","Millet","Summer","Adapted to drier conditions in some areas"],
    ["Rabi","Wheat","Oct-Apr","Major cool-season cereal in irrigated and rainfed systems"],
    ["Rabi","Gram / Chickpea","Oct-Mar/Apr","Important pulse, especially in rainfed areas"],
    ["Rabi","Barley","Oct-Apr","Cool-season cereal"],
    ["Rabi","Mustard / Rapeseed","Oct-Feb/Mar","Oilseed crop"],
    ["Rabi","Canola","Oct-Mar","Oilseed crop"],
    ["Rabi","Lentil","Oct-Mar","Pulse crop"],
    ["Rabi","Fodder","Cool season","Livestock feed and mixed farming"],
], columns=["season","crop","typical_window","engineering_water_note"])

APICULTURE_INDICATORS = pd.DataFrame([
    ["Colonies","count","Number of managed honey-bee colonies"],
    ["Apiaries","count","Number of apiary locations"],
    ["Honey production","tonnes/year","Harvested honey output"],
    ["Beeswax production","kg/year","Wax output where recorded"],
    ["Pollination service","ha served","Area benefiting from managed pollination"],
    ["Colony losses","%","Reported colony loss rate"],
    ["Forage availability","ha or index","Flowering/forage resource availability"],
], columns=["indicator","unit","description"])

AQUACULTURE_INDICATORS = pd.DataFrame([
    ["Pond area","ha","Water surface used for managed production"],
    ["Stocking density","fish/m² or fish/ha","Initial fish stocking intensity"],
    ["Harvest","tonnes/year","Fish or aquatic product harvested"],
    ["Survival","%","Stock survival to harvest"],
    ["Feed conversion","ratio","Feed required per unit of biomass gain"],
    ["Water temperature","°C","Water temperature relevant to species performance"],
    ["Dissolved oxygen","mg/L","Key water-quality variable"],
    ["pH","pH units","Water acidity/alkalinity indicator"],
    ["Turbidity","NTU","Water clarity/suspended matter indicator"],
    ["Ammonia","mg/L","Potentially important toxic water-quality parameter"],
], columns=["indicator","unit","description"])

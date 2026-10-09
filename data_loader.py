import pandas as pd

PROVINCES = [
    "Gilgit-Baltistan","Khyber Pakhtunkhwa","Punjab","Sindh",
    "Balochistan","Azad Jammu & Kashmir","Islamabad Capital Territory"
]

RIVERS = pd.DataFrame([
["Indus","Indus Basin","Gilgit-Baltistan; Khyber Pakhtunkhwa; Punjab; Sindh","Upper Indus system","Arabian Sea / Indus Delta","Gilgit, Kabul, Kurram, Gomal, Panjnad","Main trunk river"],
["Gilgit","Indus Basin","Gilgit-Baltistan","Upper Gilgit-Baltistan","Indus near Bunji","Indus","Upper Indus tributary"],
["Shyok","Indus Basin","Gilgit-Baltistan","Ladakh / upper basin","Indus","Indus","Major upper tributary"],
["Kabul","Indus Basin","Khyber Pakhtunkhwa","Afghanistan / Kabul basin","Indus near Attock","Indus","Major western tributary"],
["Swat","Indus Basin","Khyber Pakhtunkhwa","Upper Swat / Hindu Kush","Kabul near Charsadda","Kabul","Important KP river"],
["Kurram","Indus Basin","Khyber Pakhtunkhwa","Kurram valley","Indus system","Indus system","Western tributary"],
["Gomal","Indus Basin","Khyber Pakhtunkhwa; Balochistan","Gomal basin","Indus near DI Khan region","Indus","Cross-regional tributary"],
["Jhelum","Indus Basin","Azad Jammu & Kashmir; Punjab","Kashmir headwaters","Chenab at Trimmu","Chenab","Regulated by Mangla/Rasul system"],
["Neelum","Indus Basin","Azad Jammu & Kashmir","Upper Neelum Valley","Jhelum at Muzaffarabad","Jhelum","Important AJ&K tributary"],
["Poonch","Indus Basin","Azad Jammu & Kashmir; Punjab","Poonch region","Jhelum system","Jhelum","Transboundary basin"],
["Chenab","Indus Basin","Punjab","Upper Chenab / Jammu region","Panjnad","Jhelum at Trimmu; Panjnad","Major Punjab river"],
["Ravi","Indus Basin","Punjab","Upper Ravi / Jammu region","Chenab/Panjnad system","Chenab","Bari Doab system"],
["Sutlej","Indus Basin","Punjab","Upper Sutlej","Panjnad","Chenab","Eastern Punjab river"],
["Panjnad","Indus Basin","Punjab","Punjab river confluence system","Indus near Mithankot","Indus","Combined Punjab rivers"],
["Hub","Coastal basin","Balochistan; Sindh","Hub basin","Arabian Sea","Coastal drainage","Local water-supply basin"],
["Hingol","Coastal basin","Balochistan","Balochistan uplands","Arabian Sea","Coastal drainage","Major Balochistan coastal river"],
["Dasht","Coastal basin","Balochistan","Central Balochistan","Arabian Sea","Coastal drainage","Major Balochistan river"],
["Mula","Local basin","Balochistan","Jhal Magsi region","Lower Mula basin","Local drainage","Associated with Naulong project"],
["Gaj","Local basin","Sindh","Kirthar Range","Lower Sindh","Local drainage","Associated with Nai Gaj Dam"],
], columns=["name","river_system","province_region","upstream","downstream","confluences","notes"])

DAMS = pd.DataFrame([
["Tarbela Dam","Indus","Khyber Pakhtunkhwa","Operational","Upper Indus","Indus downstream","Storage/hydropower"],
["Diamer Basha Dam","Indus","Gilgit-Baltistan; Khyber Pakhtunkhwa","Under construction","Indus near Chilas","Indus toward Tarbela","Major storage/hydropower"],
["Dasu Hydropower Project","Indus","Khyber Pakhtunkhwa","Under construction / staged","Upper Indus","Indus downstream","Run-of-river hydropower"],
["Mohmand Dam","Swat","Khyber Pakhtunkhwa","Under construction","Swat upstream","Swat downstream","Flood/irrigation/hydropower"],
["Warsak Dam","Kabul","Khyber Pakhtunkhwa","Operational","Kabul upstream","Kabul downstream","Hydropower/irrigation"],
["Mangla Dam","Jhelum","Azad Jammu & Kashmir","Operational","Jhelum upstream","Jhelum downstream","Storage/hydropower"],
["Nai Gaj Dam","Gaj","Sindh","Project","Gaj River","Gaj downstream","Storage/irrigation"],
["Naulong Dam","Mula","Balochistan","Project","Mula River","Mula downstream","Storage/irrigation"],
], columns=["name","river","province_region","status","upstream","downstream","notes"])

BARRAGES = pd.DataFrame([
["Nowshera Headworks","Kabul","Khyber Pakhtunkhwa","Existing","Kabul upstream","Kabul downstream","Kabul system"],
["Chashma Barrage","Indus","Punjab; Khyber Pakhtunkhwa","Operational","Indus upstream","Indus downstream","CJ Link/CRBC"],
["Rasul Barrage","Jhelum","Punjab","Operational","Jhelum upstream","Jhelum downstream","Rasul-Qadirabad system"],
["Marala Headworks","Chenab","Punjab","Operational","Chenab upstream","Chenab downstream","Marala-Ravi system"],
["Khanki Barrage","Chenab","Punjab","Operational","Chenab upstream","Chenab downstream","Chenab control"],
["Qadirabad Barrage","Chenab","Punjab","Operational","Chenab upstream","Chenab downstream","Rasul-Qadirabad Link"],
["Trimmu Barrage","Chenab","Punjab","Operational","Chenab/Jhelum system","Chenab downstream","Lower Chenab control"],
["Balloki Headworks","Ravi","Punjab","Operational","Ravi upstream","Ravi downstream","Qadirabad-Balloki"],
["Sidhnai Barrage","Ravi","Punjab","Operational","Ravi upstream","Ravi downstream","Trimmu-Sidhnai"],
["Sulemanki Barrage","Sutlej","Punjab","Operational","Sutlej upstream","Sutlej downstream","Balloki-Sulemanki"],
["Islam Barrage","Sutlej","Punjab","Operational","Sutlej upstream","Sutlej downstream","Sutlej system"],
["Panjnad Barrage","Panjnad","Punjab","Operational","Punjab rivers upstream","Indus downstream","Panjnad control"],
["Taunsa Barrage","Indus","Punjab","Operational","Indus upstream","Indus downstream","Taunsa-Panjnad"],
["Guddu Barrage","Indus","Sindh","Operational","Indus upstream","Indus downstream","Sindh irrigation"],
["Sukkur Barrage","Indus","Sindh","Operational","Indus upstream","Indus downstream","Sindh irrigation"],
["Kotri Barrage","Indus","Sindh","Operational","Indus upstream","Indus Delta","Lowest major barrage"],
], columns=["name","river","province_region","status","upstream","downstream","notes"])

LINK_CANALS = pd.DataFrame([
["Chashma-Jhelum Link","Indus","Jhelum","Chashma","Jhelum/Rasul","Punjab; KP","Inter-river transfer"],
["Rasul-Qadirabad Link","Jhelum","Chenab","Rasul","Qadirabad","Punjab","Jhelum-to-Chenab"],
["Marala-Ravi Link","Chenab","Ravi","Marala","Ravi system","Punjab","Chenab-to-Ravi"],
["Qadirabad-Balloki Link","Chenab","Ravi","Qadirabad","Balloki","Punjab","Chenab-to-Ravi"],
["Balloki-Sulemanki Link","Ravi","Sutlej","Balloki","Sulemanki","Punjab","Ravi-to-Sutlej"],
["Trimmu-Sidhnai Link","Chenab","Ravi","Trimmu","Sidhnai","Punjab","Chenab-to-Ravi"],
["Taunsa-Panjnad Link","Indus","Panjnad","Taunsa","Panjnad","Punjab","Indus-to-Panjnad"],
["Upper Chenab-Balloki Link","Chenab","Ravi","Upper Chenab","Balloki","Punjab","Historic/major link"],
], columns=["name","source_river","receiving_river","offtake","outfall","province_region","notes"])

CONFLUENCES = pd.DataFrame([
["Indus + Kabul","Indus","Kabul","Attock region","Khyber Pakhtunkhwa","Kabul joins Indus"],
["Neelum + Jhelum","Neelum","Jhelum","Muzaffarabad","Azad Jammu & Kashmir","Neelum joins Jhelum"],
["Jhelum + Chenab","Jhelum","Chenab","Trimmu/Jhang region","Punjab","Jhelum joins Chenab system"],
["Sutlej + Chenab","Sutlej","Chenab","Panjnad","Punjab","Sutlej joins combined Punjab rivers"],
["Panjnad + Indus","Panjnad","Indus","Mithankot region","Punjab","Combined Punjab rivers join Indus"],
["Swat + Kabul","Swat","Kabul","Charsadda region","Khyber Pakhtunkhwa","Swat joins Kabul"],
["Gilgit + Indus","Gilgit","Indus","Bunji region","Gilgit-Baltistan","Gilgit joins upper Indus"],
], columns=["name","river_a","river_b","location","province_region","notes"])

CLIMATE_REGIONS = [
{"Region":"Temperate","Typical areas":"Upper valleys and mountain transition zones","Characteristics":"Cooler temperatures, strong seasonality"},
{"Region":"Tropical","Typical areas":"Lower plains and warmer southern/eastern zones","Characteristics":"Hot summers; monsoon influence varies"},
{"Region":"Polar / alpine","Typical areas":"Very high elevations in GB and northern ranges","Characteristics":"Persistent snow/ice and alpine conditions"},
{"Region":"Arid","Typical areas":"Balochistan, Thar/Cholistan and dry western areas","Characteristics":"Low/erratic precipitation and high water stress"},
{"Region":"Highland","Typical areas":"Karakoram, Himalaya, Hindu Kush and western ranges","Characteristics":"Strong elevation gradients and complex microclimates"},
]

MOUNTAINS = pd.DataFrame([
["Karakoram Range","Gilgit-Baltistan","K2 (8,611 m)","Hunza, Skardu, Shigar and upper Indus valleys","Glaciated high-relief terrain; metamorphic/plutonic rocks common","Advanced mountaineering; permits, acclimatization and professional logistics required","Indus, Shyok, Shigar, Gilgit","High-altitude climbing and glacier tourism"],
["Himalayas Range","GB; AJ&K; northern Punjab/KP margins","Nanga Parbat (8,126 m)","Diamer, Astore and adjacent valleys","Folded/uplifted mountain belt; major faults","Technical/high-altitude climbing; local regulations and guides important","Indus, Jhelum and tributaries","Trekking, mountaineering and scenic tourism"],
["Hindu Kush Range","KP; GB margins","Tirich Mir (7,708 m)","Chitral and upper KP","Complex uplifted sedimentary/metamorphic terrain","High-altitude mountaineering; route and seasonal planning needed","Chitral, Kunar/Kabul tributary systems","Trekking and mountaineering"],
["Hindu Raj Range","GB/KP transition","Koyo Zom (~6,877 m)","Upper Chitral and adjacent valleys","High rugged relief","Technical climbing and remote trekking","Upper Indus tributaries","Remote mountain tourism"],
["Spīn Ghar (Koh-e-Safed)","KP border region","Sikaram Sar (~4,755 m)","Kurram and Khyber surroundings","Folded sedimentary ranges","Local/seasonal access varies","Kurram/Kabul tributary system","Landscape and cultural tourism"],
["Sulaiman Mountains (Koh-e-Suleman)","Balochistan; KP; Punjab west","Takht-e-Sulaiman (~3,487 m)","Dera Ghazi Khan, Zhob and adjacent uplands","Fold-thrust belt sedimentary geology","Trekking subject to access/weather and local guidance","Gomal and local hill torrents","Mountain and cultural tourism"],
["Kirthar Range","Sindh; Balochistan","Kirthar high points ~2,000+ m","Dadu/Jamshoro and Balochistan borderlands","Folded sedimentary rocks","Trekking and protected-area visits; heat awareness","Gaj and seasonal streams","Kirthar National Park / wildlife"],
["Toba Kakar Range","Balochistan","Khojak / high points of range","Zhob, Qila Saifullah and border areas","Folded sedimentary mountain terrain","Remote trekking; check local access","Local Balochistan drainage","Landscape and cultural tourism"],
["Salt Range","Punjab","Sakesar (1,522 m)","Khushab, Chakwal, Jhelum surroundings","Salt-bearing evaporites plus sedimentary rocks","Accessible hiking/tourism; avoid unsafe quarry areas","Soan and local streams","Geology, lakes and viewpoints"],
], columns=["name","province_region","highest_peak","surrounding_areas","geology","climbing","rivers","tourism"])

LAKES = pd.DataFrame([
["Attabad Lake","Gilgit-Baltistan","Hunza","Landslide-dammed lake","Karimabad / Hunza Valley","Boating and scenic tourism; hazard awareness"],
["Satpara Lake","Gilgit-Baltistan","Skardu","Glacial/high-altitude lake","Skardu","Scenic tourism and reservoir system"],
["Sheosar Lake","Gilgit-Baltistan","Deosai","High-altitude lake","Deosai Plateau","Trekking/wildlife tourism"],
["Rama Lake","Gilgit-Baltistan","Astore","High-altitude lake","Rama Meadows","Trekking and scenery"],
["Phander Lake","Gilgit-Baltistan","Ghizer","Mountain lake","Phander Valley","Scenic tourism"],
["Saiful Muluk","Khyber Pakhtunkhwa","Kaghan","Glacial lake","Naran/Kaghan","Tourism; seasonal access"],
["Lulusar","Khyber Pakhtunkhwa","Kaghan","High-altitude lake","Lulusar Valley","Scenic tourism"],
["Dudipatsar","Khyber Pakhtunkhwa","Kaghan","High-altitude lake","Dudipatsar National Park","Remote trekking"],
["Keenjhar Lake","Sindh","Thatta","Freshwater lake/reservoir","Thatta region","Water supply, recreation and fisheries"],
["Manchar Lake","Sindh","Jamshoro/Dadu","Large freshwater lake","Indus/Manchar basin","Fisheries and wetland ecosystem"],
["Haleji Lake","Sindh","Thatta","Freshwater/wetland lake","Thatta","Bird habitat and wetland"],
["Hanna Lake","Balochistan","Quetta","Reservoir lake","Quetta","Recreation and scenic tourism"],
["Hub Dam Reservoir","Sindh; Balochistan","Karachi/Lasbela region","Reservoir","Hub basin","Water supply and recreation"],
["Kallar Kahar Lake","Punjab","Chakwal","Salt/freshwater lake","Salt Range","Tourism and wetland"],
["Uchhali Lake","Punjab","Soon Valley","Salt lake","Soon Valley","Birding and tourism"],
["Khabeki Lake","Punjab","Soon Valley","Freshwater/saline lake","Soon Valley","Birding and recreation"],
], columns=["name","province_region","area","type","location","tourism"])

FORESTS = pd.DataFrame([
["Changa Manga Forest","Punjab","Kasur / Lahore region","12,510 acres","Established as irrigated plantation in 1866; originally linked to fuelwood/timber needs","Shisham, eucalyptus, mulberry, poplar and other plantation species","Recreation, plantation forestry, wildlife park"],
["Ziarat Juniper Forest","Balochistan","Ziarat","Extensive ancient juniper landscape","Ancient natural juniper ecosystem","Juniper woodland and associated fauna","Ecotourism, trekking and heritage landscape"],
["Ushu Forest","Khyber Pakhtunkhwa","Swat/Kalam","Mountain forest","Natural/managed valley forest","Conifers","Scenery, trekking and tourism"],
["Dir Forests","Khyber Pakhtunkhwa","Upper/Lower Dir","Mountain forests","Natural and community forest landscapes","Conifers and mixed forests","Trekking, biodiversity and watershed protection"],
["Soon Valley Forests","Punjab","Khushab","Forest/scrub mosaic","Salt Range landscape","Scrub and planted vegetation","Lakes, hiking and birding"],
["Mukshpuri Forest","Khyber Pakhtunkhwa","Galiyat","Montane forest","Mountain watershed forest","Coniferous/mixed forest","Hiking and tourism"],
["Rama Meadows Forest","Gilgit-Baltistan","Astore","High-altitude forest/meadow","Upper Astore landscape","Conifers and alpine meadow","Trekking and scenic tourism"],
["Kalam Forest","Khyber Pakhtunkhwa","Swat","Montane forest","Swat valley forest landscape","Conifers and mixed forest","Tourism and watershed services"],
["Chitral Forests","Khyber Pakhtunkhwa","Chitral","Dry/montane forest mosaic","Upper Chitral mountain environment","Juniper, chilgoza and other mountain species","Biodiversity, trekking and culture"],
["Margalla Hills Scrub Forests","Islamabad Capital Territory","Islamabad","Hill scrub forest","Margalla Hills","Scrub and subtropical vegetation","Hiking, wildlife and recreation"],
], columns=["name","province_region","location","covered_area","history_origin","wildlife_nature","attractions"])

NATIONAL_PARKS = pd.DataFrame([
["Ayub National Park","Punjab","Rawalpindi","Urban recreation/green space"],
["Jallo Forest & Wildlife Park","Punjab","Lahore","Forest, wetland and recreation"],
["Lal Suhanra National Park","Punjab","Bahawalpur/Cholistan","Desert, forest and wetland ecosystem"],
["Kirthar National Park","Sindh","Jamshoro/Dadu","Mountain/desert wildlife"],
["Khunjerab National Park","Gilgit-Baltistan","Hunza/Khunjerab","High-altitude wildlife"],
["Chitral Gol National Park","Khyber Pakhtunkhwa","Chitral","Mountain wildlife"],
["Hingol National Park","Balochistan","Lasbela/Gwadar region","Coastal, desert and mountain landscapes"],
["Hazarganji-Chiltan National Park","Balochistan","Quetta","Mountain wildlife"],
["Machiara National Park","Azad Jammu & Kashmir","Neelum Valley","Mountain forest/wildlife"],
["Margalla Hills National Park","Islamabad Capital Territory","Islamabad","Subtropical hills and wildlife"],
["Pir Lasura National Park","Azad Jammu & Kashmir","Kotli/Neelum region","Mountain forest landscape"],
["Shakarparian Park","Islamabad Capital Territory","Islamabad","Urban green/recreation"],
["Lulusar-Dudipatsar National Park","Khyber Pakhtunkhwa","Kaghan","High-altitude lakes and mountains"],
], columns=["name","province_region","location","focus"])

HAZARDS = {
"Hydro-meteorological hazards":[
{"name":"Riverine floods","description":"Flooding along major rivers and floodplains; exposure depends on flow, embankments, settlements and land use.","mitigation":"Flood forecasting, zoning, embankment management and evacuation planning."},
{"name":"Flash floods / hill torrents","description":"Rapid runoff from steep catchments can affect mountain valleys and piedmont settlements.","mitigation":"Early warning, drainage, check structures and safe settlement planning."},
{"name":"Urban flooding","description":"Intense rainfall can overwhelm drainage in major cities.","mitigation":"Drainage upgrades, retention, warning and land-use controls."},
{"name":"Mudflows","description":"Rainfall-triggered debris and sediment flows can accompany flash floods and landslides.","mitigation":"Slope monitoring, hazard mapping and road protection."},
{"name":"Cloudbursts","description":"Localized extreme rainfall can generate rapid runoff and debris flows.","mitigation":"Nowcasting, local warnings and resilient infrastructure."},
{"name":"Monsoon variability","description":"Timing, duration and spatial distribution of monsoon rainfall can vary substantially.","mitigation":"Seasonal forecasting plus flexible reservoir and emergency planning."},
{"name":"Droughts","description":"Hydrological and agricultural drought can affect water supply, crops and livestock.","mitigation":"Demand management, groundwater governance and drought-resilient agriculture."},
{"name":"GLOFs","description":"Glacial lake outburst floods threaten high-mountain valleys and downstream infrastructure.","mitigation":"Remote sensing, lake monitoring, early warning and evacuation routes."},
{"name":"Heatwaves","description":"Extreme heat can affect health, water demand, crops and electricity demand.","mitigation":"Heat action plans, cooling centers, water planning and worker protection."},
{"name":"Water stress","description":"Water scarcity is amplified by variability, demand growth, groundwater depletion and infrastructure constraints.","mitigation":"Efficiency, storage, groundwater management and allocation planning."},
],
"Pakistan's tectonic setting":[
{"name":"Earthquakes","description":"Pakistan lies in an active collision zone between the Indian and Eurasian plates.","mitigation":"Seismic building codes, retrofits and emergency preparedness."},
{"name":"Landslides","description":"Steep terrain, earthquakes, rainfall and road cutting can destabilize slopes.","mitigation":"Slope stabilization, drainage and hazard mapping."},
{"name":"Avalanches","description":"Snow avalanches threaten high mountain settlements and transport corridors.","mitigation":"Forecasting, route closures and avalanche control where appropriate."},
{"name":"Tsunamis","description":"The Makran subduction zone creates a regional tsunami hazard for the Arabian Sea coast.","mitigation":"Coastal warning systems and evacuation planning."},
{"name":"Seismic activity and land shifts","description":"Fault movement can damage infrastructure and alter terrain/water systems.","mitigation":"Seismic monitoring and resilient infrastructure."},
{"name":"Snow contingencies","description":"Heavy snowfall and snowmelt can isolate communities and alter runoff timing.","mitigation":"Winter road plans, snow monitoring and emergency supplies."},
],
"Climatological & emerging hazards":[
{"name":"Accelerated glacier melt","description":"Changing temperature and snow conditions can affect glacier mass balance and runoff.","mitigation":"Cryosphere monitoring and adaptive water planning."},
{"name":"Sea-level rise and cyclones","description":"Low-lying Sindh and Balochistan coasts face storm-surge, salinity and drainage pressures.","mitigation":"Coastal zoning, mangrove conservation and warning systems."},
{"name":"Smog","description":"Urban/industrial emissions and seasonal atmospheric conditions can produce severe air-quality episodes.","mitigation":"Emission controls and public health alerts."},
{"name":"Air, water and soil pollution","description":"Industrial, municipal, agricultural and transport sources can degrade environmental quality.","mitigation":"Monitoring, treatment, enforcement and cleaner production."},
{"name":"Erratic global climate patterns","description":"Changing temperature and precipitation regimes can alter hazard timing and compound risks.","mitigation":"Climate services and scenario planning."},
],
"Anthropogenic hazards":[
{"name":"Industrial accidents / chemical spills","description":"Industrial activity can create localized hazardous releases.","mitigation":"Process safety, emergency plans and monitoring."},
{"name":"Transport and infrastructure risks","description":"Road, rail, bridge and utility failures can amplify disasters.","mitigation":"Asset inspection, redundancy and resilient design."},
{"name":"Maritime disasters / oil spills","description":"Ports and shipping lanes carry environmental and economic risks.","mitigation":"Port emergency response and spill contingency planning."},
{"name":"Fires","description":"Urban, industrial and forest fires can cause direct and cascading losses.","mitigation":"Fire codes, detection and response capacity."},
{"name":"Encroachments","description":"Settlement in floodplains, drainage corridors and hazard zones can increase exposure.","mitigation":"Land-use enforcement and risk-informed planning."},
{"name":"Food security","description":"Floods, droughts, heat and water shortages can disrupt food production and markets.","mitigation":"Diversified crops, storage and irrigation efficiency."},
{"name":"Population pressure","description":"Population growth can increase demand for water, land, energy and services.","mitigation":"Infrastructure planning and service expansion."},
{"name":"Biological hazards","description":"Outbreaks and biological contamination can affect people, livestock and water systems.","mitigation":"Surveillance, sanitation and emergency health systems."},
]}

RISK_SCENARIOS = pd.DataFrame([
["Baseline","Current/near-current hazard and exposure conditions","Existing climate variability and infrastructure deficits are retained."],
["Medium","Moderate intensification of climate and exposure pressures","Higher hazard intensity/frequency with partial adaptation."],
["Worst-Case","High compound risk and weak adaptation","Multiple hazards coincide with infrastructure and socioeconomic stress."],
], columns=["scenario","description","features"])

SOCIO_ECONOMIC = {
"Food Security":"Irrigated agriculture depends heavily on Indus Basin water availability, timing and infrastructure reliability.",
"Employment":"Agriculture, irrigation, construction, energy, transport and tourism create direct and indirect employment.",
"Urban growth":"Growing cities increase water, drainage, energy, transport and waste-management requirements.",
"Tourism":"Mountain, lake, forest, heritage and coastal destinations generate local service-sector activity but require carrying-capacity planning.",
"Domestic & industrial utility":"Dams, canals, groundwater and municipal systems support domestic, industrial and agricultural demand.",
"Climate & vulnerability":"Hazards can affect households and businesses unevenly according to location, income, infrastructure and access to services.",
"Energy generation":"Hydropower contributes renewable electricity while also linking energy planning to river flows and sediment/storage conditions."
}
AGRO_ECONOMIC = {
"Indus Basin Irrigation System (IBIS)":"Pakistan's irrigation economy is centered on the Indus Basin system; the World Bank describes it as a major groundwater and surface-water resource system.",
"Crop cultivation":"Punjab, Sindh, KP and Balochistan have different crop patterns driven by water availability, climate and soils.",
"Rural livelihoods":"Farm labor, livestock, fisheries, agricultural processing and irrigation services support rural incomes.",
"GDP & employment contribution":"Agriculture has broad economy-wide linkages through food, textiles, livestock, processing, transport and trade; current national statistics should be used for exact shares."
}
GEO_STRATEGIC = {
"Hydro-politics of Kashmir":"The Jhelum, Chenab and Indus headwaters cross or approach the Kashmir region, making water management a major bilateral and regional issue.",
"Indus Waters Treaty crisis":"Pakistan and India have disputed aspects of treaty implementation and project design. The PCA case record should be used for the current procedural/legal status.",
"Maritime trade infrastructure":"Karachi Port, Port Qasim and Gwadar connect water, energy and trade infrastructure to the Arabian Sea.",
"Punjab vs Sindh internal water dispute":"The provinces have longstanding disagreements over allocation, shortages, flows and operational interpretation. The dashboard presents these as competing claims rather than deciding them.",
"Indian Chenab projects and Punjab crops":"Pakistan has raised concerns about the effects of upstream Indian hydroelectric projects on downstream flows and agricultural planning. Specific claims should be tied to project-level evidence and treaty proceedings.",
"IRSA legal mechanisms":"The constitutional framework includes the Council of Common Interests under Article 155 for water-related complaints; disputes may also involve IRSA processes and judicial review.",
"CPEC / Diamer-Bhasha":"Diamer-Bhasha is a WAPDA project rather than one of the four CPEC hydropower projects listed in the PPIB CPEC table; the app keeps these portfolios separate."
}

CHINA_HYDRO = pd.DataFrame([
["Karot Hydropower Project",720,"River Jhelum","AJK/Punjab","Commissioned 29-Jun-2022","CPEC/PPIB project listing"],
["Suki Kinari Hydropower Station",884,"River Kunhar","Khyber Pakhtunkhwa","Commissioned 14-Sep-2024","CPEC/PPIB project listing"],
["Kohala Hydropower Project",1124,"River Jhelum","AJK","Pipeline / on hold per PPIB 30-Jun-2026 listing","Verify latest project status"],
["Azad Pattan Hydropower Project",700.7,"River Jhelum","AJK/Punjab","Pipeline / on hold per PPIB 30-Jun-2026 listing","Verify latest project status"],
], columns=["project","capacity_MW","river","location","status","note"])

IWT_TECHNICAL = pd.DataFrame([
["Pakal Dul","1,000 MW","Deep-level outlets / gated spillways; pondage and other design parameters have been discussed in the IWT dispute","Pakistan has raised objections concerning treaty interpretation and project design; exact legal conclusions belong to the treaty proceedings."],
["Ratle","850 MW","Pondage capacity, freeboard/dam elevation, gated spillways and outlet configuration have been contested","Pakistan's stated concerns should be read alongside India's position and the PCA awards/orders."],
["Court of Arbitration","N/A","PCA proceedings concern interpretation/application of IWT to specified design features of Indian projects","The PCA case page records awards/orders through 31-Aug-2026; consult the primary documents for operative holdings."],
], columns=["subject","capacity","technical_issue","description"])

SOURCES = [
{"title":"PCA — Indus Waters Western Rivers Arbitration (Pakistan v. India)","url":"https://pca-cpa.org/en/cases/284/"},
{"title":"PCA — June 2025 Supplemental Award on Competence","url":"https://pca-cpa.org/en/news/pca-press-release-pca-case-no-2023-01-proceedings-under-the-indus-waters-treaty-islamic-republic-of-pakistan-v-republic-of-india-3/"},
{"title":"PPIB — CPEC Projects, updated June 30, 2026","url":"https://www.ppib.gov.pk/cpec.html"},
{"title":"CPEC — Energy Projects","url":"https://cpec.gov.pk/energy"},
{"title":"CPEC — Karot","url":"https://cpec.gov.pk/project-details/16"},
{"title":"CPEC — Suki Kinari","url":"https://cpec.gov.pk/project-details/15"},
{"title":"CPEC — Kohala","url":"https://www.cpec.gov.pk/project-details/23"},
{"title":"CPEC — Azad Pattan","url":"https://cpec.gov.pk/project-details/91"},
{"title":"WAPDA — Diamer Basha Dam","url":"https://wapda.gov.pk/diamer-basha-dam-project/"},
{"title":"Ministry of Economic Affairs — Diamer Basha clarification, 29 Aug 2026","url":"https://www.ead.gov.pk/NewsDetail/ODI1M2E0ODYtMjkyMi00NzdkLWE2ODQtMDk5NWIwZGY4YmE1"},
{"title":"CCI — Functions / Article 155","url":"https://www.cci.gov.pk/Detail/NDZhY2I2ZDUtZTgzNy00MWEzLWE2M2ItZjU2NTkyODc4ZGJm"},
{"title":"World Bank — Indus Basin groundwater / IBIS","url":"https://www.worldbank.org/en/news/feature/2021/03/25/managing-groundwater-resources-in-pakistan-indus-basin"},
{"title":"NDMA — National Disaster Risk Situation","url":"https://ndma.gov.pk/storage/publications/July2024/Oz8OdDFNwuGLBFHr2u27.pdf"},
{"title":"NDMA — Hazard Projections / early warnings","url":"https://ndma.gov.pk/projection-impact-list_new"},
{"title":"Punjab Forest Department — Changa Manga Plantation","url":"https://fw.punjab.gov.pk/changa_manga_plantation"},
{"title":"Punjab Forest Department — Irrigated Plantations","url":"https://fw.punjab.gov.pk/irrigated_plantations"},
{"title":"Punjab Forest Department — Lal Suhanra National Park","url":"https://fw.punjab.gov.pk/lal_suhanera_forest_park"},
{"title":"Punjab Forest Department — Jallo Forest and Wildlife Park","url":"https://fw.punjab.gov.pk/jallo_forest_wildlife_park"},
{"title":"2025 Talidas GLOF remote-sensing study","url":"https://www.mdpi.com/2072-4292/18/9/1329"},
]

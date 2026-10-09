# IndusSphere Pakistan — Integrated Water, Climate & Strategic Intelligence Explorer

**Creator:** Engr. Syed Hassan Iqbal Shah

A reference-style Streamlit dashboard for Pakistan's provinces/territories, rivers, dams, barrages, link canals, lakes, deserts, climate regions, mountain systems, forests, parks, disaster-risk context, socio-economic/agro-economic analysis, hydropower portfolios, IWT research, ESG/ISO/SDG/MDG/Vision 2030 alignment, and input-driven analytics.

## Provinces / territories
- Gilgit-Baltistan
- Khyber Pakhtunkhwa (KPK/KP)
- Punjab
- Sindh
- Balochistan
- Azad Jammu & Kashmir
- Islamabad Capital Territory (ICT)

## Main modules
- Water and terrain inventory: rivers, upstream/downstream relationships, confluences, dams, barrages/headworks, link canals, lakes and deserts.
- Climate regions: Temperate, Tropical, Polar, Arid and Highland.
- Mountain ranges: Northern Highlands (Karakoram, Himalayas, Hindu Kush, Hindu Raj) and Western/Southern Border Ranges (Spīn Ghar/Koh-e-Safed, Sulaiman, Kirthar, Toba Kakar, Salt Range), with peaks, geology, tourism and rivers.
- Disaster-risk context: hydro-meteorological, tectonic, climatological/emerging, anthropogenic, exposure/vulnerability and scenario definitions.
- Socio-economic: food security, employment, urban growth, tourism, domestic/industrial utility, climate vulnerability and energy generation.
- Agro-economic: IBIS, Rabi/Kharif crop seasons, crop types, apiculture, aquaculture and editable regional data.
- Geo-political/strategic: Kashmir hydro-politics, Punjab-Sindh water disputes, IRSA/CCI/Article 155, maritime trade, CPEC hydropower and Indian upstream project/IWT research.
- China hydropower: Karot, Suki Kinari, Kohala and Azad Pattan project portfolio.
- India upstream/IWT: Pakal Dul, Ratle, technical issues, Head Marala/crop-impact documentation and PCA timeline.
- IWT legal/data exchange: Article VI/VIII/IX baseline, exchange audit, timeline, evidence and descriptive dispute-resolution pathways.
- Forests and parks: forest types, notable forests, national/protected/recreational areas, and representative-location park maps in the **Select a park for details** tab.
- ESG / ISO / UN SDGs / MDGs / Vision 2030 crosswalk.
- Engineering simulation engines: hydrology, flood, crop-water, climate, Monte Carlo and network routing.
- File analytics: CSV, PDF, XLSX and XLS; selectable-text/table PDFs plus OCR pathway for scanned PDFs.
- Graphs: bar, pie, scatter and line charts from actual uploaded or edited data.
- River-basin telemetry: average variance by basin and downloadable Python visualization script.
- Water quality: dissolved oxygen (DO), pH, turbidity, TDS, conductivity, temperature, nitrate, BOD, COD and coliform when present in uploaded data.
- Spatial uploads: CSV/PDF/Excel data can be mapped when latitude/longitude fields are present.
- Indus Delta environmental analytics reference: EMI survey, interpolated EC, pH, ESP and soil salinity.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

Windows helper: `run_app.bat`

## Streamlit Community Cloud
Use `app.py` as the main file and keep `requirements.txt` and `packages.txt` in the repository root. `packages.txt` includes the system dependency used by the OCR pathway.

## Important data/legal note
The application distinguishes source-derived facts, party positions, reported concerns, model calculations and uploaded evidence. In particular, IWT and Indian-project sections do not automatically determine legal violations or causation. Use the current treaty text, PCA awards/orders, authoritative project documents and hydrological datasets for formal analysis.

Map points are representative visualization coordinates unless a source explicitly provides a boundary. They are not cadastral or engineering survey data.

## Streamlit Community Cloud deployment checklist

1. Upload the **contents** of this folder to the root of a GitHub repository.
2. Confirm that `app.py`, `requirements.txt`, `packages.txt`, `runtime.txt`, and `.streamlit/config.toml` are in the repository root.
3. In Streamlit Community Cloud, choose **Deploy an app**, select the repository and branch, and set the main file to `app.py`.
4. Wait for dependency installation. The first build may take longer because PDF/OCR dependencies are installed.
5. If you do not need scanned-PDF OCR, you may remove `pytesseract`, `Pillow`, `PyMuPDF`, and `packages.txt`; CSV, XLSX, XLS, and selectable-text PDF workflows will still be available.

### Troubleshooting

- **ModuleNotFoundError:** verify that every `.py` file is in the same repository root as `app.py`.
- **Excel upload error:** keep both `openpyxl` and `xlrd` in `requirements.txt` for `.xlsx` and legacy `.xls` support.
- **Scanned PDF OCR warning:** confirm that `packages.txt` contains `tesseract-ocr`; OCR is a fallback and may be slower than normal text extraction.
- **Large upload rejected:** the included Streamlit configuration allows uploads up to 200 MB, subject to the hosting platform's own limits.
- **Slow first load:** Streamlit installs dependencies during the first deployment; subsequent runs should be faster.

The models are screening/educational tools. Validate engineering, legal, environmental, and statistical conclusions against authoritative data before professional use.

## Expanded simulation and agro-economic modules

The Streamlit-ready package now includes additional executable Python modules:

- `hydrology_engine.py` — reservoir and water-balance screening
- `flood_engine.py` — rainfall/runoff and flood-capacity screening
- `crop_water_engine.py` — Rabi/Kharif crop-water requirements
- `climate_engine.py` — climate scenario/sensitivity screening
- `monte_carlo_engine.py` — uncertainty simulation
- `network_engine.py` — river/canal network routing
- `additional_simulation_engines.py` — groundwater, drought, sediment, water-quality, irrigation and socio-agro projection engines
- `iwt_compliance_engine.py` — IWT data-exchange documentation screening
- `iwt_timeline_engine.py` — documented PCA/IWT timeline
- `iwt_evidence_engine.py` — evidence ledger
- `iwt_scenario_engine.py` — IWT scenario matrix
- `simulation_registry.py` — central executable-engine catalog

The Agro-Economic domain now contains explicit Rabi/Kharif tables with the requested fields `season`, `crop`, `typical_window`, and `engineering_water_note`, plus structured Apiculture and Aquaculture indicator tables.

The Socio-Economic and Agro-Economic domains share an editable input table with province/region, cultivated area, crop production, employment, honey production and aquaculture production. Users can choose Bar, Pie, Scatter or Line charts and the requested metric fields. A separate projection engine responds to the entered data and annual change assumption.

The Parks Details tab shows an interactive representative-location map with a highlighted selected-park marker.

### Streamlit deployment note

`requirements.txt` explicitly includes NumPy because the Monte Carlo engine uses it. `runtime.txt`, `packages.txt`, and `.streamlit/config.toml` are included for Streamlit Community Cloud deployment.

## WAPDA telecommunication network integration

This release adds `telecommunication.py` and `telecom_network_engine.py` plus the two supplied WAPDA PDF source documents under `source_documents/`.

The app includes a new **📡 WAPDA Telecommunication Networks** section covering:
- High Frequency Radio Network — Western Rivers
- Wireless Network — Eastern Rivers
- source-document traceability and CSV exports
- visualization-only approximate map points where a named location could be mapped; these coordinates are explicitly not claimed to come from the PDFs

The supplied diagrams list network locations but do not define GIS coordinates or an explicit link topology, so the application does not invent network connections.


## Pakistan Solar Projects
The application now includes a dedicated `☀️ Pakistan Solar Projects` section and a solar layer on the interactive Pakistan map. The dataset covers Punjab, Sindh, Khyber Pakhtunkhwa, Balochistan, Gilgit-Baltistan, Azad Jammu & Kashmir and Islamabad Capital Territory. It distinguishes utility-scale PV, institutional/public-sector solarization, agricultural solarization, mini-grids and solar-home-system programs. Capacity is source-derived where published; otherwise it is intentionally left unspecified.

## Solar Map Label-Overlap Fix (2026-10-05)

The Pakistan solar map now uses a collision-safe label strategy for all seven represented administrative regions (Punjab, Sindh, Khyber Pakhtunkhwa, Balochistan, Gilgit-Baltistan, Azad Jammu & Kashmir, and Islamabad Capital Territory).

- All solar projects remain visible as markers.
- Project names are available on hover instead of being printed over every marker.
- A single project can be selected for a permanent highlighted label.
- The dedicated solar page includes province/region, status, and solar-type filters.
- No project names are inferred or repositioned; the source inventory remains unchanged.

## Simulated Live Weather, Rainfall & 12-Month Telemetry

The project now includes `weather_hydraulic.py` and `telemetry_engine.py` for transparent synthetic screening at:
- Sialkot — Chenab basin
- Jhelum — Jhelum basin
- Lahore — Ravi basin

The module provides simulated current weather/rainfall, river discharge, water level, hydraulic hazard screening and 12 monthly telemetry observations. These values are explicitly synthetic and are not operational observations or flood warnings.

## 🛰️ SEBAL Evapotranspiration — Indus Basin

The project now includes a Google Earth Engine + geemap + GeoPandas evapotranspiration workspace based on the **Surface Energy Balance Algorithm for Land (SEBAL)**.

### Workflow

1. Authenticate and initialize Google Earth Engine.
2. Identify the Indus main basin chain from **WWF HydroSHEDS Level 7** using the Indus outlet point.
3. Inspect the basin geometry locally with **GeoPandas**.
4. Query **Landsat 8/9 Collection 2 Level 2** surface reflectance and land-surface temperature.
5. Query **ERA5-Land hourly** radiation, air temperature and wind fields.
6. Estimate albedo, NDVI, emissivity, net radiation, soil heat flux, sensible heat flux, latent heat flux and instantaneous ET rate.
7. Visualize ET, land-surface temperature, NDVI and the basin boundary through **geemap**.
8. Export basin-level statistics as CSV.

### Important scientific note

This is a transparent **SEBAL-style research implementation** for the Indus Basin. It is not represented as a locally calibrated or independently validated operational SEBAL product. Hot/cold pixel selection, aerodynamic resistance, emissivity and atmospheric inputs should be validated against appropriate Pakistan/Indus Basin observations before use for operational irrigation scheduling, water accounting or engineering decisions.

The official Earth Engine catalog contains OpenET **geeSEBAL**, an Earth Engine implementation of SEBAL, but the catalogued OpenET geeSEBAL products are CONUS-focused. Therefore this project does not incorrectly apply the CONUS asset to Pakistan; instead it computes the energy balance directly over the Indus Basin using globally available Landsat and ERA5-Land inputs.

### Authentication

For local development/Colab, authenticate Earth Engine once with the Earth Engine Python client and initialize it with a Google Cloud project. For deployed applications, use an appropriate secure Google Cloud/Earth Engine credential mechanism and never commit private keys to the repository.

### Upload CSV/Excel analytics in the SEBAL page (added 2026-10-09)

The SEBAL page now has two independent parts:

**A. Upload data — charts, analytics and coordinate map**
- Upload CSV, XLSX or XLS files without authenticating Earth Engine.
- Select one file or combine multiple uploads into a single table (a `source_file` field is added to help track records).
- Build interactive bar charts (sum/mean/count), pie charts, scatter plots and line charts from the uploaded columns.
- If latitude/longitude fields are detected (including common `lat`/`lon`, `latitude`/`longitude`, `lng`, decimal-coordinate and `x`/`y` aliases), the page displays an interactive map and allows download of valid mapped rows.
- Invalid or missing coordinates are excluded from the map, not deleted from the original dataset.
- Download the analysed table as CSV.

**B. Satellite-based SEBAL model (Google Earth Engine)**
- Requires a registered Earth Engine project and authorized credentials.
- Select single-scene or monthly composite processing, then run the Landsat/ERA5-Land energy-balance workflow.
- Uploaded data analytics do not automatically calculate ET. They visualize the fields present in the file; satellite SEBAL ET is computed by the authenticated GEE workflow.

`sample_sebal_upload.csv` is an illustrative template for field names and map/chart behaviour. Its values are examples for interface testing, not observed or validated evapotranspiration measurements.

### Indus Waters Treaty reference modules
The sidebar now includes six additional reference pages: **1960 Dam Design**, **Western Rivers Pakistan**, **IWT Main points**, **Impact on Transboundary Water Cooperation**, **The IWT Treaty**, and **Article XII(3) Modification by Consent**. These pages summarize the Treaty and relevant engineering/cooperation concepts in neutral language, provide primary-source links, and include the user-supplied Article XII(3) infographic on the matching page. Legal positions are attributed rather than presented as dashboard adjudications.

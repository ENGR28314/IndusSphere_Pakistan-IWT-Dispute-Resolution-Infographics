"""Google Earth Engine + geemap + GeoPandas SEBAL evapotranspiration workspace.

This module provides a transparent, basin-scale SEBAL-style implementation for the
Indus Basin. It uses Landsat 8/9 Collection 2 Level-2 surface reflectance/LST,
ERA5-Land meteorological/radiation fields, and HydroSHEDS basin geometry.

Important: this is an operational screening implementation of the SEBAL energy
balance, not a claim of validation against local flux towers or irrigation records.
The official OpenET geeSEBAL asset is a SEBAL implementation, but the catalogued
OpenET geeSEBAL monthly products are CONUS-focused; therefore the Indus Basin
workflow below computes the energy balance directly in Earth Engine rather than
attempting to use the CONUS-only OpenET asset for Pakistan.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, Tuple

import pandas as pd

EE_AVAILABLE = True
EE_IMPORT_ERROR = None
try:
    import ee
except Exception as exc:  # pragma: no cover
    EE_AVAILABLE = False
    EE_IMPORT_ERROR = exc

try:
    import geemap
    import geemap.foliumap as geemap_folium
except Exception as exc:  # pragma: no cover
    geemap = None
    geemap_folium = None
    GEEMAP_IMPORT_ERROR = exc
else:
    GEEMAP_IMPORT_ERROR = None

try:
    import geopandas as gpd
except Exception as exc:  # pragma: no cover
    gpd = None
    GEOPANDAS_IMPORT_ERROR = exc
else:
    GEOPANDAS_IMPORT_ERROR = None


HYDROSHEDS_7 = "WWF/HydroSHEDS/v1/Basins/hybas_7"
LANDSAT8 = "LANDSAT/LC08/C02/T1_L2"
LANDSAT9 = "LANDSAT/LC09/C02/T1_L2"
ERA5_LAND = "ECMWF/ERA5_LAND/HOURLY"

# Indus Delta outlet used only to identify the HydroSHEDS MAIN_BAS chain.
DEFAULT_OUTLET = (67.80, 24.10)  # lon, lat

# Landsat Collection 2 scale/offsets.
SR_SCALE = 0.0000275
SR_OFFSET = -0.2
ST_SCALE = 0.00341802
ST_OFFSET = 149.0


def earth_engine_status() -> Tuple[bool, str]:
    """Return whether the Earth Engine Python client is importable."""
    if not EE_AVAILABLE:
        return False, f"earthengine-api is unavailable: {EE_IMPORT_ERROR}"
    return True, "Earth Engine Python client is available."


def initialize_ee(project_id: Optional[str] = None, service_account: Optional[str] = None, private_key_json: Optional[str] = None) -> str:
    """Initialize Earth Engine using local credentials or a service-account key.

    Local/Colab: run ``ee.Authenticate()`` once, then initialize.
    Streamlit: keep service-account JSON in Streamlit Secrets or another secure
    secret store; never commit the private key to GitHub.
    """
    if not EE_AVAILABLE:
        raise RuntimeError(f"earthengine-api is unavailable: {EE_IMPORT_ERROR}")
    if service_account and private_key_json:
        import json
        from google.oauth2 import service_account as google_service_account
        key = json.loads(private_key_json) if isinstance(private_key_json, str) else private_key_json
        credentials = google_service_account.Credentials.from_service_account_info(
            key, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        ee.Initialize(credentials=credentials, project=project_id)
    elif project_id:
        ee.Initialize(project=project_id)
    else:
        ee.Initialize()
    return "Earth Engine initialized successfully."


def _basin_from_outlet(outlet_lon: float, outlet_lat: float):
    """Find the HydroSHEDS level-7 main basin draining through the outlet."""
    basins = ee.FeatureCollection(HYDROSHEDS_7)
    outlet = ee.Geometry.Point([float(outlet_lon), float(outlet_lat)])
    hit = basins.filterBounds(outlet).sort("SUB_AREA", False).first()
    main_bas = hit.get("MAIN_BAS").getInfo()
    if main_bas is None:
        raise ValueError("No HydroSHEDS basin was found at the selected outlet.")
    selected = basins.filter(ee.Filter.eq("MAIN_BAS", main_bas))
    return selected, int(main_bas)


def indus_basin_ee(outlet_lon: float = DEFAULT_OUTLET[0], outlet_lat: float = DEFAULT_OUTLET[1]):
    """Return an EE FeatureCollection representing the Indus main basin chain."""
    return _basin_from_outlet(outlet_lon, outlet_lat)[0]


def indus_basin_geodataframe(outlet_lon: float = DEFAULT_OUTLET[0], outlet_lat: float = DEFAULT_OUTLET[1]):
    """Convert the HydroSHEDS-derived Indus basin to a GeoDataFrame.

    A simplified geometry is used for the local GeoPandas representation to keep
    Streamlit requests manageable. The Earth Engine geometry remains the analysis
    geometry used for raster computation.
    """
    if gpd is None:
        raise RuntimeError(f"geopandas is unavailable: {GEOPANDAS_IMPORT_ERROR}")
    fc, main_bas = _basin_from_outlet(outlet_lon, outlet_lat)
    # Simplify only the local representation; retain full EE geometry for analysis.
    geom = fc.geometry(maxError=1000).simplify(1000).getInfo()
    gdf = gpd.GeoDataFrame.from_features(
        [{"type": "Feature", "geometry": geom, "properties": {"main_bas": main_bas}}],
        crs="EPSG:4326",
    )
    gdf["area_km2"] = gdf.to_crs(6933).geometry.area / 1_000_000.0
    return gdf


def _mask_landsat(img):
    qa = img.select("QA_PIXEL")
    # Fill, dilated cloud, cirrus, cloud and cloud-shadow bits.
    mask = (
        qa.bitwiseAnd(1 << 0).eq(0)
        .And(qa.bitwiseAnd(1 << 1).eq(0))
        .And(qa.bitwiseAnd(1 << 2).eq(0))
        .And(qa.bitwiseAnd(1 << 3).eq(0))
        .And(qa.bitwiseAnd(1 << 4).eq(0))
    )
    return img.updateMask(mask)


def _prepare_landsat(img):
    img = _mask_landsat(img)
    sr = img.select(["SR_B2", "SR_B3", "SR_B4", "SR_B5", "SR_B6", "SR_B7"]).multiply(SR_SCALE).add(SR_OFFSET)
    thermal = img.select("ST_B10").multiply(ST_SCALE).add(ST_OFFSET).rename("ts_k")
    out = sr.addBands(thermal)
    ndvi = out.normalizedDifference(["SR_B5", "SR_B4"]).rename("ndvi")
    # Broadband albedo approximation for Landsat 8/9 surface reflectance.
    albedo = out.expression(
        "0.356*b2 + 0.130*b4 + 0.373*b5 + 0.085*b6 + 0.072*b7 - 0.0018",
        {
            "b2": out.select("SR_B2"),
            "b4": out.select("SR_B4"),
            "b5": out.select("SR_B5"),
            "b6": out.select("SR_B6"),
            "b7": out.select("SR_B7"),
        },
    ).rename("albedo").clamp(0.02, 0.60)
    # Broadband emissivity proxy from NDVI. This is intentionally explicit so users
    # can replace it with a locally calibrated emissivity product.
    emissivity = ndvi.expression(
        "ndvi > 0.2 ? 0.985 : 0.97 + 0.01 * ndvi",
        {"ndvi": ndvi},
    ).rename("emissivity").clamp(0.95, 0.99)
    return out.addBands([ndvi, albedo, emissivity])


def _nearest_era5(image_date: ee.Date, region):
    """Get an ERA5-Land hourly image near the Landsat acquisition time."""
    center = image_date
    era = (
        ee.ImageCollection(ERA5_LAND)
        .filterDate(center.advance(-2, "hour"), center.advance(3, "hour"))
        .filterBounds(region)
        .sort("system:time_start")
    )
    return ee.Image(era.first())


def _percentile(image, band, region, low=5, high=95, scale=1000):
    return image.select(band).reduceRegion(
        reducer=ee.Reducer.percentile([low, high]),
        geometry=region,
        scale=scale,
        bestEffort=True,
        maxPixels=1e8,
    )


def sebal_image(
    start_date: str,
    end_date: Optional[str] = None,
    outlet_lon: float = DEFAULT_OUTLET[0],
    outlet_lat: float = DEFAULT_OUTLET[1],
    max_cloud_pct: float = 20,
):
    """Build a SEBAL energy-balance image for the best Landsat scene.

    Outputs bands including NDVI, albedo, land-surface temperature, net radiation,
    soil heat flux, sensible heat flux, latent heat flux and instantaneous ET rate.
    The H calculation uses image-derived hot/cold thermal anchors and an explicit
    aerodynamic-resistance approximation; this is intended for screening and
    research prototyping and requires local validation before operational use.
    """
    if not EE_AVAILABLE:
        raise RuntimeError(f"earthengine-api is unavailable: {EE_IMPORT_ERROR}")

    basin_fc, main_bas = _basin_from_outlet(outlet_lon, outlet_lat)
    region = basin_fc.geometry()
    end_date = end_date or (datetime.fromisoformat(start_date) + timedelta(days=1)).strftime("%Y-%m-%d")

    collection = (
        ee.ImageCollection(LANDSAT8)
        .merge(ee.ImageCollection(LANDSAT9))
        .filterDate(start_date, end_date)
        .filterBounds(region)
        .filter(ee.Filter.lte("CLOUD_COVER", float(max_cloud_pct)))
        .sort("CLOUD_COVER")
    )
    count = collection.size().getInfo()
    if not count:
        raise ValueError("No Landsat 8/9 scene matched the date, basin and cloud filter.")

    raw = ee.Image(collection.first())
    img = _prepare_landsat(raw)
    image_date = ee.Date(raw.get("system:time_start"))
    era = _nearest_era5(image_date, region)

    # ERA5-Land hourly variables are J/m2. Convert the hourly values to W/m2.
    rs = era.select("surface_solar_radiation_downwards_hourly").divide(3600).max(0).rename("rs_down_wm2")
    rld = era.select("surface_thermal_radiation_downwards_hourly").divide(3600).max(0).rename("rld_wm2")
    # ERA5-Land 2 m temperature is Kelvin; use it as the atmospheric reference.
    ta = era.select("temperature_2m").rename("ta_k")
    wind = era.select("u_component_of_wind_10m").hypot(era.select("v_component_of_wind_10m")).max(0.5).rename("wind_10m_ms")

    ts = img.select("ts_k")
    alpha = img.select("albedo")
    eps = img.select("emissivity")

    sigma = 5.670374419e-8
    # Upward longwave radiation and net radiation.
    rlu = eps.multiply(sigma).multiply(ts.pow(4)).rename("rlu_wm2")
    rn = rs.multiply(ee.Image(1).subtract(alpha)).add(rld).subtract(rlu).rename("rn_wm2")

    # Soil heat flux ratio: vegetation-dependent approximation used in many
    # SEBAL implementations; exposed as a clear, replaceable term.
    g_ratio = img.select("ndvi").expression(
        "ndvi < 0 ? 0.35 : 0.05 + 0.18 * exp(-0.521 * ndvi)",
        {"ndvi": img.select("ndvi")},
    ).clamp(0.03, 0.35)
    g = rn.multiply(g_ratio).rename("g_wm2")

    available = rn.subtract(g).max(0).rename("available_energy_wm2")

    # Hot/cold thermal anchors. Pixels are constrained by NDVI to reduce the
    # chance that water, snow or cloud-edge pixels become calibration anchors.
    ts_pct = _percentile(img, "ts_k", region, 5, 95, 1000)
    ndvi_p = _percentile(img, "ndvi", region, 10, 90, 1000)
    ts_low = ee.Number(ts_pct.get("ts_k_p5"))
    ts_high = ee.Number(ts_pct.get("ts_k_p95"))
    ndvi_low = ee.Number(ndvi_p.get("ndvi_p10"))
    ndvi_high = ee.Number(ndvi_p.get("ndvi_p90"))

    cold_mask = img.select("ndvi").gte(ndvi_high).And(ts.lte(ts_low.add(2)))
    hot_mask = img.select("ndvi").lte(ndvi_low).And(ts.gte(ts_high.subtract(2)))

    cold_ts = ts.updateMask(cold_mask).reduceRegion(ee.Reducer.mean(), region, 1000, bestEffort=True, maxPixels=1e8).get("ts_k")
    hot_ts = ts.updateMask(hot_mask).reduceRegion(ee.Reducer.mean(), region, 1000, bestEffort=True, maxPixels=1e8).get("ts_k")
    cold_ts = ee.Number(ee.Algorithms.If(cold_ts, cold_ts, ts_low))
    hot_ts = ee.Number(ee.Algorithms.If(hot_ts, hot_ts, ts_high))

    # Approximate aerodynamic resistance from wind and NDVI-dependent roughness.
    z0 = img.select("ndvi").multiply(0.3).add(0.01).clamp(0.01, 0.5)
    rah = ee.Image(ee.Number(110)).divide(wind).multiply(z0.add(0.05).divide(0.15)).clamp(20, 300).rename("rah_s_m")
    rho = ee.Image(1.225)
    cp = 1004.0

    # SEBAL-style hot/cold thermal anchor. Cold pixels approach H≈0 and hot
    # pixels approach H≈available energy; the image-derived thermal gradient
    # interpolates H between those anchors. The aerodynamic resistance is used
    # explicitly to keep the sensible-heat calculation physically interpretable.
    ta_ref = ta
    dT_cold = cold_ts.subtract(ta_ref)
    dT_hot = hot_ts.subtract(ta_ref)
    dT = dT_cold.add(ts.subtract(cold_ts).divide(hot_ts.subtract(cold_ts).max(0.5)).clamp(0, 1).multiply(dT_hot.subtract(dT_cold)))
    h = rho.multiply(cp).multiply(dT).divide(rah).max(0).min(available).rename("h_wm2")
    le = available.subtract(h).max(0).rename("le_wm2")

    # Penman-style conversion from latent heat flux to instantaneous ET rate.
    lambda_jkg = ee.Image(2.501e6).subtract(ts.subtract(273.15).multiply(2361)).max(2.2e6)
    et_mm_h = le.multiply(3600).divide(lambda_jkg).rename("et_mm_h")

    result = (
        img.select(["ndvi", "albedo", "ts_k", "emissivity"])
        .addBands([rs, rld, rlu, rn, g, available, h, le, et_mm_h, ta, wind, rah])
        .set({
            "system:time_start": raw.get("system:time_start"),
            "landsat_id": raw.get("LANDSAT_PRODUCT_ID"),
            "cloud_cover": raw.get("CLOUD_COVER"),
            "hydrosheds_main_bas": main_bas,
            "sebal_method": "Indus Basin SEBAL-style energy balance with Landsat hot/cold thermal anchors",
        })
    )
    return result, basin_fc, raw


def monthly_sebal(
    year: int,
    month: int,
    outlet_lon: float = DEFAULT_OUTLET[0],
    outlet_lat: float = DEFAULT_OUTLET[1],
    max_cloud_pct: float = 30,
):
    """Create a monthly median composite of SEBAL instantaneous ET rate."""
    start = f"{int(year):04d}-{int(month):02d}-01"
    if month == 12:
        end = f"{year + 1:04d}-01-01"
    else:
        end = f"{year:04d}-{month + 1:02d}-01"

    basin_fc, main_bas = _basin_from_outlet(outlet_lon, outlet_lat)
    region = basin_fc.geometry()
    col = (
        ee.ImageCollection(LANDSAT8)
        .merge(ee.ImageCollection(LANDSAT9))
        .filterDate(start, end)
        .filterBounds(region)
        .filter(ee.Filter.lte("CLOUD_COVER", float(max_cloud_pct)))
        .sort("CLOUD_COVER")
    )
    count = col.size().getInfo()
    if count == 0:
        raise ValueError(f"No Landsat scenes available for {start}–{end} at the selected cloud threshold.")

    # Map the single-scene SEBAL computation across available scenes.
    def per_image(raw):
        img = _prepare_landsat(ee.Image(raw))
        date = ee.Date(raw.get("system:time_start"))
        era = _nearest_era5(date, region)
        rs = era.select("surface_solar_radiation_downwards_hourly").divide(3600).max(0)
        rld = era.select("surface_thermal_radiation_downwards_hourly").divide(3600).max(0)
        ta = era.select("temperature_2m")
        wind = era.select("u_component_of_wind_10m").hypot(era.select("v_component_of_wind_10m")).max(0.5)
        ts = img.select("ts_k")
        alpha = img.select("albedo")
        eps = img.select("emissivity")
        sigma = 5.670374419e-8
        rlu = eps.multiply(sigma).multiply(ts.pow(4))
        rn = rs.multiply(ee.Image(1).subtract(alpha)).add(rld).subtract(rlu)
        g_ratio = img.select("ndvi").expression(
            "ndvi < 0 ? 0.35 : 0.05 + 0.18 * exp(-0.521 * ndvi)", {"ndvi": img.select("ndvi")}
        ).clamp(0.03, 0.35)
        g = rn.multiply(g_ratio)
        available = rn.subtract(g).max(0)
        pct = _percentile(img, "ts_k", region, 5, 95, 1000)
        npct = _percentile(img, "ndvi", region, 10, 90, 1000)
        low = ee.Number(pct.get("ts_k_p5")); high = ee.Number(pct.get("ts_k_p95"))
        ndlow = ee.Number(npct.get("ndvi_p10")); ndhigh = ee.Number(npct.get("ndvi_p90"))
        cold = ts.updateMask(img.select("ndvi").gte(ndhigh).And(ts.lte(low.add(2)))).reduceRegion(ee.Reducer.mean(), region, 1000, bestEffort=True, maxPixels=1e8).get("ts_k")
        hot = ts.updateMask(img.select("ndvi").lte(ndlow).And(ts.gte(high.subtract(2)))).reduceRegion(ee.Reducer.mean(), region, 1000, bestEffort=True, maxPixels=1e8).get("ts_k")
        cold = ee.Number(ee.Algorithms.If(cold, cold, low)); hot = ee.Number(ee.Algorithms.If(hot, hot, high))
        z0 = img.select("ndvi").multiply(0.3).add(0.01).clamp(0.01, 0.5)
        rah = ee.Image(ee.Number(110)).divide(wind).multiply(z0.add(0.05).divide(0.15)).clamp(20, 300)
        dT_cold = cold.subtract(ta)
        dT_hot = hot.subtract(ta)
        dT = dT_cold.add(ts.subtract(cold).divide(hot.subtract(cold).max(0.5)).clamp(0, 1).multiply(dT_hot.subtract(dT_cold)))
        h = ee.Image(1.225).multiply(1004.0).multiply(dT).divide(rah).max(0).min(available)
        le = available.subtract(h).max(0)
        lam = ee.Image(2.501e6).subtract(ts.subtract(273.15).multiply(2361)).max(2.2e6)
        et = le.multiply(3600).divide(lam).rename("et_mm_h")
        return et.addBands([img.select("ndvi"), img.select("albedo"), ts, rn.rename("rn_wm2"), g.rename("g_wm2"), le.rename("le_wm2"), ta.rename("ta_k"), wind.rename("wind_10m_ms")]).set("system:time_start", raw.get("system:time_start"))

    result = ee.ImageCollection(col.map(per_image)).median().set({
        "year": int(year), "month": int(month), "hydrosheds_main_bas": main_bas,
        "scene_count": int(count), "sebal_method": "Monthly median of Landsat/ERA5-Land SEBAL-style estimates"
    })
    return result, basin_fc, int(count)


def zonal_statistics(image, basin_fc, scale: int = 1000) -> pd.DataFrame:
    """Return basin-level mean/min/max for selected SEBAL bands."""
    bands = [b for b in ["et_mm_h", "rn_wm2", "g_wm2", "le_wm2", "ts_k", "ndvi", "albedo"] if b in image.bandNames().getInfo()]
    stats = image.select(bands).reduceRegion(
        reducer=ee.Reducer.mean().combine(ee.Reducer.minMax(), sharedInputs=True),
        geometry=basin_fc.geometry(),
        scale=scale,
        bestEffort=True,
        maxPixels=1e9,
    ).getInfo()
    rows = []
    for band in bands:
        rows.append({
            "variable": band,
            "mean": stats.get(f"{band}_mean"),
            "min": stats.get(f"{band}_min"),
            "max": stats.get(f"{band}_max"),
        })
    return pd.DataFrame(rows)


def geemap_map(image, basin_fc, center=(30.5, 70.5), zoom=5):
    """Create a geemap Folium map suitable for Streamlit via streamlit-folium."""
    if geemap is None:
        raise RuntimeError(f"geemap is unavailable: {GEEMAP_IMPORT_ERROR}")
    if geemap_folium is None:
        raise RuntimeError(f"geemap.foliumap is unavailable: {GEEMAP_IMPORT_ERROR}")
    m = geemap_folium.Map(center=list(center), zoom=zoom)
    et_vis = {"min": 0, "max": 1.0, "palette": ["440154", "31688e", "35b779", "fde725"]}
    ts_vis = {"min": 270, "max": 330, "palette": ["313695", "74add1", "fee090", "f46d43", "a50026"]}
    ndvi_vis = {"min": -0.2, "max": 0.9, "palette": ["8c510a", "f6e8c3", "5ab4ac", "01665e"]}
    m.add_layer(image.select("et_mm_h"), et_vis, "SEBAL ET rate (mm/h)")
    m.add_layer(image.select("ts_k"), ts_vis, "Land surface temperature (K)")
    m.add_layer(image.select("ndvi"), ndvi_vis, "NDVI", False)
    m.add_layer(ee.Image().paint(basin_fc, 1, 2), {"palette": ["ffffff"]}, "Indus Basin boundary")
    m.add_layer_control()
    return m


def sample_time_series(
    start_date: str,
    end_date: str,
    point_lon: float,
    point_lat: float,
    scale: int = 100,
) -> pd.DataFrame:
    """Extract SEBAL bands at a point for available Landsat scenes."""
    point = ee.Geometry.Point([point_lon, point_lat])
    col = (
        ee.ImageCollection(LANDSAT8)
        .merge(ee.ImageCollection(LANDSAT9))
        .filterDate(start_date, end_date)
        .filterBounds(point)
        .filter(ee.Filter.lte("CLOUD_COVER", 30))
        .sort("system:time_start")
    )
    ids = col.aggregate_array("LANDSAT_PRODUCT_ID").getInfo() or []
    rows = []
    for product_id in ids[:30]:
        img = col.filter(ee.Filter.eq("LANDSAT_PRODUCT_ID", product_id)).first()
        raw_date = ee.Date(img.get("system:time_start")).format("YYYY-MM-dd").getInfo()
        prepared = _prepare_landsat(img)
        values = prepared.select(["ndvi", "albedo", "ts_k"]).reduceRegion(ee.Reducer.first(), point, scale, bestEffort=True).getInfo()
        rows.append({"date": raw_date, **values})
    return pd.DataFrame(rows)

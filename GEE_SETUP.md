# Google Earth Engine setup for Indus Basin SEBAL

## Local / Google Colab

Install the project requirements, then authenticate once with the Earth Engine Python client:

```python
import ee
ee.Authenticate()
ee.Initialize(project="YOUR_EARTH_ENGINE_PROJECT")
```

The Streamlit app can then initialize Earth Engine using the same local credentials and project ID.

## Streamlit deployment

For unattended deployment, use a secure Google Cloud / Earth Engine service-account configuration. Do **not** put a private JSON key into GitHub or a public repository.

The application can read these secret names when they are configured in the deployment secret manager:

- `GEE_PROJECT`
- `GEE_SERVICE_ACCOUNT`
- `GEE_PRIVATE_KEY_JSON`

See `.streamlit/secrets.toml.example` for the names only. Replace the placeholder values in the deployment secret store, not in the repository.

## What the SEBAL module does

- Identifies the Indus upstream basin chain from WWF HydroSHEDS Level 7 using the Indus outlet point.
- Uses GeoPandas for local basin geometry inspection.
- Uses Landsat 8/9 Collection 2 Level 2 surface reflectance and land-surface temperature.
- Uses ERA5-Land hourly radiation, temperature and wind inputs.
- Computes a transparent SEBAL-style surface energy balance and instantaneous ET rate.
- Displays ET, LST and NDVI with geemap and exports basin-level statistics.

## Scientific limitation

The implementation is intended for research/prototyping and screening. It should be calibrated and validated against appropriate Indus Basin observations before operational water accounting, irrigation scheduling or engineering use.

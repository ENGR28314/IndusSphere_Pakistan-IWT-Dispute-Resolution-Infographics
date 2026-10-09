"""Optional indicator schema for user-uploaded official development data.

No fabricated current scores are included. Upload a CSV using the fields below to
turn IndusSphere into an indicator explorer.
"""

INDICATOR_SCHEMA = {
    "indicator_id": "Unique indicator code",
    "indicator_name": "Indicator name",
    "framework": "SDG / MDG / Vision 2030 / National",
    "goal": "Goal or thematic area",
    "province_region": "Pakistan province/region",
    "district": "Optional district",
    "year": "Reference year",
    "value": "Numeric indicator value",
    "unit": "Unit of measure",
    "source": "Official source",
    "source_url": "Official source URL",
}


def validate_indicator_columns(columns):
    required = {"indicator_name", "framework", "year", "value", "source"}
    return sorted(required - set(columns))

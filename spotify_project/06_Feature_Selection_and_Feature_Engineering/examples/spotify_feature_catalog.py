"""
Spotify Module 06 — Feature Catalog

This file documents candidate raw and derived features.
"""

import pandas as pd


FEATURE_CATALOG = [
    {
        "feature": "daily_listening_minutes",
        "source": "spotify_user_behavior",
        "type": "raw_numeric",
        "dimension": "Intensity",
        "business_meaning": (
            "Average daily listening volume"
        ),
        "recommended_use": "clustering",
    },
    {
        "feature": "sessions_per_day",
        "source": "spotify_user_behavior",
        "type": "raw_numeric",
        "dimension": "Frequency",
        "business_meaning": (
            "How often the user returns"
        ),
        "recommended_use": "clustering",
    },
    {
        "feature": "avg_session_minutes",
        "source": "spotify_user_behavior",
        "type": "raw_numeric",
        "dimension": "Depth",
        "business_meaning": (
            "Average session length"
        ),
        "recommended_use": "clustering",
    },
    {
        "feature": "days_active_last_30",
        "source": "spotify_user_behavior",
        "type": "raw_numeric",
        "dimension": "Consistency",
        "business_meaning": (
            "Recent usage regularity"
        ),
        "recommended_use": "clustering",
    },
    {
        "feature": "skip_rate",
        "source": "spotify_user_behavior",
        "type": "raw_numeric",
        "dimension": "Friction",
        "business_meaning": (
            "Track rejection or exploration"
        ),
        "recommended_use": "clustering",
    },
    {
        "feature": "ads_skipped_pct",
        "source": "spotify_user_behavior",
        "type": "raw_numeric",
        "dimension": "Friction",
        "business_meaning": (
            "Advertisement intolerance"
        ),
        "recommended_use": "clustering",
    },
    {
        "feature": "age",
        "source": "spotify_user_demo",
        "type": "raw_numeric",
        "dimension": "Demographic",
        "business_meaning": "User age",
        "recommended_use": "profiling",
    },
    {
        "feature": "country",
        "source": "spotify_user_demo",
        "type": "raw_category",
        "dimension": "Demographic",
        "business_meaning": "User region",
        "recommended_use": "profiling",
    },
    {
        "feature": "device_type",
        "source": "spotify_user_demo",
        "type": "raw_category",
        "dimension": "Demographic",
        "business_meaning": (
            "Primary access device"
        ),
        "recommended_use": "profiling",
    },
    {
        "feature": "active_day_ratio",
        "source": "days_active_last_30",
        "type": "derived_numeric",
        "dimension": "Consistency",
        "business_meaning": (
            "Share of days active"
        ),
        "recommended_use": "experiment",
    },
    {
        "feature": "friction_score",
        "source": (
            "skip_rate + ads_skipped_pct"
        ),
        "type": "derived_numeric",
        "dimension": "Friction",
        "business_meaning": (
            "Combined rejection behavior"
        ),
        "recommended_use": "experiment",
    },
    {
        "feature": "loyalty_score",
        "source": (
            "repeat_track_rate + "
            "repeat_artist_rate + "
            "liked_songs_pct"
        ),
        "type": "derived_numeric",
        "dimension": "Loyalty",
        "business_meaning": (
            "Repeated positive preference"
        ),
        "recommended_use": "experiment",
    },
]


def get_feature_catalog() -> pd.DataFrame:
    """Return the feature catalog as a DataFrame."""
    return pd.DataFrame(FEATURE_CATALOG)


if __name__ == "__main__":
    catalog = get_feature_catalog()
    print(catalog.to_string(index=False))

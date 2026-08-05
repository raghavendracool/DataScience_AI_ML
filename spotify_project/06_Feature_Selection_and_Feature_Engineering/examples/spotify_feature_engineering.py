"""
Spotify Module 06 — Reusable Feature Engineering Pipeline

The pipeline:
- Preserves user_id separately
- Builds candidate raw feature sets
- Creates safe derived features
- Validates required columns
- Checks missing and infinite values
- Returns model features and profiling features separately
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


CORE_FEATURES = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
    "days_active_last_30",
    "skip_rate",
    "ads_skipped_pct",
]

EXPANDED_FEATURES = [
    "daily_listening_minutes",
    "sessions_per_day",
    "days_active_last_30",
    "avg_session_minutes",
    "playlists_followed",
    "artists_followed",
    "skip_rate",
    "liked_songs_pct",
    "ads_skipped_pct",
    "repeat_track_rate",
    "repeat_artist_rate",
    "genre_diversity_score",
    "mean_track_popularity",
    "pct_top_popularity_tracks",
    "median_gap_minutes_between_plays",
]

AUDIO_FEATURES = [
    "mean_danceability",
    "mean_energy",
    "mean_valence",
    "mean_acousticness",
    "mean_speechiness",
    "mean_instrumentalness",
    "mean_tempo",
    "std_energy",
    "std_valence",
    "std_tempo",
]

PROFILING_FEATURES = [
    "age",
    "country",
    "city_tier",
    "device_type",
    "subscription_tenure_months",
]


@dataclass(frozen=True)
class FeatureOutput:
    """Feature-engineering result."""

    user_ids: pd.DataFrame
    core_raw: pd.DataFrame
    expanded_raw: pd.DataFrame
    engineered: pd.DataFrame
    profiling: pd.DataFrame
    feature_catalog: pd.DataFrame


def require_columns(
    df: pd.DataFrame,
    columns: list[str],
    table_name: str,
) -> None:
    """Raise an error for missing columns."""
    missing = set(columns) - set(df.columns)

    if missing:
        raise ValueError(
            f"{table_name} missing columns: "
            f"{sorted(missing)}"
        )


def validate_numeric_features(
    df: pd.DataFrame,
    feature_names: list[str],
) -> None:
    """Validate model features before scaling."""
    require_columns(
        df,
        feature_names,
        "feature dataframe",
    )

    non_numeric = (
        df[feature_names]
        .select_dtypes(exclude="number")
        .columns
        .tolist()
    )

    if non_numeric:
        raise TypeError(
            f"Non-numeric model features: "
            f"{non_numeric}"
        )

    missing_count = int(
        df[feature_names]
        .isna()
        .sum()
        .sum()
    )

    if missing_count:
        raise ValueError(
            f"Feature set contains "
            f"{missing_count} missing values"
        )

    values = df[feature_names].to_numpy(
        dtype=float
    )

    infinite_count = int(
        np.isinf(values).sum()
    )

    if infinite_count:
        raise ValueError(
            f"Feature set contains "
            f"{infinite_count} infinite values"
        )


def create_derived_features(
    behavior: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create business-friendly features.

    Raw columns are preserved.
    """
    required = [
        "user_id",
        "days_active_last_30",
        "skip_rate",
        "ads_skipped_pct",
        "repeat_track_rate",
        "repeat_artist_rate",
        "liked_songs_pct",
        "playlists_followed",
        "artists_followed",
        "mean_track_popularity",
        "pct_top_popularity_tracks",
        "median_gap_minutes_between_plays",
    ]

    require_columns(
        behavior,
        required,
        "spotify_user_behavior",
    )

    output = behavior.copy()

    output["active_day_ratio"] = (
        output["days_active_last_30"]
        .div(30)
    )

    output["friction_score"] = (
        output[
            [
                "skip_rate",
                "ads_skipped_pct",
            ]
        ]
        .mean(axis=1)
    )

    output["loyalty_score"] = (
        output[
            [
                "repeat_track_rate",
                "repeat_artist_rate",
                "liked_songs_pct",
            ]
        ]
        .mean(axis=1)
    )

    output["follow_depth"] = (
        output["playlists_followed"]
        + output["artists_followed"]
    )

    output["mainstream_affinity"] = (
        output["mean_track_popularity"]
        .div(100)
        .add(
            output[
                "pct_top_popularity_tracks"
            ]
        )
        .div(2)
    )

    output["return_frequency_score"] = (
        1
        / (
            1
            + output[
                "median_gap_minutes_between_plays"
            ]
        )
    )

    output = output.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    assert (
        output["active_day_ratio"]
        .dropna()
        .between(0, 1)
        .all()
    )

    for column in [
        "friction_score",
        "loyalty_score",
        "mainstream_affinity",
        "return_frequency_score",
    ]:
        if not output[column].dropna().between(
            0,
            1,
        ).all():
            raise ValueError(
                f"{column} is outside expected "
                f"0-to-1 range"
            )

    return output


def create_feature_catalog() -> pd.DataFrame:
    """Document the engineered features."""
    records = [
        {
            "feature": "active_day_ratio",
            "source": "days_active_last_30",
            "formula": (
                "days_active_last_30 / 30"
            ),
            "dimension": "Consistency",
            "business_meaning": (
                "Share of recent days active"
            ),
        },
        {
            "feature": "friction_score",
            "source": (
                "skip_rate, ads_skipped_pct"
            ),
            "formula": (
                "mean(skip_rate, "
                "ads_skipped_pct)"
            ),
            "dimension": "Friction",
            "business_meaning": (
                "Combined content and ad rejection"
            ),
        },
        {
            "feature": "loyalty_score",
            "source": (
                "repeat_track_rate, "
                "repeat_artist_rate, "
                "liked_songs_pct"
            ),
            "formula": "mean(source rates)",
            "dimension": "Loyalty",
            "business_meaning": (
                "Positive repeated preference"
            ),
        },
        {
            "feature": "follow_depth",
            "source": (
                "playlists_followed, "
                "artists_followed"
            ),
            "formula": "sum(source counts)",
            "dimension": "Loyalty",
            "business_meaning": (
                "Total explicit following behavior"
            ),
        },
        {
            "feature": "mainstream_affinity",
            "source": (
                "mean_track_popularity, "
                "pct_top_popularity_tracks"
            ),
            "formula": (
                "mean(mean_track_popularity / 100, "
                "pct_top_popularity_tracks)"
            ),
            "dimension": "Popularity",
            "business_meaning": (
                "Preference for mainstream content"
            ),
        },
        {
            "feature": "return_frequency_score",
            "source": (
                "median_gap_minutes_between_plays"
            ),
            "formula": "1 / (1 + gap)",
            "dimension": "Frequency",
            "business_meaning": (
                "Higher score means shorter return gap"
            ),
        },
    ]

    return pd.DataFrame(records)


def build_feature_output(
    behavior: pd.DataFrame,
    demo: pd.DataFrame,
) -> FeatureOutput:
    """Build raw, engineered and profiling feature tables."""
    require_columns(
        behavior,
        ["user_id"] + EXPANDED_FEATURES,
        "spotify_user_behavior",
    )

    require_columns(
        demo,
        ["user_id"] + PROFILING_FEATURES,
        "spotify_user_demo",
    )

    if not behavior["user_id"].is_unique:
        raise ValueError(
            "Behavior user_id is not unique"
        )

    if not demo["user_id"].is_unique:
        raise ValueError(
            "Demo user_id is not unique"
        )

    user_ids = behavior[["user_id"]].copy()

    core_raw = behavior[
        CORE_FEATURES
    ].copy()

    expanded_raw = behavior[
        EXPANDED_FEATURES
    ].copy()

    engineered_full = create_derived_features(
        behavior
    )

    engineered_names = [
        "active_day_ratio",
        "friction_score",
        "loyalty_score",
        "follow_depth",
        "mainstream_affinity",
        "return_frequency_score",
    ]

    engineered = engineered_full[
        engineered_names
    ].copy()

    profiling = (
        user_ids
        .merge(
            demo[
                ["user_id"]
                + PROFILING_FEATURES
            ],
            on="user_id",
            how="inner",
            validate="one_to_one",
        )
    )

    validate_numeric_features(
        behavior,
        CORE_FEATURES,
    )

    validate_numeric_features(
        behavior,
        EXPANDED_FEATURES,
    )

    validate_numeric_features(
        engineered,
        engineered_names,
    )

    return FeatureOutput(
        user_ids=user_ids,
        core_raw=core_raw,
        expanded_raw=expanded_raw,
        engineered=engineered,
        profiling=profiling,
        feature_catalog=create_feature_catalog(),
    )


if __name__ == "__main__":
    behavior_df = pd.read_excel(
        "spotify_user_behavior.xlsx"
    )

    demo_df = pd.read_excel(
        "spotify_user_demo.xlsx"
    )

    output = build_feature_output(
        behavior_df,
        demo_df,
    )

    print(
        "Core raw shape:",
        output.core_raw.shape,
    )

    print(
        "Expanded raw shape:",
        output.expanded_raw.shape,
    )

    print(
        "Engineered shape:",
        output.engineered.shape,
    )

    print(
        "Profiling shape:",
        output.profiling.shape,
    )

    print("\nEngineered Feature Catalog")
    print(
        output.feature_catalog.to_string(
            index=False
        )
    )

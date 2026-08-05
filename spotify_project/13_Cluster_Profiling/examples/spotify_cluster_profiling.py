"""
Spotify Module 13 — Complete Cluster Profiling Pipeline

Expected files:
- spotify_user_behavior.xlsx
- spotify_user_demo.xlsx
- spotify_user_clusters.csv

The cluster file must include:
- user_id
- cluster

Outputs:
- Cluster-size report
- Behavioral mean and median profiles
- Percentile profiles
- Relative-to-overall profile
- Standardized profile
- Demographic profile
- High and low feature evidence
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


OUTPUT_DIR = Path("cluster_profile_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

BEHAVIOR_FEATURES = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
    "days_active_last_30",
    "skip_rate",
    "ads_skipped_pct",
    "repeat_track_rate",
    "repeat_artist_rate",
    "liked_songs_pct",
    "genre_diversity_score",
    "mean_track_popularity",
    "pct_top_popularity_tracks",
]

DEMOGRAPHIC_COLUMNS = [
    "age",
    "country",
    "city_tier",
    "device_type",
    "subscription_tenure_months",
]


@dataclass(frozen=True)
class ProfileOutput:
    """Container for cluster profile artifacts."""

    profile_data: pd.DataFrame
    cluster_sizes: pd.DataFrame
    behavior_means: pd.DataFrame
    behavior_medians: pd.DataFrame
    behavior_percentiles: pd.DataFrame
    relative_to_overall: pd.DataFrame
    standardized_profile: pd.DataFrame
    demographic_profile: pd.DataFrame
    high_low_features: pd.DataFrame


def validate_unique_user_id(
    df: pd.DataFrame,
    table_name: str,
) -> None:
    """Validate a unique non-missing user ID."""
    if "user_id" not in df.columns:
        raise ValueError(
            f"{table_name} does not contain user_id"
        )

    if df["user_id"].isna().any():
        raise ValueError(
            f"{table_name} user_id contains missing values"
        )

    if not df["user_id"].is_unique:
        raise ValueError(
            f"{table_name} user_id is not unique"
        )


def prepare_profile_data(
    behavior: pd.DataFrame,
    demo: pd.DataFrame,
    labels: pd.DataFrame,
) -> pd.DataFrame:
    """Join behavior, demographics and cluster labels."""
    validate_unique_user_id(
        behavior,
        "behavior",
    )

    validate_unique_user_id(
        demo,
        "demo",
    )

    validate_unique_user_id(
        labels,
        "labels",
    )

    if "cluster" not in labels.columns:
        raise ValueError(
            "labels must contain cluster"
        )

    missing_behavior = (
        set(BEHAVIOR_FEATURES)
        - set(behavior.columns)
    )

    if missing_behavior:
        raise ValueError(
            "Missing behavior features: "
            f"{sorted(missing_behavior)}"
        )

    missing_demo = (
        set(DEMOGRAPHIC_COLUMNS)
        - set(demo.columns)
    )

    if missing_demo:
        raise ValueError(
            "Missing demographic columns: "
            f"{sorted(missing_demo)}"
        )

    joined = (
        behavior
        .merge(
            labels[
                ["user_id", "cluster"]
            ],
            on="user_id",
            how="inner",
            validate="one_to_one",
        )
        .merge(
            demo[
                ["user_id"]
                + DEMOGRAPHIC_COLUMNS
            ],
            on="user_id",
            how="left",
            validate="one_to_one",
        )
    )

    if len(joined) != len(labels):
        raise ValueError(
            "Not all labeled users matched "
            "the behavior data"
        )

    return joined


def cluster_size_report(
    profile_data: pd.DataFrame,
) -> pd.DataFrame:
    """Create count and percentage report."""
    report = (
        profile_data["cluster"]
        .value_counts()
        .sort_index()
        .rename_axis("cluster")
        .reset_index(name="user_count")
    )

    report["user_percentage"] = (
        report["user_count"]
        .div(report["user_count"].sum())
        .mul(100)
        .round(2)
    )

    return report


def behavior_profile_reports(
    profile_data: pd.DataFrame,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    """Create mean, median and percentile reports."""
    means = (
        profile_data
        .groupby("cluster")[
            BEHAVIOR_FEATURES
        ]
        .mean()
        .reset_index()
        .round(4)
    )

    medians = (
        profile_data
        .groupby("cluster")[
            BEHAVIOR_FEATURES
        ]
        .median()
        .reset_index()
        .round(4)
    )

    percentile_rows = []

    for cluster, group in profile_data.groupby(
        "cluster"
    ):
        for feature in BEHAVIOR_FEATURES:
            percentile_rows.append({
                "cluster": cluster,
                "feature": feature,
                "p25": group[
                    feature
                ].quantile(0.25),
                "p50": group[
                    feature
                ].quantile(0.50),
                "p75": group[
                    feature
                ].quantile(0.75),
                "std": group[
                    feature
                ].std(),
            })

    percentiles = (
        pd.DataFrame(percentile_rows)
        .round(4)
    )

    return means, medians, percentiles


def relative_profile(
    profile_data: pd.DataFrame,
    behavior_means: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate percent above or below overall mean."""
    overall = profile_data[
        BEHAVIOR_FEATURES
    ].mean()

    output = (
        behavior_means
        .set_index("cluster")[
            BEHAVIOR_FEATURES
        ]
        .div(overall)
        .sub(1)
        .mul(100)
        .reset_index()
        .round(2)
    )

    return output


def standardized_cluster_profile(
    profile_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Standardize user features globally and then calculate
    cluster means in standardized units.
    """
    scaler = StandardScaler()

    scaled = scaler.fit_transform(
        profile_data[
            BEHAVIOR_FEATURES
        ]
    )

    scaled_df = pd.DataFrame(
        scaled,
        columns=BEHAVIOR_FEATURES,
        index=profile_data.index,
    )

    scaled_df["cluster"] = (
        profile_data["cluster"]
        .to_numpy()
    )

    return (
        scaled_df
        .groupby("cluster")[
            BEHAVIOR_FEATURES
        ]
        .mean()
        .reset_index()
        .round(4)
    )


def mode_or_missing(
    series: pd.Series,
) -> object:
    """Return first mode or missing."""
    modes = series.mode(
        dropna=True
    )

    if modes.empty:
        return np.nan

    return modes.iloc[0]


def demographic_profile_report(
    profile_data: pd.DataFrame,
) -> pd.DataFrame:
    """Create numeric and categorical demographic profile."""
    numeric = (
        profile_data
        .groupby("cluster")
        .agg(
            users=("user_id", "nunique"),
            avg_age=("age", "mean"),
            median_age=("age", "median"),
            avg_tenure_months=(
                "subscription_tenure_months",
                "mean",
            ),
            median_tenure_months=(
                "subscription_tenure_months",
                "median",
            ),
        )
        .reset_index()
    )

    category_rows = []

    for cluster, group in profile_data.groupby(
        "cluster"
    ):
        category_rows.append({
            "cluster": cluster,
            "top_country": mode_or_missing(
                group["country"]
            ),
            "top_city_tier": mode_or_missing(
                group["city_tier"]
            ),
            "top_device_type": mode_or_missing(
                group["device_type"]
            ),
            "country_count": int(
                group["country"]
                .nunique(
                    dropna=True
                )
            ),
        })

    category_profile = pd.DataFrame(
        category_rows
    )

    return (
        numeric
        .merge(
            category_profile,
            on="cluster",
            how="left",
            validate="one_to_one",
        )
        .round(3)
    )


def high_low_feature_report(
    standardized_profile: pd.DataFrame,
    top_n: int = 3,
) -> pd.DataFrame:
    """Return top high and low features for each cluster."""
    rows = []

    profile = standardized_profile.set_index(
        "cluster"
    )

    for cluster, values in profile.iterrows():
        high = values.sort_values(
            ascending=False
        ).head(top_n)

        low = values.sort_values().head(
            top_n
        )

        for rank, (feature, value) in enumerate(
            high.items(),
            start=1,
        ):
            rows.append({
                "cluster": cluster,
                "direction": "HIGH",
                "rank": rank,
                "feature": feature,
                "standardized_mean": value,
            })

        for rank, (feature, value) in enumerate(
            low.items(),
            start=1,
        ):
            rows.append({
                "cluster": cluster,
                "direction": "LOW",
                "rank": rank,
                "feature": feature,
                "standardized_mean": value,
            })

    return pd.DataFrame(rows).round(4)


def run_profiling(
    behavior: pd.DataFrame,
    demo: pd.DataFrame,
    labels: pd.DataFrame,
) -> ProfileOutput:
    """Run the complete profiling workflow."""
    profile_data = prepare_profile_data(
        behavior,
        demo,
        labels,
    )

    sizes = cluster_size_report(
        profile_data
    )

    means, medians, percentiles = (
        behavior_profile_reports(
            profile_data
        )
    )

    relative = relative_profile(
        profile_data,
        means,
    )

    standardized = (
        standardized_cluster_profile(
            profile_data
        )
    )

    demographics = (
        demographic_profile_report(
            profile_data
        )
    )

    high_low = high_low_feature_report(
        standardized
    )

    outputs = {
        "profile_data": profile_data,
        "cluster_sizes": sizes,
        "behavior_means": means,
        "behavior_medians": medians,
        "behavior_percentiles": percentiles,
        "relative_to_overall": relative,
        "standardized_profile": standardized,
        "demographic_profile": demographics,
        "high_low_features": high_low,
    }

    for name, frame in outputs.items():
        frame.to_csv(
            OUTPUT_DIR / f"{name}.csv",
            index=False,
        )

    return ProfileOutput(
        profile_data=profile_data,
        cluster_sizes=sizes,
        behavior_means=means,
        behavior_medians=medians,
        behavior_percentiles=percentiles,
        relative_to_overall=relative,
        standardized_profile=standardized,
        demographic_profile=demographics,
        high_low_features=high_low,
    )


if __name__ == "__main__":
    behavior_df = pd.read_excel(
        "spotify_user_behavior.xlsx"
    )

    demo_df = pd.read_excel(
        "spotify_user_demo.xlsx"
    )

    label_df = pd.read_csv(
        "spotify_user_clusters.csv"
    )

    result = run_profiling(
        behavior_df,
        demo_df,
        label_df,
    )

    print("\nCluster Sizes")
    print(
        result.cluster_sizes.to_string(
            index=False
        )
    )

    print("\nHigh and Low Features")
    print(
        result.high_low_features.to_string(
            index=False
        )
    )

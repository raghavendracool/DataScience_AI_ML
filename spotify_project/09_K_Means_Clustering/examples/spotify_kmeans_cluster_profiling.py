"""
Spotify Module 09 — K-Means Cluster Profiling

Profiles final cluster labels using:
- User counts
- Percentages
- Mean behavior
- Median behavior
- Demographics
"""

from __future__ import annotations

import pandas as pd


FEATURES = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
    "days_active_last_30",
    "skip_rate",
    "ads_skipped_pct",
]


def create_cluster_size_report(
    clustered: pd.DataFrame,
) -> pd.DataFrame:
    """Create user counts and percentages."""
    report = (
        clustered["cluster"]
        .value_counts()
        .sort_index()
        .rename_axis("cluster")
        .reset_index(name="users")
    )

    report["percentage"] = (
        report["users"]
        .div(report["users"].sum())
        .mul(100)
        .round(2)
    )

    return report


def create_behavior_profile(
    clustered: pd.DataFrame,
) -> pd.DataFrame:
    """Create mean and median behavior profile."""
    mean_profile = (
        clustered
        .groupby("cluster")[FEATURES]
        .mean()
        .add_suffix("_mean")
    )

    median_profile = (
        clustered
        .groupby("cluster")[FEATURES]
        .median()
        .add_suffix("_median")
    )

    return (
        mean_profile
        .join(median_profile)
        .reset_index()
        .round(4)
    )


def create_demographic_profile(
    clustered: pd.DataFrame,
    demo: pd.DataFrame,
) -> pd.DataFrame:
    """Join demographics and create cluster profile."""
    joined = clustered[
        ["user_id", "cluster"]
    ].merge(
        demo,
        on="user_id",
        how="inner",
        validate="one_to_one",
    )

    numeric = (
        joined
        .groupby("cluster")
        .agg(
            users=("user_id", "nunique"),
            avg_age=("age", "mean"),
            median_age=("age", "median"),
            avg_tenure=(
                "subscription_tenure_months",
                "mean",
            ),
            median_tenure=(
                "subscription_tenure_months",
                "median",
            ),
        )
        .reset_index()
    )

    category_modes = []

    for cluster, group in joined.groupby("cluster"):
        category_modes.append({
            "cluster": cluster,
            "top_country": (
                group["country"]
                .mode()
                .iloc[0]
            ),
            "top_city_tier": (
                group["city_tier"]
                .mode()
                .iloc[0]
            ),
            "top_device": (
                group["device_type"]
                .mode()
                .iloc[0]
            ),
        })

    return (
        numeric
        .merge(
            pd.DataFrame(category_modes),
            on="cluster",
            how="left",
            validate="one_to_one",
        )
        .round(3)
    )


if __name__ == "__main__":
    behavior = pd.read_excel(
        "spotify_user_behavior.xlsx"
    )

    demo = pd.read_excel(
        "spotify_user_demo.xlsx"
    )

    labels = pd.read_csv(
        "spotify_user_clusters.csv"
    )

    clustered_behavior = (
        behavior.merge(
            labels,
            on="user_id",
            how="inner",
            validate="one_to_one",
        )
    )

    size_report = create_cluster_size_report(
        clustered_behavior
    )

    behavior_profile = create_behavior_profile(
        clustered_behavior
    )

    demographic_profile = (
        create_demographic_profile(
            clustered_behavior,
            demo,
        )
    )

    size_report.to_csv(
        "cluster_sizes.csv",
        index=False,
    )

    behavior_profile.to_csv(
        "behavior_profile.csv",
        index=False,
    )

    demographic_profile.to_csv(
        "demographic_profile.csv",
        index=False,
    )

    print("\nCluster Sizes")
    print(
        size_report.to_string(
            index=False
        )
    )

    print("\nBehavior Profile")
    print(
        behavior_profile.to_string(
            index=False
        )
    )

    print("\nDemographic Profile")
    print(
        demographic_profile.to_string(
            index=False
        )
    )

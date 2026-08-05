"""
Spotify Module 09 — End-to-End K-Means Pipeline

Expected input files:
- spotify_user_behavior.xlsx
- spotify_user_demo.xlsx

Outputs:
- K evaluation table
- Cluster labels
- Cluster sizes
- Scaled centroids
- Original-unit centroids
- Behavior profiles
- Demographic profiles
- Saved scaler and K-Means model
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


OUTPUT_DIR = Path("kmeans_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

FEATURES = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
    "days_active_last_30",
    "skip_rate",
    "ads_skipped_pct",
]


@dataclass(frozen=True)
class KMeansOutput:
    """Final K-Means output container."""

    clustered_users: pd.DataFrame
    evaluation: pd.DataFrame
    cluster_sizes: pd.DataFrame
    scaled_centroids: pd.DataFrame
    original_centroids: pd.DataFrame
    behavior_profile: pd.DataFrame
    demographic_profile: pd.DataFrame


def validate_features(
    behavior: pd.DataFrame,
) -> None:
    """Validate model input columns."""
    required = {"user_id", *FEATURES}
    missing = required - set(behavior.columns)

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    if behavior["user_id"].isna().any():
        raise ValueError(
            "user_id contains missing values"
        )

    if not behavior["user_id"].is_unique:
        raise ValueError(
            "user_id is not unique"
        )

    non_numeric = (
        behavior[FEATURES]
        .select_dtypes(exclude="number")
        .columns
        .tolist()
    )

    if non_numeric:
        raise TypeError(
            f"Non-numeric features: {non_numeric}"
        )

    if behavior[FEATURES].isna().any().any():
        raise ValueError(
            "Feature matrix contains missing values"
        )

    if not np.isfinite(
        behavior[FEATURES]
        .to_numpy(dtype=float)
    ).all():
        raise ValueError(
            "Feature matrix contains infinite values"
        )


def evaluate_k_values(
    X_scaled: np.ndarray,
    min_k: int = 2,
    max_k: int = 10,
) -> pd.DataFrame:
    """Evaluate candidate K values."""
    records = []

    for k in range(min_k, max_k + 1):
        model = KMeans(
            n_clusters=k,
            init="k-means++",
            n_init=20,
            max_iter=300,
            tol=1e-4,
            random_state=42,
        )

        labels = model.fit_predict(
            X_scaled
        )

        counts = pd.Series(
            labels
        ).value_counts()

        records.append({
            "k": k,
            "inertia": model.inertia_,
            "silhouette_score": (
                silhouette_score(
                    X_scaled,
                    labels,
                )
            ),
            "iterations": model.n_iter_,
            "smallest_cluster_count": int(
                counts.min()
            ),
            "largest_cluster_count": int(
                counts.max()
            ),
            "smallest_cluster_pct": round(
                100 * counts.min() / len(labels),
                2,
            ),
            "largest_cluster_pct": round(
                100 * counts.max() / len(labels),
                2,
            ),
        })

    return pd.DataFrame(records)


def cluster_size_report(
    labels: np.ndarray,
) -> pd.DataFrame:
    """Create cluster count and percentage report."""
    output = (
        pd.Series(labels, name="cluster")
        .value_counts()
        .sort_index()
        .rename_axis("cluster")
        .reset_index(name="users")
    )

    output["percentage"] = (
        output["users"]
        .div(output["users"].sum())
        .mul(100)
        .round(2)
    )

    return output


def centroid_dataframes(
    model: KMeans,
    scaler: StandardScaler,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return scaled and original-unit centroid tables."""
    scaled = pd.DataFrame(
        model.cluster_centers_,
        columns=FEATURES,
    )

    scaled.insert(
        0,
        "cluster",
        range(model.n_clusters),
    )

    original_values = scaler.inverse_transform(
        model.cluster_centers_
    )

    original = pd.DataFrame(
        original_values,
        columns=FEATURES,
    )

    original.insert(
        0,
        "cluster",
        range(model.n_clusters),
    )

    return (
        scaled.round(4),
        original.round(4),
    )


def behavior_profile_report(
    behavior_with_clusters: pd.DataFrame,
) -> pd.DataFrame:
    """Create mean and median behavior profiles."""
    mean_profile = (
        behavior_with_clusters
        .groupby("cluster")[FEATURES]
        .mean()
        .add_suffix("_mean")
    )

    median_profile = (
        behavior_with_clusters
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


def demographic_profile_report(
    clustered_users: pd.DataFrame,
    demo: pd.DataFrame,
) -> pd.DataFrame:
    """Create a concise demographic profile by cluster."""
    required_demo = {
        "user_id",
        "age",
        "country",
        "city_tier",
        "device_type",
        "subscription_tenure_months",
    }

    missing = required_demo - set(demo.columns)

    if missing:
        raise ValueError(
            f"Missing demo columns: {sorted(missing)}"
        )

    joined = clustered_users.merge(
        demo,
        on="user_id",
        how="inner",
        validate="one_to_one",
    )

    numeric_profile = (
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

    mode_rows = []

    for cluster, group in joined.groupby("cluster"):
        mode_rows.append({
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
            "top_device_type": (
                group["device_type"]
                .mode()
                .iloc[0]
            ),
        })

    mode_profile = pd.DataFrame(mode_rows)

    return (
        numeric_profile
        .merge(
            mode_profile,
            on="cluster",
            how="left",
            validate="one_to_one",
        )
        .round(3)
    )


def run_pipeline(
    behavior: pd.DataFrame,
    demo: pd.DataFrame,
    final_k: int = 4,
) -> KMeansOutput:
    """Run evaluation and fit the final K-Means model."""
    validate_features(behavior)

    user_ids = behavior[
        ["user_id"]
    ].copy()

    X = behavior[
        FEATURES
    ].copy()

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(
        X
    )

    evaluation = evaluate_k_values(
        X_scaled
    )

    final_model = KMeans(
        n_clusters=final_k,
        init="k-means++",
        n_init=20,
        max_iter=300,
        tol=1e-4,
        random_state=42,
    )

    labels = final_model.fit_predict(
        X_scaled
    )

    clustered_users = user_ids.copy()
    clustered_users["cluster"] = labels

    cluster_sizes = cluster_size_report(
        labels
    )

    scaled_centroids, original_centroids = (
        centroid_dataframes(
            final_model,
            scaler,
        )
    )

    behavior_with_clusters = (
        behavior.copy()
    )

    behavior_with_clusters[
        "cluster"
    ] = labels

    behavior_profile = behavior_profile_report(
        behavior_with_clusters
    )

    demographic_profile = (
        demographic_profile_report(
            clustered_users,
            demo,
        )
    )

    evaluation.to_csv(
        OUTPUT_DIR
        / "kmeans_k_evaluation.csv",
        index=False,
    )

    clustered_users.to_csv(
        OUTPUT_DIR
        / "spotify_user_clusters.csv",
        index=False,
    )

    cluster_sizes.to_csv(
        OUTPUT_DIR
        / "cluster_sizes.csv",
        index=False,
    )

    scaled_centroids.to_csv(
        OUTPUT_DIR
        / "scaled_centroids.csv",
        index=False,
    )

    original_centroids.to_csv(
        OUTPUT_DIR
        / "original_unit_centroids.csv",
        index=False,
    )

    behavior_profile.to_csv(
        OUTPUT_DIR
        / "behavior_cluster_profile.csv",
        index=False,
    )

    demographic_profile.to_csv(
        OUTPUT_DIR
        / "demographic_cluster_profile.csv",
        index=False,
    )

    joblib.dump(
        scaler,
        OUTPUT_DIR
        / "spotify_standard_scaler.joblib",
    )

    joblib.dump(
        final_model,
        OUTPUT_DIR
        / "spotify_kmeans_model.joblib",
    )

    joblib.dump(
        FEATURES,
        OUTPUT_DIR
        / "spotify_feature_order.joblib",
    )

    return KMeansOutput(
        clustered_users=clustered_users,
        evaluation=evaluation,
        cluster_sizes=cluster_sizes,
        scaled_centroids=scaled_centroids,
        original_centroids=original_centroids,
        behavior_profile=behavior_profile,
        demographic_profile=demographic_profile,
    )


if __name__ == "__main__":
    behavior_df = pd.read_excel(
        "spotify_user_behavior.xlsx"
    )

    demo_df = pd.read_excel(
        "spotify_user_demo.xlsx"
    )

    result = run_pipeline(
        behavior_df,
        demo_df,
        final_k=4,
    )

    print("\nK Evaluation")
    print(
        result.evaluation.round(4)
        .to_string(index=False)
    )

    print("\nCluster Sizes")
    print(
        result.cluster_sizes
        .to_string(index=False)
    )

    print("\nOriginal Unit Centroids")
    print(
        result.original_centroids
        .to_string(index=False)
    )

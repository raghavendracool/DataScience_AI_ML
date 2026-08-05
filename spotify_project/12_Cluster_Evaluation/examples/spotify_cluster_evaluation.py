"""
Spotify Module 12 — Complete Cluster Evaluation

Evaluates K-Means and GMM outputs using:
- Silhouette Score
- Davies-Bouldin Index
- Calinski-Harabasz Score
- Inertia
- Log-likelihood
- AIC
- BIC
- Cluster-size metrics
- GMM confidence metrics

Expected files:
- spotify_user_behavior.xlsx
- optional saved K-Means/GMM artifacts
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler


OUTPUT_DIR = Path("cluster_evaluation_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

FEATURES = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
    "days_active_last_30",
    "skip_rate",
    "ads_skipped_pct",
]


def validate_features(
    behavior: pd.DataFrame,
) -> pd.DataFrame:
    """Validate and return the model matrix."""
    required = {"user_id", *FEATURES}
    missing = required - set(behavior.columns)

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    X = behavior[
        FEATURES
    ].copy()

    non_numeric = (
        X.select_dtypes(exclude="number")
        .columns
        .tolist()
    )

    if non_numeric:
        raise TypeError(
            f"Non-numeric features: {non_numeric}"
        )

    if X.isna().any().any():
        raise ValueError(
            "Missing values exist"
        )

    if not np.isfinite(
        X.to_numpy(dtype=float)
    ).all():
        raise ValueError(
            "Infinite values exist"
        )

    return X


def cluster_size_metrics(
    labels: np.ndarray,
) -> dict[str, Any]:
    """Calculate cluster counts and balance metrics."""
    counts = (
        pd.Series(labels)
        .value_counts()
        .sort_index()
    )

    percentages = (
        counts
        .div(counts.sum())
        .mul(100)
    )

    return {
        "cluster_count": int(len(counts)),
        "smallest_cluster_count": int(
            counts.min()
        ),
        "largest_cluster_count": int(
            counts.max()
        ),
        "smallest_cluster_pct": float(
            percentages.min()
        ),
        "largest_cluster_pct": float(
            percentages.max()
        ),
        "largest_to_smallest_ratio": float(
            counts.max() / counts.min()
        ),
        "cluster_counts": counts.to_dict(),
        "cluster_percentages": (
            percentages.round(4)
            .to_dict()
        ),
    }


def hard_label_metrics(
    X: np.ndarray,
    labels: np.ndarray,
    sample_size: int = 10000,
) -> dict[str, float]:
    """Calculate internal metrics from hard labels."""
    unique_labels = np.unique(labels)

    if len(unique_labels) < 2:
        raise ValueError(
            "At least two clusters are required"
        )

    return {
        "silhouette_score": float(
            silhouette_score(
                X,
                labels,
                sample_size=min(
                    sample_size,
                    len(labels),
                ),
                random_state=42,
            )
        ),
        "davies_bouldin_index": float(
            davies_bouldin_score(
                X,
                labels,
            )
        ),
        "calinski_harabasz_score": float(
            calinski_harabasz_score(
                X,
                labels,
            )
        ),
    }


def evaluate_kmeans(
    X_scaled: np.ndarray,
    k_values: range = range(2, 11),
) -> pd.DataFrame:
    """Evaluate candidate K-Means models."""
    records = []

    for k in k_values:
        model = KMeans(
            n_clusters=k,
            init="k-means++",
            n_init=20,
            max_iter=300,
            random_state=42,
        )

        labels = model.fit_predict(
            X_scaled
        )

        record = {
            "algorithm": "KMeans",
            "candidate": f"K={k}",
            "k_or_components": k,
            "inertia": float(
                model.inertia_
            ),
            "iterations": int(
                model.n_iter_
            ),
        }

        record.update(
            hard_label_metrics(
                X_scaled,
                labels,
            )
        )

        record.update(
            cluster_size_metrics(
                labels
            )
        )

        records.append(record)

    return pd.DataFrame(records)


def evaluate_gmm(
    X_scaled: np.ndarray,
    component_values: range = range(2, 11),
    covariance_types: tuple[str, ...] = (
        "full",
        "tied",
        "diag",
        "spherical",
    ),
) -> pd.DataFrame:
    """Evaluate candidate Gaussian Mixture Models."""
    records = []

    for components in component_values:
        for covariance_type in covariance_types:
            model = GaussianMixture(
                n_components=components,
                covariance_type=(
                    covariance_type
                ),
                n_init=10,
                max_iter=300,
                tol=1e-4,
                reg_covar=1e-6,
                random_state=42,
            )

            model.fit(
                X_scaled
            )

            labels = model.predict(
                X_scaled
            )

            probabilities = (
                model.predict_proba(
                    X_scaled
                )
            )

            confidence = probabilities.max(
                axis=1
            )

            record = {
                "algorithm": "GMM",
                "candidate": (
                    f"C={components},"
                    f"{covariance_type}"
                ),
                "k_or_components": (
                    components
                ),
                "covariance_type": (
                    covariance_type
                ),
                "log_likelihood": float(
                    model.score(
                        X_scaled
                    )
                ),
                "aic": float(
                    model.aic(
                        X_scaled
                    )
                ),
                "bic": float(
                    model.bic(
                        X_scaled
                    )
                ),
                "mean_membership_confidence": float(
                    confidence.mean()
                ),
                "p10_membership_confidence": float(
                    np.quantile(
                        confidence,
                        0.10,
                    )
                ),
                "converged": bool(
                    model.converged_
                ),
                "iterations": int(
                    model.n_iter_
                ),
            }

            record.update(
                hard_label_metrics(
                    X_scaled,
                    labels,
                )
            )

            record.update(
                cluster_size_metrics(
                    labels
                )
            )

            records.append(record)

    return pd.DataFrame(records)


if __name__ == "__main__":
    behavior = pd.read_excel(
        "spotify_user_behavior.xlsx"
    )

    X = validate_features(
        behavior
    )

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(
        X
    )

    kmeans_results = evaluate_kmeans(
        X_scaled
    )

    gmm_results = evaluate_gmm(
        X_scaled
    )

    kmeans_results.to_csv(
        OUTPUT_DIR
        / "kmeans_evaluation.csv",
        index=False,
    )

    gmm_results.to_csv(
        OUTPUT_DIR
        / "gmm_evaluation.csv",
        index=False,
    )

    print("\nTop K-Means by Silhouette")
    print(
        kmeans_results
        .sort_values(
            "silhouette_score",
            ascending=False,
        )
        .head()
        .round(4)
        .to_string(index=False)
    )

    print("\nTop GMM by BIC")
    print(
        gmm_results
        .sort_values("bic")
        .head()
        .round(4)
        .to_string(index=False)
    )

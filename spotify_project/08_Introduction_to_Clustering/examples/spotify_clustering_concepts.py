"""
Spotify Module 08 — Clustering Concepts

Creates an illustrative clustering dataset and demonstrates:
- Hard clustering using K-Means
- Soft clustering using Gaussian Mixture Models
- Centroids
- Cluster labels
- Membership probabilities
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.mixture import GaussianMixture


def create_example_data() -> pd.DataFrame:
    """Create a two-feature illustrative user dataset."""
    X, _ = make_blobs(
        n_samples=480,
        centers=[
            (-4.5, -2.5),
            (-1.0, 3.8),
            (3.7, 3.0),
            (4.2, -3.0),
        ],
        cluster_std=[
            0.95,
            0.85,
            1.05,
            0.90,
        ],
        random_state=42,
    )

    return pd.DataFrame(
        X,
        columns=[
            "listening_intensity_scaled",
            "engagement_consistency_scaled",
        ],
    )


def run_hard_clustering(
    X: pd.DataFrame,
) -> tuple[pd.DataFrame, np.ndarray]:
    """Fit K-Means and return labels and centroids."""
    model = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=20,
    )

    labels = model.fit_predict(X)

    output = X.copy()
    output["cluster"] = labels

    return output, model.cluster_centers_


def run_soft_clustering(
    X: pd.DataFrame,
) -> pd.DataFrame:
    """Fit GMM and return labels and membership probabilities."""
    model = GaussianMixture(
        n_components=4,
        covariance_type="full",
        random_state=42,
        n_init=5,
    )

    model.fit(X)

    labels = model.predict(X)
    probabilities = model.predict_proba(X)

    output = X.copy()
    output["most_likely_cluster"] = labels
    output["membership_confidence"] = (
        probabilities.max(axis=1)
    )

    for index in range(probabilities.shape[1]):
        output[
            f"cluster_{index}_probability"
        ] = probabilities[:, index]

    return output


if __name__ == "__main__":
    example = create_example_data()

    hard_output, centroids = run_hard_clustering(
        example
    )

    soft_output = run_soft_clustering(
        example
    )

    print("Hard Clustering")
    print(
        hard_output.head().to_string(
            index=False
        )
    )

    print("\nCentroids")
    print(centroids)

    print("\nSoft Clustering")
    print(
        soft_output.head().to_string(
            index=False
        )
    )

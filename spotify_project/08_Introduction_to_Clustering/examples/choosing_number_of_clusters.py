"""
Spotify Module 08 — Choosing the Number of Clusters

Runs K-Means for several K values and calculates:
- Inertia
- Silhouette Score
- Cluster counts
- Cluster percentages
"""

from __future__ import annotations

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score


def create_example_data() -> pd.DataFrame:
    """Create illustrative scaled features."""
    X, _ = make_blobs(
        n_samples=480,
        centers=4,
        cluster_std=0.95,
        random_state=42,
    )

    return pd.DataFrame(
        X,
        columns=[
            "feature_1_scaled",
            "feature_2_scaled",
        ],
    )


def evaluate_k_values(
    X: pd.DataFrame,
    minimum_k: int = 2,
    maximum_k: int = 8,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Evaluate multiple K-Means solutions."""
    metric_records = []
    size_records = []

    for k in range(
        minimum_k,
        maximum_k + 1,
    ):
        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=20,
        )

        labels = model.fit_predict(X)

        metric_records.append({
            "k": k,
            "inertia": model.inertia_,
            "silhouette_score": (
                silhouette_score(
                    X,
                    labels,
                )
            ),
        })

        counts = (
            pd.Series(labels)
            .value_counts()
            .sort_index()
        )

        for cluster, count in counts.items():
            size_records.append({
                "k": k,
                "cluster": int(cluster),
                "user_count": int(count),
                "user_percentage": round(
                    100 * count / len(X),
                    2,
                ),
            })

    return (
        pd.DataFrame(metric_records),
        pd.DataFrame(size_records),
    )


if __name__ == "__main__":
    features = create_example_data()

    metrics, sizes = evaluate_k_values(
        features
    )

    print("K Evaluation Metrics")
    print(
        metrics.round(4).to_string(
            index=False
        )
    )

    print("\nCluster Sizes")
    print(
        sizes.to_string(
            index=False
        )
    )

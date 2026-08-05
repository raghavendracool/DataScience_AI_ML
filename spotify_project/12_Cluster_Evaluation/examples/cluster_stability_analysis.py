"""
Spotify Module 12 — Cluster Stability Analysis

Evaluates K-Means stability across random seeds using:
- Adjusted Rand Index
- Cluster-size consistency
- Centroid consistency
"""

from __future__ import annotations

from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.preprocessing import StandardScaler


OUTPUT_DIR = Path("cluster_stability_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

FEATURES = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
    "days_active_last_30",
    "skip_rate",
    "ads_skipped_pct",
]


def fit_seed_runs(
    X_scaled: np.ndarray,
    k: int,
    seeds: list[int],
) -> tuple[
    dict[int, np.ndarray],
    dict[int, np.ndarray],
    pd.DataFrame,
]:
    """Fit one K-Means model per random seed."""
    labels_by_seed = {}
    centroids_by_seed = {}
    size_records = []

    for seed in seeds:
        model = KMeans(
            n_clusters=k,
            init="k-means++",
            n_init=20,
            random_state=seed,
        )

        labels = model.fit_predict(
            X_scaled
        )

        labels_by_seed[seed] = labels
        centroids_by_seed[seed] = (
            model.cluster_centers_
        )

        counts = (
            pd.Series(labels)
            .value_counts()
            .sort_index()
        )

        for cluster, count in counts.items():
            size_records.append({
                "seed": seed,
                "cluster": int(cluster),
                "users": int(count),
                "percentage": (
                    100
                    * count
                    / len(labels)
                ),
            })

    return (
        labels_by_seed,
        centroids_by_seed,
        pd.DataFrame(size_records),
    )


def pairwise_ari_report(
    labels_by_seed: dict[
        int,
        np.ndarray,
    ],
) -> pd.DataFrame:
    """Calculate pairwise ARI across seeds."""
    records = []

    for seed_a, seed_b in combinations(
        labels_by_seed,
        2,
    ):
        records.append({
            "seed_a": seed_a,
            "seed_b": seed_b,
            "adjusted_rand_index": (
                adjusted_rand_score(
                    labels_by_seed[
                        seed_a
                    ],
                    labels_by_seed[
                        seed_b
                    ],
                )
            ),
        })

    return pd.DataFrame(records)


if __name__ == "__main__":
    behavior = pd.read_excel(
        "spotify_user_behavior.xlsx"
    )

    X = behavior[
        FEATURES
    ].copy()

    X_scaled = StandardScaler().fit_transform(
        X
    )

    labels_by_seed, centroids_by_seed, sizes = (
        fit_seed_runs(
            X_scaled,
            k=4,
            seeds=[
                11,
                22,
                33,
                44,
                55,
            ],
        )
    )

    ari_report = pairwise_ari_report(
        labels_by_seed
    )

    ari_report.to_csv(
        OUTPUT_DIR
        / "pairwise_ari.csv",
        index=False,
    )

    sizes.to_csv(
        OUTPUT_DIR
        / "cluster_size_stability.csv",
        index=False,
    )

    print("\nPairwise ARI")
    print(
        ari_report.round(4)
        .to_string(index=False)
    )

    print(
        "\nMean ARI:",
        round(
            ari_report[
                "adjusted_rand_index"
            ].mean(),
            4,
        ),
    )

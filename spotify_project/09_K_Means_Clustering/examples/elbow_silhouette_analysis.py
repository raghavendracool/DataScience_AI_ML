"""
Spotify Module 09 — Elbow and Silhouette Analysis
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


OUTPUT_DIR = Path("kmeans_evaluation_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

FEATURES = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
    "days_active_last_30",
    "skip_rate",
    "ads_skipped_pct",
]


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

    records = []

    for k in range(2, 11):
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
            "smallest_cluster_pct": round(
                100 * counts.min() / len(labels),
                2,
            ),
            "largest_cluster_pct": round(
                100 * counts.max() / len(labels),
                2,
            ),
        })

    evaluation = pd.DataFrame(records)

    evaluation.to_csv(
        OUTPUT_DIR / "kmeans_k_evaluation.csv",
        index=False,
    )

    plt.figure(figsize=(10, 6))
    plt.plot(
        evaluation["k"],
        evaluation["inertia"],
        marker="o",
    )
    plt.title("K-Means Elbow Method")
    plt.xlabel("Number of Clusters (K)")
    plt.ylabel("Inertia")
    plt.xticks(evaluation["k"])
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "elbow_method.png",
        dpi=175,
    )
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(
        evaluation["k"].astype(str),
        evaluation["silhouette_score"],
    )
    plt.title("Silhouette Score by K")
    plt.xlabel("Number of Clusters (K)")
    plt.ylabel("Silhouette Score")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "silhouette_by_k.png",
        dpi=175,
    )
    plt.close()

    print(
        evaluation.round(4)
        .to_string(index=False)
    )

"""
Spotify Module 16 — Cluster Visualization with PCA

Expected input:
- spotify_visualization_data.csv

Creates K-Means labels for demonstration and projects
the standardized feature matrix to two PCA dimensions.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


OUTPUT_DIR = Path(
    "visualization_outputs"
)

OUTPUT_DIR.mkdir(exist_ok=True)

FEATURES = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
    "days_active_last_30",
    "skip_rate",
    "ads_skipped_pct",
    "repeat_track_rate",
    "genre_diversity_score",
    "liked_songs_pct",
]


if __name__ == "__main__":
    data = pd.read_csv(
        "spotify_visualization_data.csv"
    )

    missing = set(FEATURES) - set(
        data.columns
    )

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    X = data[
        FEATURES
    ].copy()

    if X.isna().any().any():
        raise ValueError(
            "Feature matrix contains missing values"
        )

    X_scaled = StandardScaler().fit_transform(
        X
    )

    model = KMeans(
        n_clusters=4,
        n_init=20,
        random_state=42,
    )

    labels = model.fit_predict(
        X_scaled
    )

    pca = PCA(
        n_components=2,
        random_state=42,
    )

    X_pca = pca.fit_transform(
        X_scaled
    )

    plt.figure(figsize=(10, 6))

    for cluster in sorted(
        np.unique(labels)
    ):
        mask = labels == cluster

        plt.scatter(
            X_pca[mask, 0],
            X_pca[mask, 1],
            s=18,
            alpha=0.50,
            label=f"Cluster {cluster}",
        )

    plt.title(
        "K-Means Clusters in PCA Space"
    )
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR
        / "cluster_chart_pca.png",
        dpi=175,
    )

    plt.close()

    explained = (
        pca.explained_variance_ratio_
        .sum()
    )

    print(
        "Two-component explained variance:",
        round(float(explained), 4),
    )

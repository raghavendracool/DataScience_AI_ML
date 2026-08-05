"""
Spotify Module 12 — Evaluation Visualizations

Creates:
- Silhouette plot
- Metric-by-K charts
- Cluster-size chart
- Stability heatmap
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import (
    adjusted_rand_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_samples,
    silhouette_score,
)
from sklearn.preprocessing import StandardScaler


OUTPUT_DIR = Path(
    "cluster_evaluation_images"
)

OUTPUT_DIR.mkdir(exist_ok=True)

FEATURES = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
    "days_active_last_30",
    "skip_rate",
    "ads_skipped_pct",
]


def save_silhouette_plot(
    X: np.ndarray,
    labels: np.ndarray,
    filename: str,
) -> None:
    """Save one silhouette plot."""
    values = silhouette_samples(
        X,
        labels,
    )

    average = silhouette_score(
        X,
        labels,
    )

    plt.figure(figsize=(10, 7))
    y_lower = 10

    for cluster in sorted(
        np.unique(labels)
    ):
        cluster_values = np.sort(
            values[
                labels == cluster
            ]
        )

        size = len(cluster_values)
        y_upper = y_lower + size

        plt.fill_betweenx(
            np.arange(
                y_lower,
                y_upper,
            ),
            0,
            cluster_values,
            alpha=0.65,
        )

        plt.text(
            -0.06,
            y_lower + 0.5 * size,
            str(cluster),
        )

        y_lower = y_upper + 12

    plt.axvline(
        average,
        linestyle="--",
        label=(
            f"Average = "
            f"{average:.3f}"
        ),
    )

    plt.title("Silhouette Plot")
    plt.xlabel("Silhouette Value")
    plt.ylabel("Users by Cluster")
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / filename,
        dpi=175,
    )
    plt.close()


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

    rows = []

    for k in range(2, 9):
        model = KMeans(
            n_clusters=k,
            n_init=20,
            random_state=42,
        )

        labels = model.fit_predict(
            X_scaled
        )

        counts = (
            pd.Series(labels)
            .value_counts()
        )

        rows.append({
            "k": k,
            "silhouette": (
                silhouette_score(
                    X_scaled,
                    labels,
                    sample_size=min(
                        10000,
                        len(labels),
                    ),
                    random_state=42,
                )
            ),
            "davies_bouldin": (
                davies_bouldin_score(
                    X_scaled,
                    labels,
                )
            ),
            "calinski_harabasz": (
                calinski_harabasz_score(
                    X_scaled,
                    labels,
                )
            ),
            "inertia": model.inertia_,
            "smallest_cluster_pct": (
                100
                * counts.min()
                / len(labels)
            ),
            "largest_cluster_pct": (
                100
                * counts.max()
                / len(labels)
            ),
        })

        if k == 4:
            save_silhouette_plot(
                X_scaled,
                labels,
                "silhouette_k4.png",
            )

    metrics = pd.DataFrame(rows)

    for metric, ylabel, filename in [
        (
            "silhouette",
            "Silhouette — Higher Is Better",
            "silhouette_by_k.png",
        ),
        (
            "davies_bouldin",
            "Davies-Bouldin — Lower Is Better",
            "davies_bouldin_by_k.png",
        ),
        (
            "calinski_harabasz",
            "Calinski-Harabasz — Higher Is Better",
            "calinski_harabasz_by_k.png",
        ),
        (
            "inertia",
            "Inertia",
            "inertia_by_k.png",
        ),
    ]:
        plt.figure(figsize=(10, 6))
        plt.plot(
            metrics["k"],
            metrics[metric],
            marker="o",
        )
        plt.title(
            metric.replace(
                "_",
                " ",
            ).title()
            + " by K"
        )
        plt.xlabel("K")
        plt.ylabel(ylabel)
        plt.xticks(metrics["k"])
        plt.tight_layout()
        plt.savefig(
            OUTPUT_DIR / filename,
            dpi=175,
        )
        plt.close()

    print(
        f"Images saved to: "
        f"{OUTPUT_DIR.resolve()}"
    )

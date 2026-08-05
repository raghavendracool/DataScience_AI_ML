"""
Spotify Module 13 — Cluster Profile Visualizations

Expected files:
- cluster_profile_outputs/behavior_means.csv
- cluster_profile_outputs/standardized_profile.csv
- cluster_profile_outputs/demographic_profile.csv
- cluster_profile_outputs/cluster_sizes.csv
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


INPUT_DIR = Path(
    "cluster_profile_outputs"
)

OUTPUT_DIR = Path(
    "cluster_profile_images"
)

OUTPUT_DIR.mkdir(exist_ok=True)


def save_standardized_heatmap(
    profile: pd.DataFrame,
) -> None:
    """Save a standardized cluster-feature heatmap."""
    indexed = profile.set_index(
        "cluster"
    )

    values = indexed.to_numpy()

    plt.figure(figsize=(13, 7))
    plt.imshow(
        values,
        aspect="auto",
        vmin=-2,
        vmax=2,
    )

    plt.colorbar(
        label="Standardized Cluster Mean"
    )

    plt.xticks(
        range(len(indexed.columns)),
        [
            column.replace(
                "_",
                "\n",
            )
            for column in indexed.columns
        ],
    )

    plt.yticks(
        range(len(indexed.index)),
        indexed.index,
    )

    for row in range(values.shape[0]):
        for col in range(
            values.shape[1]
        ):
            plt.text(
                col,
                row,
                f"{values[row, col]:.1f}",
                ha="center",
                va="center",
                fontsize=8,
            )

    plt.title(
        "Standardized Cluster Profile"
    )
    plt.xlabel("Feature")
    plt.ylabel("Cluster")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR
        / "standardized_profile_heatmap.png",
        dpi=175,
    )
    plt.close()


def save_cluster_sizes(
    sizes: pd.DataFrame,
) -> None:
    """Save cluster-size bar chart."""
    plt.figure(figsize=(10, 6))
    plt.bar(
        sizes["cluster"].astype(str),
        sizes["user_count"],
    )
    plt.title("Cluster Size")
    plt.xlabel("Cluster")
    plt.ylabel("Users")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR
        / "cluster_sizes.png",
        dpi=175,
    )
    plt.close()


def save_behavior_comparison(
    means: pd.DataFrame,
) -> None:
    """Save selected original-unit feature comparisons."""
    selected = [
        "daily_listening_minutes",
        "sessions_per_day",
        "days_active_last_30",
    ]

    x = np.arange(
        len(means)
    )

    normalized = means[
        selected
    ].copy()

    normalized = (
        normalized
        - normalized.min()
    ) / (
        normalized.max()
        - normalized.min()
    )

    width = 0.25

    plt.figure(figsize=(11, 6))

    for index, feature in enumerate(
        selected
    ):
        plt.bar(
            x + (
                index - 1
            ) * width,
            normalized[feature],
            width,
            label=feature,
        )

    plt.title(
        "Normalized Behavior Comparison"
    )
    plt.xlabel("Cluster")
    plt.ylabel("Relative Level")
    plt.xticks(
        x,
        means["cluster"].astype(str),
    )
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR
        / "behavior_comparison.png",
        dpi=175,
    )
    plt.close()


if __name__ == "__main__":
    means = pd.read_csv(
        INPUT_DIR
        / "behavior_means.csv"
    )

    standardized = pd.read_csv(
        INPUT_DIR
        / "standardized_profile.csv"
    )

    sizes = pd.read_csv(
        INPUT_DIR
        / "cluster_sizes.csv"
    )

    save_standardized_heatmap(
        standardized
    )

    save_cluster_sizes(
        sizes
    )

    save_behavior_comparison(
        means
    )

    print(
        f"Images saved to: "
        f"{OUTPUT_DIR.resolve()}"
    )

"""
Spotify Module 09 — K-Means Iteration Visualization

Creates separate images for:
- Initial centroids
- First assignment
- First centroid recalculation
- Converged solution
- Centroid movement by iteration
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs


OUTPUT_DIR = Path("kmeans_iteration_images")
OUTPUT_DIR.mkdir(exist_ok=True)


def assign_labels(
    data: np.ndarray,
    centers: np.ndarray,
) -> np.ndarray:
    """Assign points to nearest centroids."""
    distances = np.linalg.norm(
        data[:, np.newaxis, :]
        - centers[np.newaxis, :, :],
        axis=2,
    )

    return distances.argmin(axis=1)


def update_centers(
    data: np.ndarray,
    labels: np.ndarray,
    old_centers: np.ndarray,
) -> np.ndarray:
    """Recalculate cluster means."""
    updated = []

    for cluster_id in range(
        len(old_centers)
    ):
        members = data[
            labels == cluster_id
        ]

        if len(members) == 0:
            updated.append(
                old_centers[cluster_id]
            )
        else:
            updated.append(
                members.mean(axis=0)
            )

    return np.array(updated)


def save_plot(
    data: np.ndarray,
    labels: np.ndarray | None,
    centers: np.ndarray,
    title: str,
    filename: str,
) -> None:
    """Save one clustering step."""
    plt.figure(figsize=(10, 6))

    if labels is None:
        plt.scatter(
            data[:, 0],
            data[:, 1],
            alpha=0.62,
            s=25,
        )
    else:
        for cluster_id in np.unique(labels):
            subset = data[
                labels == cluster_id
            ]

            plt.scatter(
                subset[:, 0],
                subset[:, 1],
                alpha=0.65,
                s=25,
                label=f"Cluster {cluster_id}",
            )

    plt.scatter(
        centers[:, 0],
        centers[:, 1],
        marker="X",
        s=230,
        linewidths=1.5,
        label="Centroids",
    )

    plt.title(title)
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / filename,
        dpi=175,
    )
    plt.close()


if __name__ == "__main__":
    X, _ = make_blobs(
        n_samples=520,
        centers=4,
        cluster_std=0.95,
        random_state=42,
    )

    centers = np.array([
        [-5.7, 4.7],
        [-3.2, -4.7],
        [1.5, 0.5],
        [5.5, 4.7],
    ])

    save_plot(
        X,
        None,
        centers,
        "Initial Centroids",
        "01_initial_centroids.png",
    )

    first_labels = assign_labels(
        X,
        centers,
    )

    save_plot(
        X,
        first_labels,
        centers,
        "First Assignment",
        "02_first_assignment.png",
    )

    centers = update_centers(
        X,
        first_labels,
        centers,
    )

    save_plot(
        X,
        first_labels,
        centers,
        "First Centroid Recalculation",
        "03_first_recalculation.png",
    )

    movement = []

    for iteration in range(1, 50):
        labels = assign_labels(
            X,
            centers,
        )

        new_centers = update_centers(
            X,
            labels,
            centers,
        )

        max_move = np.linalg.norm(
            new_centers - centers,
            axis=1,
        ).max()

        movement.append({
            "iteration": iteration,
            "movement": max_move,
        })

        centers = new_centers

        if max_move < 1e-4:
            break

    final_labels = assign_labels(
        X,
        centers,
    )

    save_plot(
        X,
        final_labels,
        centers,
        "Converged K-Means Solution",
        "04_converged_solution.png",
    )

    iterations = [
        row["iteration"]
        for row in movement
    ]

    movements = [
        row["movement"]
        for row in movement
    ]

    plt.figure(figsize=(10, 6))
    plt.plot(
        iterations,
        movements,
        marker="o",
    )
    plt.title(
        "Centroid Movement by Iteration"
    )
    plt.xlabel("Iteration")
    plt.ylabel("Maximum Centroid Movement")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR
        / "05_centroid_movement.png",
        dpi=175,
    )
    plt.close()

    print(
        f"Images saved to: "
        f"{OUTPUT_DIR.resolve()}"
    )

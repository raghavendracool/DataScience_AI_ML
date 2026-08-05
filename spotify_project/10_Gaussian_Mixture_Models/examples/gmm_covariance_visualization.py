"""
Spotify Module 10 — GMM Covariance-Type Visualizations

Creates one image for each covariance type using illustrative
two-dimensional behavior data.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
from sklearn.mixture import GaussianMixture


OUTPUT_DIR = Path("gmm_covariance_images")
OUTPUT_DIR.mkdir(exist_ok=True)


def covariance_ellipse(
    mean: np.ndarray,
    covariance: np.ndarray,
    n_std: float = 2.0,
) -> Ellipse:
    """Create a two-dimensional covariance ellipse."""
    eigenvalues, eigenvectors = np.linalg.eigh(
        covariance
    )

    order = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    angle = math.degrees(
        math.atan2(
            eigenvectors[1, 0],
            eigenvectors[0, 0],
        )
    )

    width, height = (
        2 * n_std * np.sqrt(
            eigenvalues
        )
    )

    return Ellipse(
        xy=mean,
        width=width,
        height=height,
        angle=angle,
        fill=False,
        linewidth=2.2,
    )


def covariance_matrix(
    model: GaussianMixture,
    component: int,
) -> np.ndarray:
    """Return a full 2-D matrix for any covariance type."""
    if model.covariance_type == "full":
        return model.covariances_[
            component
        ]

    if model.covariance_type == "tied":
        return model.covariances_

    if model.covariance_type == "diag":
        return np.diag(
            model.covariances_[
                component
            ]
        )

    if model.covariance_type == "spherical":
        return (
            np.eye(2)
            * model.covariances_[
                component
            ]
        )

    raise ValueError(
        model.covariance_type
    )


def save_model_plot(
    X: np.ndarray,
    model: GaussianMixture,
) -> None:
    """Save one chart for one covariance type."""
    labels = model.predict(X)

    plt.figure(figsize=(10, 6))
    ax = plt.gca()

    for component in range(
        model.n_components
    ):
        mask = labels == component

        plt.scatter(
            X[mask, 0],
            X[mask, 1],
            s=24,
            alpha=0.60,
            label=f"Component {component}",
        )

        ax.add_patch(
            covariance_ellipse(
                model.means_[component],
                covariance_matrix(
                    model,
                    component,
                ),
            )
        )

    plt.scatter(
        model.means_[:, 0],
        model.means_[:, 1],
        marker="X",
        s=220,
        linewidths=1.5,
        label="Means",
    )

    plt.title(
        f"GMM Covariance Type: "
        f"{model.covariance_type}"
    )
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR
        / (
            f"gmm_"
            f"{model.covariance_type}"
            f"_covariance.png"
        ),
        dpi=175,
    )
    plt.close()


if __name__ == "__main__":
    rng = np.random.default_rng(42)

    group_1 = rng.multivariate_normal(
        [-4.0, -2.5],
        [[1.7, 1.15], [1.15, 1.25]],
        size=190,
    )

    group_2 = rng.multivariate_normal(
        [0.0, 3.4],
        [[0.65, -0.28], [-0.28, 1.55]],
        size=170,
    )

    group_3 = rng.multivariate_normal(
        [4.2, -0.4],
        [[1.35, -0.85], [-0.85, 0.85]],
        size=190,
    )

    X = np.vstack(
        [
            group_1,
            group_2,
            group_3,
        ]
    )

    for covariance_type in [
        "full",
        "tied",
        "diag",
        "spherical",
    ]:
        model = GaussianMixture(
            n_components=3,
            covariance_type=(
                covariance_type
            ),
            n_init=10,
            max_iter=300,
            tol=1e-4,
            reg_covar=1e-6,
            random_state=42,
        )

        model.fit(X)
        save_model_plot(X, model)

    print(
        f"Images saved to: "
        f"{OUTPUT_DIR.resolve()}"
    )

"""
Spotify Module 10 — Expectation-Maximization Demonstration

Uses warm_start with one EM iteration at a time to record:
- Means
- Weights
- Average lower bound
- Responsibilities
"""

from __future__ import annotations

import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture


def create_data() -> np.ndarray:
    """Create illustrative overlapping Gaussian groups."""
    rng = np.random.default_rng(42)

    groups = [
        rng.multivariate_normal(
            [-4.0, -2.5],
            [[1.7, 1.15], [1.15, 1.25]],
            size=190,
        ),
        rng.multivariate_normal(
            [0.0, 3.4],
            [[0.65, -0.28], [-0.28, 1.55]],
            size=170,
        ),
        rng.multivariate_normal(
            [4.2, -0.4],
            [[1.35, -0.85], [-0.85, 0.85]],
            size=190,
        ),
    ]

    return np.vstack(groups)


if __name__ == "__main__":
    X = create_data()

    model = GaussianMixture(
        n_components=3,
        covariance_type="full",
        n_init=1,
        max_iter=1,
        tol=1e-9,
        reg_covar=1e-6,
        warm_start=True,
        init_params="random",
        random_state=7,
    )

    records = []

    for iteration in range(1, 31):
        model.fit(X)

        responsibilities = (
            model.predict_proba(X)
        )

        records.append({
            "iteration": iteration,
            "lower_bound": (
                model.lower_bound_
            ),
            "weight_0": (
                model.weights_[0]
            ),
            "weight_1": (
                model.weights_[1]
            ),
            "weight_2": (
                model.weights_[2]
            ),
            "mean_confidence": (
                responsibilities.max(
                    axis=1
                )
                .mean()
            ),
        })

    history = pd.DataFrame(records)

    history.to_csv(
        "gmm_em_iteration_history.csv",
        index=False,
    )

    print(
        history.round(6)
        .to_string(index=False)
    )

    print("\nFinal Means")
    print(model.means_)

    print("\nFinal Weights")
    print(model.weights_)

    print("\nConverged Flag")
    print(model.converged_)

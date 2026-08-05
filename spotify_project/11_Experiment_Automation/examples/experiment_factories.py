"""
Module 11 — Preprocessor and Model Factories
"""

from __future__ import annotations

from typing import Any

from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import (
    MinMaxScaler,
    PowerTransformer,
    QuantileTransformer,
    RobustScaler,
    StandardScaler,
)


def build_preprocessor(
    name: str,
    row_count: int,
    random_state: int = 42,
) -> Any:
    """Build one fitted-later preprocessor from a name."""
    name = name.lower().strip()

    if name == "standard":
        return StandardScaler()

    if name == "minmax":
        return MinMaxScaler()

    if name == "robust":
        return RobustScaler()

    if name == "power":
        return PowerTransformer(
            method="yeo-johnson",
            standardize=True,
        )

    if name == "quantile_normal":
        return QuantileTransformer(
            n_quantiles=min(
                1000,
                row_count,
            ),
            output_distribution="normal",
            random_state=random_state,
        )

    raise ValueError(
        f"Unsupported preprocessor: {name}"
    )


def build_kmeans(
    k: int,
    random_state: int = 42,
) -> KMeans:
    """Build one K-Means model."""
    if k < 2:
        raise ValueError(
            "K must be at least 2"
        )

    return KMeans(
        n_clusters=k,
        init="k-means++",
        n_init=20,
        max_iter=300,
        tol=1e-4,
        random_state=random_state,
    )


def build_gmm(
    components: int,
    covariance_type: str,
    random_state: int = 42,
) -> GaussianMixture:
    """Build one Gaussian Mixture Model."""
    allowed_covariance_types = {
        "full",
        "tied",
        "diag",
        "spherical",
    }

    if components < 2:
        raise ValueError(
            "Components must be at least 2"
        )

    if covariance_type not in (
        allowed_covariance_types
    ):
        raise ValueError(
            "Unsupported covariance type: "
            f"{covariance_type}"
        )

    return GaussianMixture(
        n_components=components,
        covariance_type=covariance_type,
        tol=1e-4,
        reg_covar=1e-6,
        max_iter=300,
        n_init=10,
        init_params="kmeans",
        random_state=random_state,
    )

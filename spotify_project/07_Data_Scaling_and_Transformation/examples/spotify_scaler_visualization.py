"""
Spotify Module 07 — Scaler Output Visualizations

Run this script beside spotify_user_behavior.xlsx.
It generates one chart per figure inside scaling_images/.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import (
    MinMaxScaler,
    PowerTransformer,
    QuantileTransformer,
    RobustScaler,
    StandardScaler,
)


OUTPUT_DIR = Path("scaling_images")
OUTPUT_DIR.mkdir(exist_ok=True)

FEATURE = "daily_listening_minutes"


def save_histogram(
    values: np.ndarray | pd.Series,
    title: str,
    xlabel: str,
    filename: str,
) -> None:
    """Save one histogram per figure."""
    plt.figure(figsize=(10, 6))
    plt.hist(values, bins=60)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Number of Users")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / filename,
        dpi=170,
    )
    plt.close()


def save_scatter(
    x: np.ndarray | pd.Series,
    y: np.ndarray | pd.Series,
    title: str,
    xlabel: str,
    ylabel: str,
    filename: str,
) -> None:
    """Save one scatter plot per figure."""
    plt.figure(figsize=(10, 6))
    plt.scatter(
        x,
        y,
        alpha=0.28,
        s=12,
    )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / filename,
        dpi=170,
    )
    plt.close()


def main() -> None:
    behavior = pd.read_excel(
        "spotify_user_behavior.xlsx"
    )

    required = {
        FEATURE,
        "sessions_per_day",
    }

    missing = required - set(behavior.columns)

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    feature_data = behavior[[FEATURE]].copy()

    if feature_data.isna().any().any():
        raise ValueError(
            f"{FEATURE} contains missing values"
        )

    standard = StandardScaler().fit_transform(
        feature_data
    ).ravel()

    minmax = MinMaxScaler().fit_transform(
        feature_data
    ).ravel()

    robust = RobustScaler().fit_transform(
        feature_data
    ).ravel()

    log_values = np.log1p(
        feature_data[FEATURE].to_numpy()
    )

    power = PowerTransformer(
        method="yeo-johnson",
        standardize=True,
    ).fit_transform(
        feature_data
    ).ravel()

    n_quantiles = min(
        1000,
        len(feature_data),
    )

    quantile_normal = QuantileTransformer(
        n_quantiles=n_quantiles,
        output_distribution="normal",
        random_state=42,
    ).fit_transform(
        feature_data
    ).ravel()

    quantile_uniform = QuantileTransformer(
        n_quantiles=n_quantiles,
        output_distribution="uniform",
        random_state=42,
    ).fit_transform(
        feature_data
    ).ravel()

    save_histogram(
        feature_data[FEATURE],
        "Before Transformation: Daily Listening Minutes",
        "Daily Listening Minutes",
        "01_before_transformation.png",
    )

    save_histogram(
        standard,
        "After StandardScaler",
        "Standardized Value",
        "02_after_standard_scaler.png",
    )

    save_histogram(
        minmax,
        "After MinMaxScaler",
        "Scaled Value",
        "03_after_minmax_scaler.png",
    )

    save_histogram(
        robust,
        "After RobustScaler",
        "Robust-Scaled Value",
        "04_after_robust_scaler.png",
    )

    save_histogram(
        log_values,
        "After Log Transformation: log1p(x)",
        "Log-Transformed Value",
        "05_after_log_transformation.png",
    )

    save_histogram(
        power,
        "After PowerTransformer: Yeo-Johnson",
        "Transformed Value",
        "06_after_power_transformer.png",
    )

    save_histogram(
        quantile_normal,
        "After QuantileTransformer: Normal Output",
        "Quantile-Normal Value",
        "07_after_quantile_normal.png",
    )

    save_histogram(
        quantile_uniform,
        "After QuantileTransformer: Uniform Output",
        "Quantile-Uniform Value",
        "08_after_quantile_uniform.png",
    )

    raw_two = behavior[
        [
            "sessions_per_day",
            FEATURE,
        ]
    ].copy()

    save_scatter(
        raw_two["sessions_per_day"],
        raw_two[FEATURE],
        "Before Scaling: Unequal Feature Magnitudes",
        "Sessions per Day",
        "Daily Listening Minutes",
        "09_before_scaling_two_features.png",
    )

    scaled_two = StandardScaler().fit_transform(
        raw_two
    )

    save_scatter(
        scaled_two[:, 0],
        scaled_two[:, 1],
        "After StandardScaler: Comparable Feature Magnitudes",
        "Sessions per Day (Standardized)",
        "Daily Listening Minutes (Standardized)",
        "10_after_standard_scaling_two_features.png",
    )

    print(
        f"Images saved to: {OUTPUT_DIR.resolve()}"
    )


if __name__ == "__main__":
    main()

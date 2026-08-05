"""
Spotify Module 07 — Transformation Comparison Report

Creates one table comparing location, spread, range and skewness
before and after each preprocessing method.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.preprocessing import (
    MinMaxScaler,
    PowerTransformer,
    QuantileTransformer,
    RobustScaler,
    StandardScaler,
)


FEATURE = "daily_listening_minutes"


def summarize(
    name: str,
    values: np.ndarray,
) -> dict[str, float | str]:
    """Summarize one transformed feature."""
    series = pd.Series(values)

    return {
        "method": name,
        "mean": round(series.mean(), 4),
        "median": round(series.median(), 4),
        "std_population": round(
            series.std(ddof=0),
            4,
        ),
        "minimum": round(series.min(), 4),
        "maximum": round(series.max(), 4),
        "skewness": round(series.skew(), 4),
    }


if __name__ == "__main__":
    behavior = pd.read_excel(
        "spotify_user_behavior.xlsx"
    )

    X = behavior[[FEATURE]].copy()

    n_quantiles = min(
        1000,
        len(X),
    )

    outputs = {
        "raw": X.iloc[:, 0].to_numpy(),
        "standard": (
            StandardScaler()
            .fit_transform(X)
            .ravel()
        ),
        "minmax": (
            MinMaxScaler()
            .fit_transform(X)
            .ravel()
        ),
        "robust": (
            RobustScaler()
            .fit_transform(X)
            .ravel()
        ),
        "log1p": np.log1p(
            X.iloc[:, 0].to_numpy()
        ),
        "power_yeo_johnson": (
            PowerTransformer(
                method="yeo-johnson",
                standardize=True,
            )
            .fit_transform(X)
            .ravel()
        ),
        "quantile_normal": (
            QuantileTransformer(
                n_quantiles=n_quantiles,
                output_distribution="normal",
                random_state=42,
            )
            .fit_transform(X)
            .ravel()
        ),
        "quantile_uniform": (
            QuantileTransformer(
                n_quantiles=n_quantiles,
                output_distribution="uniform",
                random_state=42,
            )
            .fit_transform(X)
            .ravel()
        ),
    }

    report = pd.DataFrame(
        [
            summarize(name, values)
            for name, values in outputs.items()
        ]
    )

    report.to_csv(
        "spotify_scaler_comparison.csv",
        index=False,
    )

    print(
        report.to_string(
            index=False
        )
    )

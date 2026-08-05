"""
Spotify Module 07 — Reusable Scaling and Transformation Pipeline

This script:
- Loads Spotify behavior data
- Removes user_id
- Validates numeric features
- Creates multiple preprocessing experiments
- Produces transformed DataFrames
- Creates a comparison report
- Saves fitted preprocessors
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    FunctionTransformer,
    MinMaxScaler,
    PowerTransformer,
    QuantileTransformer,
    RobustScaler,
    StandardScaler,
)


CORE_FEATURES = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
    "days_active_last_30",
    "skip_rate",
    "ads_skipped_pct",
]

LOG_CANDIDATE_FEATURES = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
]

RATE_FEATURES = [
    "skip_rate",
    "ads_skipped_pct",
]

OUTPUT_DIR = Path("scaling_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


@dataclass(frozen=True)
class ScalingResult:
    """One fitted preprocessing experiment."""

    name: str
    transformed: pd.DataFrame
    transformer: Any
    summary: pd.DataFrame


def validate_features(
    df: pd.DataFrame,
    features: list[str],
) -> None:
    """Validate the model feature matrix."""
    missing_columns = set(features) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing features: {sorted(missing_columns)}"
        )

    non_numeric = (
        df[features]
        .select_dtypes(exclude="number")
        .columns
        .tolist()
    )

    if non_numeric:
        raise TypeError(
            f"Non-numeric features: {non_numeric}"
        )

    if df[features].isna().any().any():
        raise ValueError(
            "Missing values exist in the feature matrix"
        )

    if not np.isfinite(
        df[features].to_numpy(dtype=float)
    ).all():
        raise ValueError(
            "Infinite values exist in the feature matrix"
        )


def create_summary(
    transformed: pd.DataFrame,
) -> pd.DataFrame:
    """Create a feature-level transformation summary."""
    summary = pd.DataFrame({
        "feature": transformed.columns,
        "mean": transformed.mean().values,
        "median": transformed.median().values,
        "std_population": (
            transformed.std(ddof=0).values
        ),
        "minimum": transformed.min().values,
        "maximum": transformed.max().values,
        "skewness": transformed.skew().values,
    })

    return summary.round(4)


def fit_experiment(
    name: str,
    transformer: Any,
    X: pd.DataFrame,
) -> ScalingResult:
    """Fit one transformer and return labeled output."""
    values = transformer.fit_transform(X)

    transformed = pd.DataFrame(
        values,
        columns=X.columns,
        index=X.index,
    )

    if transformed.isna().any().any():
        raise ValueError(
            f"{name} created missing values"
        )

    if not np.isfinite(
        transformed.to_numpy(dtype=float)
    ).all():
        raise ValueError(
            f"{name} created infinite values"
        )

    return ScalingResult(
        name=name,
        transformed=transformed,
        transformer=transformer,
        summary=create_summary(transformed),
    )


def build_log_standard_transformer(
    features: list[str],
) -> ColumnTransformer:
    """
    Apply log1p to selected non-negative features and then
    standardize both feature groups.
    """
    log_features = [
        feature
        for feature in LOG_CANDIDATE_FEATURES
        if feature in features
    ]

    remaining_features = [
        feature
        for feature in features
        if feature not in log_features
    ]

    log_standard = (
        FunctionTransformer(
            np.log1p,
            feature_names_out="one-to-one",
        )
    )

    from sklearn.pipeline import Pipeline

    transformers = []

    if log_features:
        transformers.append(
            (
                "log_then_standard",
                Pipeline(
                    steps=[
                        (
                            "log1p",
                            log_standard,
                        ),
                        (
                            "standard",
                            StandardScaler(),
                        ),
                    ]
                ),
                log_features,
            )
        )

    if remaining_features:
        transformers.append(
            (
                "standard_only",
                StandardScaler(),
                remaining_features,
            )
        )

    return ColumnTransformer(
        transformers=transformers,
        remainder="drop",
        verbose_feature_names_out=False,
    ).set_output(transform="pandas")


def run_scaling_experiments(
    behavior: pd.DataFrame,
    features: list[str] | None = None,
) -> dict[str, ScalingResult]:
    """Fit all candidate preprocessing methods."""
    selected_features = (
        features
        if features is not None
        else CORE_FEATURES
    )

    validate_features(
        behavior,
        selected_features,
    )

    X = behavior[
        selected_features
    ].copy()

    n_quantiles = min(
        1000,
        len(X),
    )

    experiments = {
        "standard": StandardScaler(),
        "minmax": MinMaxScaler(),
        "robust": RobustScaler(),
        "power_yeo_johnson": PowerTransformer(
            method="yeo-johnson",
            standardize=True,
        ),
        "quantile_normal": QuantileTransformer(
            n_quantiles=n_quantiles,
            output_distribution="normal",
            random_state=42,
        ),
        "quantile_uniform": QuantileTransformer(
            n_quantiles=n_quantiles,
            output_distribution="uniform",
            random_state=42,
        ),
        "log_standard": build_log_standard_transformer(
            selected_features
        ),
    }

    results = {}

    for name, transformer in experiments.items():
        result = fit_experiment(
            name=name,
            transformer=transformer,
            X=X,
        )

        results[name] = result

        result.transformed.to_csv(
            OUTPUT_DIR
            / f"spotify_features_{name}.csv",
            index=False,
        )

        result.summary.to_csv(
            OUTPUT_DIR
            / f"spotify_summary_{name}.csv",
            index=False,
        )

        joblib.dump(
            result.transformer,
            OUTPUT_DIR
            / f"spotify_transformer_{name}.joblib",
        )

    return results


if __name__ == "__main__":
    behavior_df = pd.read_excel(
        "spotify_user_behavior.xlsx"
    )

    outputs = run_scaling_experiments(
        behavior_df
    )

    for experiment_name, result in outputs.items():
        print(
            "\n",
            experiment_name,
            result.transformed.shape,
        )
        print(
            result.summary.to_string(
                index=False
            )
        )

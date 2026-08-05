"""
Spotify Module 10 — End-to-End Gaussian Mixture Model Pipeline

Expected input:
- spotify_user_behavior.xlsx
- spotify_user_demo.xlsx

Outputs:
- Component/covariance evaluation
- Hard labels
- Membership probabilities
- Confidence and uncertainty
- Component sizes
- Means, weights and covariance metadata
- Behavior and demographic profiles
- Saved scaler, feature order and GMM model
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler


OUTPUT_DIR = Path("gmm_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

FEATURES = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
    "days_active_last_30",
    "skip_rate",
    "ads_skipped_pct",
]

COVARIANCE_TYPES = [
    "full",
    "tied",
    "diag",
    "spherical",
]


@dataclass(frozen=True)
class GMMOutput:
    """Container for final GMM artifacts."""

    evaluation: pd.DataFrame
    user_membership: pd.DataFrame
    component_sizes: pd.DataFrame
    component_means_scaled: pd.DataFrame
    component_means_original: pd.DataFrame
    component_weights: pd.DataFrame
    behavior_profile: pd.DataFrame
    demographic_profile: pd.DataFrame


def validate_input(
    behavior: pd.DataFrame,
) -> None:
    """Validate the Spotify feature matrix."""
    required = {"user_id", *FEATURES}
    missing = required - set(behavior.columns)

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    if behavior["user_id"].isna().any():
        raise ValueError(
            "user_id contains missing values"
        )

    if not behavior["user_id"].is_unique:
        raise ValueError(
            "user_id is not unique"
        )

    non_numeric = (
        behavior[FEATURES]
        .select_dtypes(exclude="number")
        .columns
        .tolist()
    )

    if non_numeric:
        raise TypeError(
            f"Non-numeric features: {non_numeric}"
        )

    if behavior[FEATURES].isna().any().any():
        raise ValueError(
            "Feature matrix contains missing values"
        )

    if not np.isfinite(
        behavior[FEATURES]
        .to_numpy(dtype=float)
    ).all():
        raise ValueError(
            "Feature matrix contains infinite values"
        )


def safe_silhouette(
    X_scaled: np.ndarray,
    labels: np.ndarray,
) -> float:
    """Calculate Silhouette only when valid."""
    unique_labels = np.unique(labels)

    if len(unique_labels) < 2:
        return float("nan")

    if len(unique_labels) >= len(labels):
        return float("nan")

    return float(
        silhouette_score(
            X_scaled,
            labels,
        )
    )


def evaluate_gmm_models(
    X_scaled: np.ndarray,
    min_components: int = 2,
    max_components: int = 10,
) -> pd.DataFrame:
    """Evaluate component and covariance combinations."""
    records = []

    for components in range(
        min_components,
        max_components + 1,
    ):
        for covariance_type in COVARIANCE_TYPES:
            model = GaussianMixture(
                n_components=components,
                covariance_type=covariance_type,
                tol=1e-4,
                reg_covar=1e-6,
                max_iter=300,
                n_init=10,
                init_params="kmeans",
                random_state=42,
            )

            model.fit(X_scaled)

            labels = model.predict(
                X_scaled
            )

            probabilities = (
                model.predict_proba(
                    X_scaled
                )
            )

            confidence = probabilities.max(
                axis=1
            )

            counts = pd.Series(
                labels
            ).value_counts()

            records.append({
                "components": components,
                "covariance_type": covariance_type,
                "aic": model.aic(X_scaled),
                "bic": model.bic(X_scaled),
                "average_log_likelihood": (
                    model.score(X_scaled)
                ),
                "silhouette_score": (
                    safe_silhouette(
                        X_scaled,
                        labels,
                    )
                ),
                "minimum_component_pct": round(
                    100
                    * counts.min()
                    / len(labels),
                    2,
                ),
                "maximum_component_pct": round(
                    100
                    * counts.max()
                    / len(labels),
                    2,
                ),
                "mean_membership_confidence": (
                    confidence.mean()
                ),
                "p10_membership_confidence": (
                    np.quantile(
                        confidence,
                        0.10,
                    )
                ),
                "converged": model.converged_,
                "iterations": model.n_iter_,
                "lower_bound": model.lower_bound_,
            })

    return pd.DataFrame(records)


def create_membership_output(
    user_ids: pd.DataFrame,
    model: GaussianMixture,
    X_scaled: np.ndarray,
) -> pd.DataFrame:
    """Create labels, probabilities and confidence."""
    labels = model.predict(
        X_scaled
    )

    probabilities = model.predict_proba(
        X_scaled
    )

    probability_columns = [
        f"component_{index}_probability"
        for index in range(
            model.n_components
        )
    ]

    probability_df = pd.DataFrame(
        probabilities,
        columns=probability_columns,
        index=user_ids.index,
    )

    output = pd.concat(
        [
            user_ids.copy(),
            probability_df,
        ],
        axis=1,
    )

    output["gmm_component"] = labels

    output["membership_confidence"] = (
        probabilities.max(axis=1)
    )

    sorted_probabilities = np.sort(
        probabilities,
        axis=1,
    )

    output["probability_margin"] = (
        sorted_probabilities[:, -1]
        - sorted_probabilities[:, -2]
    )

    output["boundary_user_example"] = (
        output[
            "membership_confidence"
        ] < 0.70
    )

    return output


def component_size_report(
    membership: pd.DataFrame,
) -> pd.DataFrame:
    """Create component count and percentage report."""
    report = (
        membership[
            "gmm_component"
        ]
        .value_counts()
        .sort_index()
        .rename_axis(
            "gmm_component"
        )
        .reset_index(
            name="users"
        )
    )

    report["percentage"] = (
        report["users"]
        .div(report["users"].sum())
        .mul(100)
        .round(2)
    )

    return report


def component_parameter_tables(
    model: GaussianMixture,
    scaler: StandardScaler,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    """Create component mean and weight tables."""
    scaled_means = pd.DataFrame(
        model.means_,
        columns=FEATURES,
    )

    scaled_means.insert(
        0,
        "gmm_component",
        range(model.n_components),
    )

    original_values = scaler.inverse_transform(
        model.means_
    )

    original_means = pd.DataFrame(
        original_values,
        columns=FEATURES,
    )

    original_means.insert(
        0,
        "gmm_component",
        range(model.n_components),
    )

    weights = pd.DataFrame({
        "gmm_component": range(
            model.n_components
        ),
        "mixture_weight": model.weights_,
    })

    return (
        scaled_means.round(4),
        original_means.round(4),
        weights.round(6),
    )


def behavior_profile_report(
    behavior: pd.DataFrame,
    membership: pd.DataFrame,
) -> pd.DataFrame:
    """Create mean, median and confidence profiles."""
    joined = behavior.merge(
        membership[
            [
                "user_id",
                "gmm_component",
                "membership_confidence",
                "probability_margin",
            ]
        ],
        on="user_id",
        how="inner",
        validate="one_to_one",
    )

    mean_profile = (
        joined
        .groupby(
            "gmm_component"
        )[FEATURES]
        .mean()
        .add_suffix("_mean")
    )

    median_profile = (
        joined
        .groupby(
            "gmm_component"
        )[FEATURES]
        .median()
        .add_suffix("_median")
    )

    confidence_profile = (
        joined
        .groupby("gmm_component")
        .agg(
            users=("user_id", "nunique"),
            mean_confidence=(
                "membership_confidence",
                "mean",
            ),
            median_confidence=(
                "membership_confidence",
                "median",
            ),
            mean_probability_margin=(
                "probability_margin",
                "mean",
            ),
        )
    )

    return (
        confidence_profile
        .join(mean_profile)
        .join(median_profile)
        .reset_index()
        .round(4)
    )


def demographic_profile_report(
    demo: pd.DataFrame,
    membership: pd.DataFrame,
) -> pd.DataFrame:
    """Create demographic component profiles."""
    joined = membership[
        [
            "user_id",
            "gmm_component",
        ]
    ].merge(
        demo,
        on="user_id",
        how="inner",
        validate="one_to_one",
    )

    numeric = (
        joined
        .groupby(
            "gmm_component"
        )
        .agg(
            users=("user_id", "nunique"),
            avg_age=("age", "mean"),
            median_age=("age", "median"),
            avg_tenure=(
                "subscription_tenure_months",
                "mean",
            ),
            median_tenure=(
                "subscription_tenure_months",
                "median",
            ),
        )
        .reset_index()
    )

    category_rows = []

    for component, group in joined.groupby(
        "gmm_component"
    ):
        category_rows.append({
            "gmm_component": component,
            "top_country": (
                group["country"]
                .mode()
                .iloc[0]
            ),
            "top_city_tier": (
                group["city_tier"]
                .mode()
                .iloc[0]
            ),
            "top_device_type": (
                group["device_type"]
                .mode()
                .iloc[0]
            ),
        })

    return (
        numeric
        .merge(
            pd.DataFrame(
                category_rows
            ),
            on="gmm_component",
            how="left",
            validate="one_to_one",
        )
        .round(3)
    )


def run_pipeline(
    behavior: pd.DataFrame,
    demo: pd.DataFrame,
    final_components: int = 4,
    final_covariance_type: str = "full",
) -> GMMOutput:
    """Run model search and fit final GMM."""
    validate_input(behavior)

    user_ids = behavior[
        ["user_id"]
    ].copy()

    X = behavior[
        FEATURES
    ].copy()

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(
        X
    )

    evaluation = evaluate_gmm_models(
        X_scaled
    )

    final_model = GaussianMixture(
        n_components=final_components,
        covariance_type=(
            final_covariance_type
        ),
        tol=1e-4,
        reg_covar=1e-6,
        max_iter=300,
        n_init=10,
        init_params="kmeans",
        random_state=42,
    )

    final_model.fit(
        X_scaled
    )

    membership = create_membership_output(
        user_ids,
        final_model,
        X_scaled,
    )

    component_sizes = component_size_report(
        membership
    )

    (
        scaled_means,
        original_means,
        weights,
    ) = component_parameter_tables(
        final_model,
        scaler,
    )

    behavior_profile = (
        behavior_profile_report(
            behavior,
            membership,
        )
    )

    demographic_profile = (
        demographic_profile_report(
            demo,
            membership,
        )
    )

    evaluation.to_csv(
        OUTPUT_DIR
        / "gmm_model_evaluation.csv",
        index=False,
    )

    membership.to_csv(
        OUTPUT_DIR
        / "spotify_gmm_membership.csv",
        index=False,
    )

    component_sizes.to_csv(
        OUTPUT_DIR
        / "gmm_component_sizes.csv",
        index=False,
    )

    scaled_means.to_csv(
        OUTPUT_DIR
        / "gmm_component_means_scaled.csv",
        index=False,
    )

    original_means.to_csv(
        OUTPUT_DIR
        / "gmm_component_means_original.csv",
        index=False,
    )

    weights.to_csv(
        OUTPUT_DIR
        / "gmm_component_weights.csv",
        index=False,
    )

    behavior_profile.to_csv(
        OUTPUT_DIR
        / "gmm_behavior_profile.csv",
        index=False,
    )

    demographic_profile.to_csv(
        OUTPUT_DIR
        / "gmm_demographic_profile.csv",
        index=False,
    )

    joblib.dump(
        scaler,
        OUTPUT_DIR
        / "spotify_gmm_scaler.joblib",
    )

    joblib.dump(
        final_model,
        OUTPUT_DIR
        / "spotify_gmm_model.joblib",
    )

    joblib.dump(
        FEATURES,
        OUTPUT_DIR
        / "spotify_gmm_feature_order.joblib",
    )

    return GMMOutput(
        evaluation=evaluation,
        user_membership=membership,
        component_sizes=component_sizes,
        component_means_scaled=scaled_means,
        component_means_original=original_means,
        component_weights=weights,
        behavior_profile=behavior_profile,
        demographic_profile=demographic_profile,
    )


if __name__ == "__main__":
    behavior_df = pd.read_excel(
        "spotify_user_behavior.xlsx"
    )

    demo_df = pd.read_excel(
        "spotify_user_demo.xlsx"
    )

    result = run_pipeline(
        behavior_df,
        demo_df,
        final_components=4,
        final_covariance_type="full",
    )

    print("\nBest Models by BIC")
    print(
        result.evaluation
        .sort_values("bic")
        .head(10)
        .round(4)
        .to_string(index=False)
    )

    print("\nComponent Sizes")
    print(
        result.component_sizes
        .to_string(index=False)
    )

    print("\nOriginal Component Means")
    print(
        result.component_means_original
        .to_string(index=False)
    )

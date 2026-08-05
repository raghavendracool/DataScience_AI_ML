"""
Spotify Module 11 — Complete Experiment Automation

Runs:
- Multiple feature sets
- Multiple preprocessors
- K-Means K values
- GMM component and covariance combinations

Collects:
- Metrics
- Cluster-size statistics
- Runtime
- Convergence
- Errors
- Experiment metadata

Important:
- Inertia is only directly comparable within the same
  feature set and preprocessing space.
- AIC/BIC are only directly comparable within the same
  observations, features and transformed space.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)

from experiment_config import (
    FEATURE_SETS,
    GMM_COMPONENT_VALUES,
    GMM_COVARIANCE_TYPES,
    KMEANS_K_VALUES,
    LOG_FILE,
    OUTPUT_DIRECTORY,
    PREPROCESSOR_NAMES,
    RANDOM_STATE,
    RESULT_FILE,
    SILHOUETTE_SAMPLE_SIZE,
)
from experiment_factories import (
    build_gmm,
    build_kmeans,
    build_preprocessor,
)
from experiment_logging import (
    append_jsonl,
)


OUTPUT_DIR = Path(
    OUTPUT_DIRECTORY
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def validate_feature_matrix(
    data: pd.DataFrame,
    features: list[str],
) -> pd.DataFrame:
    """Validate and return one model feature matrix."""
    missing = set(features) - set(
        data.columns
    )

    if missing:
        raise ValueError(
            f"Missing features: {sorted(missing)}"
        )

    X = data[
        features
    ].copy()

    non_numeric = (
        X.select_dtypes(
            exclude="number"
        )
        .columns
        .tolist()
    )

    if non_numeric:
        raise TypeError(
            f"Non-numeric features: {non_numeric}"
        )

    if X.isna().any().any():
        raise ValueError(
            "Feature matrix contains missing values"
        )

    if not np.isfinite(
        X.to_numpy(dtype=float)
    ).all():
        raise ValueError(
            "Feature matrix contains infinite values"
        )

    return X


def cluster_size_metrics(
    labels: np.ndarray,
) -> dict[str, Any]:
    """Calculate size and balance metrics."""
    counts = (
        pd.Series(labels)
        .value_counts()
        .sort_index()
    )

    percentages = (
        counts
        .div(counts.sum())
        .mul(100)
    )

    return {
        "cluster_count": int(
            len(counts)
        ),
        "smallest_cluster_count": int(
            counts.min()
        ),
        "largest_cluster_count": int(
            counts.max()
        ),
        "smallest_cluster_pct": float(
            percentages.min()
        ),
        "largest_cluster_pct": float(
            percentages.max()
        ),
        "cluster_counts_json": (
            counts.astype(int)
            .to_dict()
        ),
        "cluster_percentages_json": (
            percentages.round(4)
            .to_dict()
        ),
    }


def safe_silhouette_score(
    X: np.ndarray,
    labels: np.ndarray,
    sample_size: int,
    random_state: int,
) -> float:
    """Calculate a sampled Silhouette Score when valid."""
    unique_labels = np.unique(labels)

    if len(unique_labels) < 2:
        return float("nan")

    if len(unique_labels) >= len(labels):
        return float("nan")

    requested_sample = min(
        sample_size,
        len(labels),
    )

    return float(
        silhouette_score(
            X,
            labels,
            sample_size=requested_sample,
            random_state=random_state,
        )
    )


def common_cluster_metrics(
    X: np.ndarray,
    labels: np.ndarray,
) -> dict[str, float]:
    """Calculate metrics shared by K-Means and GMM."""
    unique_labels = np.unique(labels)

    if len(unique_labels) < 2:
        return {
            "calinski_harabasz_score": (
                float("nan")
            ),
            "davies_bouldin_score": (
                float("nan")
            ),
        }

    return {
        "calinski_harabasz_score": float(
            calinski_harabasz_score(
                X,
                labels,
            )
        ),
        "davies_bouldin_score": float(
            davies_bouldin_score(
                X,
                labels,
            )
        ),
    }


def create_experiment_id(
    feature_set_name: str,
    preprocessor_name: str,
    algorithm: str,
    parameter_text: str,
) -> str:
    """Create a readable file-safe experiment ID."""
    parts = [
        "EXP",
        feature_set_name,
        preprocessor_name,
        algorithm,
        parameter_text,
    ]

    cleaned = [
        str(part)
        .upper()
        .replace(" ", "_")
        .replace("=", "")
        .replace(",", "_")
        .replace("-", "_")
        for part in parts
    ]

    return "_".join(cleaned)


def base_result(
    experiment_id: str,
    feature_set_name: str,
    features: list[str],
    preprocessor_name: str,
    algorithm: str,
    model_parameters: dict[str, Any],
    row_count: int,
) -> dict[str, Any]:
    """Create a standard result dictionary."""
    return {
        "experiment_id": experiment_id,
        "run_timestamp_utc": (
            datetime.now(timezone.utc)
            .isoformat()
        ),
        "status": "RUNNING",
        "row_count": row_count,
        "feature_set_name": (
            feature_set_name
        ),
        "feature_count": len(features),
        "feature_names": features,
        "preprocessor_name": (
            preprocessor_name
        ),
        "algorithm": algorithm,
        "model_parameters": (
            model_parameters
        ),
        "random_state": RANDOM_STATE,
        "runtime_seconds": float("nan"),
        "silhouette_score": float("nan"),
        "calinski_harabasz_score": (
            float("nan")
        ),
        "davies_bouldin_score": (
            float("nan")
        ),
        "inertia": float("nan"),
        "aic": float("nan"),
        "bic": float("nan"),
        "average_log_likelihood": (
            float("nan")
        ),
        "mean_membership_confidence": (
            float("nan")
        ),
        "p10_membership_confidence": (
            float("nan")
        ),
        "iterations": float("nan"),
        "converged": None,
        "error_type": "",
        "error_message": "",
    }


def run_kmeans_experiment(
    data: pd.DataFrame,
    feature_set_name: str,
    features: list[str],
    preprocessor_name: str,
    k: int,
) -> dict[str, Any]:
    """Run one complete K-Means experiment."""
    experiment_id = create_experiment_id(
        feature_set_name,
        preprocessor_name,
        "kmeans",
        f"k{k}",
    )

    result = base_result(
        experiment_id=experiment_id,
        feature_set_name=feature_set_name,
        features=features,
        preprocessor_name=(
            preprocessor_name
        ),
        algorithm="KMeans",
        model_parameters={
            "n_clusters": k,
            "n_init": 20,
        },
        row_count=len(data),
    )

    start = perf_counter()

    try:
        X = validate_feature_matrix(
            data,
            features,
        )

        preprocessor = build_preprocessor(
            preprocessor_name,
            row_count=len(X),
            random_state=RANDOM_STATE,
        )

        X_transformed = (
            preprocessor.fit_transform(X)
        )

        model = build_kmeans(
            k=k,
            random_state=RANDOM_STATE,
        )

        labels = model.fit_predict(
            X_transformed
        )

        result.update(
            cluster_size_metrics(
                labels
            )
        )

        result.update(
            common_cluster_metrics(
                X_transformed,
                labels,
            )
        )

        result["silhouette_score"] = (
            safe_silhouette_score(
                X_transformed,
                labels,
                sample_size=(
                    SILHOUETTE_SAMPLE_SIZE
                ),
                random_state=(
                    RANDOM_STATE
                ),
            )
        )

        result["inertia"] = float(
            model.inertia_
        )

        result["iterations"] = int(
            model.n_iter_
        )

        result["converged"] = True
        result["status"] = "SUCCESS"

    except Exception as error:
        result["status"] = "FAILED"
        result["error_type"] = (
            type(error).__name__
        )
        result["error_message"] = str(
            error
        )

    finally:
        result["runtime_seconds"] = (
            perf_counter() - start
        )

        append_jsonl(
            LOG_FILE,
            result,
        )

    return result


def run_gmm_experiment(
    data: pd.DataFrame,
    feature_set_name: str,
    features: list[str],
    preprocessor_name: str,
    components: int,
    covariance_type: str,
) -> dict[str, Any]:
    """Run one complete GMM experiment."""
    experiment_id = create_experiment_id(
        feature_set_name,
        preprocessor_name,
        "gmm",
        (
            f"c{components}_"
            f"{covariance_type}"
        ),
    )

    result = base_result(
        experiment_id=experiment_id,
        feature_set_name=feature_set_name,
        features=features,
        preprocessor_name=(
            preprocessor_name
        ),
        algorithm="GMM",
        model_parameters={
            "n_components": components,
            "covariance_type": (
                covariance_type
            ),
            "n_init": 10,
        },
        row_count=len(data),
    )

    start = perf_counter()

    try:
        X = validate_feature_matrix(
            data,
            features,
        )

        preprocessor = build_preprocessor(
            preprocessor_name,
            row_count=len(X),
            random_state=RANDOM_STATE,
        )

        X_transformed = (
            preprocessor.fit_transform(X)
        )

        model = build_gmm(
            components=components,
            covariance_type=(
                covariance_type
            ),
            random_state=RANDOM_STATE,
        )

        model.fit(
            X_transformed
        )

        labels = model.predict(
            X_transformed
        )

        probabilities = (
            model.predict_proba(
                X_transformed
            )
        )

        confidence = probabilities.max(
            axis=1
        )

        result.update(
            cluster_size_metrics(
                labels
            )
        )

        result.update(
            common_cluster_metrics(
                X_transformed,
                labels,
            )
        )

        result["silhouette_score"] = (
            safe_silhouette_score(
                X_transformed,
                labels,
                sample_size=(
                    SILHOUETTE_SAMPLE_SIZE
                ),
                random_state=(
                    RANDOM_STATE
                ),
            )
        )

        result["aic"] = float(
            model.aic(
                X_transformed
            )
        )

        result["bic"] = float(
            model.bic(
                X_transformed
            )
        )

        result[
            "average_log_likelihood"
        ] = float(
            model.score(
                X_transformed
            )
        )

        result[
            "mean_membership_confidence"
        ] = float(
            confidence.mean()
        )

        result[
            "p10_membership_confidence"
        ] = float(
            np.quantile(
                confidence,
                0.10,
            )
        )

        result["iterations"] = int(
            model.n_iter_
        )

        result["converged"] = bool(
            model.converged_
        )

        result["status"] = (
            "SUCCESS"
            if model.converged_
            else "FAILED"
        )

        if not model.converged_:
            result["error_type"] = (
                "ConvergenceWarning"
            )
            result["error_message"] = (
                "GMM did not converge"
            )

    except Exception as error:
        result["status"] = "FAILED"
        result["error_type"] = (
            type(error).__name__
        )
        result["error_message"] = str(
            error
        )

    finally:
        result["runtime_seconds"] = (
            perf_counter() - start
        )

        append_jsonl(
            LOG_FILE,
            result,
        )

    return result


def run_all_experiments(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Run the configured K-Means and GMM experiment grid."""
    all_results = []

    for (
        feature_set_name,
        features,
    ) in FEATURE_SETS.items():

        for preprocessor_name in (
            PREPROCESSOR_NAMES
        ):

            for k in KMEANS_K_VALUES:
                result = (
                    run_kmeans_experiment(
                        data=data,
                        feature_set_name=(
                            feature_set_name
                        ),
                        features=features,
                        preprocessor_name=(
                            preprocessor_name
                        ),
                        k=k,
                    )
                )

                all_results.append(
                    result
                )

            for components in (
                GMM_COMPONENT_VALUES
            ):
                for covariance_type in (
                    GMM_COVARIANCE_TYPES
                ):
                    result = (
                        run_gmm_experiment(
                            data=data,
                            feature_set_name=(
                                feature_set_name
                            ),
                            features=features,
                            preprocessor_name=(
                                preprocessor_name
                            ),
                            components=(
                                components
                            ),
                            covariance_type=(
                                covariance_type
                            ),
                        )
                    )

                    all_results.append(
                        result
                    )

    results_df = pd.DataFrame(
        all_results
    )

    results_df.to_csv(
        RESULT_FILE,
        index=False,
    )

    return results_df


if __name__ == "__main__":
    behavior = pd.read_excel(
        "spotify_user_behavior.xlsx"
    )

    results = run_all_experiments(
        behavior
    )

    print("\nExperiment Status")
    print(
        results["status"]
        .value_counts(
            dropna=False
        )
    )

    print("\nSuccessful K-Means Candidates")
    print(
        results[
            (
                results["status"]
                == "SUCCESS"
            )
            & (
                results["algorithm"]
                == "KMeans"
            )
        ]
        .sort_values(
            "silhouette_score",
            ascending=False,
        )
        .head(10)
        [
            [
                "experiment_id",
                "silhouette_score",
                "smallest_cluster_pct",
                "largest_cluster_pct",
                "runtime_seconds",
            ]
        ]
        .round(4)
        .to_string(index=False)
    )

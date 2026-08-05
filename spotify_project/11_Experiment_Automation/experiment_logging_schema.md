# Experiment Logging Schema

## Identity Fields

| Field | Meaning |
|---|---|
| `experiment_id` | Unique experiment name |
| `run_group` | Batch or project identifier |
| `run_timestamp_utc` | Start time |
| `status` | SUCCESS, FAILED or SKIPPED |

## Data Fields

| Field | Meaning |
|---|---|
| `dataset_name` | Input dataset |
| `row_count` | Number of records |
| `feature_set_name` | Named feature set |
| `feature_count` | Number of features |
| `feature_names` | Ordered feature list |

## Preprocessing Fields

| Field | Meaning |
|---|---|
| `preprocessor_name` | Standard, Robust, Power, etc. |
| `preprocessor_parameters` | JSON configuration |
| `transformed_shape` | Rows and columns |

## Model Fields

| Field | Meaning |
|---|---|
| `algorithm` | K-Means or GMM |
| `model_parameters` | JSON configuration |
| `random_state` | Reproducibility seed |

## Metric Fields

| Field | Meaning |
|---|---|
| `silhouette_score` | Cohesion and separation |
| `calinski_harabasz_score` | Cluster dispersion ratio |
| `davies_bouldin_score` | Lower is better |
| `inertia` | K-Means compactness |
| `aic` | GMM fit-complexity |
| `bic` | GMM fit-complexity |
| `average_log_likelihood` | GMM fit |
| `mean_membership_confidence` | Soft assignment strength |
| `smallest_cluster_pct` | Minimum cluster share |
| `largest_cluster_pct` | Maximum cluster share |

## Execution Fields

| Field | Meaning |
|---|---|
| `runtime_seconds` | Run duration |
| `iterations` | Training iterations |
| `converged` | GMM convergence flag |
| `error_type` | Exception class |
| `error_message` | Exception message |

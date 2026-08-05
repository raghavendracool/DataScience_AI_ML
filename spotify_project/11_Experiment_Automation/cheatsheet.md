# Module 11 — Quick Cheat Sheet

## Why Automate?

```text
Many scalers
× many transformations
× many K values
× many GMM covariance types
= many experiments
```

## Core Functions

```python
build_preprocessor()
build_model()
run_experiment()
calculate_metrics()
log_result()
compare_results()
```

## Loop Pattern

```python
results = []

for preprocessor in preprocessors:
    for k in k_values:
        results.append(
            run_experiment(
                preprocessor,
                k
            )
        )

results_df = pd.DataFrame(results)
```

## Log These

```text
Experiment ID
Features
Preprocessor
Algorithm
Parameters
Status
Runtime
Metrics
Cluster sizes
Errors
```

## Comparability

```text
Inertia:
Same features + same preprocessing

AIC/BIC:
Same data + same transformed feature space

Silhouette:
Useful across pipelines with caution
```

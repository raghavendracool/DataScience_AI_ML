# K-Means Experiment Register

| Experiment ID | Feature Set | Preprocessing | K | Init | n_init | Random State | Inertia | Silhouette | Smallest Cluster % | Largest Cluster % | Stability | Business Interpretation | Decision |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|---|---|
| KM_STD_K2 | Core behavior | StandardScaler | 2 | k-means++ | 20 | 42 |  |  |  |  |  |  |  |
| KM_STD_K3 | Core behavior | StandardScaler | 3 | k-means++ | 20 | 42 |  |  |  |  |  |  |  |
| KM_STD_K4 | Core behavior | StandardScaler | 4 | k-means++ | 20 | 42 |  |  |  |  |  |  |  |
| KM_STD_K5 | Core behavior | StandardScaler | 5 | k-means++ | 20 | 42 |  |  |  |  |  |  |  |
| KM_ROBUST_K4 | Core behavior | RobustScaler | 4 | k-means++ | 20 | 42 |  |  |  |  |  |  |  |
| KM_POWER_K4 | Core behavior | PowerTransformer | 4 | k-means++ | 20 | 42 |  |  |  |  |  |  |  |

## Experiment Rules

1. Keep the feature set constant while testing K.
2. Keep K constant while comparing scalers.
3. Use explicit initialization settings.
4. Record cluster counts and percentages.
5. Review stability across random seeds.
6. Compare business profiles, not only metrics.
7. Save every selected scaler and model.

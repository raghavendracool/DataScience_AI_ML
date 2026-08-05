# Scaling Experiment Register

Use one row for each preprocessing and clustering experiment.

| Experiment ID | Feature Set | Preprocessing | Algorithm | K / Parameters | Silhouette | Cluster Sizes | Stability | Business Interpretation | Decision |
|---|---|---|---|---|---:|---|---|---|---|
| EXP_01_STANDARD_CORE | Core behavior | StandardScaler | K-Means | K=4 |  |  |  |  |  |
| EXP_02_MINMAX_CORE | Core behavior | MinMaxScaler | K-Means | K=4 |  |  |  |  |  |
| EXP_03_ROBUST_CORE | Core behavior | RobustScaler | K-Means | K=4 |  |  |  |  |  |
| EXP_04_POWER_CORE | Core behavior | Yeo-Johnson | K-Means | K=4 |  |  |  |  |  |
| EXP_05_QUANTILE_CORE | Core behavior | Quantile normal | K-Means | K=4 |  |  |  |  |  |
| EXP_06_LOG_STANDARD | Core behavior | Log selected features + StandardScaler | K-Means | K=4 |  |  |  |  |  |

## Comparison Rules

1. Keep the feature set constant while comparing scalers.
2. Keep algorithm settings and random state constant.
3. Record cluster-size percentages.
4. Review metrics and business interpretation together.
5. Do not select a method only because its histogram looks normal.
6. Preserve the fitted preprocessor for reproducibility.

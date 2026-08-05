# GMM Experiment Register

| Experiment ID | Feature Set | Preprocessing | Components | Covariance | n_init | AIC | BIC | Avg Log-Likelihood | Silhouette | Min Component % | Max Component % | Mean Confidence | Converged | Iterations | Business Interpretation | Decision |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|---|
| GMM_STD_C2_FULL | Core | StandardScaler | 2 | full | 10 |  |  |  |  |  |  |  |  |  |  |  |
| GMM_STD_C3_FULL | Core | StandardScaler | 3 | full | 10 |  |  |  |  |  |  |  |  |  |  |  |
| GMM_STD_C4_FULL | Core | StandardScaler | 4 | full | 10 |  |  |  |  |  |  |  |  |  |  |  |
| GMM_STD_C4_TIED | Core | StandardScaler | 4 | tied | 10 |  |  |  |  |  |  |  |  |  |  |  |
| GMM_STD_C4_DIAG | Core | StandardScaler | 4 | diag | 10 |  |  |  |  |  |  |  |  |  |  |  |
| GMM_STD_C4_SPH | Core | StandardScaler | 4 | spherical | 10 |  |  |  |  |  |  |  |  |  |  |  |

## Experiment Rules

1. Compare models on the same observations and feature space.
2. Record both AIC and BIC.
3. Confirm convergence before selecting a model.
4. Review membership confidence and component sizes.
5. Evaluate stability across seeds or samples.
6. Do not select the model only because BIC is lowest.
7. Confirm that component profiles are meaningful and actionable.

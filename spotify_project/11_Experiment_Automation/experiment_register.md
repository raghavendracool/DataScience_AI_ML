# Experiment Automation Register

| Run Group | Experiment ID | Feature Set | Preprocessing | Algorithm | Main Parameters | Status | Silhouette | Inertia | AIC | BIC | Min Cluster % | Max Cluster % | Runtime | Stability | Business Review | Decision |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| BATCH_001 | EXP_CORE_STD_KM_K4 | Core | Standard | K-Means | K=4 |  |  |  | N/A | N/A |  |  |  |  |  |  |
| BATCH_001 | EXP_CORE_ROB_KM_K4 | Core | Robust | K-Means | K=4 |  |  |  | N/A | N/A |  |  |  |  |  |  |
| BATCH_001 | EXP_CORE_PWR_GMM_C4_FULL | Core | Power | GMM | C=4, full |  |  | N/A |  |  |  |  |  |  |  |  |

## Rules

1. One row per experiment.
2. Do not overwrite previous experiment history.
3. Record failures as rows.
4. Apply metric comparability rules.
5. Create a shortlist before saving full production artifacts.
6. Complete business review before final selection.

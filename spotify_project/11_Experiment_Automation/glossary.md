# Module 11 — Glossary

| Term | Simple Meaning | Spotify Example |
|---|---|---|
| Experiment | One configuration and result | Standard + K-Means K4 |
| Search Space | All combinations to test | Scalers × K values |
| Configuration | Settings for one run | Feature set and model |
| Automation | Run repeated tasks programmatically | Execute 200 experiments |
| Loop | Repeat code | Loop through K |
| Nested Loop | Loop inside a loop | Scaler then K |
| Function | Reusable code block | `calculate_metrics()` |
| UDF | User-defined function | `run_gmm_experiment()` |
| Factory | Builds an object from config | `build_preprocessor()` |
| Pipeline | Ordered processing workflow | Scale then cluster |
| Experiment ID | Unique run name | `EXP_CORE_STD_K4` |
| Logging | Record settings and outputs | CSV result row |
| Result Collection | Combine results | Pandas DataFrame |
| Status | Run outcome | SUCCESS |
| Exception | Runtime error | ValueError |
| Leaderboard | Ranked result table | Top Silhouette |
| Shortlist | Candidates for review | Top five pipelines |
| Artifact | Saved file from a run | Model joblib |
| Reproducibility | Ability to rerun | Saved config and seed |
| Runtime | Execution duration | 2.4 seconds |
| Comparability | Validity of metric comparison | Same transformed space |
| Batch | Group of experiments | Nightly run |

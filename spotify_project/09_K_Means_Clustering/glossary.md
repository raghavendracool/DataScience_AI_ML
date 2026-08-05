# Module 09 — Glossary

| Term | Simple Meaning | Spotify Example |
|---|---|---|
| K-Means | Centroid-based hard clustering | Four user personas |
| K | Number of clusters | K = 4 |
| Centroid | Mean cluster position | Average Power Streamer |
| Initialization | Starting centroid selection | K-Means++ |
| K-Means++ | Spread-aware initialization | Better starting centers |
| Assignment | User mapped to nearest centroid | User → Cluster 2 |
| Recalculation | Update center using mean | New cluster average |
| Iteration | One assignment/update cycle | Iteration 5 |
| Convergence | Stable solution | Centroids stop moving |
| Local Optimum | Stable but possibly not globally best | One K-Means solution |
| Inertia | Sum of squared within-cluster distance | Cluster compactness |
| Elbow Method | K selection using inertia | Bend near K = 4 |
| Silhouette Score | Cohesion and separation | Compare candidate K |
| `n_clusters` | Number of groups | 4 |
| `init` | Initialization method | `k-means++` |
| `n_init` | Initialization runs | 20 |
| `max_iter` | Iteration limit | 300 |
| `tol` | Convergence tolerance | `1e-4` |
| `random_state` | Reproducibility seed | 42 |
| Cluster Label | Technical cluster ID | 0, 1, 2, 3 |
| Cluster Profile | Cluster statistics | Means and medians |
| Inverse Scaling | Return to original units | Minutes and rates |
| Persona | Business interpretation | Habitual Loyalists |

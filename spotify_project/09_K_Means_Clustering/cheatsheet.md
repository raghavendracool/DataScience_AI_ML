# Module 09 — Quick Cheat Sheet

## Definition

```text
K-Means
= Assign each user to the nearest of K centroids
```

## Algorithm

```text
1. Choose K
2. Initialize K centroids
3. Assign users
4. Recalculate centroids
5. Repeat
6. Converge
```

## Code

```python
model = KMeans(
    n_clusters=4,
    init="k-means++",
    n_init=20,
    max_iter=300,
    tol=1e-4,
    random_state=42
)

labels = model.fit_predict(X_scaled)
```

## Outputs

```python
model.labels_
model.cluster_centers_
model.inertia_
model.n_iter_
```

## K Selection

```text
Elbow Method
Silhouette Score
Cluster sizes
Stability
Business interpretation
```

## Important

```text
Scale features first.
Keep user_id separately.
Cluster numbers have no ranking.
Inverse-scale centroids for business reporting.
```

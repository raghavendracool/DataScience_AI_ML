# Module 12 — Quick Cheat Sheet

## Metric Direction

```text
Silhouette        ↑ Higher
Davies-Bouldin    ↓ Lower
Calinski-Harabasz ↑ Higher
Inertia           ↓ Lower
Log-Likelihood    ↑ Higher
AIC               ↓ Lower
BIC               ↓ Lower
ARI Stability     ↑ Closer to 1
```

## K-Means

```python
silhouette_score(X, labels)
davies_bouldin_score(X, labels)
calinski_harabasz_score(X, labels)
model.inertia_
```

## GMM

```python
model.score(X)
model.aic(X)
model.bic(X)
model.predict_proba(X)
```

## Stability

```python
adjusted_rand_score(
    labels_run_1,
    labels_run_2
)
```

## Final Decision

```text
Metrics
+ Cluster sizes
+ Stability
+ Business meaning
+ Actionability
```

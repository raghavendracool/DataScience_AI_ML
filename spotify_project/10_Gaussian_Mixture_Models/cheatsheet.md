# Module 10 — Quick Cheat Sheet

## Definition

```text
GMM
= Weighted mixture of Gaussian components
```

## Soft Output

```python
probabilities = model.predict_proba(X_scaled)
labels = model.predict(X_scaled)
```

## EM

```text
E-step
→ Calculate component responsibilities

M-step
→ Update weights, means and covariances

Repeat
→ Converge
```

## Covariance Types

```text
full      → Each component has a full matrix
tied      → All components share one full matrix
diag      → Each component has feature variances only
spherical → Each component has one variance
```

## Evaluation

```python
model.aic(X_scaled)
model.bic(X_scaled)
model.score(X_scaled)
model.converged_
model.n_iter_
```

## K-Means vs GMM

```text
K-Means → Hard, centroid distance
GMM     → Soft, probability and covariance
```

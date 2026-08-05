# Module 07 — Quick Cheat Sheet

## Why Scale?

```text
Large numeric ranges dominate distance.
Scaling gives features comparable magnitudes.
```

## Methods

| Method | Main Result | Outlier Resistant? | Changes Shape? |
|---|---|---:|---:|
| StandardScaler | Mean 0, std 1 | No | No |
| MinMaxScaler | Range 0–1 | No | No |
| RobustScaler | Median 0, IQR scale | Yes | No |
| Log1p | Compress right tail | Partly | Yes |
| PowerTransformer | More Gaussian-like | Partly | Yes |
| QuantileTransformer | Normal/uniform rank output | Strong | Yes |

## Code

```python
X_standard = StandardScaler().fit_transform(X)
X_minmax = MinMaxScaler().fit_transform(X)
X_robust = RobustScaler().fit_transform(X)

X_power = PowerTransformer(
    method="yeo-johnson"
).fit_transform(X)

X_quantile = QuantileTransformer(
    output_distribution="normal",
    random_state=42
).fit_transform(X)
```

## Correct Reuse

```python
scaler.fit(X_reference)
X_reference_scaled = scaler.transform(X_reference)
X_future_scaled = scaler.transform(X_future)
```

## Important

```text
StandardScaler does not make data normal.
RobustScaler does not remove outliers.
MinMaxScaler does not remove skewness.
```

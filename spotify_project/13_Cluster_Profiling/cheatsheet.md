# Module 13 — Quick Cheat Sheet

## Profiling Workflow

```text
Labels
→ Join Features
→ Aggregate
→ Compare
→ Summarize
→ Name
→ Recommend
```

## Core Statistics

```python
groupby("cluster").mean()
groupby("cluster").median()
groupby("cluster").quantile(0.25)
groupby("cluster").quantile(0.75)
```

## Relative Comparison

```python
relative_pct = (
    cluster_means
    .div(overall_means)
    .sub(1)
    .mul(100)
)
```

## Profile Views

```text
Original units → Business explanation
Standardized   → Feature comparison
Percentiles    → Distribution understanding
```

## Persona Summary

```text
Cluster size
Main behavior
High features
Low features
Demographic context
Business meaning
Recommended action
Risk
```

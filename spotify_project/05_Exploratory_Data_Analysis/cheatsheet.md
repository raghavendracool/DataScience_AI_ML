# Module 05 — Quick Cheat Sheet

## Descriptive Statistics

```python
df.describe().T
df[col].mean()
df[col].median()
df[col].mode()
df[col].std()
df[col].min()
df[col].max()
df[col].quantile([0.25, 0.50, 0.75, 0.90])
df[col].skew()
```

## Analysis Types

```text
Univariate   → One variable
Bivariate    → Two variables
Multivariate → Three or more variables
```

## Correlation

```python
df.corr(method="pearson")
df.corr(method="spearman")
```

```text
+1  → Strong positive
 0  → Weak linear relationship
-1  → Strong negative
```

## Charts

```python
plt.hist()
plt.boxplot()
plt.bar()
plt.scatter()
plt.imshow()
```

## Spotify Dimensions

```text
Intensity   → daily_listening_minutes
Frequency   → sessions_per_day
Depth       → avg_session_minutes
Consistency → days_active_last_30
Friction    → skip_rate + ads_skipped_pct
```

## Insight Format

```text
Observation
→ Interpretation
→ Business impact
→ Recommended next analysis
→ Caution
```

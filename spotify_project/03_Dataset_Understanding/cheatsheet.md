# Module 03 — Quick Cheat Sheet

## Main Datasets

```text
spotify_user_behavior → What the user does
spotify_user_demo     → Who the user is
Data dictionary       → What each column means
```

## Shapes

```text
Behavior: 108,000 rows × 26 columns
Demo:     108,000 rows × 6 columns
Joined:   108,000 rows × 31 columns
```

## Key

```text
user_id
```

## Relationship

```text
One behavior row ↔ One demographic row
```

## Data Types

```text
Numerical   → listening minutes
Categorical → device type
Continuous  → skip rate
Discrete    → days active
Identifier  → user_id
Feature     → model input
```

## Core Pandas Checks

```python
df.head()
df.shape
df.columns
df.dtypes
df.info()
df.describe().T
df.nunique()
df.isna().sum()
df.duplicated().sum()
```

## Safe Join

```python
spotify_users = spotify_user_behavior.merge(
    spotify_user_demo,
    on="user_id",
    how="inner",
    validate="one_to_one"
)
```

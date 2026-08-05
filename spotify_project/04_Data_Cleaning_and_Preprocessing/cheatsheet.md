# Module 04 — Quick Cheat Sheet

## Cleaning Flow

```text
Load
→ Copy raw data
→ Validate shape
→ Validate columns
→ Check missing values
→ Check duplicates
→ Validate data types
→ Validate ranges
→ Standardize categories
→ Detect outliers
→ Validate user IDs
→ Validate relationship
→ Document decisions
```

## Core Commands

```python
df.shape
df.dtypes
df.info()
df.isna().sum()
df.duplicated().sum()
df["user_id"].duplicated().sum()
df["user_id"].is_unique
pd.to_numeric(df["col"], errors="coerce")
df["col"].str.strip()
df["col"].between(0, 1)
df["col"].isin(allowed_values)
```

## Spotify Rules

```text
days_active_last_30      : 0–30
skip_rate               : 0–1
liked_songs_pct         : 0–1
ads_skipped_pct         : 0–1
repeat_track_rate       : 0–1
repeat_artist_rate      : 0–1
mean_track_popularity   : 0–100
age                     : 18–70
city_tier               : 1–3
subscription tenure     : 1–120 months
```

## Important Principle

```text
Invalid value → correct/remove/investigate

Outlier → investigate before changing
```

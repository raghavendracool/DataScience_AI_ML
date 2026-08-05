# Module 06 — Quick Cheat Sheet

## Definitions

```text
Feature selection
→ Choose existing columns

Feature engineering
→ Create new columns
```

## Spotify Feature Groups

```text
Intensity   → daily_listening_minutes
Frequency   → sessions_per_day
Depth       → avg_session_minutes
Consistency → days_active_last_30
Friction    → skip_rate, ads_skipped_pct
Loyalty     → repeats, likes, follows
Exploration → genre diversity, variability
Popularity  → track-popularity features
```

## Remove Identifier

```python
ids = df[["user_id"]].copy()
X = df.drop(columns=["user_id"]).copy()
```

## Derived Examples

```python
df["active_day_ratio"] = (
    df["days_active_last_30"] / 30
)

df["friction_score"] = (
    df[
        ["skip_rate", "ads_skipped_pct"]
    ]
    .mean(axis=1)
)

df["loyalty_score"] = (
    df[
        [
            "repeat_track_rate",
            "repeat_artist_rate",
            "liked_songs_pct"
        ]
    ]
    .mean(axis=1)
)
```

## Selection Rules

```text
Business relevance
Data quality
Useful variation
Low redundancy
No leakage
Clear interpretation
Stable availability
Improved cluster quality
```

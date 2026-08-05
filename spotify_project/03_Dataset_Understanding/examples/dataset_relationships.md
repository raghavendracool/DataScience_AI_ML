# Spotify Dataset Relationships

## Relationship Overview

```text
spotify_user_demo
- user_id
- age
- country
- city_tier
- device_type
- subscription_tenure_months

             one-to-one on user_id

spotify_user_behavior
- user_id
- listening features
- engagement features
- audio preference features
- popularity features
```

## Why One-to-One?

Each table contains one record per user.

Expected validation:

```text
Behavior unique user IDs: 108,000
Demo unique user IDs: 108,000
Duplicate IDs: 0
Unmatched IDs: 0
```

## Safe Pandas Merge

```python
spotify_users = spotify_user_behavior.merge(
    spotify_user_demo,
    on="user_id",
    how="inner",
    validate="one_to_one"
)
```

Expected result:

```text
108,000 rows × 31 columns
```

## Business Meaning

The merge combines:

```text
Who the user is
        +
What the user does
```

This supports richer cluster profiling and persona creation.

# Spotify K-Means Business Case

## Objective

Use Spotify behavioral features to create hard user segments.

## Core Features

```text
daily_listening_minutes
sessions_per_day
avg_session_minutes
days_active_last_30
skip_rate
ads_skipped_pct
```

## Technical Process

```text
Behavior data
→ StandardScaler
→ K = 2 to 10
→ Elbow and Silhouette
→ Final K-Means
→ Cluster labels
```

## Required Outputs

- User-to-cluster mapping
- Inertia
- Silhouette Score
- Cluster counts
- Cluster percentages
- Scaled centroids
- Original-unit centroids
- Mean and median profiles
- Demographic profiles

## Business Translation

```text
Cluster label
→ Behavioral profile
→ Segment
→ Persona
→ Business action
```

## Illustrative Actions

| Persona | Possible Action |
|---|---|
| Casual Snackers | Re-engagement playlists |
| Exploratory Samplers | Discovery and variety |
| Habitual Loyalists | Retention and rewards |
| Power Streamers | Premium conversion and exclusive value |

The actual names must be supported by model profiles.

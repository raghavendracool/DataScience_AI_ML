# Spotify Clustering Business Case

## Business Problem

Spotify users show different patterns of:

- Listening intensity
- Session frequency
- Activity consistency
- Track skipping
- Advertisement skipping
- Repeat behavior
- Genre exploration

Using one strategy for all users can reduce relevance and business value.

## Analytical Objective

Create behavior-based clusters without using predefined persona labels.

## Expected Technical Output

```text
user_id | cluster
```

Example:

```text
1001 | 0
1002 | 3
1003 | 1
```

## Profiling Stage

For every cluster, calculate:

- User count
- User percentage
- Feature mean
- Feature median
- Feature percentiles
- Age profile
- Country mix
- Device mix
- Subscription tenure

## Possible Personas

- Casual Snackers
- Exploratory Samplers
- Habitual Loyalists
- Power Streamers

These names are illustrative and must be supported by the actual profiles.

## Business Actions

| Possible Persona | Possible Action |
|---|---|
| Casual Snackers | Re-engagement and simple playlists |
| Exploratory Samplers | Discovery-focused recommendations |
| Habitual Loyalists | Loyalty and retention strategy |
| Power Streamers | Premium offers and exclusive benefits |

## Success Criteria

A useful clustering solution should provide:

- Distinct behavior profiles
- Stable assignments
- Reasonable group sizes
- Clear persona descriptions
- Actionable business recommendations

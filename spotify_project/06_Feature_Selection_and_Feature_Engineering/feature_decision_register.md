# Feature Decision Register

Use one row for every raw or derived feature.

| Feature | Source | Type | Business Dimension | Business Meaning | Quality Status | Redundancy Risk | Leakage Risk | Model Use | Decision | Reason |
|---|---|---|---|---|---|---|---|---|---|---|
| `user_id` | Behavior | Identifier | N/A | User key | Pass | N/A | No | Tracking | Exclude | Not behavioral |
| `daily_listening_minutes` | Behavior | Raw numeric | Intensity | Daily usage volume | Pass | Review | No | Clustering | Include | Core engagement signal |
| `country` | Demo | Raw category | Demographic | Region | Pass | Low | No | Profiling | Profile only | Keep first model behavioral |
| `friction_score` | Derived | Composite | Friction | Track and ad rejection | Validate | High | No | Experiment | Test | Compare with raw components |

## Allowed Decisions

```text
Include
Exclude
Profile only
Engineer
Transform
Test
Review
```

## Documentation Rules

1. Record exact source columns.
2. Record the formula for every derived feature.
3. Explain the business meaning.
4. Record whether the feature is used for clustering or profiling.
5. Record leakage and redundancy risk.
6. Version the feature set used in every experiment.

# Module 06 — Feature Selection and Feature Engineering

> A detailed beginner-friendly guide to selecting, creating, validating, and interpreting Spotify user features for unsupervised Machine Learning and customer segmentation.

---

## Table of Contents

1. [Module Overview](#1-module-overview)
2. [Learning Objectives](#2-learning-objectives)
3. [What Is a Feature?](#3-what-is-a-feature)
4. [Raw Columns vs Features](#4-raw-columns-vs-features)
5. [What Is Feature Selection?](#5-what-is-feature-selection)
6. [What Is Feature Engineering?](#6-what-is-feature-engineering)
7. [Feature Selection vs Feature Engineering](#7-feature-selection-vs-feature-engineering)
8. [Why Features Matter in Clustering](#8-why-features-matter-in-clustering)
9. [Spotify Feature Sources](#9-spotify-feature-sources)
10. [Behavioral Features](#10-behavioral-features)
11. [Demographic Features](#11-demographic-features)
12. [Relevant Features](#12-relevant-features)
13. [Irrelevant Features](#13-irrelevant-features)
14. [Removing Identifiers](#14-removing-identifiers)
15. [Redundant Information](#15-redundant-information)
16. [Correlation and Redundancy Review](#16-correlation-and-redundancy-review)
17. [Low-Variance and Near-Constant Features](#17-low-variance-and-near-constant-features)
18. [Feature Groups for Spotify Segmentation](#18-feature-groups-for-spotify-segmentation)
19. [Derived Features](#19-derived-features)
20. [Feature Combinations](#20-feature-combinations)
21. [Spotify Derived-Feature Examples](#21-spotify-derived-feature-examples)
22. [Safe Feature Engineering](#22-safe-feature-engineering)
23. [Avoiding Data Leakage](#23-avoiding-data-leakage)
24. [Choosing Behavioral vs Demographic Features](#24-choosing-behavioral-vs-demographic-features)
25. [Feature Selection Methods](#25-feature-selection-methods)
26. [Business-Based Feature Selection](#26-business-based-feature-selection)
27. [Statistical Feature Selection](#27-statistical-feature-selection)
28. [Model-Based Feature Selection for Clustering](#28-model-based-feature-selection-for-clustering)
29. [Feature Decision Matrix](#29-feature-decision-matrix)
30. [Recommended Spotify Feature Sets](#30-recommended-spotify-feature-sets)
31. [Feature Scaling Considerations](#31-feature-scaling-considerations)
32. [Feature Validation Checks](#32-feature-validation-checks)
33. [Reusable Feature-Engineering Pipeline](#33-reusable-feature-engineering-pipeline)
34. [Business Interpretation of Features](#34-business-interpretation-of-features)
35. [Feature Documentation](#35-feature-documentation)
36. [Module Checklist](#36-module-checklist)
37. [Important Terminology](#37-important-terminology)
38. [Interview Questions and Answers](#38-interview-questions-and-answers)
39. [Module Summary](#39-module-summary)
40. [Quick Reference Cheat Sheet](#40-quick-reference-cheat-sheet)
41. [What Comes Next?](#41-what-comes-next)

---

# 1. Module Overview

A Machine Learning model does not understand a user directly.

It only understands the feature values provided to it.

For example, the model does not see:

```text
"This user is highly engaged."
```

It sees values such as:

```text
daily_listening_minutes = 185
sessions_per_day = 7
days_active_last_30 = 29
avg_session_minutes = 31
skip_rate = 0.12
```

From these values, the clustering algorithm tries to discover groups of users with similar behavior.

The quality of the resulting clusters depends heavily on:

- Which features are included
- Which features are excluded
- How features are created
- Whether redundant information is present
- Whether identifiers are removed
- Whether feature meaning is understood
- Whether features are scaled appropriately

The overall process is:

```text
Raw Spotify Columns
        ↓
Understand Business Meaning
        ↓
Remove Identifiers and Irrelevant Columns
        ↓
Review Redundancy
        ↓
Create Useful Derived Features
        ↓
Validate Feature Quality
        ↓
Build Candidate Feature Sets
        ↓
Scale and Transform
        ↓
Run Clustering Experiments
```

---

# 2. Learning Objectives

By the end of this module, students should be able to:

- Explain what a feature is
- Differentiate raw columns and model features
- Explain feature selection
- Explain feature engineering
- Differentiate relevant and irrelevant features
- Identify Spotify behavioral features
- Identify Spotify demographic features
- Remove identifiers from modeling
- Detect redundant information
- Identify low-variance features
- Create meaningful derived features
- Create safe feature combinations
- Avoid division-by-zero errors
- Avoid data leakage
- Build candidate feature sets
- Explain why demographics may be used for profiling instead of clustering
- Connect each feature to a business meaning
- Document feature decisions
- Build a reusable feature-engineering pipeline

---

# 3. What Is a Feature?

A feature is an input variable used by a Machine Learning algorithm.

In a table:

```text
Rows    = Users
Columns = Possible features
```

Examples of Spotify features:

```text
daily_listening_minutes
sessions_per_day
days_active_last_30
avg_session_minutes
skip_rate
genre_diversity_score
mean_track_popularity
```

A feature should describe something meaningful about the user.

---

## 3.1 Simple Example

| user_id | daily_listening_minutes | sessions_per_day | skip_rate |
|---:|---:|---:|---:|
| 1001 | 45 | 2 | 0.62 |
| 1002 | 185 | 8 | 0.15 |
| 1003 | 92 | 4 | 0.37 |

For clustering:

```text
daily_listening_minutes
sessions_per_day
skip_rate
```

can be features.

`user_id` should not be a feature.

---

# 4. Raw Columns vs Features

A raw column is any column present in the source dataset.

A feature is a column intentionally selected or created for analysis or modeling.

```text
Every feature is a column.

Not every column should become a feature.
```

| Column | Raw Column? | Use as Clustering Feature? |
|---|---|---|
| `user_id` | Yes | No |
| `daily_listening_minutes` | Yes | Yes |
| `country` | Yes | Maybe |
| `device_type` | Yes | Maybe |
| `engagement_score` | No, derived | Maybe |
| `friction_score` | No, derived | Maybe |

A column becomes a feature only after a decision.

---

# 5. What Is Feature Selection?

Feature selection is the process of choosing the most useful existing columns for a model.

It answers:

```text
Which available columns should the model use?
```

Feature selection may remove:

- Identifiers
- Irrelevant fields
- Duplicate information
- Highly redundant variables
- Near-constant variables
- Unreliable columns
- Columns with weak business meaning
- Columns that would distort clustering

---

## 5.1 Easy Example

Available columns:

```text
user_id
daily_listening_minutes
sessions_per_day
days_active_last_30
skip_rate
country
device_type
```

Possible clustering selection:

```text
daily_listening_minutes
sessions_per_day
days_active_last_30
skip_rate
```

Possible profiling columns:

```text
country
device_type
```

Removed identifier:

```text
user_id
```

---

# 6. What Is Feature Engineering?

Feature engineering is the process of creating new features from existing data.

It answers:

```text
Can the raw columns be combined or transformed into a more useful business signal?
```

Examples:

```text
active_day_ratio
minutes_per_active_day
engagement_score
loyalty_score
friction_score
exploration_score
```

Feature engineering should improve:

- Business meaning
- Model signal
- Interpretability
- Stability
- Comparability

It should not create unnecessary complexity.

---

# 7. Feature Selection vs Feature Engineering

| Feature Selection | Feature Engineering |
|---|---|
| Chooses existing columns | Creates new columns |
| Removes weak or unnecessary inputs | Combines or transforms useful inputs |
| Example: remove `user_id` | Example: create `active_day_ratio` |
| Reduces feature space | Enriches feature space |
| Focuses on relevance | Focuses on representation |

## Easy Way to Remember

```text
Feature Selection
= Which columns should we keep?

Feature Engineering
= What new columns should we create?
```

---

# 8. Why Features Matter in Clustering

Clustering groups users based on distance or probability.

For K-Means, users with similar feature values should be closer.

If poor features are included:

- Users may be grouped by meaningless numbers
- Large-scale features may dominate
- Redundant behavior may receive too much weight
- Cluster centers may become difficult to interpret
- Personas may not support business decisions

## Example

Suppose we include:

```text
daily_listening_minutes
sessions_per_day
days_active_last_30
user_id
```

`user_id` adds meaningless numeric distance.

User 90000 appears numerically far from User 1000, even though their behavior may be identical.

That damages clustering quality.

---

# 9. Spotify Feature Sources

The project contains two main feature sources.

## 9.1 Behavioral Dataset

```text
spotify_user_behavior
```

This contains 26 columns, including the identifier.

It describes:

```text
What the user does
```

Examples:

- Listening intensity
- Session frequency
- Activity consistency
- Skip behavior
- Repeat behavior
- Audio preferences
- Genre diversity
- Popularity preference

---

## 9.2 Demographic Dataset

```text
spotify_user_demo
```

This contains 6 columns, including the identifier.

It describes:

```text
Who the user is
```

Examples:

- Age
- Country
- City tier
- Device type
- Subscription tenure

---

# 10. Behavioral Features

Behavioral features are usually the strongest candidates for user segmentation because the project aims to group users by behavior.

## 10.1 Engagement Features

| Feature | Business Meaning |
|---|---|
| `daily_listening_minutes` | Total listening intensity |
| `sessions_per_day` | Frequency of platform visits |
| `days_active_last_30` | Usage consistency |
| `avg_session_minutes` | Depth of each session |
| `median_gap_minutes_between_plays` | Time between listening events |

---

## 10.2 Loyalty Features

| Feature | Business Meaning |
|---|---|
| `repeat_track_rate` | Loyalty to specific tracks |
| `repeat_artist_rate` | Loyalty to specific artists |
| `playlists_followed` | Playlist attachment |
| `artists_followed` | Artist attachment |
| `liked_songs_pct` | Positive response to content |

---

## 10.3 Friction Features

| Feature | Business Meaning |
|---|---|
| `skip_rate` | Track-level friction or exploration |
| `ads_skipped_pct` | Advertisement intolerance |
| `median_gap_minutes_between_plays` | Weak or strong return behavior |

---

## 10.4 Audio-Preference Features

| Feature | Business Meaning |
|---|---|
| `mean_danceability` | Preference for dance-oriented music |
| `mean_energy` | Preference for energetic music |
| `mean_valence` | Preference for positive or low-valence mood |
| `mean_acousticness` | Preference for acoustic tracks |
| `mean_speechiness` | Preference for speech-heavy content |
| `mean_instrumentalness` | Preference for instrumental content |
| `mean_tempo` | Preferred tempo |

---

## 10.5 Variety Features

| Feature | Business Meaning |
|---|---|
| `std_energy` | Variety in energy preference |
| `std_valence` | Variety in mood preference |
| `std_tempo` | Variety in tempo preference |
| `genre_diversity_score` | Breadth of genre exploration |

---

## 10.6 Popularity Features

| Feature | Business Meaning |
|---|---|
| `mean_track_popularity` | Mainstream vs niche preference |
| `pct_top_popularity_tracks` | Reliance on highly popular tracks |

---

# 11. Demographic Features

Demographic features describe user context.

| Feature | Business Meaning |
|---|---|
| `age` | Life-stage differences |
| `country` | Regional preferences |
| `city_tier` | Market and urban classification |
| `device_type` | Primary access pattern |
| `subscription_tenure_months` | Relationship length |

---

## 11.1 Should Demographics Be Used in Clustering?

There is no single universal answer.

### Option A — Behavioral Clustering

Use only behavioral features to discover how users behave.

Then use demographics later to profile clusters.

This is often preferred for this project.

```text
Behavioral features
        ↓
Create clusters
        ↓
Join demographics
        ↓
Describe age, country, device and tenure
```

### Option B — Mixed Clustering

Use behavior and encoded demographics together.

This may be appropriate when business strategy explicitly requires demographic separation.

Risks:

- Country may dominate through encoding
- Demographic differences may hide behavioral similarity
- Clusters may become harder to interpret
- Categorical encoding changes distance behavior

---

## 11.2 Recommended Project Approach

For the first clustering experiments:

```text
Use behavioral features for model training.

Use demographic features for cluster profiling.
```

Later, mixed feature experiments can be tested separately.

---

# 12. Relevant Features

A relevant feature supports the project objective.

The project objective is:

```text
Discover meaningful Spotify user behavior segments.
```

A relevant feature should:

- Describe listening behavior
- Differentiate users
- Have acceptable quality
- Have a clear business interpretation
- Contribute useful variation
- Avoid unnecessary duplication
- Remain available for future users

Examples:

```text
daily_listening_minutes
sessions_per_day
days_active_last_30
avg_session_minutes
skip_rate
ads_skipped_pct
genre_diversity_score
repeat_artist_rate
```

---

# 13. Irrelevant Features

An irrelevant feature does not help the segmentation objective.

Examples may include:

- Record identifiers
- Random sequence numbers
- Processing timestamps unrelated to behavior
- File names
- Technical ingestion columns
- Columns with no variation
- Fields unavailable at prediction or scoring time
- Fields unrelated to the business question

## Important Note

A feature is not irrelevant merely because its correlation is low.

Clustering is unsupervised.

A feature may still help separate groups even without strong pairwise correlation.

---

# 14. Removing Identifiers

## 14.1 Why Remove `user_id`?

`user_id` is a primary key.

It is useful for:

- Joining
- Tracking
- Exporting cluster labels
- Investigating users
- Building reports

It is not useful for:

- Distance calculations
- User-behavior representation
- Cluster formation

---

## 14.2 Correct Pattern

Keep IDs separately:

```python
user_ids = (
    spotify_user_behavior[
        ["user_id"]
    ]
    .copy()
)

feature_df = (
    spotify_user_behavior
    .drop(columns=["user_id"])
    .copy()
)
```

After clustering:

```python
cluster_output = user_ids.copy()

cluster_output[
    "cluster"
] = cluster_labels
```

---

## 14.3 Other Identifier Examples

In other projects, remove:

```text
customer_id
transaction_id
order_id
email
phone_number
row_number
```

These identify records but usually do not describe behavior.

---

# 15. Redundant Information

Redundant features carry the same or nearly the same information.

Examples:

```text
daily_listening_minutes
total_weekly_listening_minutes
```

If one is almost a direct multiplication of the other, including both may double-count listening intensity.

Possible Spotify redundancy questions:

- Does `daily_listening_minutes` overlap strongly with `avg_session_minutes × sessions_per_day`?
- Does `mean_track_popularity` overlap strongly with `pct_top_popularity_tracks`?
- Do `std_energy`, `std_valence`, and `std_tempo` measure similar variety?
- Do `repeat_track_rate` and `repeat_artist_rate` provide distinct loyalty signals?
- Does `liked_songs_pct` provide information different from `skip_rate`?

Do not remove features based only on assumptions.

Validate with:

- Correlation
- Scatter plots
- Business meaning
- Cluster experiments
- Stability analysis

---

# 16. Correlation and Redundancy Review

## 16.1 Correlation Matrix

```python
numeric_features = (
    spotify_user_behavior
    .drop(columns=["user_id"])
    .select_dtypes(include="number")
)

correlation_matrix = (
    numeric_features
    .corr(method="spearman")
)
```

Spearman is useful when distributions are skewed.

---

## 16.2 Identify Highly Correlated Pairs

```python
import numpy as np
import pandas as pd

upper_triangle = np.triu(
    np.ones(
        correlation_matrix.shape
    ),
    k=1
).astype(bool)

correlation_pairs = (
    correlation_matrix
    .where(upper_triangle)
    .stack()
    .reset_index()
)

correlation_pairs.columns = [
    "feature_1",
    "feature_2",
    "correlation"
]

correlation_pairs[
    "absolute_correlation"
] = (
    correlation_pairs[
        "correlation"
    ]
    .abs()
)

high_correlation_pairs = (
    correlation_pairs[
        correlation_pairs[
            "absolute_correlation"
        ] >= 0.85
    ]
    .sort_values(
        "absolute_correlation",
        ascending=False
    )
)

display(high_correlation_pairs)
```

---

## 16.3 Does High Correlation Mean Remove One?

Not automatically.

Ask:

1. Do the features have the same business meaning?
2. Is one derived from the other?
3. Is one more stable or easier to explain?
4. Does keeping both over-weight a dimension?
5. Does cluster quality improve or decline?
6. Are personas easier to interpret with one or both?

---

# 17. Low-Variance and Near-Constant Features

A feature with almost the same value for all users may contribute little to clustering.

## 17.1 Variance Check

```python
feature_variance = (
    numeric_features
    .var()
    .sort_values()
)

display(feature_variance)
```

Raw variance depends on scale, so it should not be interpreted alone.

---

## 17.2 Unique Ratio

```python
unique_ratio = (
    numeric_features
    .nunique()
    .div(
        len(numeric_features)
    )
    .sort_values()
)

display(unique_ratio)
```

---

## 17.3 Near-Constant Check

```python
def near_constant_report(
    df: pd.DataFrame,
    threshold: float = 0.98
) -> pd.DataFrame:
    records = []

    for column in df.columns:
        proportions = (
            df[column]
            .value_counts(
                normalize=True,
                dropna=False
            )
        )

        top_share = (
            float(proportions.iloc[0])
            if not proportions.empty
            else 0.0
        )

        records.append({
            "feature": column,
            "most_common_share": round(
                top_share,
                4
            ),
            "near_constant": (
                top_share >= threshold
            )
        })

    return pd.DataFrame(records)
```

A near-constant feature should be reviewed, not blindly removed.

---

# 18. Feature Groups for Spotify Segmentation

The project can organize features into business dimensions.

## 18.1 Intensity

```text
daily_listening_minutes
```

Meaning:

> How much does the user listen?

---

## 18.2 Frequency

```text
sessions_per_day
```

Meaning:

> How often does the user return?

---

## 18.3 Depth

```text
avg_session_minutes
```

Meaning:

> How immersive is each session?

---

## 18.4 Consistency

```text
days_active_last_30
```

Meaning:

> How regularly does the user engage?

---

## 18.5 Friction

```text
skip_rate
ads_skipped_pct
```

Meaning:

> How much does the user reject tracks or advertisements?

---

## 18.6 Loyalty

```text
repeat_track_rate
repeat_artist_rate
liked_songs_pct
playlists_followed
artists_followed
```

Meaning:

> How strongly does the user return to preferred content?

---

## 18.7 Exploration

```text
genre_diversity_score
std_energy
std_valence
std_tempo
```

Meaning:

> How broad and varied is the user's music taste?

---

## 18.8 Popularity Preference

```text
mean_track_popularity
pct_top_popularity_tracks
```

Meaning:

> Does the user prefer mainstream or niche music?

---

# 19. Derived Features

A derived feature is created from one or more raw features.

## 19.1 Why Create Derived Features?

Derived features may:

- Represent a clearer business concept
- Normalize behavior
- Combine related signals
- Reduce complexity
- Improve persona interpretation
- Capture interaction between behaviors

---

## 19.2 Risks

Poorly designed derived features can:

- Duplicate raw information
- Over-weight one dimension
- Hide useful variation
- Introduce division errors
- Create leakage
- Become difficult to explain
- Add unnecessary complexity

Derived features should be treated as experiments.

---

# 20. Feature Combinations

Feature combinations capture interaction between variables.

Example:

```text
daily_listening_minutes alone
```

shows intensity.

But:

```text
daily_listening_minutes
÷
days_active_last_30
```

shows listening intensity per active day.

Two users may have the same total listening level but different habits.

---

## 20.1 Additive Combination

```text
skip_rate + ads_skipped_pct
```

May represent total friction.

---

## 20.2 Average Combination

```text
(repeat_track_rate + repeat_artist_rate) ÷ 2
```

May represent loyalty.

---

## 20.3 Ratio Combination

```text
daily_listening_minutes ÷ sessions_per_day
```

May represent minutes per session.

But the dataset already contains:

```text
avg_session_minutes
```

Creating the ratio may be redundant.

This is a good example of why feature engineering and redundancy review must happen together.

---

## 20.4 Interaction Feature

```text
daily_listening_minutes × days_active_last_30
```

Could represent monthly engagement volume.

However, it may create a large-scale, highly skewed feature.

It should be validated and scaled before use.

---

# 21. Spotify Derived-Feature Examples

The following examples are candidate features, not automatically approved final features.

---

## 21.1 Active-Day Ratio

```text
active_day_ratio
=
days_active_last_30 ÷ 30
```

Range:

```text
0 to 1
```

Business meaning:

> Proportion of days on which the user was active.

```python
features[
    "active_day_ratio"
] = (
    features[
        "days_active_last_30"
    ]
    .div(30)
)
```

---

## 21.2 Minutes per Active Day

```text
minutes_per_active_day
=
daily_listening_minutes
÷
active_day_ratio
```

Important:

The exact interpretation depends on how `daily_listening_minutes` was defined in the source.

A safer direct ratio can be used only after confirming the dictionary definition.

For a generic total-period metric:

```python
features[
    "minutes_per_active_day"
] = (
    total_minutes
    ÷
    days_active_last_30
)
```

Do not invent a ratio when the raw feature already represents a daily average.

---

## 21.3 Engagement Score

A simple conceptual score:

```text
engagement_score
=
average of scaled:
- daily_listening_minutes
- sessions_per_day
- days_active_last_30
- avg_session_minutes
```

Important:

Raw features must not be averaged before scaling because their units differ.

Correct approach:

```text
Select inputs
→ Scale inputs
→ Average scaled values
```

---

## 21.4 Friction Score

```text
friction_score
=
(skip_rate + ads_skipped_pct) ÷ 2
```

```python
features[
    "friction_score"
] = (
    features[
        [
            "skip_rate",
            "ads_skipped_pct"
        ]
    ]
    .mean(axis=1)
)
```

Business meaning:

> Combined rejection of content and advertisement interruptions.

Caution:

Track skipping and ad skipping have different causes.

The combined feature should be tested against the two raw variables.

---

## 21.5 Loyalty Score

```text
loyalty_score
=
average of:
- repeat_track_rate
- repeat_artist_rate
- liked_songs_pct
```

```python
features[
    "loyalty_score"
] = (
    features[
        [
            "repeat_track_rate",
            "repeat_artist_rate",
            "liked_songs_pct"
        ]
    ]
    .mean(axis=1)
)
```

Business meaning:

> Strength of repeated and positive content preference.

---

## 21.6 Exploration Score

```text
exploration_score
=
average of:
- genre_diversity_score
- std_energy
- std_valence
- normalized std_tempo
```

Caution:

`std_tempo` may use a different scale.

It must be scaled before combination.

---

## 21.7 Follow Depth

```text
follow_depth
=
playlists_followed + artists_followed
```

Business meaning:

> Total explicit following behavior.

Caution:

Playlist and artist counts may have different distributions.

A scaled average may be more appropriate.

---

## 21.8 Mainstream Affinity

Possible combination:

```text
mainstream_affinity
=
average of:
- mean_track_popularity / 100
- pct_top_popularity_tracks
```

```python
features[
    "mainstream_affinity"
] = (
    (
        features[
            "mean_track_popularity"
        ]
        .div(100)
    )
    + features[
        "pct_top_popularity_tracks"
    ]
).div(2)
```

Business meaning:

> Preference for widely popular content.

---

## 21.9 Return-Frequency Score

A smaller gap between plays may indicate frequent return.

Because lower gap means stronger return behavior, a transformed feature could be:

```text
return_frequency_score
=
1 ÷ (1 + median_gap_minutes_between_plays)
```

```python
features[
    "return_frequency_score"
] = (
    1
    / (
        1
        + features[
            "median_gap_minutes_between_plays"
        ]
    )
)
```

This converts:

```text
Large gap → Smaller score
Small gap → Larger score
```

---

## 21.10 Engagement-Friction Interaction

```text
engagement_friction_index
=
scaled engagement
-
scaled friction
```

Possible interpretation:

- High engagement and low friction
- High engagement and high friction
- Low engagement and low friction
- Low engagement and high friction

This should be built after scaling and evaluated carefully.

---

# 22. Safe Feature Engineering

## 22.1 Work on a Copy

```python
engineered = (
    spotify_user_behavior
    .copy()
)
```

---

## 22.2 Protect Against Division by Zero

```python
import numpy as np

engineered[
    "sessions_per_active_day"
] = np.where(
    engineered[
        "days_active_last_30"
    ] > 0,
    engineered[
        "sessions_per_day"
    ]
    / engineered[
        "days_active_last_30"
    ],
    np.nan
)
```

---

## 22.3 Validate New Ranges

```python
assert (
    engineered[
        "active_day_ratio"
    ]
    .between(0, 1)
    .all()
)
```

---

## 22.4 Check Missing and Infinite Values

```python
import numpy as np

engineered = engineered.replace(
    [np.inf, -np.inf],
    np.nan
)

print(
    engineered.isna().sum()
)
```

---

## 22.5 Preserve Raw Features

Do not overwrite raw columns.

Prefer:

```text
skip_rate
friction_score
```

instead of replacing `skip_rate`.

This supports:

- Comparison
- Explainability
- Debugging
- Rollback

---

# 23. Avoiding Data Leakage

Data leakage means using information that should not be available when the model is applied.

In unsupervised segmentation, leakage can still happen.

Examples:

- Using a future outcome to create current clusters
- Using manually assigned personas as input
- Using cluster labels from a previous model as a feature
- Using post-campaign behavior to build pre-campaign segments
- Using revenue generated after the segmentation date

For this project, avoid using:

```text
cluster label
persona name
future Premium conversion
future churn status
future campaign response
```

as clustering inputs.

---

# 24. Choosing Behavioral vs Demographic Features

## 24.1 Behavioral-Only Model

Advantages:

- Groups are based on user actions
- Personas remain behavior-focused
- Demographics can explain clusters afterward
- Less categorical encoding complexity

Disadvantages:

- May miss important market context

---

## 24.2 Demographic-Only Model

Advantages:

- Easy market grouping
- Useful for campaign planning

Disadvantages:

- Does not capture listening behavior
- Can produce stereotypes rather than behavioral personas
- Less aligned with this project's objective

---

## 24.3 Mixed Model

Advantages:

- Combines behavior and context

Disadvantages:

- Requires encoding
- Distance interpretation becomes harder
- Country/device categories may dominate
- Business meaning may become less clear

---

## 24.4 Recommended Sequence

```text
Experiment 1:
Core behavioral features

Experiment 2:
Expanded behavioral features

Experiment 3:
Behavioral + engineered scores

Experiment 4:
Behavioral + selected demographics
```

Compare results rather than assuming one set is best.

---

# 25. Feature Selection Methods

Feature selection for unsupervised learning can use several methods.

## 25.1 Business Relevance

Does the feature support the project objective?

---

## 25.2 Data Quality

Is the feature:

- Complete?
- Valid?
- Stable?
- Correctly typed?
- Available for all users?

---

## 25.3 Variability

Does the feature differentiate users?

---

## 25.4 Redundancy Review

Does another feature contain nearly the same information?

---

## 25.5 Distribution Review

Is the feature extremely skewed?

Does it require transformation?

---

## 25.6 Cluster Experiment Comparison

Does the feature improve:

- Silhouette score?
- Cluster balance?
- Stability?
- Persona separation?
- Business interpretability?

---

# 26. Business-Based Feature Selection

Business-based selection starts with the question:

```text
What behavior do we want the clusters to represent?
```

For Spotify personas, important dimensions are:

| Business Dimension | Candidate Features |
|---|---|
| Intensity | `daily_listening_minutes` |
| Frequency | `sessions_per_day` |
| Depth | `avg_session_minutes` |
| Consistency | `days_active_last_30` |
| Friction | `skip_rate`, `ads_skipped_pct` |
| Loyalty | `repeat_track_rate`, `repeat_artist_rate` |
| Exploration | `genre_diversity_score` |
| Popularity | `mean_track_popularity` |

A feature should not be selected only because it is available.

It should answer a business question.

---

# 27. Statistical Feature Selection

## 27.1 Missingness

```python
missing_pct = (
    feature_df
    .isna()
    .mean()
    .mul(100)
)
```

---

## 27.2 Unique Values

```python
unique_counts = (
    feature_df
    .nunique()
)
```

---

## 27.3 Near-Constant Features

```python
near_constant = (
    near_constant_report(
        feature_df
    )
)
```

---

## 27.4 Correlation

```python
spearman_corr = (
    feature_df
    .corr(
        method="spearman"
    )
)
```

---

## 27.5 Skewness

```python
feature_skewness = (
    feature_df
    .skew()
    .sort_values(
        key=abs,
        ascending=False
    )
)
```

Statistics guide decisions, but do not replace business interpretation.

---

# 28. Model-Based Feature Selection for Clustering

Unsupervised learning has no target label.

Therefore, supervised feature-importance methods are not directly available.

We can compare candidate feature sets using:

- Silhouette score
- Cluster-size balance
- Inertia
- GMM AIC
- GMM BIC
- Stability across random seeds
- Cluster-profile separation
- Business interpretability

## Example Experiment

```text
Feature Set A:
4 core engagement features

Feature Set B:
Core engagement + friction

Feature Set C:
Expanded behavioral features

Feature Set D:
Engineered scores
```

The best feature set is not simply the one with the most columns.

---

# 29. Feature Decision Matrix

Use a decision matrix for every feature.

| Feature | Source | Business Meaning | Quality | Redundancy | Model Use | Decision |
|---|---|---|---|---|---|---|
| `user_id` | Behavior | Identifier | Good | N/A | Join only | Exclude |
| `daily_listening_minutes` | Behavior | Intensity | Good | Review | Clustering | Include |
| `country` | Demo | Region | Good | Low | Profiling | Profile |
| `friction_score` | Derived | Combined friction | Validate | High with components | Experiment | Test |

Possible decisions:

```text
Include
Exclude
Profile only
Engineer
Transform
Review
Test in experiment
```

A template is included in:

```text
feature_decision_register.md
```

---

# 30. Recommended Spotify Feature Sets

These are candidate sets for experiments.

---

## 30.1 Core Persona Feature Set

```python
core_features = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
    "days_active_last_30",
    "skip_rate",
    "ads_skipped_pct"
]
```

Business dimensions:

```text
Intensity
Frequency
Depth
Consistency
Friction
```

---

## 30.2 Expanded Behavioral Feature Set

```python
expanded_features = [
    "daily_listening_minutes",
    "sessions_per_day",
    "days_active_last_30",
    "avg_session_minutes",
    "playlists_followed",
    "artists_followed",
    "skip_rate",
    "liked_songs_pct",
    "ads_skipped_pct",
    "repeat_track_rate",
    "repeat_artist_rate",
    "genre_diversity_score",
    "mean_track_popularity",
    "pct_top_popularity_tracks"
]
```

---

## 30.3 Audio-Preference Feature Set

```python
audio_features = [
    "mean_danceability",
    "mean_energy",
    "mean_valence",
    "mean_acousticness",
    "mean_speechiness",
    "mean_instrumentalness",
    "mean_tempo",
    "std_energy",
    "std_valence",
    "std_tempo"
]
```

This set may be used for a music-taste segmentation experiment.

---

## 30.4 Engineered-Score Feature Set

```python
engineered_features = [
    "active_day_ratio",
    "friction_score",
    "loyalty_score",
    "mainstream_affinity",
    "return_frequency_score"
]
```

This is more compact and business-friendly.

However, it may lose raw detail.

---

## 30.5 Profiling Features

```python
profiling_features = [
    "age",
    "country",
    "city_tier",
    "device_type",
    "subscription_tenure_months"
]
```

These can be joined after clustering.

---

# 31. Feature Scaling Considerations

Features use different units.

Examples:

```text
daily_listening_minutes → Minutes
sessions_per_day        → Count
skip_rate               → 0 to 1
mean_track_popularity   → 0 to 100
```

Without scaling:

```text
A large-unit feature may dominate distance.
```

Feature selection happens before scaling.

The next preprocessing stage should compare:

- StandardScaler
- MinMaxScaler
- RobustScaler
- PowerTransformer
- QuantileTransformer

Do not average raw features with different units.

---

# 32. Feature Validation Checks

Before using a feature set, validate:

## 32.1 Required Columns

```python
missing_features = (
    set(core_features)
    - set(
        spotify_user_behavior.columns
    )
)

if missing_features:
    raise ValueError(
        f"Missing features: "
        f"{sorted(missing_features)}"
    )
```

---

## 32.2 Numeric Types

```python
non_numeric = (
    spotify_user_behavior[
        core_features
    ]
    .select_dtypes(
        exclude="number"
    )
    .columns
    .tolist()
)

if non_numeric:
    raise TypeError(
        f"Non-numeric features: "
        f"{non_numeric}"
    )
```

---

## 32.3 Missing Values

```python
missing_counts = (
    spotify_user_behavior[
        core_features
    ]
    .isna()
    .sum()
)
```

---

## 32.4 Infinite Values

```python
import numpy as np

infinite_counts = (
    np.isinf(
        spotify_user_behavior[
            core_features
        ]
    )
    .sum()
)
```

---

## 32.5 Constant Features

```python
constant_features = [
    column
    for column in core_features
    if spotify_user_behavior[
        column
    ].nunique() <= 1
]
```

---

# 33. Reusable Feature-Engineering Pipeline

A reusable pipeline should:

- Preserve the raw data
- Validate required columns
- Remove identifiers from model inputs
- Create derived features safely
- Check ranges
- Check missing and infinite values
- Return separate model and profiling tables
- Record feature metadata

The complete implementation is included in:

```text
examples/spotify_feature_engineering.py
```

The feature-selection report is included in:

```text
examples/spotify_feature_selection_report.py
```

---

# 34. Business Interpretation of Features

A technical feature should always have a business explanation.

## 34.1 Example: `daily_listening_minutes`

Technical meaning:

> Average listening minutes per day.

Business interpretation:

> Overall engagement intensity.

Potential segment meaning:

```text
Low → Casual usage
Medium → Regular usage
High → Power usage
```

---

## 34.2 Example: `sessions_per_day`

Technical meaning:

> Average number of sessions per day.

Business interpretation:

> Frequency of user return.

A user may have:

```text
High frequency + short sessions
```

or:

```text
Low frequency + long sessions
```

These may represent different personas.

---

## 34.3 Example: `skip_rate`

Technical meaning:

> Proportion of tracks skipped.

Possible interpretations:

- Content dissatisfaction
- Strong preference
- Active exploration
- Recommendation mismatch

Do not interpret one feature in isolation.

---

## 34.4 Example: `ads_skipped_pct`

Technical meaning:

> Proportion of advertisements skipped.

Possible business meaning:

- Advertisement intolerance
- High Premium-conversion potential
- Low ad relevance

It must be combined with engagement.

A low-engagement user who skips ads may not be as valuable as a highly engaged ad-skipping user.

---

## 34.5 Example: `genre_diversity_score`

Technical meaning:

> Breadth of genres consumed.

Possible business meaning:

- High score → Explorer
- Low score → Focused or loyal listener

---

## 34.6 Example: `subscription_tenure_months`

Technical meaning:

> Length of user relationship.

Possible business meaning:

- New user
- Established user
- Long-term loyal user

Recommended use:

```text
Profile clusters first.

Test as model input separately.
```

---

# 35. Feature Documentation

Every approved feature should be documented.

Recommended fields:

| Field | Purpose |
|---|---|
| Feature name | Exact model column |
| Source column(s) | Raw origin |
| Feature type | Raw or derived |
| Formula | Calculation |
| Data type | Numeric/category |
| Valid range | Expected values |
| Business meaning | Human interpretation |
| Model use | Clustering or profiling |
| Transformation | Scaling or power transform |
| Leakage risk | Yes/No |
| Decision | Include/Exclude/Test |
| Version | Feature-definition version |

A sample feature catalog is included in:

```text
examples/spotify_feature_catalog.py
```

---

# 36. Module Checklist

## Understanding

- [ ] Project objective is clear
- [ ] Raw columns are understood
- [ ] Behavioral and demographic features are separated
- [ ] Business meaning is documented

## Selection

- [ ] Identifiers removed
- [ ] Irrelevant columns reviewed
- [ ] Missingness checked
- [ ] Near-constant features checked
- [ ] Redundancy reviewed
- [ ] Correlation reviewed
- [ ] Candidate feature sets created

## Engineering

- [ ] Derived features have clear formulas
- [ ] Division by zero is handled
- [ ] Infinite values are handled
- [ ] Raw columns are preserved
- [ ] New ranges are validated
- [ ] Leakage is checked
- [ ] Derived features are tested against raw inputs

## Modeling Preparation

- [ ] Features are numeric
- [ ] IDs are stored separately
- [ ] Profiling columns are stored separately
- [ ] Scaling is planned
- [ ] Feature decisions are documented
- [ ] Experiment names identify the feature set

---

# 37. Important Terminology

| Term | Meaning |
|---|---|
| Feature | Model input variable |
| Raw feature | Existing source column used directly |
| Derived feature | New feature created from raw columns |
| Feature selection | Choosing useful existing features |
| Feature engineering | Creating or transforming features |
| Identifier | Record key such as `user_id` |
| Relevant feature | Feature supporting the business objective |
| Irrelevant feature | Feature not useful for the objective |
| Redundancy | Repeated or overlapping information |
| Correlation | Relationship between numerical features |
| Low variance | Little difference across users |
| Near constant | Almost all rows contain the same value |
| Interaction feature | Feature combining two behaviors |
| Ratio feature | One measure divided by another |
| Composite score | Combined score from multiple features |
| Data leakage | Using unavailable or future information |
| Feature set | Group of features used in one experiment |
| Feature catalog | Documentation of feature definitions |
| Profiling feature | Used to describe clusters after modeling |
| Model feature | Used to form clusters |
| Scaling | Making feature magnitudes comparable |
| Encoding | Converting categories to numeric form |
| Interpretability | Ability to explain feature meaning |
| Feature stability | Consistency of a feature over time |

---

# 38. Interview Questions and Answers

## 1. What is a feature?

A feature is an input variable used by a Machine Learning model.

---

## 2. What is feature selection?

Feature selection is choosing the most useful existing columns for modeling.

---

## 3. What is feature engineering?

Feature engineering is creating new, useful variables from existing data.

---

## 4. Feature selection vs feature engineering?

Selection chooses existing columns. Engineering creates new columns.

---

## 5. Why should `user_id` be removed?

It identifies a user but does not describe behavior.

---

## 6. Should `user_id` be deleted completely?

No. Keep it separately for joins, tracking, and attaching cluster labels.

---

## 7. What is a relevant feature?

A feature that supports the project objective and provides useful variation.

---

## 8. What is an irrelevant feature?

A feature that does not help represent the behavior being modeled.

---

## 9. What is a redundant feature?

A feature containing the same or nearly the same information as another feature.

---

## 10. Does high correlation always mean one feature must be removed?

No. Business meaning and experiment results must also be reviewed.

---

## 11. What is a low-variance feature?

A feature with little variation across records.

---

## 12. Why can low-variance features be weak for clustering?

They may not help separate users.

---

## 13. What are behavioral features?

Features describing user actions such as listening, skipping and repeating.

---

## 14. What are demographic features?

Features describing user background such as age, country and device.

---

## 15. Why use demographics for profiling?

It keeps clusters behavior-focused while adding business context afterward.

---

## 16. What is a derived feature?

A new feature calculated from existing columns.

---

## 17. Give a Spotify derived-feature example.

`active_day_ratio = days_active_last_30 / 30`.

---

## 18. What is a composite score?

A feature combining multiple related inputs, such as a loyalty score.

---

## 19. Why must features be scaled before averaging?

Different units would otherwise give more weight to large-scale variables.

---

## 20. What is data leakage?

Using future, target-like, or unavailable information when building features.

---

## 21. Can leakage happen in unsupervised learning?

Yes. Future outcomes or previous cluster labels can improperly influence clusters.

---

## 22. What is an interaction feature?

A feature representing the combined behavior of two inputs.

---

## 23. What is the risk of too many features?

Noise, redundancy, unstable clusters and reduced interpretability.

---

## 24. What is the risk of too few features?

Important behavioral differences may be missed.

---

## 25. How do you select features for clustering?

Use business relevance, quality, variability, redundancy review, distribution analysis, cluster metrics, stability and interpretability.

---

## 26. How do you evaluate a feature set without labels?

Compare silhouette score, balance, stability, AIC/BIC for GMM, profile separation and business usefulness.

---

## 27. Why are behavioral features important in this project?

The project aims to discover user behavior personas.

---

## 28. Why might `country` be excluded from the first model?

To prevent geography from dominating behavioral grouping.

---

## 29. What is a feature decision matrix?

A documented table recording why each feature is included, excluded, engineered or reserved for profiling.

---

## 30. What are the core Spotify persona dimensions?

Intensity, frequency, depth, consistency and friction.

---

# 39. Module Summary

In this module, we learned:

- A feature is an input used by a model
- Not every dataset column should become a feature
- Feature selection chooses existing columns
- Feature engineering creates new columns
- Behavioral features are central to Spotify segmentation
- Demographic features are valuable for profiling
- `user_id` must be removed from model inputs but preserved separately
- Relevant features support the business objective
- Irrelevant features add noise
- Redundant features may over-weight one behavioral dimension
- Correlation is useful but not the only decision rule
- Low-variance features may provide little separation
- Derived features can improve business meaning
- Composite scores require scaling when units differ
- Division-by-zero and infinite values must be handled
- Data leakage must be avoided
- Candidate feature sets should be compared experimentally
- Every feature should have a clear business interpretation
- Feature decisions should be documented

---

# 40. Quick Reference Cheat Sheet

## Core Definitions

```text
Feature
= Model input

Feature Selection
= Choose existing features

Feature Engineering
= Create new features
```

## Remove Identifier

```python
user_ids = df[["user_id"]].copy()

X = df.drop(
    columns=["user_id"]
).copy()
```

## Candidate Core Features

```python
core_features = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
    "days_active_last_30",
    "skip_rate",
    "ads_skipped_pct"
]
```

## Derived Features

```python
df["active_day_ratio"] = (
    df["days_active_last_30"] / 30
)

df["friction_score"] = (
    df[
        [
            "skip_rate",
            "ads_skipped_pct"
        ]
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

## Redundancy Review

```python
corr = X.corr(
    method="spearman"
)
```

## Feature Decision

```text
Include
Exclude
Profile only
Engineer
Transform
Test
```

---

# 41. What Comes Next?

## Module 07 — Feature Scaling and Transformation

The next module will cover:

- Why scaling is required
- StandardScaler
- MinMaxScaler
- RobustScaler
- Log transformation
- PowerTransformer
- QuantileTransformer
- How scaling affects K-Means and GMM
- Comparing preprocessing experiments

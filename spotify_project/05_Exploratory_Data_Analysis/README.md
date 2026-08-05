# Module 05 — Exploratory Data Analysis

> A detailed beginner-friendly guide to understanding Spotify user data using descriptive statistics, distributions, skewness, univariate, bivariate and multivariate analysis, correlation, visualizations, and business interpretation.

---

## Table of Contents

1. [Module Overview](#1-module-overview)
2. [Learning Objectives](#2-learning-objectives)
3. [What Is Exploratory Data Analysis?](#3-what-is-exploratory-data-analysis)
4. [Why EDA Is Important](#4-why-eda-is-important)
5. [Spotify EDA Scope](#5-spotify-eda-scope)
6. [Preparing Data for EDA](#6-preparing-data-for-eda)
7. [Descriptive Statistics](#7-descriptive-statistics)
8. [Mean](#8-mean)
9. [Median](#9-median)
10. [Mode](#10-mode)
11. [Standard Deviation](#11-standard-deviation)
12. [Minimum and Maximum](#12-minimum-and-maximum)
13. [Percentiles and Quartiles](#13-percentiles-and-quartiles)
14. [Mean vs Median vs Mode](#14-mean-vs-median-vs-mode)
15. [Distribution Analysis](#15-distribution-analysis)
16. [Skewness](#16-skewness)
17. [Univariate Analysis](#17-univariate-analysis)
18. [Bivariate Analysis](#18-bivariate-analysis)
19. [Multivariate Analysis](#19-multivariate-analysis)
20. [Correlation](#20-correlation)
21. [Pearson vs Spearman Correlation](#21-pearson-vs-spearman-correlation)
22. [Visualization](#22-visualization)
23. [Histogram](#23-histogram)
24. [Box Plot](#24-box-plot)
25. [Bar Chart](#25-bar-chart)
26. [Scatter Plot](#26-scatter-plot)
27. [Correlation Heatmap](#27-correlation-heatmap)
28. [Spotify Behavioral Dimensions](#28-spotify-behavioral-dimensions)
29. [Business Insights](#29-business-insights)
30. [From Observation to Business Insight](#30-from-observation-to-business-insight)
31. [Complete Spotify EDA Workflow](#31-complete-spotify-eda-workflow)
32. [EDA Checklist](#32-eda-checklist)
33. [Important Terminology](#33-important-terminology)
34. [Interview Questions and Answers](#34-interview-questions-and-answers)
35. [Module Summary](#35-module-summary)
36. [Quick Reference Cheat Sheet](#36-quick-reference-cheat-sheet)
37. [What Comes Next?](#37-what-comes-next)

---

# 1. Module Overview

Exploratory Data Analysis, commonly called **EDA**, is the process of examining a dataset before building a Machine Learning model.

EDA helps us understand:

- What typical users look like
- How widely user behavior varies
- Whether distributions are symmetric or skewed
- Whether unusual values are present
- How two variables move together
- Whether several variables form meaningful behavioral patterns
- Which features may be useful for segmentation
- Which business questions the data can answer

The Spotify project contains behavioral and demographic information for users.

EDA helps convert those columns into understandable patterns.

```text
Clean Spotify Data
        ↓
Descriptive Statistics
        ↓
Distribution Analysis
        ↓
Univariate Analysis
        ↓
Bivariate Analysis
        ↓
Multivariate Analysis
        ↓
Business Interpretation
        ↓
Feature Selection and Clustering Preparation
```

---

# 2. Learning Objectives

By the end of this module, students should be able to:

- Explain Exploratory Data Analysis
- Calculate and interpret descriptive statistics
- Explain mean, median and mode
- Explain standard deviation
- Interpret minimum and maximum values
- Understand percentiles and quartiles
- Analyze distributions
- Calculate and interpret skewness
- Perform univariate analysis
- Perform bivariate analysis
- Perform multivariate analysis
- Calculate correlation
- Explain Pearson and Spearman correlation
- Select an appropriate visualization
- Create charts using Matplotlib
- Translate statistical observations into Spotify business insights
- Prepare an EDA summary for feature selection and clustering

---

# 3. What Is Exploratory Data Analysis?

EDA is the process of studying data using:

- Summary statistics
- Frequency tables
- Distribution analysis
- Visualizations
- Relationships between variables
- Business interpretation

EDA is called **exploratory** because we are exploring the data before making final modeling decisions.

## Easy Example

Suppose Spotify has the following listening minutes:

```text
30, 45, 50, 60, 300
```

EDA helps us ask:

- What is the average?
- What is the middle value?
- Is 300 unusually high?
- Is the distribution right-skewed?
- Does the high value represent a genuine power user?
- Should the feature be transformed before clustering?

---

# 4. Why EDA Is Important

Without EDA, we may:

- Select weak or redundant features
- Miss strongly skewed distributions
- Remove valid high-value users
- Misinterpret correlation
- Use an unsuitable scaler
- Create poor clusters
- Generate incorrect personas

EDA supports decisions in later modules:

| EDA Finding | Possible Next Decision |
|---|---|
| Strong right skew | Consider log or power transformation |
| Extreme valid users | Consider RobustScaler |
| Two features are highly correlated | Investigate redundancy |
| Category groups behave differently | Use demographic profiling |
| Rate feature is concentrated near 0 | Review usefulness |
| Feature has almost no variation | Consider excluding it |
| Distinct behavioral groups appear | Good signal for clustering |

---

# 5. Spotify EDA Scope

The project primarily analyzes behavioral data.

Important feature groups include:

## Engagement

- `daily_listening_minutes`
- `sessions_per_day`
- `days_active_last_30`
- `avg_session_minutes`

## Friction and Satisfaction

- `skip_rate`
- `liked_songs_pct`
- `ads_skipped_pct`

## Loyalty

- `repeat_track_rate`
- `repeat_artist_rate`
- `playlists_followed`
- `artists_followed`

## Taste and Audio Preference

- `mean_danceability`
- `mean_energy`
- `mean_valence`
- `mean_acousticness`
- `mean_speechiness`
- `mean_instrumentalness`
- `mean_tempo`

## Variety

- `std_energy`
- `std_valence`
- `std_tempo`
- `genre_diversity_score`

## Popularity Preference

- `mean_track_popularity`
- `pct_top_popularity_tracks`

## Demographics for Profiling

- `age`
- `country`
- `city_tier`
- `device_type`
- `subscription_tenure_months`

---

# 6. Preparing Data for EDA

Use the cleaned datasets from Module 04.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

spotify_user_behavior = pd.read_excel(
    "spotify_user_behavior.xlsx"
)

spotify_user_demo = pd.read_excel(
    "spotify_user_demo.xlsx"
)
```

Create a safe joined dataset:

```python
spotify_users = spotify_user_behavior.merge(
    spotify_user_demo,
    how="inner",
    on="user_id",
    validate="one_to_one"
)
```

Exclude the identifier from numerical analysis:

```python
behavior_numeric = (
    spotify_user_behavior
    .drop(columns=["user_id"])
    .select_dtypes(include="number")
)
```

Why exclude `user_id`?

Because it identifies users but does not describe their behavior.

---

# 7. Descriptive Statistics

Descriptive statistics summarize the main properties of a dataset.

Common measures include:

- Count
- Mean
- Standard deviation
- Minimum
- 25th percentile
- Median or 50th percentile
- 75th percentile
- Maximum

Pandas command:

```python
description = (
    behavior_numeric
    .describe()
    .T
    .round(3)
)

display(description)
```

The `.T` transposes the result so that each feature appears as one row.

Example structure:

| Feature | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `daily_listening_minutes` | ... | ... | ... | ... | ... | ... | ... | ... |
| `sessions_per_day` | ... | ... | ... | ... | ... | ... | ... | ... |

---

# 8. Mean

## 8.1 What Is Mean?

The mean is the arithmetic average.

Formula:

```text
Mean = Sum of all values ÷ Number of values
```

Example:

```text
Listening minutes = 30, 40, 50

Mean = (30 + 40 + 50) ÷ 3
Mean = 40
```

Pandas:

```python
mean_listening = (
    spotify_user_behavior[
        "daily_listening_minutes"
    ]
    .mean()
)

print(mean_listening)
```

---

## 8.2 Business Meaning

The mean listening time answers:

> On average, how many minutes does a Spotify user listen per day?

---

## 8.3 Limitation of Mean

The mean is sensitive to extreme values.

Example:

```text
30, 40, 50, 60, 500
```

The value `500` pulls the mean upward.

Therefore, the mean should be compared with the median.

---

# 9. Median

## 9.1 What Is Median?

The median is the middle value after sorting the data.

Example:

```text
20, 30, 40, 50, 60

Median = 40
```

For an even number of values:

```text
20, 30, 40, 50

Median = (30 + 40) ÷ 2
Median = 35
```

Pandas:

```python
median_listening = (
    spotify_user_behavior[
        "daily_listening_minutes"
    ]
    .median()
)
```

---

## 9.2 Why Median Is Important

Median is less influenced by extreme values.

If:

```text
Mean > Median
```

the distribution may be right-skewed.

If:

```text
Mean < Median
```

the distribution may be left-skewed.

---

## 9.3 Business Meaning

The median answers:

> What is the typical middle user's listening behavior?

For skewed customer behavior, the median may describe the typical user better than the mean.

---

# 10. Mode

## 10.1 What Is Mode?

The mode is the most frequently occurring value.

Example:

```text
Mobile, Mobile, Desktop, Tablet, Mobile

Mode = Mobile
```

Pandas:

```python
device_mode = (
    spotify_user_demo[
        "device_type"
    ]
    .mode()
)

print(device_mode)
```

A dataset can have:

- One mode
- Multiple modes
- No meaningful mode for nearly unique continuous values

---

## 10.2 Business Meaning

Mode is useful for questions such as:

- What is the most common device?
- What is the most common country?
- What is the most common city tier?
- What is the most frequent category?

Mode is especially useful for categorical data.

---

# 11. Standard Deviation

## 11.1 What Is Standard Deviation?

Standard deviation measures how far values usually spread from the mean.

```text
Low standard deviation
→ Users behave similarly

High standard deviation
→ Users behave very differently
```

Pandas:

```python
listening_std = (
    spotify_user_behavior[
        "daily_listening_minutes"
    ]
    .std()
)
```

---

## 11.2 Easy Example

Dataset A:

```text
48, 49, 50, 51, 52
```

Values are close together.

Standard deviation is low.

Dataset B:

```text
10, 30, 50, 70, 90
```

Values are more spread out.

Standard deviation is high.

---

## 11.3 Business Meaning

A high standard deviation in listening minutes may indicate:

- Casual users
- Regular users
- Heavy users
- Power users

This variation may support meaningful segmentation.

---

# 12. Minimum and Maximum

## 12.1 Minimum

The smallest value.

```python
minimum = (
    spotify_user_behavior[
        "daily_listening_minutes"
    ]
    .min()
)
```

## 12.2 Maximum

The largest value.

```python
maximum = (
    spotify_user_behavior[
        "daily_listening_minutes"
    ]
    .max()
)
```

---

## 12.3 Why Min and Max Matter

They help detect:

- Impossible values
- Extreme users
- Potential outliers
- Data-entry errors
- Valid behavioral extremes

Example questions:

- Is the minimum skip rate below 0?
- Is the maximum skip rate above 1?
- Is the maximum active days above 30?
- Are listening minutes extremely high?

Min and max are useful, but they should not be interpreted without percentiles and distributions.

---

# 13. Percentiles and Quartiles

## 13.1 What Is a Percentile?

A percentile tells us the value below which a percentage of observations falls.

Examples:

```text
25th percentile → 25% of users are at or below this value
50th percentile → Median
75th percentile → 75% of users are at or below this value
90th percentile → 90% of users are at or below this value
```

---

## 13.2 Quartiles

Quartiles divide data into four sections:

```text
Q1 = 25th percentile
Q2 = 50th percentile or median
Q3 = 75th percentile
```

---

## 13.3 Pandas Calculation

```python
percentiles = (
    spotify_user_behavior[
        "daily_listening_minutes"
    ]
    .quantile(
        [0.25, 0.50, 0.75, 0.90, 0.95]
    )
)

print(percentiles)
```

---

## 13.4 Business Use

Percentiles can help define behavioral groups.

Illustrative logic:

```text
Below 25th percentile
→ Lower-intensity listeners

25th to 75th percentile
→ Main user population

Above 90th percentile
→ Highly active users
```

These are analytical descriptions, not final personas.

The final segmentation should be based on multiple features.

---

# 14. Mean vs Median vs Mode

| Measure | Meaning | Best Used For | Limitation |
|---|---|---|---|
| Mean | Arithmetic average | Symmetric numerical data | Sensitive to extreme values |
| Median | Middle value | Skewed numerical data | Does not use all value magnitudes |
| Mode | Most common value | Categorical or repeated data | May have multiple results |

## Spotify Examples

| Business Question | Suitable Measure |
|---|---|
| Average daily listening minutes | Mean |
| Typical listening minutes in skewed data | Median |
| Most common device type | Mode |
| Most common country | Mode |
| Typical subscription tenure | Median and mean together |

---

# 15. Distribution Analysis

## 15.1 What Is a Distribution?

A distribution shows how values are spread across a variable.

It helps us understand:

- Where most values are located
- Whether values are symmetric
- Whether there are long tails
- Whether multiple peaks exist
- Whether extreme observations exist
- Whether transformation may be needed

---

## 15.2 Common Distribution Shapes

### Symmetric

```text
Mean ≈ Median
```

Values are balanced around the center.

### Right-Skewed

```text
Long tail on the right
Mean > Median
```

Possible Spotify examples:

- Playlists followed
- Artists followed
- Daily listening minutes
- Sessions per day

### Left-Skewed

```text
Long tail on the left
Mean < Median
```

### Bimodal or Multimodal

Two or more peaks may indicate different subgroups.

---

## 15.3 Distribution Summary Table

```python
distribution_summary = (
    behavior_numeric
    .agg(
        [
            "count",
            "mean",
            "median",
            "std",
            "min",
            "max",
            "skew"
        ]
    )
    .T
    .round(3)
)

display(distribution_summary)
```

---

# 16. Skewness

## 16.1 What Is Skewness?

Skewness measures the asymmetry of a distribution.

General interpretation:

| Skewness | Interpretation |
|---:|---|
| Around 0 | Approximately symmetric |
| Positive | Right-skewed |
| Negative | Left-skewed |
| Large absolute value | Stronger asymmetry |

Pandas:

```python
skewness = (
    behavior_numeric
    .skew()
    .sort_values(
        ascending=False
    )
)

display(skewness)
```

---

## 16.2 Positive Skew

```text
Most values are lower
A smaller number of values are very high
```

Spotify example:

A large number of users may follow only a few playlists, while a small number follow many playlists.

---

## 16.3 Why Skewness Matters for Clustering

Distance-based algorithms such as K-Means can be influenced by:

- Long tails
- Large scales
- Extreme values

Possible responses include:

- StandardScaler
- RobustScaler
- Log transformation
- Power transformation
- Quantile transformation

These decisions are made later after comparing preprocessing experiments.

---

## 16.4 Do Not Transform Automatically

A skewed distribution is not automatically bad.

It may represent real business behavior.

Always ask:

```text
Is the skew caused by errors?
Is the skew caused by real power users?
Does the model need transformation?
Will transformation reduce interpretability?
```

---

# 17. Univariate Analysis

## 17.1 What Is Univariate Analysis?

Univariate analysis studies one variable at a time.

```text
Uni = One
Variate = Variable
```

Examples:

- Distribution of listening minutes
- Most common device type
- Skip-rate summary
- Age distribution

---

## 17.2 Numerical Univariate Analysis

For each numerical column, examine:

- Count
- Mean
- Median
- Standard deviation
- Minimum
- Maximum
- Percentiles
- Skewness
- Histogram
- Box plot

Reusable function:

```python
def numerical_summary(
    df: pd.DataFrame,
    column: str
) -> pd.Series:
    series = df[column].dropna()

    return pd.Series({
        "count": series.count(),
        "mean": series.mean(),
        "median": series.median(),
        "mode": (
            series.mode().iloc[0]
            if not series.mode().empty
            else np.nan
        ),
        "std": series.std(),
        "min": series.min(),
        "p25": series.quantile(0.25),
        "p50": series.quantile(0.50),
        "p75": series.quantile(0.75),
        "p90": series.quantile(0.90),
        "max": series.max(),
        "skewness": series.skew()
    })
```

---

## 17.3 Categorical Univariate Analysis

For categorical data, examine:

- Unique values
- Frequency
- Percentage
- Mode

```python
device_distribution = (
    spotify_user_demo[
        "device_type"
    ]
    .value_counts(
        dropna=False
    )
    .rename_axis(
        "device_type"
    )
    .reset_index(
        name="users"
    )
)

device_distribution[
    "percentage"
] = (
    device_distribution[
        "users"
    ]
    .div(
        device_distribution[
            "users"
        ]
        .sum()
    )
    .mul(100)
    .round(2)
)

display(device_distribution)
```

---

# 18. Bivariate Analysis

## 18.1 What Is Bivariate Analysis?

Bivariate analysis studies the relationship between two variables.

```text
Bi = Two
```

Examples:

- Listening minutes vs sessions per day
- Listening minutes vs skip rate
- Device type vs average session length
- Country vs average listening minutes
- Age vs daily listening minutes

---

## 18.2 Numerical vs Numerical

Useful methods:

- Scatter plot
- Correlation
- Grouping into bands

Example:

```python
relationship = (
    spotify_user_behavior[
        [
            "daily_listening_minutes",
            "sessions_per_day"
        ]
    ]
    .corr()
)

display(relationship)
```

---

## 18.3 Categorical vs Numerical

Use `groupby()`:

```python
device_summary = (
    spotify_users
    .groupby(
        "device_type",
        observed=True
    )
    .agg(
        users=(
            "user_id",
            "nunique"
        ),
        avg_listening_minutes=(
            "daily_listening_minutes",
            "mean"
        ),
        median_listening_minutes=(
            "daily_listening_minutes",
            "median"
        ),
        avg_skip_rate=(
            "skip_rate",
            "mean"
        )
    )
    .reset_index()
)

display(device_summary)
```

---

## 18.4 Categorical vs Categorical

Use a cross-tabulation:

```python
country_device_table = (
    pd.crosstab(
        spotify_users["country"],
        spotify_users["device_type"],
        normalize="index"
    )
    .mul(100)
    .round(2)
)

display(country_device_table)
```

---

# 19. Multivariate Analysis

## 19.1 What Is Multivariate Analysis?

Multivariate analysis studies three or more variables together.

```text
Multi = Many
```

Spotify user behavior is naturally multivariate.

A user cannot be fully understood using only listening minutes.

Example:

```text
High listening minutes
+ High days active
+ Long sessions
+ Low skip rate
= Deeply engaged listener
```

Another user may have:

```text
Medium listening minutes
+ Many sessions
+ High skip rate
+ High genre diversity
= Exploratory listener
```

---

## 19.2 Multivariate Group Summary

```python
country_device_summary = (
    spotify_users
    .groupby(
        [
            "country",
            "device_type"
        ],
        observed=True
    )
    .agg(
        users=(
            "user_id",
            "nunique"
        ),
        avg_listening=(
            "daily_listening_minutes",
            "mean"
        ),
        avg_sessions=(
            "sessions_per_day",
            "mean"
        ),
        avg_skip_rate=(
            "skip_rate",
            "mean"
        )
    )
    .reset_index()
)

display(country_device_summary)
```

---

## 19.3 Why Multivariate Analysis Matters

Clustering is multivariate.

The algorithm groups users using several behavioral dimensions at the same time.

EDA should therefore examine:

- Individual feature behavior
- Pairwise relationships
- Combined business patterns

---

# 20. Correlation

## 20.1 What Is Correlation?

Correlation measures the direction and strength of a relationship between two numerical variables.

Values usually range from:

```text
-1 to +1
```

| Correlation | Meaning |
|---:|---|
| Close to +1 | Strong positive relationship |
| Close to 0 | Weak linear relationship |
| Close to -1 | Strong negative relationship |

---

## 20.2 Positive Correlation

When one variable increases, the other tends to increase.

Possible example:

```text
Sessions per day ↑
Daily listening minutes ↑
```

---

## 20.3 Negative Correlation

When one variable increases, the other tends to decrease.

Possible example:

```text
Skip rate ↑
Liked songs percentage ↓
```

This is a hypothesis to test, not an assumed project result.

---

## 20.4 Correlation Matrix

```python
correlation_matrix = (
    behavior_numeric
    .corr()
    .round(3)
)

display(correlation_matrix)
```

---

## 20.5 Strongest Correlation Pairs

```python
correlation_pairs = (
    correlation_matrix
    .where(
        np.triu(
            np.ones(
                correlation_matrix.shape
            ),
            k=1
        )
        .astype(bool)
    )
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

correlation_pairs = (
    correlation_pairs
    .sort_values(
        "absolute_correlation",
        ascending=False
    )
)

display(
    correlation_pairs.head(20)
)
```

---

## 20.6 Correlation Does Not Mean Causation

A relationship does not prove that one variable causes the other.

Example:

If listening minutes and playlists followed are correlated, we cannot immediately conclude:

```text
Following playlists causes higher listening time.
```

Possible explanations include:

- Engaged users both listen more and follow more playlists
- Recommendations drive both behaviors
- Another variable influences both

---

# 21. Pearson vs Spearman Correlation

## 21.1 Pearson Correlation

Pearson measures linear relationships.

Use it when:

- Variables are numerical
- Relationship is approximately linear
- Extreme values are not dominating

```python
pearson_corr = (
    behavior_numeric
    .corr(
        method="pearson"
    )
)
```

---

## 21.2 Spearman Correlation

Spearman measures monotonic rank relationships.

Use it when:

- Data is skewed
- Relationship is monotonic but not linear
- Outliers may influence Pearson
- Variables are ordinal or rank-based

```python
spearman_corr = (
    behavior_numeric
    .corr(
        method="spearman"
    )
)
```

---

## 21.3 Comparison

| Pearson | Spearman |
|---|---|
| Measures linear relationship | Measures rank-based monotonic relationship |
| Uses raw values | Uses ranks |
| More sensitive to outliers | More robust to extreme values |
| Suitable for linear patterns | Suitable for skewed or non-linear monotonic patterns |

Comparing both can improve understanding.

---

# 22. Visualization

Visualizations make statistical patterns easier to understand.

A chart should answer a specific question.

| Business Question | Suitable Chart |
|---|---|
| How is one numerical feature distributed? | Histogram |
| Are extreme values present? | Box plot |
| Which category has more users? | Bar chart |
| How are two numeric features related? | Scatter plot |
| Which features move together? | Correlation heatmap |
| How does a metric compare across categories? | Bar chart or box plot |

Good visualization requires:

- Clear title
- Clear axis labels
- Suitable chart type
- Readable category labels
- No unnecessary decoration
- Business interpretation

---

# 23. Histogram

## 23.1 Purpose

A histogram shows the distribution of one numerical variable.

```python
column = "daily_listening_minutes"

plt.figure(figsize=(8, 5))
plt.hist(
    spotify_user_behavior[column],
    bins=60
)
plt.title(
    "Distribution of Daily Listening Minutes"
)
plt.xlabel(
    "Daily Listening Minutes"
)
plt.ylabel(
    "Number of Users"
)
plt.tight_layout()
plt.show()
```

---

## 23.2 What to Observe

- Center
- Spread
- Skewness
- Long tails
- Multiple peaks
- Empty ranges
- Extreme values

---

# 24. Box Plot

## 24.1 Purpose

A box plot summarizes:

- Median
- Q1
- Q3
- Interquartile range
- Potential outliers

```python
column = "daily_listening_minutes"

plt.figure(figsize=(8, 4))
plt.boxplot(
    spotify_user_behavior[column]
    .dropna(),
    vert=False
)
plt.title(
    "Box Plot of Daily Listening Minutes"
)
plt.xlabel(
    "Daily Listening Minutes"
)
plt.tight_layout()
plt.show()
```

---

## 24.2 Important Note

Points beyond the whiskers are statistical outliers.

They are not automatically errors.

---

# 25. Bar Chart

## 25.1 Purpose

A bar chart compares categories.

```python
device_counts = (
    spotify_user_demo[
        "device_type"
    ]
    .value_counts()
)

plt.figure(figsize=(8, 5))
plt.bar(
    device_counts.index,
    device_counts.values
)
plt.title(
    "Spotify Users by Device Type"
)
plt.xlabel(
    "Device Type"
)
plt.ylabel(
    "Number of Users"
)
plt.tight_layout()
plt.show()
```

---

# 26. Scatter Plot

## 26.1 Purpose

A scatter plot shows the relationship between two numerical variables.

```python
plt.figure(figsize=(8, 5))
plt.scatter(
    spotify_user_behavior[
        "sessions_per_day"
    ],
    spotify_user_behavior[
        "daily_listening_minutes"
    ],
    alpha=0.3
)
plt.title(
    "Sessions per Day vs Daily Listening Minutes"
)
plt.xlabel(
    "Sessions per Day"
)
plt.ylabel(
    "Daily Listening Minutes"
)
plt.tight_layout()
plt.show()
```

Observe:

- Positive or negative direction
- Linear or curved pattern
- Separate groups
- Dense regions
- Extreme values

---

# 27. Correlation Heatmap

This module uses only Matplotlib.

```python
correlation_matrix = (
    behavior_numeric
    .corr()
)

plt.figure(figsize=(14, 12))
image = plt.imshow(
    correlation_matrix,
    aspect="auto"
)

plt.colorbar(
    image,
    label="Correlation"
)

plt.xticks(
    range(
        len(correlation_matrix.columns)
    ),
    correlation_matrix.columns,
    rotation=90
)

plt.yticks(
    range(
        len(correlation_matrix.index)
    ),
    correlation_matrix.index
)

plt.title(
    "Spotify Behavioral Feature Correlation"
)
plt.tight_layout()
plt.show()
```

A heatmap helps identify:

- Strong positive relationships
- Strong negative relationships
- Groups of related features
- Potentially redundant features

---

# 28. Spotify Behavioral Dimensions

The persona framework uses five strategic behavioral dimensions.

| Dimension | Main Feature | Business Meaning |
|---|---|---|
| Intensity | `daily_listening_minutes` | Total daily audio consumption |
| Frequency | `sessions_per_day` | How often the user returns |
| Depth | `avg_session_minutes` | Length of each listening session |
| Consistency | `days_active_last_30` | Regularity across 30 days |
| Friction | `skip_rate` and `ads_skipped_pct` | Tolerance for content and interruptions |

These dimensions should be explored individually and together.

---

## 28.1 Intensity

Questions:

- What is the typical daily listening time?
- Is the distribution right-skewed?
- Are there high-intensity power users?

---

## 28.2 Frequency

Questions:

- How many sessions do users start per day?
- Do frequent users also listen longer?
- Are there frequent but shallow users?

---

## 28.3 Depth

Questions:

- Are sessions short or immersive?
- Does session depth differ by device?
- Do long sessions have lower skip rates?

---

## 28.4 Consistency

Questions:

- How many days are users active?
- Are some users active nearly every day?
- Does consistency relate to subscription tenure?

---

## 28.5 Friction

Questions:

- Which users skip songs frequently?
- Which users skip advertisements frequently?
- Is high friction linked to exploration or dissatisfaction?
- Could high ad skipping indicate Premium conversion potential?

---

# 29. Business Insights

EDA should not stop with statistics.

Each finding should connect to a business question.

## 29.1 Engagement Insight

Possible observation:

```text
Listening minutes and active days increase together.
```

Possible business meaning:

```text
Consistent users may form a loyal or high-lifetime-value segment.
```

---

## 29.2 Exploration Insight

Possible observation:

```text
Users with high genre diversity also have higher skip rates.
```

Possible business meaning:

```text
These users may be active explorers rather than dissatisfied users.
Recommendation diversity may be valuable.
```

---

## 29.3 Premium Conversion Insight

Possible observation:

```text
Highly active users also skip a large percentage of advertisements.
```

Possible business meaning:

```text
They may receive strong value from an ad-free Premium plan.
```

---

## 29.4 Retention Insight

Possible observation:

```text
Users with low days active and long gaps between plays show weak usage consistency.
```

Possible business meaning:

```text
They may require re-engagement campaigns.
```

---

## 29.5 Personalization Insight

Possible observation:

```text
Audio-preference features show meaningful variation across users.
```

Possible business meaning:

```text
Recommendation strategies should reflect mood, energy, tempo and genre diversity.
```

---

# 30. From Observation to Business Insight

Use the following format:

```text
Statistical Observation
        ↓
Behavioral Interpretation
        ↓
Business Risk or Opportunity
        ↓
Recommended Next Analysis
```

## Example

```text
Observation:
Daily listening minutes are strongly right-skewed.

Interpretation:
Most users have moderate usage, while a smaller group listens heavily.

Opportunity:
Heavy listeners may represent high-value or Premium-ready users.

Next Analysis:
Compare heavy listeners with skip rate, days active, ad skipping and tenure.
```

---

## Insight Template

| Section | Question |
|---|---|
| Observation | What does the statistic or chart show? |
| Evidence | Which metric, percentile or relationship supports it? |
| Interpretation | What user behavior may explain it? |
| Business Impact | Why does it matter to Spotify? |
| Action | What should be analyzed or tested next? |
| Caution | What alternative explanation exists? |

---

# 31. Complete Spotify EDA Workflow

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

behavior = pd.read_excel(
    "spotify_user_behavior.xlsx"
)

demo = pd.read_excel(
    "spotify_user_demo.xlsx"
)

users = behavior.merge(
    demo,
    on="user_id",
    how="inner",
    validate="one_to_one"
)

numeric_behavior = (
    behavior
    .drop(columns=["user_id"])
    .select_dtypes(include="number")
)

descriptive_statistics = (
    numeric_behavior
    .describe(
        percentiles=[
            0.10,
            0.25,
            0.50,
            0.75,
            0.90,
            0.95
        ]
    )
    .T
)

descriptive_statistics[
    "median"
] = numeric_behavior.median()

descriptive_statistics[
    "skewness"
] = numeric_behavior.skew()

descriptive_statistics[
    "missing_pct"
] = (
    numeric_behavior
    .isna()
    .mean()
    .mul(100)
)

descriptive_statistics = (
    descriptive_statistics
    .round(3)
)

display(
    descriptive_statistics
)

correlation_pearson = (
    numeric_behavior
    .corr(
        method="pearson"
    )
)

correlation_spearman = (
    numeric_behavior
    .corr(
        method="spearman"
    )
)

display(correlation_pearson)
display(correlation_spearman)
```

A complete reusable implementation is available in:

```text
examples/spotify_eda_workflow.py
```

---

# 32. EDA Checklist

## Dataset Preparation

- [ ] Clean datasets loaded
- [ ] Dataset shapes validated
- [ ] `user_id` excluded from numerical statistics
- [ ] Behavioral and demographic datasets joined safely

## Descriptive Statistics

- [ ] Count reviewed
- [ ] Mean reviewed
- [ ] Median reviewed
- [ ] Mode reviewed where meaningful
- [ ] Standard deviation reviewed
- [ ] Minimum and maximum reviewed
- [ ] Percentiles reviewed

## Distribution Analysis

- [ ] Histograms created
- [ ] Box plots created
- [ ] Skewness calculated
- [ ] Long tails identified
- [ ] Potential outliers investigated
- [ ] Multiple peaks investigated

## Relationships

- [ ] Numerical vs numerical analyzed
- [ ] Categorical vs numerical analyzed
- [ ] Categorical vs categorical analyzed
- [ ] Pearson correlation reviewed
- [ ] Spearman correlation reviewed
- [ ] Strong correlation pairs documented

## Business Interpretation

- [ ] Engagement insights written
- [ ] Retention insights written
- [ ] Premium-conversion opportunities considered
- [ ] Ad-behavior insights considered
- [ ] Listening patterns interpreted
- [ ] Alternative explanations recorded
- [ ] Feature-selection implications documented

---

# 33. Important Terminology

| Term | Meaning |
|---|---|
| EDA | Exploratory Data Analysis |
| Descriptive statistics | Numerical summary of data |
| Mean | Arithmetic average |
| Median | Middle value |
| Mode | Most frequent value |
| Standard deviation | Typical spread around mean |
| Minimum | Smallest value |
| Maximum | Largest value |
| Percentile | Value below which a percentage falls |
| Quartile | One of four data sections |
| Distribution | Pattern of values |
| Skewness | Distribution asymmetry |
| Right skew | Long tail on the right |
| Left skew | Long tail on the left |
| Univariate | One-variable analysis |
| Bivariate | Two-variable analysis |
| Multivariate | Three-or-more-variable analysis |
| Correlation | Strength and direction of relationship |
| Pearson correlation | Linear correlation |
| Spearman correlation | Rank-based monotonic correlation |
| Histogram | Numeric distribution chart |
| Box plot | Median, quartiles and outlier chart |
| Bar chart | Category comparison chart |
| Scatter plot | Two-numeric-variable relationship chart |
| Heatmap | Matrix represented through color intensity |
| Business insight | Actionable interpretation of data |
| Causation | One variable directly produces change in another |

---

# 34. Interview Questions and Answers

## 1. What is Exploratory Data Analysis?

EDA is the process of understanding a dataset using statistics, distributions, visualizations and relationship analysis before modeling.

---

## 2. Why is EDA important?

It identifies patterns, skewness, extreme values, relationships and potential feature problems before model training.

---

## 3. What is descriptive statistics?

Descriptive statistics summarize the main properties of data using measures such as mean, median, standard deviation, minimum, maximum and percentiles.

---

## 4. What is mean?

The arithmetic average.

---

## 5. What is median?

The middle value after sorting the data.

---

## 6. When is median preferred over mean?

When the data is skewed or influenced by extreme values.

---

## 7. What is mode?

The most frequently occurring value.

---

## 8. What is standard deviation?

A measure of spread around the mean.

---

## 9. What do minimum and maximum tell us?

They show the observed boundaries and help identify invalid or extreme values.

---

## 10. What is a percentile?

A value below which a specified percentage of observations falls.

---

## 11. What is the 50th percentile?

The median.

---

## 12. What is distribution analysis?

Studying how values are spread, centered and shaped.

---

## 13. What is skewness?

A measure of distribution asymmetry.

---

## 14. What does positive skewness mean?

The distribution has a long right tail.

---

## 15. Why does skewness matter for K-Means?

Long tails and extreme values may influence distance calculations and cluster centers.

---

## 16. What is univariate analysis?

Analysis of one variable.

---

## 17. What is bivariate analysis?

Analysis of the relationship between two variables.

---

## 18. What is multivariate analysis?

Analysis involving three or more variables.

---

## 19. What is correlation?

A measure of relationship strength and direction between numerical variables.

---

## 20. What is the range of correlation?

From `-1` to `+1`.

---

## 21. What is Pearson correlation?

A measure of linear relationship using raw values.

---

## 22. What is Spearman correlation?

A rank-based measure of monotonic relationship.

---

## 23. Why compare Pearson and Spearman?

Differences may reveal skewness, outlier influence or non-linear monotonic relationships.

---

## 24. Does correlation prove causation?

No.

---

## 25. Why exclude `user_id` from EDA statistics?

It identifies users but does not measure behavior.

---

## 26. Which chart is used for a numerical distribution?

Histogram.

---

## 27. Which chart is used for category counts?

Bar chart.

---

## 28. Which chart shows two numerical variables?

Scatter plot.

---

## 29. What does a box plot show?

Median, quartiles, spread and potential outliers.

---

## 30. How can EDA support business decisions?

It identifies engagement patterns, churn indicators, Premium opportunities and personalization needs.

---

# 35. Module Summary

In this module, we learned:

- EDA is performed after cleaning and before modeling
- Descriptive statistics summarize user behavior
- Mean is the arithmetic average
- Median represents the middle user
- Mode identifies the most common category or value
- Standard deviation measures spread
- Minimum and maximum show observed boundaries
- Percentiles describe user positions within a distribution
- Distribution analysis reveals shape and tails
- Skewness measures asymmetry
- Univariate analysis studies one variable
- Bivariate analysis studies two variables
- Multivariate analysis studies several variables
- Correlation measures relationships
- Pearson and Spearman serve different purposes
- Visualizations make statistical patterns easier to understand
- EDA must produce business insights, not only charts
- Spotify behavior should be studied through intensity, frequency, depth, consistency and friction
- EDA findings guide feature selection, scaling and transformation

---

# 36. Quick Reference Cheat Sheet

| Objective | Pandas / Matplotlib |
|---|---|
| Full numeric summary | `df.describe().T` |
| Mean | `df[col].mean()` |
| Median | `df[col].median()` |
| Mode | `df[col].mode()` |
| Standard deviation | `df[col].std()` |
| Minimum | `df[col].min()` |
| Maximum | `df[col].max()` |
| Percentiles | `df[col].quantile([...])` |
| Skewness | `df[col].skew()` |
| Category counts | `df[col].value_counts()` |
| Group summary | `df.groupby(...).agg(...)` |
| Pearson correlation | `df.corr(method="pearson")` |
| Spearman correlation | `df.corr(method="spearman")` |
| Histogram | `plt.hist()` |
| Bar chart | `plt.bar()` |
| Scatter plot | `plt.scatter()` |
| Box plot | `plt.boxplot()` |
| Heatmap | `plt.imshow()` |

---

# 37. What Comes Next?

## Module 06 — Statistics for Machine Learning

The next module can cover:

- Population and sample
- Variance
- Probability
- Normal distribution
- Z-score
- Confidence intervals
- Hypothesis testing
- Statistical significance
- Covariance
- Statistical interpretation for Machine Learning

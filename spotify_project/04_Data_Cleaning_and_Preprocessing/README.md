# Module 04 — Data Cleaning and Preprocessing

> A detailed beginner-friendly guide to validating, cleaning, and preparing the Spotify user datasets before Exploratory Data Analysis and Machine Learning.

---

## Table of Contents

1. [Module Overview](#1-module-overview)
2. [Learning Objectives](#2-learning-objectives)
3. [Why Data Cleaning Matters](#3-why-data-cleaning-matters)
4. [Spotify Project Data-Quality Baseline](#4-spotify-project-data-quality-baseline)
5. [Recommended Cleaning Workflow](#5-recommended-cleaning-workflow)
6. [Loading the Spotify Datasets](#6-loading-the-spotify-datasets)
7. [Protecting the Raw Data](#7-protecting-the-raw-data)
8. [Shape and Schema Validation](#8-shape-and-schema-validation)
9. [Missing Values](#9-missing-values)
10. [Duplicate Records](#10-duplicate-records)
11. [Wrong Data Types](#11-wrong-data-types)
12. [Invalid Values](#12-invalid-values)
13. [Inconsistent Values](#13-inconsistent-values)
14. [Range Validation](#14-range-validation)
15. [Outlier Detection](#15-outlier-detection)
16. [Data Formatting](#16-data-formatting)
17. [User ID Validation](#17-user-id-validation)
18. [Dataset Relationship Validation](#18-dataset-relationship-validation)
19. [Complete Data-Quality Checks](#19-complete-data-quality-checks)
20. [Data-Cleaning Decisions](#20-data-cleaning-decisions)
21. [Cleaning vs Transformation](#21-cleaning-vs-transformation)
22. [Building a Reusable Cleaning Pipeline](#22-building-a-reusable-cleaning-pipeline)
23. [Before-and-After Validation](#23-before-and-after-validation)
24. [Data-Quality Report](#24-data-quality-report)
25. [Spotify Project Cleaning Conclusion](#25-spotify-project-cleaning-conclusion)
26. [Important Terminology](#26-important-terminology)
27. [Interview Questions and Answers](#27-interview-questions-and-answers)
28. [Module Summary](#28-module-summary)
29. [Quick Reference Cheat Sheet](#29-quick-reference-cheat-sheet)
30. [What Comes Next?](#30-what-comes-next)

---

# 1. Module Overview

Data cleaning is the process of identifying and handling problems in a dataset before analysis or Machine Learning.

Typical data problems include:

- Missing values
- Duplicate records
- Wrong data types
- Invalid values
- Inconsistent categories
- Values outside expected ranges
- Extreme observations
- Incorrect formatting
- Broken identifiers
- Unmatched records between datasets

The objective is not to change data unnecessarily.

The objective is to make sure the data is:

```text
Complete
Accurate
Consistent
Valid
Unique
Usable
Traceable
```

In this Spotify project, the two main tables are:

```text
spotify_user_behavior
spotify_user_demo
```

They must be validated before:

- Exploratory Data Analysis
- Feature engineering
- Scaling
- K-Means clustering
- Gaussian Mixture Models
- Cluster profiling
- Persona creation

---

# 2. Learning Objectives

By the end of this module, students should be able to:

- Explain why data cleaning is required
- Create a safe copy before cleaning
- Check missing values and fill rates
- Detect duplicate rows and duplicate user IDs
- Identify wrong data types
- Detect invalid numerical and categorical values
- Standardize inconsistent text values
- Validate business ranges
- Detect potential outliers using IQR
- Format column names and text values
- Validate `user_id`
- Validate the relationship between Spotify datasets
- Create a data-quality issue report
- Make documented cleaning decisions
- Build a reusable cleaning pipeline
- Confirm whether the final data is ready for analysis

---

# 3. Why Data Cleaning Matters

A Machine Learning model learns patterns from the data given to it.

If the data contains errors, the model may learn incorrect patterns.

```text
Poor-quality data
        ↓
Incorrect analysis
        ↓
Incorrect clusters
        ↓
Incorrect personas
        ↓
Incorrect business decisions
```

## Example

Suppose `skip_rate` should be between `0` and `1`.

Valid values:

```text
0.10
0.45
0.92
```

Invalid values:

```text
-0.20
1.40
75
```

A value of `75` may mean:

- 75%
- 0.75 entered incorrectly
- A data-entry error
- A completely different measurement

We must investigate before correcting or deleting it.

---

# 4. Spotify Project Data-Quality Baseline

The project quality checks establish the following expected structure:

| Check | Expected Result |
|---|---:|
| Behavioral dataset shape | 108,000 rows × 26 columns |
| Demographic dataset shape | 108,000 rows × 6 columns |
| Unique users in behavior | 108,000 |
| Unique users in demo | 108,000 |
| Duplicate `user_id` in behavior | 0 |
| Duplicate `user_id` in demo | 0 |
| Users missing from either dataset | 0 |
| Missing values | 0% in the current project dataset |
| Relationship | One-to-one using `user_id` |

This means the current project data already has a strong quality baseline.

However, we still learn every cleaning technique because real production data may not be as clean.

---

# 5. Recommended Cleaning Workflow

Use the following order:

```text
1. Load data
2. Create raw backup copies
3. Validate shapes
4. Validate required columns
5. Inspect data types
6. Check missing values
7. Check duplicate rows
8. Validate user IDs
9. Validate numerical ranges
10. Validate categorical values
11. Detect potential outliers
12. Standardize formatting
13. Apply approved cleaning decisions
14. Validate dataset relationships
15. Compare before and after
16. Export a quality report
```

Why this order?

Because each step protects the next one.

For example:

- Shape checks confirm the correct tables were loaded.
- Key checks confirm the grain.
- Missing-value checks tell us whether imputation is required.
- Range checks identify impossible values.
- Outlier checks identify unusual but possibly valid behavior.

---

# 6. Loading the Spotify Datasets

## 6.1 Databricks / Spark Catalog

The project source uses Spark catalog tables and converts them to Pandas:

```python
import pandas as pd

spotify_user_behavior = (
    spark
    .table("workspace.spotify.spotify_user_behavior")
    .toPandas()
)

spotify_user_demo = (
    spark
    .table("workspace.spotify.spotify_user_demo")
    .toPandas()
)
```

Why `.toPandas()`?

The datasets contain 108,000 rows, which is manageable for local Pandas validation in this project.

---

## 6.2 Excel Files

For local practice:

```python
import pandas as pd

spotify_user_behavior = pd.read_excel(
    "spotify_user_behavior.xlsx"
)

spotify_user_demo = pd.read_excel(
    "spotify_user_demo.xlsx"
)
```

---

# 7. Protecting the Raw Data

Never clean the only copy of a dataset.

Create working copies:

```python
behavior_raw = spotify_user_behavior.copy()
demo_raw = spotify_user_demo.copy()

behavior_clean = behavior_raw.copy()
demo_clean = demo_raw.copy()
```

## Why Use `.copy()`?

It allows us to:

- Compare before and after
- Recover from mistakes
- Preserve raw evidence
- Avoid modifying the original DataFrame
- Maintain reproducibility

## Recommended Naming

```text
behavior_raw
behavior_clean

demo_raw
demo_clean
```

---

# 8. Shape and Schema Validation

## 8.1 Shape Validation

```python
print(
    "Behavior shape:",
    behavior_clean.shape
)

print(
    "Demo shape:",
    demo_clean.shape
)
```

Expected:

```text
Behavior shape: (108000, 26)
Demo shape: (108000, 6)
```

A wrong shape may indicate:

- Wrong table loaded
- Missing columns
- Partial file
- Incorrect worksheet
- Upstream processing failure

---

## 8.2 Required Column Validation

```python
required_behavior_columns = {
    "user_id",
    "daily_listening_minutes",
    "sessions_per_day",
    "days_active_last_30",
    "avg_session_minutes",
    "skip_rate",
    "liked_songs_pct",
    "ads_skipped_pct"
}

missing_behavior_columns = (
    required_behavior_columns
    - set(behavior_clean.columns)
)

if missing_behavior_columns:
    raise ValueError(
        "Missing behavior columns: "
        f"{sorted(missing_behavior_columns)}"
    )
```

For demographic data:

```python
required_demo_columns = {
    "user_id",
    "age",
    "country",
    "city_tier",
    "device_type",
    "subscription_tenure_months"
}

missing_demo_columns = (
    required_demo_columns
    - set(demo_clean.columns)
)

if missing_demo_columns:
    raise ValueError(
        "Missing demo columns: "
        f"{sorted(missing_demo_columns)}"
    )
```

---

# 9. Missing Values

## 9.1 What Is a Missing Value?

A missing value means information is unavailable.

Common Pandas missing values:

```text
NaN
None
NaT
```

Text may also hide missing values:

```text
""
"NA"
"N/A"
"null"
"unknown"
"-"
```

---

## 9.2 Check Missing Counts

```python
print(
    behavior_clean.isna().sum()
)

print(
    demo_clean.isna().sum()
)
```

---

## 9.3 Missing Percentage and Fill Rate

```python
def fill_rate(df: pd.DataFrame) -> pd.DataFrame:
    report = (
        df.isna()
        .mean()
        .mul(100)
        .round(2)
        .sort_values(ascending=False)
        .reset_index()
    )

    report.columns = [
        "column",
        "missing_pct"
    ]

    report["fill_rate_pct"] = (
        100 - report["missing_pct"]
    ).round(2)

    return report
```

Usage:

```python
display(
    fill_rate(behavior_clean)
)

display(
    fill_rate(demo_clean)
)
```

For the current Spotify project data, all columns have a 100% fill rate.

---

## 9.4 Hidden Missing Values

Convert blank-like values to proper missing values:

```python
missing_tokens = [
    "",
    " ",
    "NA",
    "N/A",
    "null",
    "None",
    "-"
]

behavior_clean = behavior_clean.replace(
    missing_tokens,
    pd.NA
)

demo_clean = demo_clean.replace(
    missing_tokens,
    pd.NA
)
```

For text columns, trim first:

```python
text_columns = [
    "country",
    "device_type"
]

for column in text_columns:
    demo_clean[column] = (
        demo_clean[column]
        .astype("string")
        .str.strip()
    )
```

---

## 9.5 Missing-Value Decisions

Possible strategies:

| Strategy | When to Use |
|---|---|
| Keep missing | Missingness itself may carry meaning |
| Drop rows | Very few rows are affected and data is not recoverable |
| Fill with median | Skewed numerical data |
| Fill with mean | Symmetric numerical data without extreme values |
| Fill with mode | Categorical data |
| Fill with `"Unknown"` | Category is genuinely unavailable |
| Investigate source | Critical key or high-value business field |
| Drop column | Excessive missingness and low business value |

---

## 9.6 Numerical Imputation Example

```python
median_value = (
    behavior_clean[
        "daily_listening_minutes"
    ]
    .median()
)

behavior_clean[
    "daily_listening_minutes"
] = (
    behavior_clean[
        "daily_listening_minutes"
    ]
    .fillna(median_value)
)
```

---

## 9.7 Categorical Imputation Example

```python
demo_clean["device_type"] = (
    demo_clean["device_type"]
    .fillna("Unknown")
)
```

---

## 9.8 Important Rule

Do not automatically fill every missing value.

First ask:

```text
Why is the value missing?
How many rows are affected?
Is the column important?
Will the cleaning decision change the business meaning?
```

---

# 10. Duplicate Records

## 10.1 What Is a Duplicate?

A duplicate record repeats information already present.

Two types:

### Exact Duplicate Row

Every column is repeated.

### Duplicate Business Key

The same `user_id` appears more than once, even if other values differ.

---

## 10.2 Exact Duplicate Rows

```python
behavior_exact_duplicates = (
    behavior_clean
    .duplicated()
    .sum()
)

demo_exact_duplicates = (
    demo_clean
    .duplicated()
    .sum()
)

print(
    "Behavior exact duplicates:",
    behavior_exact_duplicates
)

print(
    "Demo exact duplicates:",
    demo_exact_duplicates
)
```

To display them:

```python
display(
    behavior_clean[
        behavior_clean.duplicated(
            keep=False
        )
    ]
)
```

---

## 10.3 Duplicate User IDs

```python
behavior_duplicate_ids = (
    behavior_clean["user_id"]
    .duplicated()
    .sum()
)

demo_duplicate_ids = (
    demo_clean["user_id"]
    .duplicated()
    .sum()
)

print(
    "Behavior duplicate user IDs:",
    behavior_duplicate_ids
)

print(
    "Demo duplicate user IDs:",
    demo_duplicate_ids
)
```

The current project result is:

```text
0 duplicate user IDs in both datasets
```

---

## 10.4 Why Duplicate IDs Are Serious

The grain is:

```text
One row per user
```

If one user appears twice:

- User counts become incorrect
- A one-to-one join may become one-to-many
- Some users may influence clustering more than others
- Aggregate metrics become biased

---

## 10.5 Removing Exact Duplicates

Only after confirmation:

```python
behavior_clean = (
    behavior_clean
    .drop_duplicates()
    .copy()
)
```

For duplicate keys, do not immediately use:

```python
drop_duplicates("user_id")
```

First investigate which row is correct.

---

## 10.6 Duplicate-Key Investigation

```python
duplicate_users = (
    behavior_clean[
        behavior_clean["user_id"]
        .duplicated(keep=False)
    ]
    .sort_values("user_id")
)

display(duplicate_users)
```

Possible decisions:

- Keep the latest record
- Aggregate records
- Correct an upstream duplication
- Remove a confirmed duplicate
- Escalate conflicting records

---

# 11. Wrong Data Types

## 11.1 What Is a Wrong Data Type?

A column has a wrong data type when Pandas stores it differently from its business meaning.

Examples:

```text
age stored as text
skip_rate stored as object
user_id stored as float
city_tier stored as free text
```

---

## 11.2 Inspect Data Types

```python
print(
    behavior_clean.dtypes
)

print(
    demo_clean.dtypes
)
```

or:

```python
behavior_clean.info()
demo_clean.info()
```

---

## 11.3 Numeric Conversion

```python
numeric_behavior_columns = [
    column
    for column in behavior_clean.columns
    if column != "user_id"
]

for column in numeric_behavior_columns:
    behavior_clean[column] = (
        pd.to_numeric(
            behavior_clean[column],
            errors="coerce"
        )
    )
```

Why use `errors="coerce"`?

Invalid text is converted to `NaN`, allowing us to detect it.

---

## 11.4 Integer Conversion

For a nullable integer:

```python
demo_clean["age"] = (
    pd.to_numeric(
        demo_clean["age"],
        errors="coerce"
    )
    .astype("Int64")
)
```

`Int64` supports missing values.

---

## 11.5 String Conversion

```python
demo_clean["country"] = (
    demo_clean["country"]
    .astype("string")
)
```

---

## 11.6 Category Conversion

```python
demo_clean["device_type"] = (
    demo_clean["device_type"]
    .astype("category")
)
```

Use category dtype when:

- Values repeat frequently
- Categories are known
- Memory efficiency is useful
- Grouping and filtering are common

---

# 12. Invalid Values

## 12.1 What Is an Invalid Value?

An invalid value breaks a business or logical rule.

Examples:

```text
age = -4
days_active_last_30 = 42
skip_rate = 1.25
country = "123"
device_type = "Car"
```

---

## 12.2 Invalid vs Outlier

| Invalid Value | Outlier |
|---|---|
| Impossible | Unusual but possible |
| Must be corrected, removed, or quarantined | Must be investigated |
| `skip_rate = 1.4` | `daily_listening_minutes = 700` |
| `age = -2` | `age = 70` |

This difference is critical.

---

## 12.3 Flag Invalid Values

```python
invalid_skip_rate = (
    ~behavior_clean["skip_rate"]
    .between(0, 1)
)

display(
    behavior_clean[
        invalid_skip_rate
    ]
)
```

---

## 12.4 Invalid Category Values

```python
allowed_devices = {
    "Mobile",
    "Desktop",
    "Tablet"
}

invalid_devices = (
    ~demo_clean["device_type"]
    .isin(allowed_devices)
)

display(
    demo_clean[
        invalid_devices
    ]
)
```

---

# 13. Inconsistent Values

## 13.1 What Are Inconsistent Values?

Inconsistent values represent the same meaning using different formats.

Example:

```text
Mobile
mobile
MOBILE
 Mobile
```

These are logically the same category.

---

## 13.2 Standardize Text

```python
demo_clean["device_type"] = (
    demo_clean["device_type"]
    .astype("string")
    .str.strip()
    .str.title()
)
```

Country values:

```python
demo_clean["country"] = (
    demo_clean["country"]
    .astype("string")
    .str.strip()
    .str.upper()
)
```

---

## 13.3 Map Known Variations

```python
device_map = {
    "Phone": "Mobile",
    "Smartphone": "Mobile",
    "PC": "Desktop",
    "Laptop": "Desktop"
}

demo_clean["device_type"] = (
    demo_clean["device_type"]
    .replace(device_map)
)
```

---

## 13.4 Validate After Standardization

```python
print(
    demo_clean["device_type"]
    .value_counts(dropna=False)
)
```

Never assume the mapping worked.

Always check the result.

---

# 14. Range Validation

## 14.1 What Is Range Validation?

Range validation checks whether values fall within acceptable business limits.

Examples:

| Column | Expected Range |
|---|---|
| `age` | 18–70 |
| `city_tier` | 1–3 |
| `subscription_tenure_months` | 1–120 |
| `days_active_last_30` | 0–30 |
| `skip_rate` | 0–1 |
| `liked_songs_pct` | 0–1 |
| `ads_skipped_pct` | 0–1 |
| `repeat_track_rate` | 0–1 |
| `repeat_artist_rate` | 0–1 |
| `mean_track_popularity` | 0–100 |
| `pct_top_popularity_tracks` | 0–1 |

---

## 14.2 Reusable Range Rules

```python
behavior_rules = {
    "daily_listening_minutes": (0, None),
    "sessions_per_day": (0, None),
    "days_active_last_30": (0, 30),
    "avg_session_minutes": (0, None),
    "playlists_followed": (0, None),
    "artists_followed": (0, None),
    "skip_rate": (0, 1),
    "liked_songs_pct": (0, 1),
    "ads_skipped_pct": (0, 1),
    "repeat_track_rate": (0, 1),
    "repeat_artist_rate": (0, 1),
    "mean_danceability": (0, 1),
    "mean_energy": (0, 1),
    "mean_valence": (0, 1),
    "mean_acousticness": (0, 1),
    "mean_speechiness": (0, 1),
    "mean_instrumentalness": (0, 1),
    "mean_track_popularity": (0, 100),
    "pct_top_popularity_tracks": (0, 1),
    "genre_diversity_score": (0, 1)
}
```

Demographic rules:

```python
demo_rules = {
    "age": (18, 70),
    "city_tier": (1, 3),
    "subscription_tenure_months": (
        1,
        120
    )
}
```

---

## 14.3 Generic Range-Validation Function

```python
def validate_ranges(
    df: pd.DataFrame,
    rules: dict,
    table_name: str
) -> pd.DataFrame:
    issues = []

    for column, (minimum, maximum) in rules.items():
        if column not in df.columns:
            issues.append({
                "table": table_name,
                "column": column,
                "issue_type": "missing_column",
                "rows_affected": None
            })
            continue

        series = df[column]

        if minimum is not None:
            count = int(
                (series < minimum).sum()
            )

            if count > 0:
                issues.append({
                    "table": table_name,
                    "column": column,
                    "issue_type": (
                        f"value_below_{minimum}"
                    ),
                    "rows_affected": count
                })

        if maximum is not None:
            count = int(
                (series > maximum).sum()
            )

            if count > 0:
                issues.append({
                    "table": table_name,
                    "column": column,
                    "issue_type": (
                        f"value_above_{maximum}"
                    ),
                    "rows_affected": count
                })

    return pd.DataFrame(issues)
```

Usage:

```python
behavior_range_issues = validate_ranges(
    behavior_clean,
    behavior_rules,
    "spotify_user_behavior"
)

demo_range_issues = validate_ranges(
    demo_clean,
    demo_rules,
    "spotify_user_demo"
)
```

---

# 15. Outlier Detection

## 15.1 What Is an Outlier?

An outlier is a value far from most observations.

Spotify examples may include unusually high:

- Listening minutes
- Sessions per day
- Playlists followed
- Artists followed
- Session duration

These features can naturally have long right tails.

---

## 15.2 Do Not Automatically Delete Outliers

A very active listener may be a real user.

Outliers can represent:

- Power users
- High-value customers
- Bot activity
- Data errors
- Shared accounts
- Exceptional behavior

For segmentation, power users may form an important persona.

Therefore:

```text
Detect first
Investigate second
Decide third
```

---

## 15.3 IQR Method

The Interquartile Range method uses:

```text
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1
```

Possible outlier boundaries:

```text
Lower = Q1 - 1.5 × IQR
Upper = Q3 + 1.5 × IQR
```

---

## 15.4 IQR Function

```python
def iqr_outlier_report(
    df: pd.DataFrame,
    columns: list[str]
) -> pd.DataFrame:
    records = []

    for column in columns:
        series = df[column].dropna()

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        lower = q1 - (1.5 * iqr)
        upper = q3 + (1.5 * iqr)

        outlier_count = int(
            (
                (series < lower)
                | (series > upper)
            ).sum()
        )

        records.append({
            "column": column,
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "lower_bound": lower,
            "upper_bound": upper,
            "outlier_count": outlier_count,
            "outlier_pct": round(
                100 * outlier_count / len(series),
                2
            )
        })

    return pd.DataFrame(records)
```

Usage:

```python
outlier_columns = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
    "playlists_followed",
    "artists_followed"
]

outlier_report = iqr_outlier_report(
    behavior_clean,
    outlier_columns
)

display(outlier_report)
```

---

## 15.5 Outlier Treatment Options

| Treatment | When Appropriate |
|---|---|
| Keep unchanged | Valid business behavior |
| Investigate source | Possible data issue |
| Cap / winsorize | Extreme tail dominates analysis |
| Log transform | Strong right skew |
| Robust scaling | Keep values but reduce influence |
| Remove | Confirmed error or invalid record |
| Create flag | Outlier status has business value |

Outlier treatment is not the same as data cleaning.

Some treatments belong to feature engineering or preprocessing.

---

# 16. Data Formatting

## 16.1 Clean Column Names

```python
def clean_column_names(
    df: pd.DataFrame
) -> pd.DataFrame:
    cleaned = df.copy()

    cleaned.columns = (
        cleaned.columns
        .str.strip()
        .str.lower()
        .str.replace(
            r"[^a-z0-9]+",
            "_",
            regex=True
        )
        .str.strip("_")
    )

    return cleaned
```

---

## 16.2 Clean Text Columns

```python
text_columns = (
    demo_clean
    .select_dtypes(
        include=["object", "string"]
    )
    .columns
)

for column in text_columns:
    demo_clean[column] = (
        demo_clean[column]
        .astype("string")
        .str.strip()
    )
```

---

## 16.3 Avoid Unnecessary Rounding

Do not round raw features too early.

Example:

```text
skip_rate = 0.4567
```

If rounded to:

```text
0.46
```

some information is lost.

Round only:

- Reports
- Tables
- Printed summaries
- Business presentations

Keep full precision for modeling.

---

# 17. User ID Validation

## 17.1 Why `user_id` Is Critical

`user_id` is:

- The primary key
- The join key
- The record-tracking field
- The link between behavior and demographics

It is not a clustering feature.

---

## 17.2 Check Missing User IDs

```python
print(
    behavior_clean["user_id"]
    .isna()
    .sum()
)

print(
    demo_clean["user_id"]
    .isna()
    .sum()
)
```

Expected:

```text
0
0
```

---

## 17.3 Check Uniqueness

```python
assert (
    behavior_clean["user_id"]
    .is_unique
), "Behavior user_id is not unique"

assert (
    demo_clean["user_id"]
    .is_unique
), "Demo user_id is not unique"
```

---

## 17.4 Check ID Type

```python
print(
    behavior_clean["user_id"].dtype
)

print(
    demo_clean["user_id"].dtype
)
```

Both datasets should use compatible types.

Example:

```python
behavior_clean["user_id"] = (
    pd.to_numeric(
        behavior_clean["user_id"],
        errors="raise"
    )
    .astype("int64")
)

demo_clean["user_id"] = (
    pd.to_numeric(
        demo_clean["user_id"],
        errors="raise"
    )
    .astype("int64")
)
```

---

## 17.5 Do Not Use `user_id` in Clustering

```python
model_features = (
    behavior_clean
    .drop(columns=["user_id"])
)
```

Reason:

`user_id` identifies a user but does not measure behavior.

---

# 18. Dataset Relationship Validation

## 18.1 Check User Overlap

```python
behavior_users = set(
    behavior_clean["user_id"]
)

demo_users = set(
    demo_clean["user_id"]
)

behavior_only = (
    behavior_users - demo_users
)

demo_only = (
    demo_users - behavior_users
)

print(
    "Users only in behavior:",
    len(behavior_only)
)

print(
    "Users only in demo:",
    len(demo_only)
)
```

Expected:

```text
0
0
```

---

## 18.2 Safe One-to-One Merge

```python
spotify_users_clean = (
    behavior_clean
    .merge(
        demo_clean,
        how="inner",
        on="user_id",
        validate="one_to_one"
    )
)
```

Expected shape:

```text
108,000 rows × 31 columns
```

---

## 18.3 Why `validate="one_to_one"` Matters

Without validation, duplicate keys can silently multiply records.

Example:

```text
2 behavior records
×
2 demographic records
=
4 merged records
```

Validation prevents this silent error.

---

# 19. Complete Data-Quality Checks

## 19.1 Data Profile Function

```python
def create_data_profile(
    df: pd.DataFrame
) -> pd.DataFrame:
    return pd.DataFrame({
        "column_name": df.columns,
        "data_type": (
            df.dtypes
            .astype(str)
            .values
        ),
        "row_count": len(df),
        "non_null_count": (
            df.notna()
            .sum()
            .values
        ),
        "missing_count": (
            df.isna()
            .sum()
            .values
        ),
        "missing_pct": (
            df.isna()
            .mean()
            .mul(100)
            .round(2)
            .values
        ),
        "unique_count": (
            df.nunique(
                dropna=True
            )
            .values
        )
    })
```

---

## 19.2 Category Validation

```python
category_rules = {
    "country": {
        "US",
        "IN",
        "UK",
        "DE",
        "BR"
    },
    "city_tier": {
        1,
        2,
        3
    },
    "device_type": {
        "Mobile",
        "Desktop",
        "Tablet"
    }
}
```

```python
def validate_categories(
    df: pd.DataFrame,
    rules: dict,
    table_name: str
) -> pd.DataFrame:
    issues = []

    for column, allowed_values in rules.items():
        if column not in df.columns:
            continue

        invalid_mask = (
            df[column]
            .notna()
            & ~df[column]
            .isin(allowed_values)
        )

        invalid_count = int(
            invalid_mask.sum()
        )

        if invalid_count > 0:
            invalid_values = (
                df.loc[
                    invalid_mask,
                    column
                ]
                .drop_duplicates()
                .astype(str)
                .tolist()
            )

            issues.append({
                "table": table_name,
                "column": column,
                "issue_type": (
                    "invalid_category"
                ),
                "rows_affected": (
                    invalid_count
                ),
                "sample_values": (
                    invalid_values[:10]
                )
            })

    return pd.DataFrame(issues)
```

---

## 19.3 Quality Status

A simple status can be assigned:

```python
def quality_status(
    issue_count: int
) -> str:
    if issue_count == 0:
        return "PASS"

    return "REVIEW"
```

Use:

```python
status = quality_status(
    len(behavior_range_issues)
)
```

---

# 20. Data-Cleaning Decisions

## 20.1 Why Decisions Must Be Documented

A cleaning step changes the data.

Every change should answer:

```text
What problem was found?
How many rows were affected?
What action was taken?
Why was that action selected?
What was the result?
```

---

## 20.2 Decision Log Template

| Date | Dataset | Column | Issue | Rows | Decision | Reason | Result |
|---|---|---|---|---:|---|---|---|
| YYYY-MM-DD | behavior | skip_rate | Values > 1 | 12 | Investigate and set confirmed errors to null | Range rule | Pending |
| YYYY-MM-DD | demo | device_type | `" mobile "` | 25 | Trim and standardize | Same business category | Fixed |

---

## 20.3 Cleaning Decision Examples

### Missing Numerical Feature

```text
Decision:
Fill with median only when missingness is small and the feature is required.

Reason:
Median is less affected by skew and extreme values.
```

### Invalid Percentage

```text
Decision:
Do not automatically clip 75 to 1.

Reason:
75 may represent 75%, meaning the correct value could be 0.75.
Investigate the source first.
```

### Duplicate User ID

```text
Decision:
Do not keep the first row without investigation.

Reason:
Rows may contain conflicting behavior values.
```

### Valid Extreme Listener

```text
Decision:
Keep the row and use robust scaling later.

Reason:
The user may be a genuine Power Streamer persona.
```

---

# 21. Cleaning vs Transformation

These concepts are related but different.

| Cleaning | Transformation |
|---|---|
| Fixes errors | Changes representation |
| Removes exact duplicates | Applies log transform |
| Corrects data types | Applies StandardScaler |
| Standardizes categories | Applies PowerTransformer |
| Handles invalid values | Creates derived features |
| Required for trustworthy data | Required for modeling suitability |

Example:

```text
skip_rate = 1.4
```

is a cleaning issue because it is invalid.

```text
daily_listening_minutes is right-skewed
```

is not necessarily a cleaning issue. It may require transformation later.

---

# 22. Building a Reusable Cleaning Pipeline

## 22.1 Pipeline Goals

A good pipeline should:

- Avoid modifying raw data
- Apply checks in a consistent order
- Generate reports
- Stop on critical failures
- Document row-count changes
- Return clean copies

---

## 22.2 Simple Pipeline

```python
def clean_spotify_data(
    behavior_df: pd.DataFrame,
    demo_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    behavior = behavior_df.copy()
    demo = demo_df.copy()

    behavior = clean_column_names(
        behavior
    )

    demo = clean_column_names(
        demo
    )

    demo["country"] = (
        demo["country"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    demo["device_type"] = (
        demo["device_type"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    if behavior["user_id"].isna().any():
        raise ValueError(
            "Missing behavior user_id"
        )

    if demo["user_id"].isna().any():
        raise ValueError(
            "Missing demo user_id"
        )

    if not behavior["user_id"].is_unique:
        raise ValueError(
            "Duplicate behavior user_id"
        )

    if not demo["user_id"].is_unique:
        raise ValueError(
            "Duplicate demo user_id"
        )

    return behavior, demo
```

The complete reusable script is included in:

```text
examples/spotify_data_cleaning_pipeline.py
```

---

# 23. Before-and-After Validation

## 23.1 Record Row Counts

```python
audit = {
    "behavior_rows_before": len(
        behavior_raw
    ),
    "behavior_rows_after": len(
        behavior_clean
    ),
    "demo_rows_before": len(
        demo_raw
    ),
    "demo_rows_after": len(
        demo_clean
    )
}

print(audit)
```

---

## 23.2 Compare Data Types

```python
dtype_comparison = pd.DataFrame({
    "before": behavior_raw.dtypes,
    "after": behavior_clean.dtypes
})

display(dtype_comparison)
```

---

## 23.3 Verify No New Missing Values

```python
assert (
    behavior_clean
    .isna()
    .sum()
    .sum()
    == 0
)

assert (
    demo_clean
    .isna()
    .sum()
    .sum()
    == 0
)
```

Only use this assertion when the project rule requires zero missing values.

---

## 23.4 Verify Final Relationship

```python
final_users = (
    behavior_clean
    .merge(
        demo_clean,
        on="user_id",
        how="inner",
        validate="one_to_one"
    )
)

assert len(final_users) == 108000
```

---

# 24. Data-Quality Report

A professional data-quality report should include:

- Dataset name
- Shape
- Required-column status
- Data types
- Missing count
- Missing percentage
- Duplicate-row count
- Duplicate-key count
- Invalid-range count
- Invalid-category count
- Outlier count
- Cleaning action
- Final status

Example:

| Check | Behavior | Demo | Status |
|---|---:|---:|---|
| Rows | 108,000 | 108,000 | PASS |
| Duplicate user IDs | 0 | 0 | PASS |
| Missing values | 0 | 0 | PASS |
| Unmatched users | 0 | 0 | PASS |
| Relationship | One-to-one | One-to-one | PASS |

---

# 25. Spotify Project Cleaning Conclusion

For the current Spotify project data:

- Both datasets loaded with the expected shapes
- Every row represents one user
- `user_id` is unique in both datasets
- No duplicate user IDs were found
- All users match between datasets
- The current quality report shows a 100% fill rate
- Rate fields are validated against expected business ranges
- `user_id` must be retained for traceability and joining
- `user_id` must be excluded from statistical analysis and clustering
- Valid extreme behavior should not be removed automatically
- Distribution and skewness analysis should follow after quality validation

Because the current datasets are already clean, the main project action is:

```text
Validate
Document
Preserve
Proceed
```

not:

```text
Change data without evidence
```

---

# 26. Important Terminology

| Term | Meaning |
|---|---|
| Data cleaning | Fixing or handling data-quality problems |
| Preprocessing | Preparing data for analysis or modeling |
| Missing value | Unavailable information |
| Fill rate | Percentage of non-missing values |
| Imputation | Replacing missing values |
| Duplicate row | Repeated full record |
| Duplicate key | Repeated primary identifier |
| Data type | Technical type of a column |
| Invalid value | Value breaking a logical rule |
| Inconsistent value | Same meaning in different formats |
| Range validation | Checking allowed minimum and maximum |
| Outlier | Unusually distant observation |
| IQR | Interquartile Range |
| Formatting | Standardizing names and text |
| Primary key | Unique, non-null identifier |
| Business rule | Domain-specific validation rule |
| Data-quality report | Summary of validation findings |
| Decision log | Record of cleaning actions |
| Quarantine | Isolating suspicious records |
| Winsorization | Capping extreme values |
| Reproducibility | Ability to repeat the same process |
| Audit trail | Evidence of what changed |
| Schema validation | Confirming expected columns and types |
| Cardinality | Relationship type between tables |

---

# 27. Interview Questions and Answers

## 1. What is data cleaning?

Data cleaning is the process of identifying and handling missing, duplicated, invalid, inconsistent, or incorrectly formatted data.

---

## 2. Why is data cleaning important?

Poor-quality inputs produce unreliable analysis and Machine Learning results.

---

## 3. What is the difference between cleaning and preprocessing?

Cleaning fixes data-quality problems. Preprocessing prepares valid data for modeling through scaling, encoding, and transformation.

---

## 4. How do you check missing values in Pandas?

```python
df.isna().sum()
```

---

## 5. What is fill rate?

The percentage of values that are present in a column.

```text
Fill Rate = 100% - Missing Percentage
```

---

## 6. How do you check exact duplicates?

```python
df.duplicated().sum()
```

---

## 7. How do you check duplicate user IDs?

```python
df["user_id"].duplicated().sum()
```

---

## 8. Why are duplicate user IDs dangerous?

They break the one-row-per-user grain and may multiply rows during joining.

---

## 9. What is a wrong data type?

A technical type that does not match the business meaning, such as age stored as text.

---

## 10. Why use `pd.to_numeric(errors="coerce")`?

It converts numeric-looking values and changes invalid text to missing values for investigation.

---

## 11. What is an invalid value?

A value that violates a business or logical rule.

---

## 12. What is the difference between an invalid value and an outlier?

An invalid value is impossible. An outlier is unusual but may be real.

---

## 13. What is range validation?

Checking whether numerical values fall between approved minimum and maximum limits.

---

## 14. Why must `skip_rate` be between 0 and 1?

It is stored as a proportion.

---

## 15. How do you standardize category text?

Use string methods such as:

```python
.str.strip().str.title()
```

---

## 16. What is the IQR method?

A method that flags values outside:

```text
Q1 - 1.5 × IQR
Q3 + 1.5 × IQR
```

---

## 17. Should all outliers be removed?

No. They may represent real and valuable user behavior.

---

## 18. Why create a raw copy?

To preserve the original data and support before-and-after validation.

---

## 19. How do you validate a primary key?

Check that it is non-null and unique.

---

## 20. Why is `user_id` excluded from clustering?

It identifies a user but does not measure behavior.

---

## 21. How do you confirm a one-to-one join?

Use:

```python
merge(
    ...,
    validate="one_to_one"
)
```

---

## 22. What were the missing-value results in this project?

The current Spotify datasets have a 100% fill rate across columns.

---

## 23. What were the duplicate-key results?

Both datasets have zero duplicate `user_id` values.

---

## 24. What is a cleaning decision log?

A record of the issue, affected rows, selected action, reason, and result.

---

## 25. Why should cleaning decisions be documented?

Because cleaning changes the data and must remain explainable and reproducible.

---

# 28. Module Summary

In this module, we learned:

- Data cleaning protects all downstream analysis
- Raw data should be preserved
- Shape and required columns should be validated first
- Missing values require business-based decisions
- Exact duplicates and duplicate keys are different
- Wrong data types can create incorrect calculations
- Invalid values violate business rules
- Inconsistent categories require standardization
- Range rules make quality checks repeatable
- Outliers must be investigated before treatment
- `user_id` must be unique and non-null
- Dataset relationships must be validated
- Cleaning decisions should be documented
- Cleaning is different from transformation
- Reusable pipelines improve consistency
- Before-and-after validation confirms that cleaning did not damage the data

---

# 29. Quick Reference Cheat Sheet

| Task | Pandas Command |
|---|---|
| Shape | `df.shape` |
| Data types | `df.dtypes` |
| Summary | `df.info()` |
| Missing count | `df.isna().sum()` |
| Missing percentage | `df.isna().mean() * 100` |
| Exact duplicates | `df.duplicated().sum()` |
| Duplicate ID | `df["user_id"].duplicated().sum()` |
| Unique ID check | `df["user_id"].is_unique` |
| Convert numeric | `pd.to_numeric(..., errors="coerce")` |
| Trim text | `.str.strip()` |
| Standardize case | `.str.upper()` / `.str.title()` |
| Allowed categories | `.isin(allowed_values)` |
| Range check | `.between(minimum, maximum)` |
| Remove exact duplicate | `.drop_duplicates()` |
| Safe copy | `.copy()` |
| Safe merge | `merge(..., validate="one_to_one")` |

---

# 30. What Comes Next?

## Module 05 — Exploratory Data Analysis

The next module will cover:

- Univariate analysis
- Bivariate analysis
- Distribution analysis
- Histograms
- Boxplots
- Skewness
- Correlation
- Category counts
- Business interpretation
- Spotify user behavior patterns

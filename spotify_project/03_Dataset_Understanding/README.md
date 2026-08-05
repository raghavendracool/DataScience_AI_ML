# Module 03 — Dataset Understanding

> A beginner-friendly module for understanding the Spotify project datasets, their structure, column types, relationships, business meaning, and role in the Machine Learning workflow.

---

## Table of Contents

1. [Module Overview](#1-module-overview)
2. [Learning Objectives](#2-learning-objectives)
3. [Why Dataset Understanding Comes Before Data Cleaning](#3-why-dataset-understanding-comes-before-data-cleaning)
4. [Spotify Project Datasets](#4-spotify-project-datasets)
5. [Spotify Behavioral Dataset](#5-spotify-behavioral-dataset)
6. [Spotify Demographic Dataset](#6-spotify-demographic-dataset)
7. [Spotify Data Dictionary](#7-spotify-data-dictionary)
8. [Rows and Columns](#8-rows-and-columns)
9. [Data Types](#9-data-types)
10. [Numerical Data](#10-numerical-data)
11. [Categorical Data](#11-categorical-data)
12. [Continuous and Discrete Data](#12-continuous-and-discrete-data)
13. [Identifiers](#13-identifiers)
14. [Features](#14-features)
15. [Dataset Relationships](#15-dataset-relationships)
16. [Business Meaning of the Columns](#16-business-meaning-of-the-columns)
17. [How to Inspect the Datasets Using Pandas](#17-how-to-inspect-the-datasets-using-pandas)
18. [How to Join the Spotify Datasets](#18-how-to-join-the-spotify-datasets)
19. [Dataset Understanding Checklist](#19-dataset-understanding-checklist)
20. [Important Terminology](#20-important-terminology)
21. [Interview Questions and Answers](#21-interview-questions-and-answers)
22. [Module Summary](#22-module-summary)
23. [Quick Reference Cheat Sheet](#23-quick-reference-cheat-sheet)
24. [What Comes Next?](#24-what-comes-next)

---

# 1. Module Overview

Before cleaning data, creating charts, selecting features, or training a Machine Learning model, we must first understand the datasets.

Dataset understanding answers questions such as:

- What files or tables are available?
- What does each table represent?
- What does one row represent?
- How many rows and columns are present?
- Which column uniquely identifies a user?
- Which columns are numerical?
- Which columns are categorical?
- Which columns describe user behavior?
- Which columns describe user demographics?
- How are the datasets connected?
- Which columns may become Machine Learning features?
- What is the business meaning of every column?

In this Spotify project, the main data is divided into two user-level datasets:

```text
spotify_user_demo
        +
spotify_user_behavior
        ↓
Joined using user_id
        ↓
Complete user-level analysis dataset
```

Both tables contain one row per user and can be joined using `user_id`.

---

# 2. Learning Objectives

By the end of this module, students should be able to:

- Explain the purpose of each Spotify dataset
- Explain the difference between behavioral and demographic data
- Explain the purpose of a data dictionary
- Define rows, columns, observations, and variables
- Identify common data types
- Differentiate numerical and categorical data
- Differentiate continuous and discrete data
- Explain what an identifier is
- Explain what a feature is
- Explain the relationship between the Spotify datasets
- Join the datasets correctly using `user_id`
- Describe the business meaning of important Spotify columns
- Inspect the datasets using Pandas
- Validate whether the datasets are structurally ready for analysis

---

# 3. Why Dataset Understanding Comes Before Data Cleaning

A common beginner mistake is to start changing the data immediately after loading it.

Before changing anything, we must understand:

```text
What the data represents
        ↓
What each row represents
        ↓
What each column means
        ↓
What values are expected
        ↓
How the tables are related
```

Without this understanding, we may:

- Remove valid records by mistake
- Treat an identifier as a behavior feature
- Convert the wrong column to numeric
- Join tables using the wrong key
- Misunderstand percentages and rates
- Create incorrect business conclusions
- Train a model using meaningless columns

## Easy Example

Suppose a column contains:

```text
0.72
```

Without a data dictionary, we may not know whether it means:

- 72% skip rate
- A model probability
- A normalized popularity score
- A danceability score

The number only becomes useful when its business meaning is understood.

---

# 4. Spotify Project Datasets

The project uses the following core datasets:

| Dataset | Purpose | Grain |
|---|---|---|
| `spotify_user_behavior` | Describes how each user listens and interacts with Spotify | One row per user |
| `spotify_user_demo` | Describes who the user is | One row per user |
| `Spotify_Data_Dictionary_v0` | Explains column names, data types, descriptions, and typical values | One row per documented column |
| `Spotify_Cluster_PrimaryEvaluation` | Stores the results of clustering experiments | One row per experiment |

The two primary user datasets are:

```text
spotify_user_behavior : 108,000 rows × 26 columns
spotify_user_demo     : 108,000 rows × 6 columns
```

They are designed to join one-to-one using:

```text
user_id
```

---

# 5. Spotify Behavioral Dataset

## 5.1 What Is a Behavioral Dataset?

A behavioral dataset describes what a user does.

It captures actions, usage patterns, preferences, and engagement.

In this project:

```text
spotify_user_behavior
```

describes how each user interacts with Spotify.

It answers questions such as:

- How long does the user listen?
- How frequently does the user open Spotify?
- How many days was the user active?
- How often does the user skip songs?
- How often does the user repeat tracks or artists?
- Does the user prefer popular tracks?
- How diverse is the user's music taste?
- What type of audio characteristics does the user prefer?

---

## 5.2 Dataset Size

```text
Rows    : 108,000
Columns : 26
Grain   : One row per user
Key     : user_id
```

### What Does Grain Mean?

**Grain** means what one row represents.

For this table:

```text
One row = One Spotify user
```

This is important because the same `user_id` should not appear more than once.

---

## 5.3 Behavioral Dataset Columns

### User Identifier

| Column | Meaning |
|---|---|
| `user_id` | Unique identifier for each user |

### Listening and Engagement Features

| Column | Meaning | Typical Interpretation |
|---|---|---|
| `daily_listening_minutes` | Average minutes listened per day | Listening intensity |
| `sessions_per_day` | Average sessions per day | Usage frequency |
| `days_active_last_30` | Active days in the last 30 days | Usage consistency |
| `avg_session_minutes` | Average length of one session | Session depth |
| `playlists_followed` | Number of followed playlists | Playlist engagement |
| `artists_followed` | Number of followed artists | Artist engagement |
| `skip_rate` | Proportion of tracks skipped | Content friction |
| `liked_songs_pct` | Proportion of tracks liked | Positive content response |
| `ads_skipped_pct` | Proportion of ads skipped | Advertisement tolerance |
| `repeat_track_rate` | Proportion of repeated track listens | Track loyalty |
| `repeat_artist_rate` | Proportion of repeated artist listens | Artist loyalty |
| `median_gap_minutes_between_plays` | Median time gap between plays | Return frequency |

### Audio Preference Features

| Column | Meaning |
|---|---|
| `mean_danceability` | Average danceability of tracks listened to |
| `mean_energy` | Average energy level of tracks |
| `mean_valence` | Average positivity or mood score |
| `mean_acousticness` | Average acoustic content |
| `mean_speechiness` | Average speech-like content |
| `mean_instrumentalness` | Average instrumental content |
| `mean_tempo` | Average tempo in beats per minute |

### Audio Variability and Popularity Features

| Column | Meaning |
|---|---|
| `std_energy` | Variation in energy across tracks |
| `std_valence` | Variation in mood across tracks |
| `std_tempo` | Variation in tempo across tracks |
| `genre_diversity_score` | Diversity of genres consumed |
| `mean_track_popularity` | Average popularity of tracks listened to |
| `pct_top_popularity_tracks` | Share of listening going to highly popular tracks |

---

## 5.4 Why This Dataset Is Important

This dataset is the main source for:

- Behavioral analysis
- User engagement analysis
- Listening-pattern analysis
- Feature selection
- Scaling and transformation
- K-Means clustering
- Gaussian Mixture Models
- Cluster profiling
- User segmentation
- Persona creation

The behavioral dataset tells us:

```text
What the user does
```

---

# 6. Spotify Demographic Dataset

## 6.1 What Is a Demographic Dataset?

A demographic dataset describes who the user is.

It contains background or profile information.

In this project:

```text
spotify_user_demo
```

contains user-level demographic and account information.

---

## 6.2 Dataset Size

```text
Rows    : 108,000
Columns : 6
Grain   : One row per user
Key     : user_id
```

---

## 6.3 Demographic Dataset Columns

| Column | Description | Typical Values |
|---|---|---|
| `user_id` | Unique identifier for each user | Unique integer |
| `age` | Age of the user in years | 18–70 |
| `country` | User's country of residence | US, IN, UK, DE, BR |
| `city_tier` | Urban classification of the user's city | 1, 2, 3 |
| `device_type` | Primary device used to access Spotify | Mobile, Desktop, Tablet |
| `subscription_tenure_months` | Months since the subscription or account relationship started | 1–120 |

---

## 6.4 Why This Dataset Is Important

The demographic dataset helps answer questions such as:

- Do younger and older users behave differently?
- Does listening behavior differ by country?
- Do mobile users have different session patterns?
- Does city tier influence engagement?
- Do long-tenure users behave differently from new users?

The demographic dataset tells us:

```text
Who the user is
```

---

## 6.5 Behavior vs Demographics

| Behavioral Data | Demographic Data |
|---|---|
| Describes actions | Describes user profile |
| Listening minutes | Age |
| Skip rate | Country |
| Sessions per day | City tier |
| Days active | Device type |
| Artist follows | Subscription tenure |
| Used heavily for clustering | Used heavily for profiling and interpretation |

### Easy Way to Remember

```text
Behavioral dataset = What the user does

Demographic dataset = Who the user is
```

---

# 7. Spotify Data Dictionary

## 7.1 What Is a Data Dictionary?

A data dictionary is a reference document that explains the structure and meaning of a dataset.

It usually contains:

- Column name
- Data type
- Description
- Typical values
- Valid range
- Business meaning

In this project, the data dictionary contains fields such as:

| Data Dictionary Field | Purpose |
|---|---|
| `Column Name` | Exact name used in the dataset |
| `Data Type` | Expected type of data |
| `Description` | Meaning of the column |
| `Typical Values` | Example values or expected range |

---

## 7.2 Why a Data Dictionary Is Important

A data dictionary helps:

- Students understand the dataset
- Analysts avoid incorrect assumptions
- Developers use correct field names
- Data-quality rules define valid ranges
- Business teams understand technical columns
- Teams communicate using the same definitions

---

## 7.3 Example

| Column Name | Data Type | Description | Typical Values |
|---|---|---|---|
| `skip_rate` | Float | Proportion of tracks skipped | 0–1 |
| `days_active_last_30` | Integer | Active days in last 30 days | 0–30 |
| `device_type` | Category | Primary Spotify device | Mobile, Desktop, Tablet |

Without a data dictionary, `skip_rate = 0.75` may be misunderstood.

With the dictionary:

```text
skip_rate = 0.75
```

means:

```text
The user skips approximately 75% of played tracks.
```

---

# 8. Rows and Columns

## 8.1 What Is a Row?

A row represents one observation.

In the Spotify user datasets:

```text
One row = One user
```

Example:

| user_id | age | country | device_type |
|---:|---:|---|---|
| 1001 | 24 | IN | Mobile |

This row describes one user.

---

## 8.2 What Is a Column?

A column represents one variable or attribute.

Examples:

```text
age
country
skip_rate
daily_listening_minutes
```

---

## 8.3 Row vs Column

| Row | Column |
|---|---|
| One observation | One variable |
| One Spotify user | One characteristic |
| Horizontal | Vertical |
| Example: User 1001 | Example: `skip_rate` |

---

## 8.4 Shape of a Dataset

In Pandas:

```python
df.shape
```

returns:

```text
(number_of_rows, number_of_columns)
```

Example:

```python
spotify_user_behavior.shape
```

Expected output:

```text
(108000, 26)
```

---

# 9. Data Types

## 9.1 What Is a Data Type?

A data type describes the kind of value stored in a column.

Common Pandas data types include:

| Pandas Type | Meaning |
|---|---|
| `int64` | Whole number |
| `float64` | Decimal number |
| `object` | Usually text or mixed data |
| `bool` | True or False |
| `datetime64` | Date and time |
| `category` | Repeated categories |

---

## 9.2 Why Data Types Matter

Data types determine which operations are allowed.

Example:

```python
20 + 10
```

works because both values are numeric.

But:

```python
"20" + "10"
```

produces:

```text
"2010"
```

because the values are text.

Wrong data types can cause:

- Incorrect calculations
- Failed comparisons
- Failed charts
- Failed model training
- Incorrect grouping

---

## 9.3 Checking Data Types

```python
spotify_user_behavior.dtypes
spotify_user_demo.dtypes
```

For a full summary:

```python
spotify_user_behavior.info()
spotify_user_demo.info()
```

---

# 10. Numerical Data

## 10.1 What Is Numerical Data?

Numerical data contains numbers that can be used in mathematical calculations.

Examples:

- Age
- Listening minutes
- Sessions per day
- Skip rate
- Tempo

---

## 10.2 Spotify Numerical Examples

```text
age
daily_listening_minutes
sessions_per_day
days_active_last_30
avg_session_minutes
skip_rate
mean_energy
mean_tempo
subscription_tenure_months
```

---

## 10.3 Operations on Numerical Data

We can calculate:

- Mean
- Median
- Minimum
- Maximum
- Standard deviation
- Correlation
- Percentiles

Example:

```python
spotify_user_behavior["daily_listening_minutes"].mean()
```

---

## 10.4 Percentage and Rate Columns

Some numerical columns represent proportions:

```text
skip_rate
liked_songs_pct
ads_skipped_pct
repeat_track_rate
repeat_artist_rate
pct_top_popularity_tracks
```

Typical range:

```text
0 to 1
```

Interpretation:

```text
0.25 = 25%
0.75 = 75%
```

---

# 11. Categorical Data

## 11.1 What Is Categorical Data?

Categorical data represents groups, names, labels, or classes.

Examples:

- Country
- Device type
- City tier

---

## 11.2 Spotify Categorical Examples

```text
country
city_tier
device_type
```

Even though `city_tier` may be stored as a number, it represents a category:

```text
Tier 1
Tier 2
Tier 3
```

It should not automatically be treated as a continuous measurement.

---

## 11.3 Inspecting Categories

```python
spotify_user_demo["country"].value_counts()
spotify_user_demo["device_type"].value_counts()
spotify_user_demo["city_tier"].value_counts()
```

Unique categories:

```python
spotify_user_demo["device_type"].unique()
```

---

## 11.4 Numerical Code vs Numerical Meaning

A column may contain numbers but still be categorical.

Example:

```text
city_tier = 1, 2, 3
```

The numbers identify categories.

They do not necessarily mean that Tier 3 is exactly three times Tier 1.

This distinction is important in analysis and modeling.

---

# 12. Continuous and Discrete Data

## 12.1 Continuous Data

Continuous data can take many decimal values within a range.

Examples:

```text
daily_listening_minutes = 87.45
skip_rate = 0.63
mean_energy = 0.71
mean_tempo = 124.58
```

Continuous values are measured.

---

## 12.2 Discrete Data

Discrete data usually represents countable whole values.

Examples:

```text
sessions_per_day = 5
days_active_last_30 = 24
playlists_followed = 18
artists_followed = 42
subscription_tenure_months = 16
```

Discrete values are counted.

---

## 12.3 Continuous vs Discrete

| Continuous | Discrete |
|---|---|
| Measured | Counted |
| Can contain decimals | Usually whole numbers |
| Listening minutes | Number of playlists |
| Skip rate | Days active |
| Mean tempo | Sessions per day |

---

## 12.4 Why This Difference Matters

The distinction affects:

- Chart selection
- Statistical analysis
- Outlier checks
- Data validation
- Feature transformation
- Model preparation

---

# 13. Identifiers

## 13.1 What Is an Identifier?

An identifier uniquely identifies a record.

In this project:

```text
user_id
```

is the unique identifier.

---

## 13.2 Primary Key

A primary key must be:

- Unique
- Non-null
- Stable
- Present in every row

Expected validation:

```text
Unique user_id in behavior : 108,000
Unique user_id in demo     : 108,000
Duplicate user_id          : 0
```

---

## 13.3 Why `user_id` Is Not a Behavioral Feature

`user_id` identifies the user, but it does not describe behavior.

Example:

```text
User 10001 is not behaviorally greater than User 10000.
```

Using `user_id` in clustering may create meaningless distance patterns.

Therefore:

```text
Use user_id for joining and tracking.

Do not use user_id as a clustering feature.
```

---

# 14. Features

## 14.1 What Is a Feature?

A feature is a column used as input to an analysis or Machine Learning model.

Possible Spotify clustering features:

- `daily_listening_minutes`
- `sessions_per_day`
- `days_active_last_30`
- `avg_session_minutes`
- `skip_rate`
- `ads_skipped_pct`
- `genre_diversity_score`

---

## 14.2 Column vs Feature

Every feature is a column.

But not every column should become a feature.

| Column | Use as Feature? | Reason |
|---|---|---|
| `user_id` | No | Identifier only |
| `daily_listening_minutes` | Yes | Describes engagement |
| `skip_rate` | Yes | Describes friction |
| `country` | Maybe | Useful for profiling; encoding needed for modeling |
| `device_type` | Maybe | Useful for profiling or encoded modeling |

---

## 14.3 Feature Groups in This Project

### Engagement Features

- Daily listening minutes
- Sessions per day
- Days active
- Average session duration

### Loyalty Features

- Repeat track rate
- Repeat artist rate
- Playlist follows
- Artist follows

### Friction Features

- Skip rate
- Ads skipped percentage
- Gap between plays

### Taste Features

- Danceability
- Energy
- Valence
- Acousticness
- Speechiness
- Instrumentalness
- Tempo

### Variety Features

- Genre diversity
- Standard deviation of energy
- Standard deviation of valence
- Standard deviation of tempo

### Popularity Features

- Mean track popularity
- Percentage of top-popularity tracks

---

# 15. Dataset Relationships

## 15.1 Relationship Between the Two User Tables

The two datasets are connected using:

```text
user_id
```

Relationship:

```text
spotify_user_demo.user_id
          1
          │
          │ one-to-one
          │
          1
spotify_user_behavior.user_id
```

---

## 15.2 Why It Is a One-to-One Relationship

Each user appears:

- Once in the demographic table
- Once in the behavioral table

The project validation confirms:

```text
Duplicate user_id in behavior = 0
Duplicate user_id in demo     = 0
Users missing from either side = 0
```

---

## 15.3 Expected Joined Dataset

Before joining:

```text
Behavior : 26 columns
Demo     : 6 columns
```

Because `user_id` exists in both tables, the expected joined structure is:

```text
26 + 6 - 1 shared key = 31 columns
```

Expected rows:

```text
108,000
```

---

## 15.4 Why the Join Is Important

The joined dataset combines:

```text
Who the user is
        +
What the user does
```

Example:

| user_id | age | country | device_type | listening_minutes | skip_rate |
|---:|---:|---|---|---:|---:|
| 1001 | 24 | IN | Mobile | 145.5 | 0.21 |

This makes it possible to:

- Analyze behavior by age
- Compare countries
- Profile clusters by device
- Understand long-tenure users
- Build richer personas

---

## 15.5 The Data Dictionary Relationship

The data dictionary is not joined to users like the two analytical tables.

It is metadata.

```text
User datasets = Actual records

Data dictionary = Explanation of the records
```

---

# 16. Business Meaning of the Columns

Understanding business meaning is more important than only knowing the data type.

## 16.1 Engagement and Usage

| Column | Business Meaning |
|---|---|
| `daily_listening_minutes` | Overall content-consumption intensity |
| `sessions_per_day` | How frequently the user returns |
| `days_active_last_30` | Habit and consistency |
| `avg_session_minutes` | Depth of each visit |
| `median_gap_minutes_between_plays` | How quickly the user returns to listening |

---

## 16.2 Content Satisfaction and Friction

| Column | Business Meaning |
|---|---|
| `skip_rate` | Possible dissatisfaction or exploration behavior |
| `liked_songs_pct` | Positive response to recommended content |
| `repeat_track_rate` | Loyalty toward specific tracks |
| `repeat_artist_rate` | Loyalty toward specific artists |
| `ads_skipped_pct` | Advertisement tolerance and Premium potential |

A high skip rate does not always mean dissatisfaction.

It may also indicate:

- Active exploration
- Strict music preference
- Poor recommendation relevance

Business interpretation requires multiple features together.

---

## 16.3 Music Taste

| Column | Business Meaning |
|---|---|
| `mean_danceability` | Preference for dance-oriented music |
| `mean_energy` | Preference for energetic tracks |
| `mean_valence` | Preference for positive or low-valence moods |
| `mean_acousticness` | Preference for acoustic content |
| `mean_speechiness` | Preference for speech-heavy audio |
| `mean_instrumentalness` | Preference for instrumental tracks |
| `mean_tempo` | Preferred listening tempo |

---

## 16.4 Taste Variety

| Column | Business Meaning |
|---|---|
| `std_energy` | How much energy preference changes |
| `std_valence` | How much mood preference changes |
| `std_tempo` | How much tempo preference changes |
| `genre_diversity_score` | Breadth of musical exploration |

---

## 16.5 Popularity Preference

| Column | Business Meaning |
|---|---|
| `mean_track_popularity` | Preference for mainstream vs niche tracks |
| `pct_top_popularity_tracks` | Dependence on highly popular music |

---

## 16.6 Demographic and Account Meaning

| Column | Business Meaning |
|---|---|
| `age` | Age-based listening and marketing differences |
| `country` | Regional content and campaign strategy |
| `city_tier` | Urban-market classification |
| `device_type` | Product and device experience |
| `subscription_tenure_months` | Length of user relationship and possible loyalty |

---

# 17. How to Inspect the Datasets Using Pandas

## 17.1 Load the Excel Files

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

## 17.2 Preview the Data

```python
display(spotify_user_behavior.head())
display(spotify_user_demo.head())
```

What this tells us:

- Column names
- Example values
- Basic structure
- Possible formatting issues

---

## 17.3 Check Shape

```python
print("Behavior shape:", spotify_user_behavior.shape)
print("Demo shape:", spotify_user_demo.shape)
```

Expected:

```text
Behavior shape: (108000, 26)
Demo shape: (108000, 6)
```

---

## 17.4 Check Column Names

```python
print(spotify_user_behavior.columns.tolist())
print(spotify_user_demo.columns.tolist())
```

This helps avoid:

```text
KeyError
```

caused by incorrect column names.

---

## 17.5 Check Data Types

```python
print(spotify_user_behavior.dtypes)
print(spotify_user_demo.dtypes)
```

---

## 17.6 Check General Information

```python
spotify_user_behavior.info()
spotify_user_demo.info()
```

`info()` shows:

- Column names
- Non-null counts
- Data types
- Memory usage

---

## 17.7 Check Numeric Summary

```python
display(
    spotify_user_behavior
    .drop(columns=["user_id"])
    .describe()
    .T
    .round(3)
)
```

For demographic numeric columns:

```python
display(
    spotify_user_demo
    .select_dtypes(include="number")
    .describe()
    .T
    .round(3)
)
```

---

## 17.8 Check Unique Values

```python
print(
    spotify_user_demo["country"].value_counts()
)

print(
    spotify_user_demo["device_type"].value_counts()
)

print(
    spotify_user_demo["city_tier"].value_counts()
)
```

---

## 17.9 Check Missing Values

```python
print(
    spotify_user_behavior.isna().sum()
)

print(
    spotify_user_demo.isna().sum()
)
```

---

## 17.10 Check Duplicate User IDs

```python
print(
    spotify_user_behavior["user_id"]
    .duplicated()
    .sum()
)

print(
    spotify_user_demo["user_id"]
    .duplicated()
    .sum()
)
```

Expected:

```text
0
0
```

---

# 18. How to Join the Spotify Datasets

## 18.1 Basic Merge

```python
spotify_users = spotify_user_behavior.merge(
    spotify_user_demo,
    how="inner",
    on="user_id"
)
```

---

## 18.2 Safer One-to-One Merge

```python
spotify_users = spotify_user_behavior.merge(
    spotify_user_demo,
    how="inner",
    on="user_id",
    validate="one_to_one"
)
```

### Why Use `validate="one_to_one"`?

It asks Pandas to confirm:

```text
One user in behavior
matches
One user in demo
```

If duplicate user IDs exist, Pandas raises an error instead of silently creating duplicate joined rows.

---

## 18.3 Validate the Joined Result

```python
print("Joined shape:", spotify_users.shape)
print(
    "Unique users:",
    spotify_users["user_id"].nunique()
)
```

Expected:

```text
Joined shape: (108000, 31)
Unique users: 108000
```

---

## 18.4 Check Unmatched Users

```python
behavior_users = set(
    spotify_user_behavior["user_id"]
)

demo_users = set(
    spotify_user_demo["user_id"]
)

print(
    "Behavior users missing in demo:",
    len(behavior_users - demo_users)
)

print(
    "Demo users missing in behavior:",
    len(demo_users - behavior_users)
)
```

Expected:

```text
0
0
```

---

# 19. Dataset Understanding Checklist

Before moving to data cleaning, confirm:

- [ ] Both datasets loaded successfully
- [ ] Behavior shape is `(108000, 26)`
- [ ] Demo shape is `(108000, 6)`
- [ ] `user_id` exists in both datasets
- [ ] `user_id` is unique in both datasets
- [ ] There are no unmatched users
- [ ] Behavioral and demographic columns are understood
- [ ] Numerical and categorical columns are identified
- [ ] Rate columns are recognized as proportions
- [ ] `user_id` is excluded from clustering features
- [ ] Data dictionary definitions are reviewed
- [ ] Joined dataset has the expected row count
- [ ] Business meaning is understood before modeling

---

# 20. Important Terminology

| Term | Meaning |
|---|---|
| Dataset | Collection of related records |
| DataFrame | Pandas table structure |
| Row | One observation |
| Column | One variable |
| Observation | One record, such as one user |
| Variable | A measurable property |
| Grain | Meaning of one row |
| Schema | Structure of a table |
| Data type | Kind of data stored |
| Numerical data | Data used in calculations |
| Categorical data | Data representing groups |
| Continuous data | Measured values that may contain decimals |
| Discrete data | Countable values |
| Identifier | Column used to identify a record |
| Primary key | Unique and non-null identifier |
| Feature | Input used for analysis or modeling |
| Metadata | Data that explains other data |
| Data dictionary | Documentation of columns |
| Relationship | Connection between datasets |
| One-to-one | One record matches one record |
| Join | Combining datasets using a key |
| Cardinality | Nature of a relationship |
| Behavioral data | Data describing user actions |
| Demographic data | Data describing user profile |

---

# 21. Interview Questions and Answers

## 1. What datasets are used in this Spotify project?

The project uses a behavioral dataset, a demographic dataset, a data dictionary, and an experiment-evaluation dataset.

---

## 2. What is the shape of the behavioral dataset?

It contains 108,000 rows and 26 columns.

---

## 3. What is the shape of the demographic dataset?

It contains 108,000 rows and 6 columns.

---

## 4. What does one row represent?

One row represents one Spotify user.

---

## 5. What is the primary key?

`user_id` is the primary key.

---

## 6. How are the two user datasets related?

They have a one-to-one relationship using `user_id`.

---

## 7. What is behavioral data?

Behavioral data describes what users do, such as listening time, sessions, skips, likes, and repeat behavior.

---

## 8. What is demographic data?

Demographic data describes who users are, such as age, country, city tier, and device type.

---

## 9. What is a data dictionary?

A data dictionary documents column names, data types, descriptions, and typical values.

---

## 10. What is the difference between a row and a column?

A row is one observation. A column is one variable.

---

## 11. What is numerical data?

Numerical data contains numbers used for calculations.

---

## 12. What is categorical data?

Categorical data represents groups or labels.

---

## 13. Is `city_tier` numerical or categorical?

It may be stored as a number, but conceptually it represents an ordered category.

---

## 14. What is continuous data?

Continuous data can take decimal values within a range.

---

## 15. What is discrete data?

Discrete data contains countable values, usually whole numbers.

---

## 16. Why should `user_id` not be used as a clustering feature?

It identifies users but does not describe their behavior.

---

## 17. What is a feature?

A feature is a column used as an input for analysis or Machine Learning.

---

## 18. What is dataset grain?

Grain defines what one row represents.

---

## 19. What is a one-to-one relationship?

One record in the first table matches exactly one record in the second table.

---

## 20. Why use `validate="one_to_one"` during a merge?

It ensures that duplicate keys do not silently create duplicate joined rows.

---

## 21. What is the expected shape after joining?

The expected joined dataset contains 108,000 rows and 31 columns.

---

## 22. Why is business meaning important?

A column cannot be interpreted correctly using its name or number alone. Business meaning tells us what the value represents and how it should be used.

---

# 22. Module Summary

In this module, we learned:

- The project uses behavioral and demographic user datasets
- Both tables contain 108,000 users
- The behavioral table contains 26 columns
- The demographic table contains 6 columns
- One row represents one user
- `user_id` is the primary key
- The datasets have a one-to-one relationship
- Behavioral data explains what users do
- Demographic data explains who users are
- The data dictionary explains every field
- Numerical data supports mathematical analysis
- Categorical data represents groups
- Continuous data is measured
- Discrete data is counted
- Identifiers are used for joining, not clustering
- Features are selected inputs for analysis or Machine Learning
- Business meaning must be understood before cleaning or modeling
- Pandas can inspect shapes, types, nulls, duplicates, categories, and relationships

---

# 23. Quick Reference Cheat Sheet

| Question | Answer |
|---|---|
| Main behavioral table | `spotify_user_behavior` |
| Main demographic table | `spotify_user_demo` |
| Behavior table shape | 108,000 × 26 |
| Demo table shape | 108,000 × 6 |
| One row represents | One user |
| Primary key | `user_id` |
| Relationship | One-to-one |
| Behavior means | What the user does |
| Demographics means | Who the user is |
| Metadata file | Data dictionary |
| Numerical example | `daily_listening_minutes` |
| Categorical example | `device_type` |
| Continuous example | `skip_rate` |
| Discrete example | `days_active_last_30` |
| Identifier used in clustering? | No |
| Expected joined shape | 108,000 × 31 |

---

# 24. What Comes Next?

## Module 04 — Data Cleaning and Preprocessing

The next module will cover:

- Missing values
- Duplicate records
- Wrong data types
- Invalid values
- Inconsistent categories
- Range validation
- Outlier detection
- Data formatting
- Data-quality rules
- Data-cleaning decisions

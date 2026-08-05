"""
Spotify Module 05 — Beginner Visualization Examples

Each chart uses a separate Matplotlib figure.
No chart uses subplots.
"""

import matplotlib.pyplot as plt
import pandas as pd


behavior = pd.read_excel(
    "spotify_user_behavior.xlsx"
)

demo = pd.read_excel(
    "spotify_user_demo.xlsx"
)


# 1. Histogram
plt.figure(figsize=(8, 5))
plt.hist(
    behavior["daily_listening_minutes"],
    bins=60,
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


# 2. Box plot
plt.figure(figsize=(8, 4))
plt.boxplot(
    behavior["daily_listening_minutes"]
    .dropna(),
    vert=False,
)
plt.title(
    "Box Plot of Daily Listening Minutes"
)
plt.xlabel(
    "Daily Listening Minutes"
)
plt.tight_layout()
plt.show()


# 3. Bar chart
device_counts = (
    demo["device_type"]
    .value_counts()
)

plt.figure(figsize=(8, 5))
plt.bar(
    device_counts.index,
    device_counts.values,
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


# 4. Scatter plot
plt.figure(figsize=(8, 5))
plt.scatter(
    behavior["sessions_per_day"],
    behavior["daily_listening_minutes"],
    alpha=0.3,
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


# 5. Correlation heatmap using Matplotlib
numeric_behavior = (
    behavior
    .drop(columns=["user_id"])
    .select_dtypes(include="number")
)

correlation = numeric_behavior.corr()

plt.figure(figsize=(14, 12))
image = plt.imshow(
    correlation,
    aspect="auto",
)
plt.colorbar(
    image,
    label="Correlation",
)
plt.xticks(
    range(len(correlation.columns)),
    correlation.columns,
    rotation=90,
)
plt.yticks(
    range(len(correlation.index)),
    correlation.index,
)
plt.title(
    "Spotify Behavioral Feature Correlation"
)
plt.tight_layout()
plt.show()

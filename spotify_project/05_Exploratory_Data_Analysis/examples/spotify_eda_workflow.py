"""
Spotify Module 05 — Complete Exploratory Data Analysis Workflow

The script calculates:
- Descriptive statistics
- Mean, median, mode and standard deviation
- Percentiles
- Distribution summary
- Skewness
- Category summaries
- Pearson and Spearman correlations
- Strongest correlation pairs
- Univariate charts
- Bivariate charts
- Multivariate grouped summaries

Charts use Matplotlib and create one figure at a time.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


OUTPUT_DIR = Path("eda_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load and safely join the Spotify project datasets."""
    behavior = pd.read_excel("spotify_user_behavior.xlsx")
    demo = pd.read_excel("spotify_user_demo.xlsx")

    users = behavior.merge(
        demo,
        how="inner",
        on="user_id",
        validate="one_to_one",
    )

    return behavior, demo, users


def select_behavior_numeric(
    behavior: pd.DataFrame,
) -> pd.DataFrame:
    """Select numerical behavior columns and exclude user_id."""
    return (
        behavior
        .drop(columns=["user_id"], errors="ignore")
        .select_dtypes(include="number")
        .copy()
    )


def descriptive_statistics(
    numeric_df: pd.DataFrame,
) -> pd.DataFrame:
    """Create a detailed descriptive statistics table."""
    output = (
        numeric_df
        .describe(
            percentiles=[
                0.10,
                0.25,
                0.50,
                0.75,
                0.90,
                0.95,
            ]
        )
        .T
    )

    output["median"] = numeric_df.median()
    output["mode"] = numeric_df.mode().iloc[0]
    output["skewness"] = numeric_df.skew()
    output["missing_pct"] = (
        numeric_df.isna().mean().mul(100)
    )

    return output.round(3)


def category_summary(
    df: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    """Return category counts and percentages."""
    output = (
        df[column]
        .value_counts(dropna=False)
        .rename_axis(column)
        .reset_index(name="users")
    )

    output["percentage"] = (
        output["users"]
        .div(output["users"].sum())
        .mul(100)
        .round(2)
    )

    return output


def strongest_correlation_pairs(
    numeric_df: pd.DataFrame,
    method: str = "pearson",
) -> pd.DataFrame:
    """Return unique feature pairs ranked by absolute correlation."""
    correlation = numeric_df.corr(method=method)

    upper_triangle = np.triu(
        np.ones(correlation.shape),
        k=1,
    ).astype(bool)

    pairs = (
        correlation
        .where(upper_triangle)
        .stack()
        .reset_index()
    )

    pairs.columns = [
        "feature_1",
        "feature_2",
        "correlation",
    ]

    pairs["absolute_correlation"] = (
        pairs["correlation"].abs()
    )

    return (
        pairs
        .sort_values(
            "absolute_correlation",
            ascending=False,
        )
        .reset_index(drop=True)
    )


def save_histogram(
    df: pd.DataFrame,
    column: str,
) -> None:
    """Save one histogram."""
    plt.figure(figsize=(8, 5))
    plt.hist(df[column].dropna(), bins=60)
    plt.title(
        f"Distribution of {column.replace('_', ' ').title()}"
    )
    plt.xlabel(column.replace("_", " ").title())
    plt.ylabel("Number of Users")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / f"histogram_{column}.png",
        dpi=150,
    )
    plt.close()


def save_boxplot(
    df: pd.DataFrame,
    column: str,
) -> None:
    """Save one horizontal box plot."""
    plt.figure(figsize=(8, 4))
    plt.boxplot(
        df[column].dropna(),
        vert=False,
    )
    plt.title(
        f"Box Plot of {column.replace('_', ' ').title()}"
    )
    plt.xlabel(column.replace("_", " ").title())
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / f"boxplot_{column}.png",
        dpi=150,
    )
    plt.close()


def save_category_bar_chart(
    df: pd.DataFrame,
    column: str,
) -> None:
    """Save a category-count bar chart."""
    counts = df[column].value_counts(dropna=False)

    plt.figure(figsize=(8, 5))
    plt.bar(
        counts.index.astype(str),
        counts.values,
    )
    plt.title(
        f"Users by {column.replace('_', ' ').title()}"
    )
    plt.xlabel(column.replace("_", " ").title())
    plt.ylabel("Number of Users")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / f"bar_{column}.png",
        dpi=150,
    )
    plt.close()


def save_scatter_plot(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
) -> None:
    """Save one scatter plot."""
    valid = df[[x_column, y_column]].dropna()

    plt.figure(figsize=(8, 5))
    plt.scatter(
        valid[x_column],
        valid[y_column],
        alpha=0.3,
    )
    plt.title(
        f"{x_column.replace('_', ' ').title()} vs "
        f"{y_column.replace('_', ' ').title()}"
    )
    plt.xlabel(x_column.replace("_", " ").title())
    plt.ylabel(y_column.replace("_", " ").title())
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR
        / f"scatter_{x_column}_vs_{y_column}.png",
        dpi=150,
    )
    plt.close()


def save_correlation_heatmap(
    numeric_df: pd.DataFrame,
) -> None:
    """Save a Matplotlib correlation heatmap."""
    correlation = numeric_df.corr()

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
    plt.savefig(
        OUTPUT_DIR / "correlation_heatmap.png",
        dpi=150,
    )
    plt.close()


def demographic_behavior_summary(
    users: pd.DataFrame,
    category: str,
) -> pd.DataFrame:
    """Compare behavior across one demographic category."""
    return (
        users
        .groupby(category, observed=True)
        .agg(
            users=("user_id", "nunique"),
            avg_listening_minutes=(
                "daily_listening_minutes",
                "mean",
            ),
            median_listening_minutes=(
                "daily_listening_minutes",
                "median",
            ),
            avg_sessions=(
                "sessions_per_day",
                "mean",
            ),
            avg_active_days=(
                "days_active_last_30",
                "mean",
            ),
            avg_skip_rate=(
                "skip_rate",
                "mean",
            ),
            avg_ads_skipped_pct=(
                "ads_skipped_pct",
                "mean",
            ),
        )
        .reset_index()
        .round(3)
    )


def run_eda() -> None:
    """Run the complete analysis and save outputs."""
    behavior, demo, users = load_data()
    numeric_behavior = select_behavior_numeric(behavior)

    stats = descriptive_statistics(numeric_behavior)
    stats.to_csv(
        OUTPUT_DIR / "descriptive_statistics.csv"
    )

    for category in [
        "country",
        "city_tier",
        "device_type",
    ]:
        category_summary(
            demo,
            category,
        ).to_csv(
            OUTPUT_DIR / f"category_{category}.csv",
            index=False,
        )

        demographic_behavior_summary(
            users,
            category,
        ).to_csv(
            OUTPUT_DIR
            / f"behavior_by_{category}.csv",
            index=False,
        )

    pearson_pairs = strongest_correlation_pairs(
        numeric_behavior,
        method="pearson",
    )

    spearman_pairs = strongest_correlation_pairs(
        numeric_behavior,
        method="spearman",
    )

    pearson_pairs.to_csv(
        OUTPUT_DIR / "pearson_correlation_pairs.csv",
        index=False,
    )

    spearman_pairs.to_csv(
        OUTPUT_DIR / "spearman_correlation_pairs.csv",
        index=False,
    )

    important_features = [
        "daily_listening_minutes",
        "sessions_per_day",
        "days_active_last_30",
        "avg_session_minutes",
        "skip_rate",
        "ads_skipped_pct",
        "genre_diversity_score",
    ]

    for feature in important_features:
        if feature in behavior.columns:
            save_histogram(behavior, feature)
            save_boxplot(behavior, feature)

    for category in [
        "country",
        "device_type",
        "city_tier",
    ]:
        save_category_bar_chart(demo, category)

    scatter_pairs = [
        (
            "sessions_per_day",
            "daily_listening_minutes",
        ),
        (
            "avg_session_minutes",
            "daily_listening_minutes",
        ),
        (
            "skip_rate",
            "daily_listening_minutes",
        ),
        (
            "days_active_last_30",
            "daily_listening_minutes",
        ),
        (
            "genre_diversity_score",
            "skip_rate",
        ),
    ]

    for x_column, y_column in scatter_pairs:
        save_scatter_plot(
            behavior,
            x_column,
            y_column,
        )

    save_correlation_heatmap(numeric_behavior)

    print(
        f"EDA outputs saved to: {OUTPUT_DIR.resolve()}"
    )


if __name__ == "__main__":
    run_eda()

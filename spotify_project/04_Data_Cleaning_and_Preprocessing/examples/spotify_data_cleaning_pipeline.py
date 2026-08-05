"""
Spotify Module 04 — Reusable Data Cleaning and Quality Pipeline

This script:
1. Preserves raw copies
2. Standardizes column names and text
3. Validates required columns
4. Creates data profiles
5. Checks missing values
6. Checks duplicates and user IDs
7. Validates numeric ranges
8. Validates categories
9. Builds an IQR outlier report
10. Validates the one-to-one relationship
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class QualityResult:
    """Container for cleaned data and quality reports."""

    behavior_clean: pd.DataFrame
    demo_clean: pd.DataFrame
    behavior_profile: pd.DataFrame
    demo_profile: pd.DataFrame
    range_issues: pd.DataFrame
    category_issues: pd.DataFrame
    outlier_report: pd.DataFrame
    audit_summary: pd.DataFrame


BEHAVIOR_REQUIRED_COLUMNS = {
    "user_id",
    "daily_listening_minutes",
    "sessions_per_day",
    "days_active_last_30",
    "avg_session_minutes",
    "skip_rate",
    "liked_songs_pct",
    "ads_skipped_pct",
}

DEMO_REQUIRED_COLUMNS = {
    "user_id",
    "age",
    "country",
    "city_tier",
    "device_type",
    "subscription_tenure_months",
}

BEHAVIOR_RANGE_RULES = {
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
    "genre_diversity_score": (0, 1),
}

DEMO_RANGE_RULES = {
    "age": (18, 70),
    "city_tier": (1, 3),
    "subscription_tenure_months": (1, 120),
}

DEMO_CATEGORY_RULES = {
    "country": {"US", "IN", "UK", "DE", "BR"},
    "city_tier": {1, 2, 3},
    "device_type": {"Mobile", "Desktop", "Tablet"},
}

OUTLIER_COLUMNS = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
    "playlists_followed",
    "artists_followed",
]


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with lowercase snake_case column names."""
    cleaned = df.copy()
    cleaned.columns = (
        cleaned.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return cleaned


def require_columns(
    df: pd.DataFrame,
    required_columns: set[str],
    table_name: str,
) -> None:
    """Raise an error when required columns are missing."""
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"{table_name} is missing columns: {sorted(missing)}"
        )


def create_data_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Create a column-level data-quality profile."""
    return pd.DataFrame({
        "column_name": df.columns,
        "data_type": df.dtypes.astype(str).values,
        "row_count": len(df),
        "non_null_count": df.notna().sum().values,
        "missing_count": df.isna().sum().values,
        "missing_pct": (
            df.isna().mean().mul(100).round(2).values
        ),
        "unique_count": df.nunique(dropna=True).values,
    })


def validate_ranges(
    df: pd.DataFrame,
    rules: dict[str, tuple[float | None, float | None]],
    table_name: str,
) -> pd.DataFrame:
    """Return rows describing values outside approved ranges."""
    issues: list[dict[str, Any]] = []

    for column, (minimum, maximum) in rules.items():
        if column not in df.columns:
            continue

        series = df[column]

        if minimum is not None:
            mask = series.notna() & (series < minimum)
            count = int(mask.sum())

            if count:
                issues.append({
                    "table": table_name,
                    "column": column,
                    "issue_type": "below_minimum",
                    "expected": f">= {minimum}",
                    "rows_affected": count,
                    "sample_values": (
                        series.loc[mask]
                        .drop_duplicates()
                        .head(10)
                        .tolist()
                    ),
                })

        if maximum is not None:
            mask = series.notna() & (series > maximum)
            count = int(mask.sum())

            if count:
                issues.append({
                    "table": table_name,
                    "column": column,
                    "issue_type": "above_maximum",
                    "expected": f"<= {maximum}",
                    "rows_affected": count,
                    "sample_values": (
                        series.loc[mask]
                        .drop_duplicates()
                        .head(10)
                        .tolist()
                    ),
                })

    return pd.DataFrame(issues)


def validate_categories(
    df: pd.DataFrame,
    rules: dict[str, set[Any]],
    table_name: str,
) -> pd.DataFrame:
    """Return invalid category values."""
    issues: list[dict[str, Any]] = []

    for column, allowed_values in rules.items():
        if column not in df.columns:
            continue

        mask = (
            df[column].notna()
            & ~df[column].isin(allowed_values)
        )

        count = int(mask.sum())

        if count:
            issues.append({
                "table": table_name,
                "column": column,
                "issue_type": "invalid_category",
                "expected": sorted(map(str, allowed_values)),
                "rows_affected": count,
                "sample_values": (
                    df.loc[mask, column]
                    .drop_duplicates()
                    .astype(str)
                    .head(10)
                    .tolist()
                ),
            })

    return pd.DataFrame(issues)


def iqr_outlier_report(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """Report potential outliers without removing them."""
    records: list[dict[str, Any]] = []

    for column in columns:
        if column not in df.columns:
            continue

        series = df[column].dropna()

        if series.empty:
            continue

        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1
        lower = q1 - (1.5 * iqr)
        upper = q3 + (1.5 * iqr)

        mask = (series < lower) | (series > upper)
        count = int(mask.sum())

        records.append({
            "column": column,
            "q1": round(q1, 4),
            "q3": round(q3, 4),
            "iqr": round(iqr, 4),
            "lower_bound": round(lower, 4),
            "upper_bound": round(upper, 4),
            "outlier_count": count,
            "outlier_pct": round(
                100 * count / len(series),
                2,
            ),
        })

    return pd.DataFrame(records)


def validate_user_ids(
    behavior: pd.DataFrame,
    demo: pd.DataFrame,
) -> None:
    """Raise errors for missing, duplicate, or unmatched IDs."""
    for name, df in [
        ("spotify_user_behavior", behavior),
        ("spotify_user_demo", demo),
    ]:
        if df["user_id"].isna().any():
            raise ValueError(f"{name} has missing user_id")

        if not df["user_id"].is_unique:
            raise ValueError(f"{name} has duplicate user_id")

    behavior_users = set(behavior["user_id"])
    demo_users = set(demo["user_id"])

    behavior_only = behavior_users - demo_users
    demo_only = demo_users - behavior_users

    if behavior_only or demo_only:
        raise ValueError(
            "Unmatched users detected. "
            f"Behavior only: {len(behavior_only)}; "
            f"Demo only: {len(demo_only)}"
        )


def build_audit_summary(
    behavior_raw: pd.DataFrame,
    behavior_clean: pd.DataFrame,
    demo_raw: pd.DataFrame,
    demo_clean: pd.DataFrame,
) -> pd.DataFrame:
    """Create a concise before/after audit table."""
    records = [
        {
            "dataset": "spotify_user_behavior",
            "rows_before": len(behavior_raw),
            "rows_after": len(behavior_clean),
            "columns_before": behavior_raw.shape[1],
            "columns_after": behavior_clean.shape[1],
            "missing_after": int(
                behavior_clean.isna().sum().sum()
            ),
            "duplicate_rows_after": int(
                behavior_clean.duplicated().sum()
            ),
            "duplicate_user_ids_after": int(
                behavior_clean["user_id"]
                .duplicated()
                .sum()
            ),
        },
        {
            "dataset": "spotify_user_demo",
            "rows_before": len(demo_raw),
            "rows_after": len(demo_clean),
            "columns_before": demo_raw.shape[1],
            "columns_after": demo_clean.shape[1],
            "missing_after": int(
                demo_clean.isna().sum().sum()
            ),
            "duplicate_rows_after": int(
                demo_clean.duplicated().sum()
            ),
            "duplicate_user_ids_after": int(
                demo_clean["user_id"]
                .duplicated()
                .sum()
            ),
        },
    ]

    return pd.DataFrame(records)


def run_quality_pipeline(
    behavior_df: pd.DataFrame,
    demo_df: pd.DataFrame,
) -> QualityResult:
    """Run the complete Spotify quality pipeline."""
    behavior_raw = behavior_df.copy()
    demo_raw = demo_df.copy()

    behavior = clean_column_names(behavior_raw)
    demo = clean_column_names(demo_raw)

    require_columns(
        behavior,
        BEHAVIOR_REQUIRED_COLUMNS,
        "spotify_user_behavior",
    )

    require_columns(
        demo,
        DEMO_REQUIRED_COLUMNS,
        "spotify_user_demo",
    )

    missing_tokens = ["", " ", "NA", "N/A", "null", "None", "-"]
    behavior = behavior.replace(missing_tokens, pd.NA)
    demo = demo.replace(missing_tokens, pd.NA)

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

    for column in behavior.columns:
        if column != "user_id":
            behavior[column] = pd.to_numeric(
                behavior[column],
                errors="coerce",
            )

    for column in [
        "user_id",
        "age",
        "city_tier",
        "subscription_tenure_months",
    ]:
        demo[column] = pd.to_numeric(
            demo[column],
            errors="coerce",
        )

    behavior["user_id"] = pd.to_numeric(
        behavior["user_id"],
        errors="raise",
    ).astype("int64")

    demo["user_id"] = pd.to_numeric(
        demo["user_id"],
        errors="raise",
    ).astype("int64")

    validate_user_ids(behavior, demo)

    behavior_profile = create_data_profile(behavior)
    demo_profile = create_data_profile(demo)

    behavior_range = validate_ranges(
        behavior,
        BEHAVIOR_RANGE_RULES,
        "spotify_user_behavior",
    )

    demo_range = validate_ranges(
        demo,
        DEMO_RANGE_RULES,
        "spotify_user_demo",
    )

    range_issues = pd.concat(
        [behavior_range, demo_range],
        ignore_index=True,
    )

    category_issues = validate_categories(
        demo,
        DEMO_CATEGORY_RULES,
        "spotify_user_demo",
    )

    outlier_report = iqr_outlier_report(
        behavior,
        OUTLIER_COLUMNS,
    )

    behavior.merge(
        demo,
        how="inner",
        on="user_id",
        validate="one_to_one",
    )

    audit_summary = build_audit_summary(
        behavior_raw,
        behavior,
        demo_raw,
        demo,
    )

    return QualityResult(
        behavior_clean=behavior,
        demo_clean=demo,
        behavior_profile=behavior_profile,
        demo_profile=demo_profile,
        range_issues=range_issues,
        category_issues=category_issues,
        outlier_report=outlier_report,
        audit_summary=audit_summary,
    )


if __name__ == "__main__":
    behavior = pd.read_excel("spotify_user_behavior.xlsx")
    demo = pd.read_excel("spotify_user_demo.xlsx")

    result = run_quality_pipeline(
        behavior,
        demo,
    )

    print("\nAudit Summary")
    print(result.audit_summary.to_string(index=False))

    print("\nRange Issues")
    if result.range_issues.empty:
        print("No range issues found.")
    else:
        print(result.range_issues.to_string(index=False))

    print("\nCategory Issues")
    if result.category_issues.empty:
        print("No category issues found.")
    else:
        print(result.category_issues.to_string(index=False))

    print("\nPotential Outliers")
    print(result.outlier_report.to_string(index=False))

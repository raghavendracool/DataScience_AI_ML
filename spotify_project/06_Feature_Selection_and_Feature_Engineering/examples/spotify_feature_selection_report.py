"""
Spotify Module 06 — Feature Selection Report

This script creates:
- Missing-value report
- Data-type report
- Unique-value report
- Near-constant report
- Skewness report
- Spearman correlation-pair report
- Candidate feature decision table
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def near_constant_report(
    df: pd.DataFrame,
    threshold: float = 0.98,
) -> pd.DataFrame:
    """Flag features dominated by one value."""
    records = []

    for column in df.columns:
        proportions = (
            df[column]
            .value_counts(
                normalize=True,
                dropna=False,
            )
        )

        top_share = (
            float(proportions.iloc[0])
            if not proportions.empty
            else 0.0
        )

        records.append({
            "feature": column,
            "unique_count": int(
                df[column].nunique(
                    dropna=False
                )
            ),
            "most_common_share": round(
                top_share,
                4,
            ),
            "near_constant": (
                top_share >= threshold
            ),
        })

    return pd.DataFrame(records)


def correlation_pair_report(
    df: pd.DataFrame,
    threshold: float = 0.85,
) -> pd.DataFrame:
    """Return unique Spearman pairs above a threshold."""
    correlation = df.corr(
        method="spearman"
    )

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
        pairs["correlation"]
        .abs()
    )

    return (
        pairs[
            pairs[
                "absolute_correlation"
            ] >= threshold
        ]
        .sort_values(
            "absolute_correlation",
            ascending=False,
        )
        .reset_index(drop=True)
    )


def create_selection_profile(
    feature_df: pd.DataFrame,
) -> pd.DataFrame:
    """Create one feature-level selection report."""
    profile = pd.DataFrame({
        "feature": feature_df.columns,
        "data_type": (
            feature_df.dtypes
            .astype(str)
            .values
        ),
        "missing_count": (
            feature_df.isna()
            .sum()
            .values
        ),
        "missing_pct": (
            feature_df.isna()
            .mean()
            .mul(100)
            .round(2)
            .values
        ),
        "unique_count": (
            feature_df.nunique(
                dropna=True
            )
            .values
        ),
        "variance": (
            feature_df.var(
                numeric_only=True
            )
            .reindex(
                feature_df.columns
            )
            .values
        ),
        "skewness": (
            feature_df.skew(
                numeric_only=True
            )
            .reindex(
                feature_df.columns
            )
            .values
        ),
    })

    return profile


if __name__ == "__main__":
    behavior = pd.read_excel(
        "spotify_user_behavior.xlsx"
    )

    feature_df = (
        behavior
        .drop(columns=["user_id"])
        .select_dtypes(include="number")
        .copy()
    )

    selection_profile = (
        create_selection_profile(
            feature_df
        )
    )

    constant_report = (
        near_constant_report(
            feature_df
        )
    )

    correlation_report = (
        correlation_pair_report(
            feature_df,
            threshold=0.85,
        )
    )

    selection_profile.to_csv(
        "spotify_feature_selection_profile.csv",
        index=False,
    )

    constant_report.to_csv(
        "spotify_near_constant_report.csv",
        index=False,
    )

    correlation_report.to_csv(
        "spotify_high_correlation_pairs.csv",
        index=False,
    )

    print("Feature Selection Profile")
    print(
        selection_profile.to_string(
            index=False
        )
    )

    print("\nNear-Constant Features")
    print(
        constant_report[
            constant_report[
                "near_constant"
            ]
        ].to_string(index=False)
    )

    print("\nHighly Correlated Pairs")
    if correlation_report.empty:
        print(
            "No pairs met the threshold."
        )
    else:
        print(
            correlation_report.to_string(
                index=False
            )
        )

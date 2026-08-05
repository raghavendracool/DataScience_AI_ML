"""
Spotify Module 13 — Persona Summary Generator

Generates Markdown drafts from reviewed persona mapping data.

Expected:
- cluster_profile_outputs/cluster_sizes.csv
- cluster_profile_outputs/behavior_means.csv
- cluster_profile_outputs/demographic_profile.csv
- reviewed_persona_mapping.csv
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


INPUT_DIR = Path(
    "cluster_profile_outputs"
)

OUTPUT_DIR = Path(
    "persona_summaries"
)

OUTPUT_DIR.mkdir(exist_ok=True)


def safe_filename(
    value: str,
) -> str:
    """Create a simple file-safe name."""
    return (
        value.strip()
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
    )


def build_persona_markdown(
    cluster: object,
    persona_name: str,
    size_row: pd.Series,
    behavior_row: pd.Series,
    demographic_row: pd.Series,
    mapping_row: pd.Series,
) -> str:
    """Create one reviewed persona summary."""
    return f"""# {persona_name}

## Cluster Identity

```text
Cluster: {cluster}
Users: {int(size_row['user_count']):,}
Percentage: {size_row['user_percentage']:.2f}%
```

## Behavioral Summary

{mapping_row['behavior_summary']}

## Key Evidence

| Feature | Cluster Mean |
|---|---:|
| Daily Listening Minutes | {behavior_row['daily_listening_minutes']:.2f} |
| Sessions per Day | {behavior_row['sessions_per_day']:.2f} |
| Average Session Minutes | {behavior_row['avg_session_minutes']:.2f} |
| Days Active Last 30 | {behavior_row['days_active_last_30']:.2f} |
| Skip Rate | {behavior_row['skip_rate']:.2%} |
| Ads Skipped Percentage | {behavior_row['ads_skipped_pct']:.2%} |

## Demographic Context

```text
Average Age: {demographic_row['avg_age']:.2f}
Average Tenure: {demographic_row['avg_tenure_months']:.2f} months
Top Country: {demographic_row['top_country']}
Top City Tier: {demographic_row['top_city_tier']}
Top Device: {demographic_row['top_device_type']}
```

## Business Interpretation

{mapping_row['business_interpretation']}

## Recommended Actions

{mapping_row['recommended_actions']}

## Risks and Limitations

{mapping_row['risks_and_limitations']}
"""


if __name__ == "__main__":
    sizes = pd.read_csv(
        INPUT_DIR
        / "cluster_sizes.csv"
    )

    means = pd.read_csv(
        INPUT_DIR
        / "behavior_means.csv"
    )

    demographics = pd.read_csv(
        INPUT_DIR
        / "demographic_profile.csv"
    )

    mapping = pd.read_csv(
        "reviewed_persona_mapping.csv"
    )

    required_mapping_columns = {
        "cluster",
        "persona_name",
        "behavior_summary",
        "business_interpretation",
        "recommended_actions",
        "risks_and_limitations",
    }

    missing = (
        required_mapping_columns
        - set(mapping.columns)
    )

    if missing:
        raise ValueError(
            "Missing mapping columns: "
            f"{sorted(missing)}"
        )

    for _, mapping_row in mapping.iterrows():
        cluster = mapping_row["cluster"]

        size_row = sizes[
            sizes["cluster"]
            == cluster
        ].iloc[0]

        behavior_row = means[
            means["cluster"]
            == cluster
        ].iloc[0]

        demographic_row = demographics[
            demographics["cluster"]
            == cluster
        ].iloc[0]

        markdown = build_persona_markdown(
            cluster=cluster,
            persona_name=(
                mapping_row[
                    "persona_name"
                ]
            ),
            size_row=size_row,
            behavior_row=behavior_row,
            demographic_row=(
                demographic_row
            ),
            mapping_row=mapping_row,
        )

        filename = (
            safe_filename(
                mapping_row[
                    "persona_name"
                ]
            )
            + ".md"
        )

        (
            OUTPUT_DIR
            / filename
        ).write_text(
            markdown,
            encoding="utf-8",
        )

    print(
        f"Persona summaries saved to: "
        f"{OUTPUT_DIR.resolve()}"
    )

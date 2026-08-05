"""
Spotify Module 14 — Persona Card Generator

Expected:
- reviewed_persona_mapping.csv

Required columns:
- cluster
- segment_name
- persona_name
- user_count
- user_percentage
- one_line_summary
- characteristics
- primary_need
- primary_risk
- primary_opportunity
- recommended_actions
- evidence
- limitations
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path(
    "persona_cards"
)

OUTPUT_DIR.mkdir(exist_ok=True)


def safe_filename(
    value: str,
) -> str:
    """Convert a persona name to a file-safe value."""
    return (
        value.strip()
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
    )


def build_card(
    row: pd.Series,
) -> str:
    """Create one Markdown persona card."""
    return f"""# {row['persona_name']}

## Segment Identity

```text
Cluster: {row['cluster']}
Segment: {row['segment_name']}
Users: {int(row['user_count']):,}
Percentage: {row['user_percentage']:.2f}%
```

## One-Line Summary

{row['one_line_summary']}

## Characteristics

{row['characteristics']}

## Primary Need

{row['primary_need']}

## Primary Risk

{row['primary_risk']}

## Primary Opportunity

{row['primary_opportunity']}

## Recommended Actions

{row['recommended_actions']}

## Evidence

{row['evidence']}

## Limitations

{row['limitations']}
"""


if __name__ == "__main__":
    mapping = pd.read_csv(
        "reviewed_persona_mapping.csv"
    )

    required = {
        "cluster",
        "segment_name",
        "persona_name",
        "user_count",
        "user_percentage",
        "one_line_summary",
        "characteristics",
        "primary_need",
        "primary_risk",
        "primary_opportunity",
        "recommended_actions",
        "evidence",
        "limitations",
    }

    missing = required - set(
        mapping.columns
    )

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    for _, row in mapping.iterrows():
        card = build_card(row)

        filename = (
            safe_filename(
                row["persona_name"]
            )
            + ".md"
        )

        (
            OUTPUT_DIR
            / filename
        ).write_text(
            card,
            encoding="utf-8",
        )

    print(
        f"Persona cards saved to: "
        f"{OUTPUT_DIR.resolve()}"
    )

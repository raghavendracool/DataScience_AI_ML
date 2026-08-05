"""
Module 17 — Final Persona Report Generator
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path(
    "final_persona_reports"
)

OUTPUT_DIR.mkdir(exist_ok=True)


def safe_filename(
    value: str,
) -> str:
    """Create a file-safe persona name."""
    return (
        value.strip()
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
    )


def create_persona_report(
    persona: pd.Series,
    recommendation: pd.Series,
) -> str:
    """Create one persona Markdown report."""
    return f"""# {persona['persona_name']}

## Cluster

```text
Cluster: {int(persona['cluster'])}
Illustrative User Share: {persona['user_percentage']:.1f}%
```

## Behavioral Profile

| Feature | Value |
|---|---:|
| Daily Listening Minutes | {persona['daily_listening_minutes']:.1f} |
| Sessions per Day | {persona['sessions_per_day']:.1f} |
| Days Active Last 30 | {persona['days_active_last_30']:.1f} |
| Skip Rate | {persona['skip_rate']:.1%} |
| Repeat Track Rate | {persona['repeat_track_rate']:.1%} |
| Genre Diversity | {persona['genre_diversity_score']:.2f} |

## Primary Need

{persona['primary_need']}

## Primary Recommendation

{recommendation['primary_action']}

## Primary KPI

{recommendation['primary_kpi']}

## Guardrail KPI

{recommendation['guardrail_kpi']}

## Important Limitation

This persona description is illustrative and must be replaced
with actual final model outputs before official use.
"""


if __name__ == "__main__":
    personas = pd.read_csv(
        "final_personas.csv"
    )

    recommendations = pd.read_csv(
        "business_recommendations.csv"
    )

    merged = personas.merge(
        recommendations,
        on="persona_name",
        how="left",
        validate="one_to_one",
    )

    for _, row in merged.iterrows():
        report = create_persona_report(
            row,
            row,
        )

        filename = (
            safe_filename(
                row["persona_name"]
            )
            + ".md"
        )

        (
            OUTPUT_DIR / filename
        ).write_text(
            report,
            encoding="utf-8",
        )

    print(
        f"Persona reports saved to: "
        f"{OUTPUT_DIR.resolve()}"
    )

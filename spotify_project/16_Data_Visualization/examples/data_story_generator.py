"""
Spotify Module 16 — Data Story Generator

Creates a Markdown story from structured inputs.

Expected input:
- data_story_input.csv

Required columns:
- story_id
- title
- context
- question
- evidence
- observation
- insight
- action_hypothesis
- primary_kpi
- guardrail_kpis
- limitation
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path(
    "data_stories"
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


def build_story(
    row: pd.Series,
) -> str:
    """Build one Markdown data story."""
    return f"""# {row['title']}

## Context

{row['context']}

## Business Question

{row['question']}

## Evidence

{row['evidence']}

## Observation

{row['observation']}

## Insight

{row['insight']}

## Action Hypothesis

{row['action_hypothesis']}

## Primary KPI

{row['primary_kpi']}

## Guardrail KPIs

{row['guardrail_kpis']}

## Limitation

{row['limitation']}
"""


if __name__ == "__main__":
    stories = pd.read_csv(
        "data_story_input.csv"
    )

    required = {
        "story_id",
        "title",
        "context",
        "question",
        "evidence",
        "observation",
        "insight",
        "action_hypothesis",
        "primary_kpi",
        "guardrail_kpis",
        "limitation",
    }

    missing = required - set(
        stories.columns
    )

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    for _, row in stories.iterrows():
        filename = (
            safe_filename(
                row["story_id"]
            )
            + "_"
            + safe_filename(
                row["title"]
            )
            + ".md"
        )

        (
            OUTPUT_DIR / filename
        ).write_text(
            build_story(row),
            encoding="utf-8",
        )

    print(
        f"Stories saved to: "
        f"{OUTPUT_DIR.resolve()}"
    )

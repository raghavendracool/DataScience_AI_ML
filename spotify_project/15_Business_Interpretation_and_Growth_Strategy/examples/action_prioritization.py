"""
Spotify Module 15 — Action Prioritization

Calculates:
- Priority score
- Risk-adjusted priority
- Impact-effort category
- Ranked action table

Expected input:
- persona_actions.csv
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_DIR = Path(
    "action_prioritization_outputs"
)

OUTPUT_DIR.mkdir(exist_ok=True)


def validate_scores(
    actions: pd.DataFrame,
) -> None:
    """Validate required numeric scoring columns."""
    required = {
        "action_id",
        "persona",
        "action",
        "estimated_impact",
        "estimated_effort",
        "confidence",
        "risk_score",
    }

    missing = required - set(
        actions.columns
    )

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    if (
        actions["estimated_effort"]
        <= 0
    ).any():
        raise ValueError(
            "Estimated effort must be positive"
        )

    if not actions["confidence"].between(
        0,
        1,
    ).all():
        raise ValueError(
            "Confidence must be between 0 and 1"
        )


def classify_action(
    impact: float,
    effort: float,
    impact_median: float,
    effort_median: float,
) -> str:
    """Classify an action in an impact-effort matrix."""
    if (
        impact >= impact_median
        and effort <= effort_median
    ):
        return "QUICK_WIN"

    if (
        impact >= impact_median
        and effort > effort_median
    ):
        return "STRATEGIC_PROJECT"

    if (
        impact < impact_median
        and effort <= effort_median
    ):
        return "FILL_IN"

    return "DEPRIORITIZE"


def prioritize_actions(
    actions: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate priority and classification."""
    validate_scores(actions)

    output = actions.copy()

    output["priority_score"] = (
        output["estimated_impact"]
        * output["confidence"]
        / output["estimated_effort"]
    )

    output["risk_adjusted_priority"] = (
        output["priority_score"]
        / (
            1
            + output["risk_score"] / 10
        )
    )

    impact_median = output[
        "estimated_impact"
    ].median()

    effort_median = output[
        "estimated_effort"
    ].median()

    output["priority_category"] = (
        output.apply(
            lambda row: classify_action(
                impact=row[
                    "estimated_impact"
                ],
                effort=row[
                    "estimated_effort"
                ],
                impact_median=impact_median,
                effort_median=effort_median,
            ),
            axis=1,
        )
    )

    return (
        output
        .sort_values(
            "risk_adjusted_priority",
            ascending=False,
        )
        .reset_index(drop=True)
    )


if __name__ == "__main__":
    actions = pd.read_csv(
        "persona_actions.csv"
    )

    ranked = prioritize_actions(
        actions
    )

    ranked.to_csv(
        OUTPUT_DIR
        / "ranked_actions.csv",
        index=False,
    )

    print(
        ranked.round(4)
        .to_string(index=False)
    )

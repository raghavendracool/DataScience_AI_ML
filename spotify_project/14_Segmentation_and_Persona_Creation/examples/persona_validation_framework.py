"""
Spotify Module 14 — Persona Validation Framework

Evaluates whether each persona is ready for business testing.

Expected file:
- persona_validation_input.csv
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path(
    "persona_validation_outputs"
)

OUTPUT_DIR.mkdir(exist_ok=True)

BOOLEAN_COLUMNS = [
    "evidence_complete",
    "stable_across_seeds",
    "profile_stable",
    "stakeholder_reviewed",
    "fairness_reviewed",
    "business_test_defined",
    "success_metrics_defined",
]


def determine_status(
    row: pd.Series,
) -> str:
    """Return one validation status."""
    checks = [
        bool(row[column])
        for column in BOOLEAN_COLUMNS
    ]

    if all(checks):
        return "READY_FOR_TESTING"

    if row["evidence_complete"] and row[
        "stakeholder_reviewed"
    ]:
        return "REQUIRES_ADDITIONAL_VALIDATION"

    return "DRAFT"


if __name__ == "__main__":
    validation = pd.read_csv(
        "persona_validation_input.csv"
    )

    missing = set(
        ["persona", *BOOLEAN_COLUMNS]
    ) - set(validation.columns)

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    validation["validation_status"] = (
        validation.apply(
            determine_status,
            axis=1,
        )
    )

    validation.to_csv(
        OUTPUT_DIR
        / "persona_validation_results.csv",
        index=False,
    )

    print(
        validation.to_string(
            index=False
        )
    )

"""
Spotify Module 15 — Persona Experiment Planner

Creates a structured experiment-plan table from proposed actions.

Expected input:
- proposed_growth_actions.csv
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path(
    "growth_experiment_outputs"
)

OUTPUT_DIR.mkdir(exist_ok=True)


def build_experiment_plan(
    actions: pd.DataFrame,
) -> pd.DataFrame:
    """Create one experiment-plan row per action."""
    required = {
        "action_id",
        "persona",
        "business_problem",
        "evidence",
        "action_hypothesis",
        "primary_kpi",
        "guardrail_kpis",
        "owner",
    }

    missing = required - set(
        actions.columns
    )

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    output = actions.copy()

    output["experiment_id"] = (
        "EXP_"
        + output["action_id"]
        .astype(str)
        .str.replace(
            "ACT-",
            "",
            regex=False,
        )
    )

    output["treatment_definition"] = ""
    output["control_definition"] = ""
    output["eligibility_criteria"] = ""
    output["exclusion_criteria"] = ""
    output["measurement_window"] = ""
    output["minimum_detectable_improvement"] = ""
    output["stop_condition"] = ""
    output["decision"] = "DRAFT"

    ordered_columns = [
        "experiment_id",
        "action_id",
        "persona",
        "business_problem",
        "evidence",
        "action_hypothesis",
        "eligibility_criteria",
        "exclusion_criteria",
        "treatment_definition",
        "control_definition",
        "primary_kpi",
        "guardrail_kpis",
        "measurement_window",
        "minimum_detectable_improvement",
        "stop_condition",
        "owner",
        "decision",
    ]

    return output[
        ordered_columns
    ]


if __name__ == "__main__":
    actions = pd.read_csv(
        "proposed_growth_actions.csv"
    )

    plan = build_experiment_plan(
        actions
    )

    plan.to_csv(
        OUTPUT_DIR
        / "persona_growth_experiment_plan.csv",
        index=False,
    )

    print(
        plan.to_string(
            index=False
        )
    )

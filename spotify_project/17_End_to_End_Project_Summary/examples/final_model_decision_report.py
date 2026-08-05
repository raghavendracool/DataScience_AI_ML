"""
Module 17 — Final Model Decision Report
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path(
    "final_project_outputs"
)

OUTPUT_DIR.mkdir(exist_ok=True)


def calculate_overall_score(
    decisions: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate an illustrative multi-dimensional score."""
    required = {
        "candidate_id",
        "silhouette_score",
        "stability_score",
        "cluster_balance_score",
        "business_interpretability_score",
        "deployment_simplicity_score",
    }

    missing = required - set(
        decisions.columns
    )

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    output = decisions.copy()

    output["overall_decision_score"] = (
        0.20 * output["silhouette_score"]
        + 0.25 * output["stability_score"]
        + 0.15 * output["cluster_balance_score"]
        + 0.25
        * output[
            "business_interpretability_score"
        ]
        + 0.15
        * output[
            "deployment_simplicity_score"
        ]
    )

    return output.sort_values(
        "overall_decision_score",
        ascending=False,
    )


if __name__ == "__main__":
    decisions = pd.read_csv(
        "final_model_decisions.csv"
    )

    ranked = calculate_overall_score(
        decisions
    )

    ranked.to_csv(
        OUTPUT_DIR
        / "ranked_model_decisions.csv",
        index=False,
    )

    print(
        ranked[
            [
                "candidate_id",
                "algorithm",
                "overall_decision_score",
                "status",
                "decision_reason",
            ]
        ]
        .round(4)
        .to_string(index=False)
    )

    print(
        "\nThe weighted score is a decision aid, "
        "not objective truth."
    )

"""
Module 17 — Build Final Project Summary

Reads final project CSV files and creates:
- Markdown summary
- JSON project summary
- Persona section
- Model-decision section
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("final_project_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def build_markdown(
    model_decisions: pd.DataFrame,
    personas: pd.DataFrame,
    recommendations: pd.DataFrame,
) -> str:
    """Create a concise final project Markdown report."""
    selected = model_decisions[
        model_decisions["status"] == "SELECTED"
    ]

    if selected.empty:
        raise ValueError(
            "No selected model exists"
        )

    selected_row = selected.iloc[0]

    lines = [
        "# Final Spotify Segmentation Project Summary",
        "",
        "## Selected Model",
        "",
        f"- Candidate: {selected_row['candidate_id']}",
        f"- Algorithm: {selected_row['algorithm']}",
        f"- Preprocessing: {selected_row['preprocessing']}",
        (
            "- Clusters / Components: "
            f"{int(selected_row['clusters_or_components'])}"
        ),
        f"- Reason: {selected_row['decision_reason']}",
        "",
        "## Final Personas",
        "",
    ]

    for _, row in personas.iterrows():
        lines.extend([
            f"### {row['persona_name']}",
            "",
            (
                f"- Illustrative share: "
                f"{row['user_percentage']:.1f}%"
            ),
            (
                f"- Listening: "
                f"{row['daily_listening_minutes']:.0f} minutes/day"
            ),
            (
                f"- Sessions: "
                f"{row['sessions_per_day']:.1f}/day"
            ),
            f"- Need: {row['primary_need']}",
            "",
        ])

    lines.extend([
        "## Business Recommendations",
        "",
    ])

    for _, row in recommendations.iterrows():
        lines.extend([
            f"### {row['persona_name']}",
            "",
            f"- Area: {row['recommendation_area']}",
            f"- Action: {row['primary_action']}",
            f"- Primary KPI: {row['primary_kpi']}",
            f"- Guardrail: {row['guardrail_kpi']}",
            "",
        ])

    return "\n".join(lines)


if __name__ == "__main__":
    model_decisions = pd.read_csv(
        "final_model_decisions.csv"
    )

    personas = pd.read_csv(
        "final_personas.csv"
    )

    recommendations = pd.read_csv(
        "business_recommendations.csv"
    )

    markdown = build_markdown(
        model_decisions,
        personas,
        recommendations,
    )

    (
        OUTPUT_DIR
        / "final_project_summary.md"
    ).write_text(
        markdown,
        encoding="utf-8",
    )

    selected = (
        model_decisions[
            model_decisions["status"]
            == "SELECTED"
        ]
        .iloc[0]
        .to_dict()
    )

    project_json = {
        "selected_model": selected,
        "personas": personas.to_dict(
            orient="records"
        ),
        "recommendations": (
            recommendations.to_dict(
                orient="records"
            )
        ),
    }

    (
        OUTPUT_DIR
        / "final_project_summary.json"
    ).write_text(
        json.dumps(
            project_json,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    print(
        f"Outputs saved to: "
        f"{OUTPUT_DIR.resolve()}"
    )

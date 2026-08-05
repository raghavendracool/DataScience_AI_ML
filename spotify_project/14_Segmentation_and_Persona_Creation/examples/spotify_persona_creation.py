"""
Spotify Module 14 — Persona Creation Pipeline

Expected files:
- cluster_profile_outputs/cluster_sizes.csv
- cluster_profile_outputs/behavior_means.csv
- cluster_profile_outputs/standardized_profile.csv
- cluster_profile_outputs/demographic_profile.csv
- cluster_profile_outputs/high_low_features.csv

Outputs:
- Draft segment definitions
- Draft persona evidence
- Needs, risks and opportunities table
- Cluster-to-persona mapping template

Important:
This script creates drafts for analyst and stakeholder review.
It does not treat persona names as objective model output.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


INPUT_DIR = Path(
    "cluster_profile_outputs"
)

OUTPUT_DIR = Path(
    "persona_creation_outputs"
)

OUTPUT_DIR.mkdir(exist_ok=True)


def combine_high_low_features(
    high_low: pd.DataFrame,
) -> pd.DataFrame:
    """Create one row per cluster with high and low features."""
    rows = []

    for cluster in sorted(
        high_low["cluster"].unique()
    ):
        subset = high_low[
            high_low["cluster"]
            == cluster
        ]

        high_features = (
            subset[
                subset["direction"]
                == "HIGH"
            ]
            .sort_values("rank")[
                "feature"
            ]
            .tolist()
        )

        low_features = (
            subset[
                subset["direction"]
                == "LOW"
            ]
            .sort_values("rank")[
                "feature"
            ]
            .tolist()
        )

        rows.append({
            "cluster": cluster,
            "high_features": (
                ", ".join(high_features)
            ),
            "low_features": (
                ", ".join(low_features)
            ),
        })

    return pd.DataFrame(rows)


def create_persona_draft(
    sizes: pd.DataFrame,
    high_low: pd.DataFrame,
    demographics: pd.DataFrame,
) -> pd.DataFrame:
    """Create one persona-draft row per cluster."""
    evidence = combine_high_low_features(
        high_low
    )

    draft = (
        sizes
        .merge(
            evidence,
            on="cluster",
            how="left",
            validate="one_to_one",
        )
        .merge(
            demographics,
            on="cluster",
            how="left",
            validate="one_to_one",
        )
    )

    draft["segment_definition"] = ""
    draft["persona_name"] = ""
    draft["one_line_summary"] = ""
    draft["primary_need"] = ""
    draft["primary_risk"] = ""
    draft["primary_opportunity"] = ""
    draft["recommended_actions"] = ""
    draft["limitations"] = ""
    draft["stakeholder_status"] = "PENDING"
    draft["persona_version"] = "v0.1-draft"

    return draft


if __name__ == "__main__":
    sizes = pd.read_csv(
        INPUT_DIR
        / "cluster_sizes.csv"
    )

    high_low = pd.read_csv(
        INPUT_DIR
        / "high_low_features.csv"
    )

    demographics = pd.read_csv(
        INPUT_DIR
        / "demographic_profile.csv"
    )

    draft = create_persona_draft(
        sizes,
        high_low,
        demographics,
    )

    draft.to_csv(
        OUTPUT_DIR
        / "persona_creation_draft.csv",
        index=False,
    )

    print(
        draft.to_string(
            index=False
        )
    )

    print(
        "\nComplete the business fields "
        "through analyst and stakeholder review."
    )

"""
Spotify Module 13 — Cluster Naming Framework

Creates evidence tables for persona naming.

This script does not assign final names automatically.
It creates a naming draft for analyst and stakeholder review.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


INPUT_DIR = Path(
    "cluster_profile_outputs"
)

OUTPUT_DIR = Path(
    "cluster_naming_outputs"
)

OUTPUT_DIR.mkdir(exist_ok=True)


def create_naming_evidence(
    high_low: pd.DataFrame,
    sizes: pd.DataFrame,
) -> pd.DataFrame:
    """Create one evidence row per cluster."""
    rows = []

    for cluster in sorted(
        high_low["cluster"].unique()
    ):
        cluster_rows = high_low[
            high_low["cluster"]
            == cluster
        ]

        high_features = (
            cluster_rows[
                cluster_rows["direction"]
                == "HIGH"
            ]
            .sort_values("rank")[
                "feature"
            ]
            .tolist()
        )

        low_features = (
            cluster_rows[
                cluster_rows["direction"]
                == "LOW"
            ]
            .sort_values("rank")[
                "feature"
            ]
            .tolist()
        )

        size_row = sizes[
            sizes["cluster"]
            == cluster
        ].iloc[0]

        rows.append({
            "cluster": cluster,
            "user_count": int(
                size_row["user_count"]
            ),
            "user_percentage": float(
                size_row[
                    "user_percentage"
                ]
            ),
            "top_high_features": (
                ", ".join(
                    high_features
                )
            ),
            "top_low_features": (
                ", ".join(
                    low_features
                )
            ),
            "neutral_behavior_summary": "",
            "suggested_persona_name": "",
            "business_interpretation": "",
            "recommended_action": "",
            "stakeholder_status": (
                "PENDING"
            ),
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    high_low = pd.read_csv(
        INPUT_DIR
        / "high_low_features.csv"
    )

    sizes = pd.read_csv(
        INPUT_DIR
        / "cluster_sizes.csv"
    )

    evidence = create_naming_evidence(
        high_low,
        sizes,
    )

    evidence.to_csv(
        OUTPUT_DIR
        / "cluster_naming_evidence.csv",
        index=False,
    )

    print(
        evidence.to_string(
            index=False
        )
    )

    print(
        "\nFinal names require analyst "
        "and stakeholder review."
    )

"""
Spotify Module 14 — Cluster, Segment and Persona Mapping
"""

from __future__ import annotations

import pandas as pd


def validate_mapping(
    mapping: pd.DataFrame,
) -> None:
    """Validate one-to-one active persona mapping."""
    required = {
        "cluster",
        "segment_name",
        "persona_name",
        "mapping_version",
        "status",
    }

    missing = required - set(
        mapping.columns
    )

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    active = mapping[
        mapping["status"]
        == "ACTIVE"
    ]

    if active["cluster"].duplicated().any():
        raise ValueError(
            "More than one active persona "
            "exists for a cluster"
        )

    if active["persona_name"].duplicated().any():
        raise ValueError(
            "Duplicate active persona names exist"
        )


if __name__ == "__main__":
    mapping = pd.read_csv(
        "cluster_segment_persona_mapping.csv"
    )

    validate_mapping(mapping)

    print(
        "Mapping validation passed."
    )

    print(
        mapping.to_string(
            index=False
        )
    )

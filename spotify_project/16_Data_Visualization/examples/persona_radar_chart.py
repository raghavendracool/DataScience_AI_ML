"""
Spotify Module 16 — Persona Radar Chart

Expected input:
- persona_radar_profile.csv

Required columns:
- persona
- one or more normalized numerical dimensions
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


OUTPUT_DIR = Path(
    "visualization_outputs"
)

OUTPUT_DIR.mkdir(exist_ok=True)


if __name__ == "__main__":
    profile = pd.read_csv(
        "persona_radar_profile.csv"
    )

    if "persona" not in profile.columns:
        raise ValueError(
            "The profile must contain persona"
        )

    dimensions = [
        column
        for column in profile.columns
        if column != "persona"
    ]

    if len(dimensions) < 3:
        raise ValueError(
            "Radar chart requires at least "
            "three dimensions"
        )

    if not profile[
        dimensions
    ].apply(
        lambda series: series.between(
            0,
            1,
        ).all()
    ).all():
        raise ValueError(
            "Radar dimensions must be "
            "normalized between 0 and 1"
        )

    angles = np.linspace(
        0,
        2 * np.pi,
        len(dimensions),
        endpoint=False,
    ).tolist()

    angles += angles[:1]

    plt.figure(figsize=(9, 8))
    ax = plt.subplot(
        111,
        polar=True,
    )

    for _, row in profile.iterrows():
        values = row[
            dimensions
        ].to_list()

        values += values[:1]

        ax.plot(
            angles,
            values,
            linewidth=2,
            label=row["persona"],
        )

        ax.fill(
            angles,
            values,
            alpha=0.08,
        )

    ax.set_xticks(
        angles[:-1]
    )
    ax.set_xticklabels(
        dimensions
    )
    ax.set_ylim(0, 1)
    ax.set_title(
        "Persona Radar Chart"
    )
    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.35, 1.12),
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR
        / "persona_radar_chart.png",
        dpi=175,
    )

    plt.close()

    print(
        "Radar chart saved."
    )

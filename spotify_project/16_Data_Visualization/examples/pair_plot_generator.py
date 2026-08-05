"""
Spotify Module 16 — Pair Plot Generator

Uses Pandas scatter_matrix for a selected sample.

Expected input:
- spotify_visualization_data.csv
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import scatter_matrix


OUTPUT_DIR = Path(
    "visualization_outputs"
)

OUTPUT_DIR.mkdir(exist_ok=True)


if __name__ == "__main__":
    data = pd.read_csv(
        "spotify_visualization_data.csv"
    )

    features = [
        "daily_listening_minutes",
        "sessions_per_day",
        "skip_rate",
        "repeat_track_rate",
    ]

    missing = set(features) - set(
        data.columns
    )

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    sample = (
        data[features]
        .sample(
            min(1000, len(data)),
            random_state=42,
        )
    )

    scatter_matrix(
        sample,
        figsize=(12, 12),
        diagonal="hist",
        alpha=0.35,
    )

    plt.suptitle(
        "Spotify Behavioral Pair Plot"
    )

    plt.savefig(
        OUTPUT_DIR
        / "behavior_pair_plot.png",
        dpi=175,
        bbox_inches="tight",
    )

    plt.close()

    print(
        "Pair plot saved."
    )

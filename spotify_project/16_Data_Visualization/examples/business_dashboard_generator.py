"""
Spotify Module 16 — Static Business Dashboard Generator

Creates a single static dashboard-style figure using one
Matplotlib canvas.

Expected input:
- spotify_visualization_data.csv
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import pandas as pd


OUTPUT_DIR = Path(
    "visualization_outputs"
)

OUTPUT_DIR.mkdir(exist_ok=True)


def add_box(
    ax,
    x: float,
    y: float,
    width: float,
    height: float,
    text: str,
) -> None:
    """Draw one dashboard box."""
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.02",
        fill=False,
        linewidth=2,
    )

    ax.add_patch(patch)

    ax.text(
        x + width / 2,
        y + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=11,
    )


if __name__ == "__main__":
    data = pd.read_csv(
        "spotify_visualization_data.csv"
    )

    summary = (
        data["persona"]
        .value_counts()
        .sort_values(
            ascending=False
        )
    )

    plt.figure(figsize=(14, 8))
    ax = plt.gca()
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    ax.text(
        7,
        7.45,
        "Spotify Persona KPI Dashboard",
        ha="center",
        fontsize=18,
    )

    kpis = [
        (
            "Users",
            f"{len(data):,}",
        ),
        (
            "Premium Rate",
            f"{data['premium_flag'].mean():.1%}",
        ),
        (
            "Avg Listening",
            (
                f"{data['daily_listening_minutes'].mean():.1f} min"
            ),
        ),
        (
            "Revenue",
            (
                f"{data['monthly_revenue'].sum():,.0f}"
            ),
        ),
    ]

    positions = [
        0.4,
        3.8,
        7.2,
        10.6,
    ]

    for x0, (name, value) in zip(
        positions,
        kpis,
    ):
        add_box(
            ax,
            x0,
            6.0,
            3.0,
            0.9,
            f"{name}\n{value}",
        )

    max_users = summary.max()

    for index, (
        persona,
        users,
    ) in enumerate(
        summary.items()
    ):
        y0 = 4.9 - index * 0.75

        ax.text(
            0.6,
            y0 + 0.15,
            persona,
            fontsize=10,
            va="center",
        )

        width = (
            4.0
            * users
            / max_users
        )

        ax.add_patch(
            Rectangle(
                (3.0, y0),
                width,
                0.3,
                fill=False,
                linewidth=1.5,
            )
        )

        ax.text(
            7.3,
            y0 + 0.15,
            f"{int(users):,}",
            fontsize=10,
            va="center",
        )

    add_box(
        ax,
        8.1,
        2.8,
        5.2,
        2.5,
        (
            "Business Questions\n\n"
            "Which persona is growing?\n"
            "Which has Premium potential?\n"
            "Which requires retention action?\n"
            "Which strategy has incremental lift?"
        ),
    )

    add_box(
        ax,
        0.6,
        0.65,
        12.7,
        1.1,
        (
            "Every KPI should link to "
            "a question, owner and action"
        ),
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR
        / "persona_kpi_dashboard.png",
        dpi=175,
    )

    plt.close()

    print(
        "Dashboard saved."
    )

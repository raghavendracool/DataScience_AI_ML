"""
Module 17 — Architecture Diagram Generator

Creates simple technical and business architecture diagrams
using Matplotlib.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


OUTPUT_DIR = Path(
    "architecture_images"
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
    """Draw one rounded box."""
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
        fontsize=10,
    )


def add_arrow(
    ax,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
) -> None:
    """Draw one arrow."""
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops={
            "arrowstyle": "->",
            "linewidth": 2,
        },
    )


def create_technical_architecture() -> None:
    """Create technical architecture diagram."""
    plt.figure(figsize=(14, 6))
    ax = plt.gca()
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis("off")

    boxes = [
        (0.4, "Data"),
        (2.5, "Validation"),
        (4.6, "Features"),
        (6.7, "Preprocessing"),
        (8.8, "Models"),
        (10.9, "Evaluation"),
        (12.4, "Profiles"),
    ]

    for x0, label in boxes:
        add_box(
            ax,
            x0,
            3.1,
            1.4,
            0.9,
            label,
        )

    for index in range(
        len(boxes) - 1
    ):
        add_arrow(
            ax,
            boxes[index][0] + 1.4,
            3.55,
            boxes[index + 1][0],
            3.55,
        )

    add_box(
        ax,
        2.3,
        1.1,
        2.8,
        0.9,
        "Artifacts and Config",
    )

    add_box(
        ax,
        5.7,
        1.1,
        2.8,
        0.9,
        "Results and Logs",
    )

    add_box(
        ax,
        9.1,
        1.1,
        2.8,
        0.9,
        "Business Outputs",
    )

    plt.title(
        "Technical Architecture"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR
        / "technical_architecture.png",
        dpi=175,
    )

    plt.close()


def create_business_architecture() -> None:
    """Create business architecture diagram."""
    plt.figure(figsize=(14, 6))
    ax = plt.gca()
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis("off")

    boxes = [
        (0.4, "Users"),
        (2.5, "Behavior"),
        (4.6, "Segments"),
        (6.7, "Personas"),
        (8.8, "Actions"),
        (10.9, "KPIs"),
        (12.4, "Learning"),
    ]

    for x0, label in boxes:
        add_box(
            ax,
            x0,
            3.1,
            1.4,
            0.9,
            label,
        )

    for index in range(
        len(boxes) - 1
    ):
        add_arrow(
            ax,
            boxes[index][0] + 1.4,
            3.55,
            boxes[index + 1][0],
            3.55,
        )

    plt.title(
        "Business Architecture"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR
        / "business_architecture.png",
        dpi=175,
    )

    plt.close()


if __name__ == "__main__":
    create_technical_architecture()
    create_business_architecture()

    print(
        f"Architecture images saved to: "
        f"{OUTPUT_DIR.resolve()}"
    )

"""
Spotify Module 16 — Visualization Pipeline

Creates:
- Histogram
- Box plot
- Bar chart
- Scatter plot
- Correlation heatmap
- Persona comparison chart

Expected input:
- spotify_visualization_data.csv
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


OUTPUT_DIR = Path("visualization_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

PERSONA_ORDER = [
    "Casual Snackers",
    "Exploratory Samplers",
    "Habitual Loyalists",
    "Power Streamers",
]


def validate_data(
    data: pd.DataFrame,
) -> None:
    """Validate required visualization columns."""
    required = {
        "user_id",
        "persona",
        "daily_listening_minutes",
        "sessions_per_day",
        "skip_rate",
        "repeat_track_rate",
        "days_active_last_30",
        "premium_flag",
        "monthly_revenue",
    }

    missing = required - set(data.columns)

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )


def save_histogram(
    data: pd.DataFrame,
) -> None:
    """Save listening-minute histogram."""
    plt.figure(figsize=(10, 6))
    plt.hist(
        data["daily_listening_minutes"],
        bins=30,
        edgecolor="black",
        alpha=0.75,
    )
    plt.title(
        "Distribution of Daily Listening Minutes"
    )
    plt.xlabel(
        "Daily Listening Minutes"
    )
    plt.ylabel("Users")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR
        / "histogram_listening_minutes.png",
        dpi=175,
    )
    plt.close()


def save_boxplot(
    data: pd.DataFrame,
) -> None:
    """Save skip-rate box plot by persona."""
    box_data = [
        data.loc[
            data["persona"] == persona,
            "skip_rate",
        ]
        for persona in PERSONA_ORDER
    ]

    plt.figure(figsize=(12, 6))
    plt.boxplot(
        box_data,
        labels=PERSONA_ORDER,
    )
    plt.title(
        "Skip Rate Distribution by Persona"
    )
    plt.xlabel("Persona")
    plt.ylabel("Skip Rate")
    plt.xticks(rotation=12)
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR
        / "boxplot_skip_rate.png",
        dpi=175,
    )
    plt.close()


def save_persona_bar_chart(
    data: pd.DataFrame,
) -> None:
    """Save persona-size bar chart."""
    counts = (
        data["persona"]
        .value_counts()
        .reindex(PERSONA_ORDER)
    )

    plt.figure(figsize=(10, 6))
    plt.bar(
        counts.index,
        counts.values,
    )
    plt.title("Users by Persona")
    plt.xlabel("Persona")
    plt.ylabel("Users")
    plt.xticks(rotation=12)
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR
        / "bar_chart_persona_sizes.png",
        dpi=175,
    )
    plt.close()


def save_scatter_plot(
    data: pd.DataFrame,
) -> None:
    """Save sessions-vs-listening scatter plot."""
    plt.figure(figsize=(10, 6))

    for persona in PERSONA_ORDER:
        subset = data[
            data["persona"] == persona
        ]

        plt.scatter(
            subset["sessions_per_day"],
            subset[
                "daily_listening_minutes"
            ],
            s=18,
            alpha=0.45,
            label=persona,
        )

    plt.title(
        "Sessions per Day vs Listening Minutes"
    )
    plt.xlabel("Sessions per Day")
    plt.ylabel(
        "Daily Listening Minutes"
    )
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR
        / "scatter_sessions_vs_listening.png",
        dpi=175,
    )
    plt.close()


def save_correlation_heatmap(
    data: pd.DataFrame,
) -> None:
    """Save numerical correlation heatmap."""
    features = [
        "daily_listening_minutes",
        "sessions_per_day",
        "days_active_last_30",
        "skip_rate",
        "repeat_track_rate",
        "monthly_revenue",
    ]

    correlation = data[
        features
    ].corr()

    plt.figure(figsize=(10, 8))
    plt.imshow(
        correlation.values,
        aspect="auto",
        vmin=-1,
        vmax=1,
    )
    plt.colorbar(
        label="Correlation"
    )

    plt.xticks(
        range(len(features)),
        [
            value.replace(
                "_",
                "\n",
            )
            for value in features
        ],
        fontsize=8,
    )

    plt.yticks(
        range(len(features)),
        [
            value.replace(
                "_",
                "\n",
            )
            for value in features
        ],
        fontsize=8,
    )

    for row in range(
        correlation.shape[0]
    ):
        for col in range(
            correlation.shape[1]
        ):
            plt.text(
                col,
                row,
                f"{correlation.iloc[row, col]:.2f}",
                ha="center",
                va="center",
                fontsize=8,
            )

    plt.title(
        "Feature Correlation Heatmap"
    )
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR
        / "correlation_heatmap.png",
        dpi=175,
    )
    plt.close()


def save_persona_comparison(
    data: pd.DataFrame,
) -> None:
    """Save normalized persona comparison."""
    summary = (
        data.groupby("persona")
        .agg(
            listening=(
                "daily_listening_minutes",
                "mean",
            ),
            active_days=(
                "days_active_last_30",
                "mean",
            ),
            repeat_rate=(
                "repeat_track_rate",
                "mean",
            ),
            premium_rate=(
                "premium_flag",
                "mean",
            ),
        )
        .reindex(PERSONA_ORDER)
    )

    normalized = (
        summary
        - summary.min()
    ) / (
        summary.max()
        - summary.min()
    )

    x = np.arange(
        len(normalized)
    )

    width = 0.20

    plt.figure(figsize=(12, 6))

    for index, column in enumerate(
        normalized.columns
    ):
        plt.bar(
            x
            + (
                index - 1.5
            )
            * width,
            normalized[column],
            width,
            label=column,
        )

    plt.title(
        "Normalized Persona Comparison"
    )
    plt.xlabel("Persona")
    plt.ylabel("Relative Level")
    plt.xticks(
        x,
        normalized.index,
        rotation=12,
    )
    plt.ylim(0, 1.05)
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR
        / "persona_comparison.png",
        dpi=175,
    )
    plt.close()


if __name__ == "__main__":
    spotify = pd.read_csv(
        "spotify_visualization_data.csv"
    )

    validate_data(spotify)

    save_histogram(spotify)
    save_boxplot(spotify)
    save_persona_bar_chart(spotify)
    save_scatter_plot(spotify)
    save_correlation_heatmap(spotify)
    save_persona_comparison(spotify)

    print(
        f"Visualizations saved to: "
        f"{OUTPUT_DIR.resolve()}"
    )

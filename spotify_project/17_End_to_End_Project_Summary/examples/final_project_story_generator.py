"""
Module 17 — Final Project Story Generator
"""

from __future__ import annotations

from pathlib import Path


OUTPUT_DIR = Path(
    "final_project_outputs"
)

OUTPUT_DIR.mkdir(exist_ok=True)


SHORT_STORY = """# 30-Second Project Explanation

I built an end-to-end Spotify user-segmentation project using
behavioral and demographic data. I compared scaling methods,
automated K-Means and GMM experiments, evaluated them using
technical metrics, stability and business interpretation, and
selected an illustrative four-cluster K-Means solution. I translated
the clusters into Casual Snackers, Exploratory Samplers, Habitual
Loyalists and Power Streamers, then created persona-specific growth
recommendations with measurable primary and guardrail KPIs.
"""


DETAILED_STORY = """# Detailed Project Explanation

## Problem

Users behave differently, so one recommendation and growth strategy
is not suitable for everyone.

## Data

The project uses behavioral data and demographic context.

## Preparation

The workflow validates missing values, duplicates, ranges, identifiers,
feature relevance, scaling and transformations.

## Modeling

K-Means and Gaussian Mixture Models are compared through automated
experiments.

## Evaluation

The project uses Silhouette, Davies-Bouldin, Calinski-Harabasz,
inertia, AIC, BIC, cluster sizes, stability and business meaning.

## Illustrative Final Selection

StandardScaler plus K-Means with four clusters.

## Personas

- Casual Snackers
- Exploratory Samplers
- Habitual Loyalists
- Power Streamers

## Business Value

Persona-specific recommendation, retention, discovery, loyalty and
Premium-conversion hypotheses.

## Next Step

Deploy, monitor drift and test recommendations through controlled
experiments.
"""


if __name__ == "__main__":
    (
        OUTPUT_DIR
        / "project_explanation_30_seconds.md"
    ).write_text(
        SHORT_STORY,
        encoding="utf-8",
    )

    (
        OUTPUT_DIR
        / "project_explanation_detailed.md"
    ).write_text(
        DETAILED_STORY,
        encoding="utf-8",
    )

    print(
        f"Project stories saved to: "
        f"{OUTPUT_DIR.resolve()}"
    )

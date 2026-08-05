"""
Spotify Module 15 — Persona Growth Strategy

Creates a business strategy register from a reviewed persona mapping.

Expected input:
- reviewed_persona_mapping.csv

Required columns:
- cluster
- persona_name
- user_count
- user_percentage
- behavior_summary
- primary_need
- primary_risk
- primary_opportunity
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path(
    "growth_strategy_outputs"
)

OUTPUT_DIR.mkdir(exist_ok=True)


STRATEGY_LIBRARY = {
    "Casual Snackers": {
        "recommendation_strategy": (
            "Short, familiar playlists and "
            "simple re-entry recommendations"
        ),
        "premium_strategy": (
            "Prioritize engagement before "
            "aggressive conversion"
        ),
        "retention_strategy": (
            "Reactivation, habit building and "
            "carefully timed reminders"
        ),
        "advertisement_strategy": (
            "Limit ad pressure during short sessions"
        ),
        "playlist_strategy": (
            "Quick-start and short familiar mixes"
        ),
    },
    "Exploratory Samplers": {
        "recommendation_strategy": (
            "High-variety discovery and "
            "cross-genre recommendations"
        ),
        "premium_strategy": (
            "Test discovery-led Premium trials"
        ),
        "retention_strategy": (
            "Protect discovery quality and freshness"
        ),
        "advertisement_strategy": (
            "Use contextually relevant discovery ads"
        ),
        "playlist_strategy": (
            "Fresh finds, new releases and genre journeys"
        ),
    },
    "Habitual Loyalists": {
        "recommendation_strategy": (
            "Repeat mixes, artist updates and continuity"
        ),
        "premium_strategy": (
            "Emphasize continuity and offline access"
        ),
        "retention_strategy": (
            "Loyalty recognition and reliable experiences"
        ),
        "advertisement_strategy": (
            "Avoid repetitive advertisements"
        ),
        "playlist_strategy": (
            "Artist-based and saved-content refresh"
        ),
    },
    "Power Streamers": {
        "recommendation_strategy": (
            "Deep personalization and long-session mixes"
        ),
        "premium_strategy": (
            "Emphasize ad-free and uninterrupted listening"
        ),
        "retention_strategy": (
            "Protect quality and avoid excessive messaging"
        ),
        "advertisement_strategy": (
            "Review ad friction and Premium opportunities"
        ),
        "playlist_strategy": (
            "Long-form, focus and advanced personalized mixes"
        ),
    },
}


def create_strategy_register(
    personas: pd.DataFrame,
) -> pd.DataFrame:
    """Attach draft strategies to reviewed personas."""
    required = {
        "persona_name",
        "primary_need",
        "primary_risk",
        "primary_opportunity",
    }

    missing = required - set(
        personas.columns
    )

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    rows = []

    for _, row in personas.iterrows():
        name = row["persona_name"]

        if name not in STRATEGY_LIBRARY:
            raise ValueError(
                f"No strategy draft exists for {name}"
            )

        strategy = STRATEGY_LIBRARY[name]

        rows.append({
            "persona_name": name,
            "primary_need": row["primary_need"],
            "primary_risk": row["primary_risk"],
            "primary_opportunity": (
                row["primary_opportunity"]
            ),
            **strategy,
            "primary_kpi": "",
            "guardrail_kpis": "",
            "owner": "",
            "status": "DRAFT",
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    personas = pd.read_csv(
        "reviewed_persona_mapping.csv"
    )

    strategy_register = (
        create_strategy_register(
            personas
        )
    )

    strategy_register.to_csv(
        OUTPUT_DIR
        / "persona_growth_strategy_register.csv",
        index=False,
    )

    print(
        strategy_register.to_string(
            index=False
        )
    )

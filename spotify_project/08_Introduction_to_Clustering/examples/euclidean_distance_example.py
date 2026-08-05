"""
Spotify Module 08 — Euclidean Distance Example
"""

from __future__ import annotations

import numpy as np
import pandas as pd


FEATURES = [
    "daily_listening_minutes_scaled",
    "sessions_per_day_scaled",
    "days_active_last_30_scaled",
    "skip_rate_scaled",
]


def euclidean_distance(
    user_a: np.ndarray,
    user_b: np.ndarray,
) -> float:
    """Calculate straight-line distance."""
    return float(
        np.sqrt(
            np.sum(
                (user_a - user_b) ** 2
            )
        )
    )


if __name__ == "__main__":
    users = pd.DataFrame(
        {
            "user_id": [
                "User A",
                "User B",
                "User C",
            ],
            "daily_listening_minutes_scaled": [
                1.20,
                1.05,
                -1.10,
            ],
            "sessions_per_day_scaled": [
                0.90,
                1.10,
                -0.85,
            ],
            "days_active_last_30_scaled": [
                1.25,
                1.15,
                -1.20,
            ],
            "skip_rate_scaled": [
                -0.75,
                -0.62,
                1.10,
            ],
        }
    ).set_index("user_id")

    user_a = users.loc["User A", FEATURES].to_numpy()
    user_b = users.loc["User B", FEATURES].to_numpy()
    user_c = users.loc["User C", FEATURES].to_numpy()

    distance_ab = euclidean_distance(
        user_a,
        user_b,
    )

    distance_ac = euclidean_distance(
        user_a,
        user_c,
    )

    print(
        "Distance between User A and User B:",
        round(distance_ab, 4),
    )

    print(
        "Distance between User A and User C:",
        round(distance_ac, 4),
    )

    print(
        "\nInterpretation:",
        "A and B are more similar."
        if distance_ab < distance_ac
        else "A and C are more similar.",
    )

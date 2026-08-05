"""
Spotify Module 11 — Save a Selected Experiment

This script demonstrates fitting and saving only the selected
pipeline after experiment comparison.
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd

from experiment_factories import (
    build_kmeans,
    build_preprocessor,
)


ARTIFACT_DIR = Path(
    "experiment_outputs/"
    "selected_experiment"
)

ARTIFACT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

SELECTED_CONFIG = {
    "experiment_id": (
        "EXP_CORE_STANDARD_KMEANS_K4"
    ),
    "feature_set_name": "core",
    "features": [
        "daily_listening_minutes",
        "sessions_per_day",
        "avg_session_minutes",
        "days_active_last_30",
        "skip_rate",
        "ads_skipped_pct",
    ],
    "preprocessor_name": "standard",
    "algorithm": "KMeans",
    "n_clusters": 4,
    "random_state": 42,
}


if __name__ == "__main__":
    behavior = pd.read_excel(
        "spotify_user_behavior.xlsx"
    )

    features = SELECTED_CONFIG[
        "features"
    ]

    X = behavior[
        features
    ].copy()

    preprocessor = build_preprocessor(
        name=SELECTED_CONFIG[
            "preprocessor_name"
        ],
        row_count=len(X),
        random_state=SELECTED_CONFIG[
            "random_state"
        ],
    )

    X_transformed = (
        preprocessor.fit_transform(X)
    )

    model = build_kmeans(
        k=SELECTED_CONFIG[
            "n_clusters"
        ],
        random_state=SELECTED_CONFIG[
            "random_state"
        ],
    )

    labels = model.fit_predict(
        X_transformed
    )

    user_clusters = behavior[
        ["user_id"]
    ].copy()

    user_clusters[
        "cluster"
    ] = labels

    joblib.dump(
        preprocessor,
        ARTIFACT_DIR
        / "preprocessor.joblib",
    )

    joblib.dump(
        model,
        ARTIFACT_DIR
        / "model.joblib",
    )

    joblib.dump(
        features,
        ARTIFACT_DIR
        / "feature_order.joblib",
    )

    with (
        ARTIFACT_DIR
        / "configuration.json"
    ).open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            SELECTED_CONFIG,
            file,
            indent=2,
        )

    user_clusters.to_csv(
        ARTIFACT_DIR
        / "spotify_user_clusters.csv",
        index=False,
    )

    print(
        "Selected experiment artifacts "
        f"saved to: {ARTIFACT_DIR.resolve()}"
    )

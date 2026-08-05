"""
Module 11 — Experiment Configuration

Central configuration for Spotify clustering experiments.
"""

from __future__ import annotations

FEATURE_SETS = {
    "core": [
        "daily_listening_minutes",
        "sessions_per_day",
        "avg_session_minutes",
        "days_active_last_30",
        "skip_rate",
        "ads_skipped_pct",
    ],
    "expanded": [
        "daily_listening_minutes",
        "sessions_per_day",
        "avg_session_minutes",
        "days_active_last_30",
        "skip_rate",
        "ads_skipped_pct",
        "repeat_track_rate",
        "repeat_artist_rate",
        "liked_songs_pct",
        "genre_diversity_score",
        "mean_track_popularity",
        "pct_top_popularity_tracks",
    ],
}

PREPROCESSOR_NAMES = [
    "standard",
    "minmax",
    "robust",
    "power",
    "quantile_normal",
]

KMEANS_K_VALUES = list(
    range(2, 9)
)

GMM_COMPONENT_VALUES = list(
    range(2, 9)
)

GMM_COVARIANCE_TYPES = [
    "full",
    "tied",
    "diag",
    "spherical",
]

RANDOM_STATE = 42

SILHOUETTE_SAMPLE_SIZE = 10000

OUTPUT_DIRECTORY = "experiment_outputs"

LOG_FILE = (
    "experiment_outputs/"
    "experiment_log.jsonl"
)

RESULT_FILE = (
    "experiment_outputs/"
    "all_experiment_results.csv"
)

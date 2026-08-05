"""
Spotify Module 04 — Business Validation Rules

Keep business rules separate from execution code so they can
be reviewed and changed without rewriting the entire pipeline.
"""

BEHAVIOR_RANGE_RULES = {
    "daily_listening_minutes": (0, None),
    "sessions_per_day": (0, None),
    "days_active_last_30": (0, 30),
    "avg_session_minutes": (0, None),
    "playlists_followed": (0, None),
    "artists_followed": (0, None),
    "skip_rate": (0, 1),
    "liked_songs_pct": (0, 1),
    "ads_skipped_pct": (0, 1),
    "repeat_track_rate": (0, 1),
    "repeat_artist_rate": (0, 1),
    "mean_danceability": (0, 1),
    "mean_energy": (0, 1),
    "mean_valence": (0, 1),
    "mean_acousticness": (0, 1),
    "mean_speechiness": (0, 1),
    "mean_instrumentalness": (0, 1),
    "mean_track_popularity": (0, 100),
    "pct_top_popularity_tracks": (0, 1),
    "genre_diversity_score": (0, 1),
}

DEMO_RANGE_RULES = {
    "age": (18, 70),
    "city_tier": (1, 3),
    "subscription_tenure_months": (1, 120),
}

DEMO_CATEGORY_RULES = {
    "country": {"US", "IN", "UK", "DE", "BR"},
    "city_tier": {1, 2, 3},
    "device_type": {"Mobile", "Desktop", "Tablet"},
}

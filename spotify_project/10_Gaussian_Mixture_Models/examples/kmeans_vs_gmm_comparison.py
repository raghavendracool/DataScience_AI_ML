"""
Spotify Module 10 — K-Means vs GMM Comparison

Compares:
- Hard K-Means labels
- Hard GMM labels
- GMM probabilities
- Inertia
- Silhouette
- AIC and BIC
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler


FEATURES = [
    "daily_listening_minutes",
    "sessions_per_day",
    "avg_session_minutes",
    "days_active_last_30",
    "skip_rate",
    "ads_skipped_pct",
]


if __name__ == "__main__":
    behavior = pd.read_excel(
        "spotify_user_behavior.xlsx"
    )

    X = behavior[
        FEATURES
    ].copy()

    X_scaled = StandardScaler().fit_transform(
        X
    )

    kmeans = KMeans(
        n_clusters=4,
        n_init=20,
        random_state=42,
    )

    kmeans_labels = kmeans.fit_predict(
        X_scaled
    )

    gmm = GaussianMixture(
        n_components=4,
        covariance_type="full",
        n_init=10,
        max_iter=300,
        tol=1e-4,
        reg_covar=1e-6,
        random_state=42,
    )

    gmm.fit(X_scaled)

    gmm_labels = gmm.predict(
        X_scaled
    )

    gmm_probabilities = (
        gmm.predict_proba(
            X_scaled
        )
    )

    comparison = pd.DataFrame([
        {
            "model": "K-Means",
            "hard_silhouette": (
                silhouette_score(
                    X_scaled,
                    kmeans_labels,
                )
            ),
            "inertia": kmeans.inertia_,
            "aic": np.nan,
            "bic": np.nan,
            "mean_membership_confidence": (
                np.nan
            ),
        },
        {
            "model": "GMM",
            "hard_silhouette": (
                silhouette_score(
                    X_scaled,
                    gmm_labels,
                )
            ),
            "inertia": np.nan,
            "aic": gmm.aic(X_scaled),
            "bic": gmm.bic(X_scaled),
            "mean_membership_confidence": (
                gmm_probabilities
                .max(axis=1)
                .mean()
            ),
        },
    ])

    comparison.to_csv(
        "kmeans_vs_gmm_metrics.csv",
        index=False,
    )

    print(
        comparison.round(4)
        .to_string(index=False)
    )

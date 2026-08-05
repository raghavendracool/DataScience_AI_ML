"""
Spotify Module 11 — Experiment Comparison and Shortlisting

Important comparison rules:
- Inertia is grouped by feature set and preprocessing.
- GMM AIC/BIC are grouped by feature set and preprocessing.
- Silhouette can screen complete pipelines, but business
  interpretation and stability are still required.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path(
    "experiment_outputs"
)


def successful_results(
    results: pd.DataFrame,
) -> pd.DataFrame:
    """Return successful experiments only."""
    return results[
        results["status"]
        == "SUCCESS"
    ].copy()


def kmeans_leaderboard(
    results: pd.DataFrame,
) -> pd.DataFrame:
    """Rank successful K-Means experiments for screening."""
    kmeans = successful_results(
        results
    )

    kmeans = kmeans[
        kmeans["algorithm"]
        == "KMeans"
    ].copy()

    return (
        kmeans
        .sort_values(
            [
                "silhouette_score",
                "davies_bouldin_score",
            ],
            ascending=[
                False,
                True,
            ],
        )
        .reset_index(drop=True)
    )


def gmm_within_space_ranking(
    results: pd.DataFrame,
) -> pd.DataFrame:
    """
    Rank GMM models only within the same feature set
    and preprocessing space.
    """
    gmm = successful_results(
        results
    )

    gmm = gmm[
        gmm["algorithm"]
        == "GMM"
    ].copy()

    gmm["bic_rank_within_space"] = (
        gmm
        .groupby(
            [
                "feature_set_name",
                "preprocessor_name",
            ]
        )["bic"]
        .rank(
            method="dense",
            ascending=True,
        )
    )

    gmm["aic_rank_within_space"] = (
        gmm
        .groupby(
            [
                "feature_set_name",
                "preprocessor_name",
            ]
        )["aic"]
        .rank(
            method="dense",
            ascending=True,
        )
    )

    return (
        gmm
        .sort_values(
            [
                "feature_set_name",
                "preprocessor_name",
                "bic_rank_within_space",
            ]
        )
        .reset_index(drop=True)
    )


def create_shortlist(
    results: pd.DataFrame,
    minimum_cluster_pct: float = 5.0,
    maximum_cluster_pct: float = 60.0,
) -> pd.DataFrame:
    """Create a technical shortlist for business review."""
    success = successful_results(
        results
    )

    shortlist = success[
        (
            success[
                "smallest_cluster_pct"
            ]
            >= minimum_cluster_pct
        )
        & (
            success[
                "largest_cluster_pct"
            ]
            <= maximum_cluster_pct
        )
    ].copy()

    return shortlist.sort_values(
        "silhouette_score",
        ascending=False,
    )


if __name__ == "__main__":
    results = pd.read_csv(
        OUTPUT_DIR
        / "all_experiment_results.csv"
    )

    kmeans = kmeans_leaderboard(
        results
    )

    gmm = gmm_within_space_ranking(
        results
    )

    shortlist = create_shortlist(
        results
    )

    kmeans.to_csv(
        OUTPUT_DIR
        / "kmeans_leaderboard.csv",
        index=False,
    )

    gmm.to_csv(
        OUTPUT_DIR
        / "gmm_within_space_ranking.csv",
        index=False,
    )

    shortlist.to_csv(
        OUTPUT_DIR
        / "technical_shortlist.csv",
        index=False,
    )

    print("\nK-Means Leaderboard")
    print(
        kmeans.head(10)
        [
            [
                "experiment_id",
                "silhouette_score",
                "davies_bouldin_score",
                "smallest_cluster_pct",
                "largest_cluster_pct",
            ]
        ]
        .round(4)
        .to_string(index=False)
    )

    print("\nGMM Best Within Each Space")
    print(
        gmm[
            gmm[
                "bic_rank_within_space"
            ] == 1
        ]
        [
            [
                "experiment_id",
                "feature_set_name",
                "preprocessor_name",
                "bic",
                "silhouette_score",
                "mean_membership_confidence",
            ]
        ]
        .round(4)
        .to_string(index=False)
    )

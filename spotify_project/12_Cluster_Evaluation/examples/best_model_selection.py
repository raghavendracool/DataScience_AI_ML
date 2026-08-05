"""
Spotify Module 12 — Best Model Selection Framework

This script:
- Loads experiment results
- Removes failed runs
- Applies technical filters
- Separates K-Means and GMM
- Ranks K-Means broadly by hard-label metrics
- Ranks GMM by BIC only within compatible feature spaces
- Creates a business-review shortlist
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path(
    "best_model_selection_outputs"
)

OUTPUT_DIR.mkdir(exist_ok=True)


def filter_successful(
    results: pd.DataFrame,
) -> pd.DataFrame:
    """Keep valid completed experiments."""
    if "status" in results.columns:
        return results[
            results["status"]
            == "SUCCESS"
        ].copy()

    return results.copy()


def technical_shortlist(
    results: pd.DataFrame,
    minimum_cluster_pct: float = 5.0,
    maximum_cluster_pct: float = 60.0,
) -> pd.DataFrame:
    """Apply general cluster-structure filters."""
    success = filter_successful(
        results
    )

    return success[
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


def rank_kmeans(
    shortlist: pd.DataFrame,
) -> pd.DataFrame:
    """Create a K-Means screening leaderboard."""
    kmeans = shortlist[
        shortlist["algorithm"]
        == "KMeans"
    ].copy()

    return (
        kmeans
        .sort_values(
            [
                "silhouette_score",
                "davies_bouldin_index",
                "calinski_harabasz_score",
            ],
            ascending=[
                False,
                True,
                False,
            ],
        )
        .reset_index(drop=True)
    )


def rank_gmm_within_space(
    shortlist: pd.DataFrame,
) -> pd.DataFrame:
    """
    Rank GMM BIC only within the same
    feature and preprocessing space.
    """
    gmm = shortlist[
        shortlist["algorithm"]
        == "GMM"
    ].copy()

    required_group_columns = [
        "feature_set_name",
        "preprocessor_name",
    ]

    for column in required_group_columns:
        if column not in gmm.columns:
            gmm[column] = "single_space"

    gmm["bic_rank_within_space"] = (
        gmm
        .groupby(
            required_group_columns
        )["bic"]
        .rank(
            method="dense",
            ascending=True,
        )
    )

    return (
        gmm
        .sort_values(
            required_group_columns
            + ["bic_rank_within_space"]
        )
        .reset_index(drop=True)
    )


if __name__ == "__main__":
    results = pd.read_csv(
        "all_experiment_results.csv"
    )

    shortlist = technical_shortlist(
        results
    )

    kmeans_ranking = rank_kmeans(
        shortlist
    )

    gmm_ranking = rank_gmm_within_space(
        shortlist
    )

    shortlist.to_csv(
        OUTPUT_DIR
        / "technical_shortlist.csv",
        index=False,
    )

    kmeans_ranking.to_csv(
        OUTPUT_DIR
        / "kmeans_ranking.csv",
        index=False,
    )

    gmm_ranking.to_csv(
        OUTPUT_DIR
        / "gmm_within_space_ranking.csv",
        index=False,
    )

    print(
        "\nThe next step is business review."
    )

    print(
        "Do not select the final model "
        "from this ranking alone."
    )

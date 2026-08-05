"""
Spotify Module 15 — CLV and Revenue Scenarios

This uses a simplified illustrative CLV formula.

The script is for teaching and scenario comparison.
It is not a financial valuation model.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path(
    "clv_revenue_outputs"
)

OUTPUT_DIR.mkdir(exist_ok=True)


def calculate_simplified_clv(
    monthly_revenue: float,
    gross_margin_rate: float,
    monthly_retention_rate: float,
    monthly_discount_rate: float,
) -> float:
    """
    Calculate simplified contribution-margin CLV.

    CLV =
    monthly revenue * gross margin
    / (1 + discount rate - retention rate)
    """
    denominator = (
        1
        + monthly_discount_rate
        - monthly_retention_rate
    )

    if denominator <= 0:
        raise ValueError(
            "CLV denominator must be positive"
        )

    return (
        monthly_revenue
        * gross_margin_rate
        / denominator
    )


def calculate_scenarios(
    scenarios: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate CLV for every scenario."""
    required = {
        "scenario",
        "average_monthly_revenue_per_user",
        "monthly_retention_rate",
        "gross_margin_rate",
        "discount_rate_monthly",
    }

    missing = required - set(
        scenarios.columns
    )

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    output = scenarios.copy()

    output["illustrative_clv"] = (
        output.apply(
            lambda row: calculate_simplified_clv(
                monthly_revenue=row[
                    "average_monthly_revenue_per_user"
                ],
                gross_margin_rate=row[
                    "gross_margin_rate"
                ],
                monthly_retention_rate=row[
                    "monthly_retention_rate"
                ],
                monthly_discount_rate=row[
                    "discount_rate_monthly"
                ],
            ),
            axis=1,
        )
    )

    baseline = output.loc[
        output["scenario"] == "Current State",
        "illustrative_clv",
    ]

    if baseline.empty:
        output["clv_lift_vs_current"] = (
            float("nan")
        )
    else:
        baseline_value = baseline.iloc[0]
        output["clv_lift_vs_current"] = (
            output["illustrative_clv"]
            - baseline_value
        )

    return output


if __name__ == "__main__":
    scenarios = pd.read_csv(
        "clv_scenarios.csv"
    )

    results = calculate_scenarios(
        scenarios
    )

    results.to_csv(
        OUTPUT_DIR
        / "clv_scenario_results.csv",
        index=False,
    )

    print(
        results.round(4)
        .to_string(index=False)
    )

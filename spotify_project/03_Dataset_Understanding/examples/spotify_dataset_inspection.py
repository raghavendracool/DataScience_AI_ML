"""
Spotify Module 03 — Dataset Inspection Example
"""

import pandas as pd


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load the two user-level Spotify Excel datasets."""
    behavior = pd.read_excel("spotify_user_behavior.xlsx")
    demo = pd.read_excel("spotify_user_demo.xlsx")
    return behavior, demo


def inspect_dataset(name: str, df: pd.DataFrame) -> None:
    """Print beginner-friendly structural checks."""
    print(f"\n{'=' * 60}")
    print(name)
    print(f"{'=' * 60}")

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nPreview:")
    print(df.head())


def validate_user_key(
    behavior: pd.DataFrame,
    demo: pd.DataFrame
) -> None:
    """Validate uniqueness and overlap of user_id."""
    for name, df in [
        ("Behavior", behavior),
        ("Demo", demo),
    ]:
        if "user_id" not in df.columns:
            raise KeyError(f"user_id missing from {name} dataset")

        print(
            f"{name} unique users:",
            df["user_id"].nunique()
        )

        print(
            f"{name} duplicate user IDs:",
            df["user_id"].duplicated().sum()
        )

    behavior_users = set(behavior["user_id"])
    demo_users = set(demo["user_id"])

    print(
        "Behavior users missing from demo:",
        len(behavior_users - demo_users)
    )

    print(
        "Demo users missing from behavior:",
        len(demo_users - behavior_users)
    )


def join_datasets(
    behavior: pd.DataFrame,
    demo: pd.DataFrame
) -> pd.DataFrame:
    """Perform a safe one-to-one join."""
    joined = behavior.merge(
        demo,
        how="inner",
        on="user_id",
        validate="one_to_one"
    )

    print("\nJoined shape:", joined.shape)
    print(
        "Joined unique users:",
        joined["user_id"].nunique()
    )

    return joined


def main() -> None:
    behavior, demo = load_data()

    inspect_dataset(
        "spotify_user_behavior",
        behavior
    )

    inspect_dataset(
        "spotify_user_demo",
        demo
    )

    validate_user_key(behavior, demo)

    joined = join_datasets(behavior, demo)

    print("\nJoined preview:")
    print(joined.head())


if __name__ == "__main__":
    main()

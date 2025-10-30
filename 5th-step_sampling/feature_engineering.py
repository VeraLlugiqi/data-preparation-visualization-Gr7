#!/usr/bin/env python3
"""
Step 5 feature engineering script.
- Loads the full cleaned dataset via sampling.get_datasets()
- Adds derived indices, trends, discretizations, and binary flags
- Output: university_data_engineered.csv
"""

from pathlib import Path
import pandas as pd
import numpy as np

import sampling

BASE_DIR = Path(__file__).resolve().parent
FULL_OUTPUT = BASE_DIR / "university_data_engineered.csv"


def compute_rank_consistency(df: pd.DataFrame) -> pd.Series:
    """Return standard deviation of world_rank per university."""
    return df.groupby("university_name")["world_rank"].transform("std")


def compute_research_index(df: pd.DataFrame) -> pd.Series:
    return df[["research", "citations"]].mean(axis=1)


def compute_teaching_index(df: pd.DataFrame) -> pd.Series:
    return df[["teaching", "international"]].mean(axis=1)


def compute_rank_change(df: pd.DataFrame) -> pd.Series:
    """Year-over-year world rank change within each university."""
    return (
        df.sort_values(["university_name", "year"])
        .groupby("university_name")["world_rank"]
        .diff()
        .fillna(0)
    )


def map_trajectory(rank_change: float) -> str:
    if rank_change <= -10:
        return "rising"
    if rank_change >= 10:
        return "declining"
    return "stable"


COUNTRY_TO_REGION = {
    "USA": "North America",
    "United States of America": "North America",
    "Canada": "North America",
    "UK": "Europe",
    "United Kingdom": "Europe",
    "Germany": "Europe",
    "France": "Europe",
    "China": "Asia",
    "Japan": "Asia",
    "Australia": "Oceania",
}


def map_region(country: str) -> str:
    return COUNTRY_TO_REGION.get(country, "Other")


def diversity_index(row: pd.Series) -> float:
    """Combine international student share and inverted student-staff ratio."""
    int_share = row["international_students"]

    min_ratio, max_ratio = 4, 35  # coarse bounds based on dataset exploration
    ratio = row["student_staff_ratio"]
    if pd.isna(ratio):
        inv_ratio = np.nan
    else:
        inv_ratio = 1 - ((ratio - min_ratio) / (max_ratio - min_ratio))
        inv_ratio = np.clip(inv_ratio, 0, 1)

    values = [int_share if not pd.isna(int_share) else np.nan,
              inv_ratio if not pd.isna(inv_ratio) else np.nan]
    return np.nanmean(values)


def zscore(series: pd.Series) -> pd.Series:
    mean = series.mean()
    std = series.std()
    if std == 0 or pd.isna(std):
        return pd.Series(0, index=series.index)
    return (series - mean) / std


def main():
    print("Loading dataset via sampling.get_datasets() ...")
    full_df, _ = sampling.get_datasets()
    engineered_df = full_df.copy()

    print("Computing derived indices and trends ...")
    rank_std = compute_rank_consistency(engineered_df)
    engineered_df["rank_consistency_std"] = rank_std
    engineered_df["consistency_score"] = 1 / (1 + rank_std.fillna(0))

    engineered_df["research_index"] = compute_research_index(engineered_df)
    engineered_df["teaching_index"] = compute_teaching_index(engineered_df)
    engineered_df["global_index"] = engineered_df[["research_index", "teaching_index"]].mean(axis=1)

    engineered_df["rank_change"] = compute_rank_change(engineered_df)
    engineered_df["trajectory"] = engineered_df["rank_change"].apply(map_trajectory)
    engineered_df["region"] = engineered_df["country"].apply(map_region)
    engineered_df["diversity_index"] = engineered_df.apply(diversity_index, axis=1)

    print("Applying standardization, discretization, and flags ...")
    engineered_df["research_index_z"] = zscore(engineered_df["research_index"])
    engineered_df["teaching_index_z"] = zscore(engineered_df["teaching_index"])

    engineered_df["rank_tier"] = pd.cut(
        engineered_df["world_rank"],
        bins=[0, 100, 200, 500, np.inf],
        labels=["Top 100", "101–200", "201–500", "501+"],
        right=True,
    )

    engineered_df["performance_category"] = pd.cut(
        engineered_df["teaching_index"],
        bins=[-np.inf, 40, 60, np.inf],
        labels=["Low", "Medium", "High"],
        include_lowest=True,
    )

    quantiles = engineered_df["num_students"].quantile([0.33, 0.66]).values
    # Protect against identical quantiles (e.g., when data is constant)
    if np.isclose(quantiles[0], quantiles[1]):
        quantiles[1] = quantiles[0] + 1
    engineered_df["size_category"] = pd.cut(
        engineered_df["num_students"],
        bins=[-np.inf, quantiles[0], quantiles[1], np.inf],
        labels=["Small", "Medium", "Large"],
    )

    engineered_df["is_top_100"] = engineered_df["world_rank"] <= 100
    engineered_df["is_research_intensive"] = engineered_df["research_index"] >= 70
    engineered_df["is_rising"] = engineered_df["trajectory"] == "rising"

    engineered_columns = [
        "rank_consistency_std",
        "consistency_score",
        "research_index",
        "teaching_index",
        "global_index",
        "rank_change",
        "trajectory",
        "region",
        "diversity_index",
        "research_index_z",
        "teaching_index_z",
        "rank_tier",
        "performance_category",
        "size_category",
        "is_top_100",
        "is_research_intensive",
        "is_rising",
    ]

    round_to_one_decimal = [
        "rank_consistency_std",
        "consistency_score",
        "research_index",
        "teaching_index",
        "global_index",
        "rank_change",
        "diversity_index",
        "research_index_z",
        "teaching_index_z",
    ]
    for col in round_to_one_decimal:
        if col in engineered_df.columns:
            engineered_df[col] = engineered_df[col].round(1)

    print("Saving engineered dataset ...")
    engineered_df.to_csv(FULL_OUTPUT, index=False)
    print(f"{FULL_OUTPUT.name} saved to {FULL_OUTPUT.parent}/")

    remaining_nans = engineered_df[engineered_columns].isna().sum().sum()
    print(
        f"Feature engineering complete. Rows: {len(engineered_df)}, "
        f"new columns: {len(engineered_columns)}, "
        f"NaNs in engineered columns: {remaining_nans}"
    )


if __name__ == "__main__":
    main()

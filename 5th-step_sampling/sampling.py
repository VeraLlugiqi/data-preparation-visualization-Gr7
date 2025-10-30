#!/usr/bin/env python3
"""
Step 5 sampling script.
- Reads the Step 4 cleaned dataset
- Creates a 20% stratified sample per year (random_state=42)
- Saves sampled_dataset.csv in this folder
- Provides get_datasets() for reuse by other scripts
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR.parent / "4th-step-data_cleaning" / "cleaned_university_data.csv"
OUTPUT_FILE = BASE_DIR / "sampled_dataset.csv"


def get_datasets():
    """Return the full cleaned DataFrame and the year-stratified 20% sample."""
    full_df = pd.read_csv(INPUT_FILE)
    sampled_df = full_df.groupby("year", group_keys=False).sample(frac=0.2, random_state=42)
    return full_df, sampled_df


def main():
    print(f"Loading cleaned data from: {INPUT_FILE}")
    full_df, sampled_df = get_datasets()

    print(f"Full dataset rows: {len(full_df)}")
    print(f"Sampled dataset rows: {len(sampled_df)} (20% per year)")

    sampled_df.to_csv(OUTPUT_FILE, index=False)
    print(f"{OUTPUT_FILE.name} saved to {OUTPUT_FILE.parent}/")


if __name__ == "__main__":
    main()

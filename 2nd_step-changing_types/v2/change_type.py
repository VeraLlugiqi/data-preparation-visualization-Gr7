#!/usr/bin/env python3
"""
Clean merged_university_data.csv WITHOUT renaming or reordering existing columns unnecessarily.
- Keeps original columns and order, except removes 'female_male_ratio'.
- Converts numeric-looking columns to numeric.
- Removes 'female_male_ratio' and adds 'female_male_percent' instead.
- Converts values like '14%' -> 14.0, removes commas, ranges, etc.
- Coerces unparsable values to NaN.
"""

import pandas as pd
import numpy as np
import re

INPUT = "../../1st_step-merging/v2/merged_university_data.csv"
OUTPUT = "merged_university_data_cleaned.csv"

# -------------------------------------------------------
# Helper: extract first numeric value (handles %, commas, ranges)
# -------------------------------------------------------
def extract_first_number(s):
    if pd.isna(s):
        return np.nan
    s = str(s).strip()
    if s == "" or s == "-" or s.lower() == "nan":
        return np.nan
    s_clean = s.replace(',', '')
    if '%' in s_clean:
        m = re.search(r'(-?\d+(\.\d+)?)', s_clean)
        return float(m.group(1)) / 100 if m else np.nan
    m = re.search(r'(-?\d+(\.\d+)?)', s_clean)
    if m:
        num = m.group(1)
        try:
            if '.' in num:
                return float(num)
            else:
                return int(num)
        except:
            try:
                return float(num)
            except:
                return np.nan
    return np.nan

# -------------------------------------------------------
# Helper: parse female_male_ratio into female percentage
# -------------------------------------------------------
def parse_female_male_ratio_to_percent(s):
    if pd.isna(s):
        return np.nan
    s = str(s).strip()
    if s == "" or s == "-" or s.lower() == "nan":
        return np.nan
    if '%' in s:
        m = re.search(r'(-?\d+(\.\d+)?)', s)
        return float(m.group(1)) if m else np.nan
    nums = re.findall(r'(\d+(?:\.\d+)?)', s)
    if len(nums) >= 2:
        female = float(nums[0])
        male = float(nums[1])
        denom = female + male
        if denom == 0:
            return np.nan
        return (female / denom) * 100
    elif len(nums) == 1:
        return float(nums[0])
    else:
        return np.nan

# -------------------------------------------------------
# Main cleaning logic
# -------------------------------------------------------
def main():
    print("Loading:", INPUT)
    df = pd.read_csv(INPUT, dtype=str)
    print("Initial shape:", df.shape)
    print("Columns:", list(df.columns))

    numeric_candidates = [
        'world_rank', 'teaching', 'international', 'research', 'citations',
        'income', 'total_score', 'num_students', 'student_staff_ratio',
        'international_students',
        'cwur_world_rank', 'cwur_national_rank', 'cwur_quality_of_education',
        'cwur_alumni_employment', 'cwur_quality_of_faculty', 'cwur_publications',
        'cwur_influence', 'cwur_citations', 'cwur_broad_impact', 'cwur_patents',
        'cwur_score'
    ]

    # Parse numeric columns
    for col in numeric_candidates:
        if col in df.columns:
            print(f"Parsing numeric column: {col}")
            df[col] = df[col].apply(extract_first_number)

    # Convert specific columns to float
    if 'num_students' in df.columns:
        df['num_students'] = pd.to_numeric(df['num_students'], errors='coerce')

    if 'international_students' in df.columns:
        df['international_students'] = pd.to_numeric(df['international_students'], errors='coerce')

    # Handle female_male_ratio -> remove old, add new
    if 'female_male_ratio' in df.columns:
        print("Converting female_male_ratio -> female_male_percent (removing old column)")
        parsed = df['female_male_ratio'].apply(parse_female_male_ratio_to_percent)
        idx = list(df.columns).index('female_male_ratio')
        df.drop(columns=['female_male_ratio'], inplace=True)
        df.insert(idx, 'female_male_percent', parsed)

    # Show data types
    print("\nData types after parsing:")
    print(df.dtypes)

    # Show missing percentages
    missing_pct = (df.isna().sum() / len(df) * 100).sort_values(ascending=False)
    print("\n% missing per column (top 10):")
    print(missing_pct.head(10))

    # Save cleaned data
    df.to_csv(OUTPUT, index=False)
    print(f"\nSaved cleaned dataset to: {OUTPUT}")
    print("Final shape:", df.shape)

    # Preview
    preview_cols = [c for c in ['university_name', 'country', 'international_students', 'female_male_percent'] if c in df.columns]
    print("\nPreview (first 8 rows):")
    print(df[preview_cols].head(8).to_string(index=False))

# -------------------------------------------------------
if __name__ == "__main__":
    main()
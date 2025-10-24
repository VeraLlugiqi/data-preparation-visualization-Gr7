#!/usr/bin/env python3
"""
Merge timesData and cwurData university rankings by year and university name.
Includes universities from both datasets - those that exist in only times, only cwur, or both.
Empty columns are preserved when data is missing from either source.
"""

import sys
import subprocess
import re
import unicodedata

# Check if pandas is installed, if not install it
try:
    import pandas as pd
except ImportError:
    print("pandas not found. Installing pandas...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd


def clean_for_merge(name):
    """Normalize and clean university names for robust merging."""
    if pd.isna(name):
        return ""

    s = str(name)
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[\u200B-\u200F\uFEFF]", "", s)  # remove invisible chars
    s = s.lower().strip()

    # Replace all dash-like characters with spaces
    dash_pattern = r"[\u2010-\u2015\u2212\uFE58\uFE63\uFF0D-]"  # all dash unicode
    s = re.sub(dash_pattern, " ", s)

    # Remove parentheses and their content
    s = re.sub(r"\(.*?\)", "", s)

    # Remove trailing campus/city suffixes like ", Cambridge" or "- Bloomington"
    s = re.sub(r"[,|-]\s*[^,|-]*$", "", s)

    # Remove punctuation except spaces and ampersand
    s = re.sub(r"[^\w\s&]", "", s)

    # Collapse extra spaces
    s = re.sub(r"\s+", " ", s).strip()

    # Canonical replacements for known duplicates
    canonical_map = {
        # --- Specific equivalences ---
        r"\bpierre( and)? marie curie( university)?\b": "pierre and marie curie university",
        r"\btechnion( israel institute of technology)?\b": "technion israel institute of technology",
        r"\bbrunel university( london)?\b": "brunel university",
        r"\bwageningen university( and research (center|centre))?\b": "wageningen university",
        r"\bindiana university( bloomington)?\b": "indiana university",
        r"\buniversity of pittsburgh( pittsburgh campus)?\b": "university of pittsburgh",
        r"\buniversity of washington( seattle)?\b": "university of washington",
    }

    for pattern, replacement in canonical_map.items():
        if re.search(pattern, s):
            s = re.sub(pattern, replacement, s)
            s = re.sub(r"\s+", " ", s).strip()
            break

    return s



def normalize_university_name(name):
    """Simplified normalization (retained for country normalization)."""
    if pd.isna(name):
        return name
    normalized = str(name).lower().strip()
    replacements = {
        "united states of america": "usa",
        "united kingdom": "uk",
    }
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    return normalized


def show_examples(df, col_original, col_norm, patterns, sample=20):
    """Diagnostic printout for checking name normalization."""
    print(f"\n--- Checking column {col_original} ---")
    for pat in patterns:
        mask = df[col_original].astype(str).str.contains(pat, case=False, na=False)
        subset = df.loc[mask, [col_original, col_norm]].drop_duplicates().head(sample)
        if subset.empty:
            print(f"No examples matching pattern: {pat!r}")
        else:
            print(f"\nPattern: {pat!r}")
            for orig, norm in subset.values:
                print(f"ORIG: {orig!r}  -->  NORM: {norm!r}")


def main():
    print("Starting merge process...")

    times_df = pd.read_csv("../../timesData.csv")
    cwur_df = pd.read_csv("../../cwurData.csv")

    # Normalize and clean names
    times_df["_norm_name"] = times_df["university_name"].apply(clean_for_merge)
    cwur_df["_norm_name"] = cwur_df["institution"].apply(clean_for_merge)

    # Country normalization
    times_df["_norm_country"] = times_df["country"].apply(normalize_university_name)
    cwur_df["_norm_country"] = cwur_df["country"].apply(normalize_university_name)

    # Diagnostics — see if normalization is working as expected
    patterns = [
        "pierre",
        "technion",
        "brunel",
        "wageningen",
        "indiana",
        "pittsburgh",
    ]
    show_examples(times_df, "university_name", "_norm_name", patterns)
    show_examples(cwur_df, "institution", "_norm_name", patterns)

    # Rename CWUR columns
    cwur_columns_to_rename = {
        "world_rank": "cwur_world_rank",
        "national_rank": "cwur_national_rank",
        "quality_of_education": "cwur_quality_of_education",
        "alumni_employment": "cwur_alumni_employment",
        "quality_of_faculty": "cwur_quality_of_faculty",
        "publications": "cwur_publications",
        "influence": "cwur_influence",
        "citations": "cwur_citations",
        "broad_impact": "cwur_broad_impact",
        "patents": "cwur_patents",
        "score": "cwur_score",
        "institution": "cwur_institution",
        "country": "cwur_country",
    }
    cwur_df = cwur_df.rename(columns=cwur_columns_to_rename)

    # Merge both datasets
    merged_df = pd.merge(
        times_df,
        cwur_df,
        left_on=["year", "_norm_name"],
        right_on=["year", "_norm_name"],
        how="outer",
        suffixes=("", "_cwur"),
    )

    # Fill missing name and country from cwur data
    merged_df["university_name"] = merged_df["university_name"].fillna(
        merged_df.get("cwur_institution")
    )
    merged_df["country"] = merged_df["country"].fillna(merged_df.get("cwur_country"))

    # Drop unnecessary columns
    columns_to_drop = [
        "_norm_name",
        "_norm_country",
        "_norm_name_cwur",
        "_norm_country_cwur",
        "cwur_institution",
        "cwur_country",
    ]
    merged_df = merged_df.drop(
        columns=[col for col in columns_to_drop if col in merged_df.columns]
    )

    # Drop duplicates based on normalized name and year
    merged_df = merged_df.sort_values("year")
    merged_df = merged_df.drop_duplicates(subset=["year", "university_name"], keep="first")

    # Reorder columns
    times_columns = [
        "world_rank",
        "university_name",
        "country",
        "teaching",
        "international",
        "research",
        "citations",
        "income",
        "total_score",
        "num_students",
        "student_staff_ratio",
        "international_students",
        "female_male_ratio",
        "year",
    ]

    cwur_columns = [
        "cwur_world_rank",
        "cwur_national_rank",
        "cwur_quality_of_education",
        "cwur_alumni_employment",
        "cwur_quality_of_faculty",
        "cwur_publications",
        "cwur_influence",
        "cwur_citations",
        "cwur_broad_impact",
        "cwur_patents",
        "cwur_score",
    ]

    final_columns = times_columns + cwur_columns
    final_columns = [col for col in final_columns if col in merged_df.columns]

    merged_df = merged_df[final_columns]
    merged_df = merged_df.fillna("-")

    output_file = "merged_university_data.csv"
    merged_df.to_csv(output_file, index=False)

    print(f"\nMerge completed successfully! Output saved to: {output_file}")


if __name__ == "__main__":
    main()

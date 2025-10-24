#!/usr/bin/env python3
"""
Merge timesData and cwurData university rankings by year and university name.
Includes universities from both datasets - those that exist in only times, only cwur, or both.
Empty columns are preserved when data is missing from either source.
"""

import sys
import subprocess

# Check if pandas is installed, if not install it
try:
    import pandas as pd
except ImportError:
    print("pandas not found. Installing pandas...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd


def normalize_university_name(name):
    """Normalize university names for better matching."""
    if pd.isna(name):
        return name
    normalized = str(name).lower().strip()
    replacements = {
        'united states of america': 'usa',
        'united kingdom': 'uk',
    }
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    return normalized


def main():
    print("Starting merge process...")
    times_df = pd.read_csv('../../timesData.csv')
    cwur_df = pd.read_csv('../../cwurData.csv')

    times_df['_norm_name'] = times_df['university_name'].apply(normalize_university_name)
    times_df['_norm_country'] = times_df['country'].apply(normalize_university_name)

    cwur_df['_norm_name'] = cwur_df['institution'].apply(normalize_university_name)
    cwur_df['_norm_country'] = cwur_df['country'].apply(normalize_university_name)

    cwur_columns_to_rename = {
        'world_rank': 'cwur_world_rank',
        'national_rank': 'cwur_national_rank',
        'quality_of_education': 'cwur_quality_of_education',
        'alumni_employment': 'cwur_alumni_employment',
        'quality_of_faculty': 'cwur_quality_of_faculty',
        'publications': 'cwur_publications',
        'influence': 'cwur_influence',
        'citations': 'cwur_citations',
        'broad_impact': 'cwur_broad_impact',
        'patents': 'cwur_patents',
        'score': 'cwur_score',
        'institution': 'cwur_institution',
        'country': 'cwur_country'
    }

    cwur_df = cwur_df.rename(columns=cwur_columns_to_rename)

    merged_df = pd.merge(
        times_df,
        cwur_df,
        left_on=['year', '_norm_name'],
        right_on=['year', '_norm_name'],
        how='outer',
        suffixes=('', '_cwur')
    )

    # Fill university_name and country from cwur data when they don't exist in times
    merged_df['university_name'] = merged_df['university_name'].fillna(merged_df['cwur_institution'])
    merged_df['country'] = merged_df['country'].fillna(merged_df['cwur_country'])

    columns_to_drop = ['_norm_name', '_norm_country', '_norm_name_cwur', '_norm_country_cwur',
                       'cwur_institution', 'cwur_country']
    merged_df = merged_df.drop(columns=[col for col in columns_to_drop if col in merged_df.columns])

    times_columns = [
        'world_rank', 'university_name', 'country', 'teaching', 'international',
        'research', 'citations', 'income', 'total_score', 'num_students',
        'student_staff_ratio', 'international_students', 'female_male_ratio', 'year'
    ]

    cwur_columns = [
        'cwur_world_rank', 'cwur_national_rank',
        'cwur_quality_of_education', 'cwur_alumni_employment', 'cwur_quality_of_faculty',
        'cwur_publications', 'cwur_influence', 'cwur_citations', 'cwur_broad_impact',
        'cwur_patents', 'cwur_score'
    ]

    final_columns = times_columns + cwur_columns
    final_columns = [col for col in final_columns if col in merged_df.columns]

    merged_df = merged_df[final_columns]

    merged_df = merged_df.fillna('-')

    output_file = 'merged_university_data.csv'
    merged_df.to_csv(output_file, index=False)

    print(f"Merge completed successfully! Output saved to: {output_file}")


if __name__ == '__main__':
    main()
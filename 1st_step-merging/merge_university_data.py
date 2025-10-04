#!/usr/bin/env python3
"""
Merge timesData and cwurData university rankings by year and university name.
Keeps the order from timesData and preserves empty columns for missing cwurData years (e.g., 2011).
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
    # Convert to lowercase and strip whitespace
    normalized = str(name).lower().strip()
    # Common replacements for better matching
    replacements = {
        'united states of america': 'usa',
        'united kingdom': 'uk',
    }
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    return normalized

def main():
    # Read the data files
    print("Reading timesData.csv...")
    times_df = pd.read_csv('../timesData.csv')
    
    print("Reading cwurData.csv...")
    cwur_df = pd.read_csv('../cwurData.csv')
    
    print(f"\ntimesData shape: {times_df.shape}")
    print(f"cwurData shape: {cwur_df.shape}")
    print(f"\ntimesData years: {sorted(times_df['year'].unique())}")
    print(f"cwurData years: {sorted(cwur_df['year'].unique())}")
    
    # Create normalized columns for matching
    times_df['_norm_name'] = times_df['university_name'].apply(normalize_university_name)
    times_df['_norm_country'] = times_df['country'].apply(normalize_university_name)
    
    cwur_df['_norm_name'] = cwur_df['institution'].apply(normalize_university_name)
    cwur_df['_norm_country'] = cwur_df['country'].apply(normalize_university_name)
    
    # Rename cwurData columns to avoid conflicts (prefix with cwur_)
    # Note: We don't include institution and country since they're already in timesData
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
        'score': 'cwur_score'
    }
    
    cwur_df = cwur_df.rename(columns=cwur_columns_to_rename)
    
    # Drop institution and country columns from cwur_df since we have them in timesData
    cwur_df = cwur_df.drop(columns=['institution', 'country'], errors='ignore')
    
    # Perform left merge on year and normalized university name
    print("\nMerging datasets...")
    merged_df = pd.merge(
        times_df,
        cwur_df,
        left_on=['year', '_norm_name'],
        right_on=['year', '_norm_name'],
        how='left',
        suffixes=('', '_cwur')
    )
    
    # If the first merge didn't match well, try matching by year and country as fallback
    # (this is optional and can help with some edge cases)
    
    # Drop the temporary normalized columns
    columns_to_drop = ['_norm_name', '_norm_country', '_norm_name_cwur', '_norm_country_cwur']
    merged_df = merged_df.drop(columns=[col for col in columns_to_drop if col in merged_df.columns])
    
    # Reorder columns: all timesData columns first, then all cwurData columns
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
    
    # Ensure all columns exist in the merged dataframe
    final_columns = times_columns + cwur_columns
    final_columns = [col for col in final_columns if col in merged_df.columns]
    
    # Reorder the dataframe
    merged_df = merged_df[final_columns]
    
    # Replace NaN values with '-' for empty cells
    merged_df = merged_df.fillna('-')
    
    # Save the merged data
    output_file = 'merged_university_data.csv'
    print(f"\nSaving merged data to {output_file}...")
    merged_df.to_csv(output_file, index=False)
    
    print(f"\nMerge complete!")
    print(f"Output shape: {merged_df.shape}")
    print(f"Output file: {output_file}")
    
    # Show some statistics
    print(f"\nMerge statistics:")
    print(f"Total records: {len(merged_df)}")
    print(f"Records with cwurData: {merged_df['cwur_world_rank'].notna().sum()}")
    print(f"Records without cwurData (e.g., 2011): {merged_df['cwur_world_rank'].isna().sum()}")
    
    # Show sample of merged data
    print("\nFirst 5 rows of merged data:")
    print(merged_df.head())
    
    # Show a sample from 2011 (should have empty cwur columns)
    print("\nSample from 2011 (should have empty cwur columns):")
    sample_2011 = merged_df[merged_df['year'] == 2011].head(3)
    if not sample_2011.empty:
        print(sample_2011)
    else:
        print("No 2011 data found in timesData")
    
    # Show a sample from 2012 (should have cwur data)
    print("\nSample from 2012 (should have cwur data):")
    sample_2012 = merged_df[merged_df['year'] == 2012].head(3)
    if not sample_2012.empty:
        print(sample_2012)
    else:
        print("No 2012 data found")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Filter University Rankings Dataset by Year

This script filters the cleaned university dataset to include only years 2012-2015,
removing 2011 and 2016 which have missing CWUR data.

Input: ../2nd_step-changing_types/v2/merged_university_data_cleaned.csv
Output: filtered_university_data.csv
"""

import pandas as pd
import sys
from pathlib import Path


def main():
    # Define file paths
    input_file = Path(__file__).parent.parent.parent / '2nd_step-changing_types' / 'v2' / 'merged_university_data_cleaned.csv'
    output_file = Path(__file__).parent / 'filtered_university_data.csv'
    
    print(f"Reading data from: {input_file}")
    
    # Check if input file exists
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    # Read the cleaned dataset
    df = pd.read_csv(input_file)
    
    print(f"\nOriginal dataset shape: {df.shape}")
    print(f"Years in original data: {sorted(df['year'].unique())}")
    print(f"Records per year:\n{df['year'].value_counts().sort_index()}")
    
    # Filter for years 2012-2015 (years with CWUR data)
    df_filtered = df[df['year'].isin([2012, 2013, 2014, 2015])].copy()
    
    print(f"\n{'='*60}")
    print("FILTERING: Keeping only years 2012-2015")
    print(f"{'='*60}")
    
    print(f"\nFiltered dataset shape: {df_filtered.shape}")
    print(f"Years in filtered data: {sorted(df_filtered['year'].unique())}")
    print(f"Records per year:\n{df_filtered['year'].value_counts().sort_index()}")
    
    # Calculate removed records
    removed_count = len(df) - len(df_filtered)
    removed_percentage = (removed_count / len(df)) * 100
    
    print(f"\nRemoved {removed_count} records ({removed_percentage:.1f}%)")
    print(f"Kept {len(df_filtered)} records ({100-removed_percentage:.1f}%)")
    
    # Display CWUR data availability
    cwur_columns = [col for col in df_filtered.columns if col.startswith('cwur_')]
    cwur_missing = df_filtered[cwur_columns].isna().all(axis=1).sum()
    cwur_present = len(df_filtered) - cwur_missing
    
    print(f"\nCWUR data availability in filtered dataset:")
    print(f"  Records with CWUR data: {cwur_present} ({(cwur_present/len(df_filtered)*100):.1f}%)")
    print(f"  Records without CWUR data: {cwur_missing} ({(cwur_missing/len(df_filtered)*100):.1f}%)")
    
    # Save filtered dataset
    df_filtered.to_csv(output_file, index=False)
    print(f"\nFiltered dataset saved to: {output_file}")
    
    # Display sample of filtered data
    print(f"\nSample of filtered data (first 5 records):")
    print(df_filtered[['world_rank', 'university_name', 'country', 'year', 'total_score']].head())
    
    print("\nFiltering complete!")


if __name__ == "__main__":
    main()

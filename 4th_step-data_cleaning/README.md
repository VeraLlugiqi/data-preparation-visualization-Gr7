# Step 4 – Advanced Data Cleaning and Imputation

This step performs advanced data cleaning on the university dataset to handle missing values, improve consistency, and prepare the data for visualization and analysis.

## Overview

In this stage, the following actions are taken:

- **Normalize column names**
- **Remove columns with excessive missing data**
- **Combine overlapping ranking columns**
- **Fill missing values using median imputation per university**
- **Convert CWUR-related columns to integers**
- **Remove rows with missing ranking data**
- **Save the cleaned dataset for the next step**

## Detailed Steps

### Column Normalization
All column names are converted to lowercase, stripped of spaces, and replaced with underscores for consistency.

### Remove Columns with High Missing Rates
The following columns are removed due to more than 45–70% missing values:

- `total_score`
- `female_male_percent`
- `income`

### Combine Ranking Columns
Missing values in one ranking column are filled using the other:

- `world_rank` is filled using `cwur_world_rank`
- `cwur_world_rank` is filled using `world_rank`

### Median Imputation per University
For numeric columns, missing values are filled with the median of that university based on its historical data (e.g., across different years).

### Global Median Imputation
If any missing values remain after the university-level imputation, they are filled with the overall column median.

### Convert CWUR Columns to Integers
All columns starting with `cwur_` are converted to **int type**, since ranking data should not contain decimals.

### Remove Incomplete Rows
Any rows missing both `world_rank` and `cwur_world_rank` are removed to ensure data integrity.

### Save the Cleaned Dataset
The final dataset is exported as:

- `cleaned_university_data.csv`

## Purpose

This step ensures that the dataset is:

- **Consistent** and free of redundant columns
- **Complete** enough for analysis and visualization
- **Structured** properly for subsequent preprocessing and reporting steps

It represents the fourth phase of the overall data preparation pipeline.

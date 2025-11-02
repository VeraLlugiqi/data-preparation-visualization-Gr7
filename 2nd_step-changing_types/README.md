#  Dataset Cleaning and Type Conversion

## Overview

The **`change_type.py`** script performs comprehensive data cleaning and type conversion on the merged university dataset. It preserves the original column structure while ensuring data quality and numeric compatibility for analysis.

### Input/Output
- **Input**: `../1st_step-merging/merged_university_data.csv`
- **Output**: `merged_university_data_cleaned.csv`

## What the Script Does

### 1. **Numeric Type Conversion**
Converts string-based numeric columns to proper numeric types (`int` or `float`):
- **Ranking columns**: `world_rank`, `cwur_world_rank`, `cwur_national_rank`
- **Performance metrics**: `teaching`, `international`, `research`, `citations`, `income`, `total_score`
- **CWUR metrics**: `cwur_quality_of_education`, `cwur_alumni_employment`, `cwur_quality_of_faculty`, `cwur_publications`, `cwur_influence`, `cwur_citations`, `cwur_broad_impact`, `cwur_patents`, `cwur_score`
- **Student data**: `num_students`, `student_staff_ratio`, `international_students`

### 2. **Data Cleaning Features**
- **Removes commas**: `"1,234"` → `1234`
- **Handles percentages**: `"14%"` → `14.0` (or `0.14` for ratios)
- **Extracts from ranges**: `"100-200"` → `100` (first value)
- **Handles missing data**: Converts `"-"`, empty strings, and unparsable values to `NaN`
- **Coerces errors gracefully**: Invalid numeric values become `NaN` instead of causing errors

### 3. **Gender Ratio Transformation**
**`female_male_ratio` → `female_male_percent`**
- Converts ratio format (e.g., `"45:55"`) to female percentage: `45.0`
- Handles percentage format (e.g., `"24%"`) → `24.0`
- Handles single numeric values as percentages
- Maintains column position (replaces old column in same location)
- Male percentage can be calculated as `100 - female_male_percent`

### 4. **Data Quality Reporting**
The script outputs:
- Initial and final dataset shapes
- Data types after conversion
- Missing value percentages per column (top 10)
- Preview of key columns

## Key Functions

- **`extract_first_number(s)`**: Extracts the first numeric value from strings, handling percentages, commas, and ranges
- **`parse_female_male_ratio_to_percent(s)`**: Converts female-to-male ratio strings into female percentage values

## Result

The cleaned dataset:
- Maintains original column order (except `female_male_ratio` replacement)
- All numeric columns are proper numeric types for calculations
- Ready for statistical analysis and visualization
- Missing values are properly represented as `NaN`


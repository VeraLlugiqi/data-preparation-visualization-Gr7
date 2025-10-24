# Year Filtering - Regional Comparison Focus

## Overview

This step filters the cleaned university dataset to include only years with complete CWUR data (2012-2015), removing 2011 and 2016. This prepares the data for **regional comparison analysis** of university performance across countries and continents.

## Goal

**End Goal: Regional Comparison**  
Compare university performance across countries/continents using both Times Higher Education (THE) and CWUR metrics to understand:
- Which regions dominate in university rankings
- Performance differences across continents
- Country-specific strengths and weaknesses
- Regional trends in education quality, research output, and international outlook

## Why Filter Years?

- **2011**: No CWUR data available (only THE rankings)
- **2016**: No CWUR data available (only THE rankings)
- **2012-2015**: Complete data from both ranking systems

By keeping only 2012-2015, we ensure all records have the potential for both THE and CWUR metrics, creating a more balanced dataset for comparison.

## Files

### Input
- **Source**: `../2nd_step-changing_types/v2/merged_university_data_cleaned.csv`
- **Records**: 2,603 (years 2011-2016)

### Output
- **Destination**: `v1/filtered_university_data.csv`
- **Records**: ~1,700+ (years 2012-2015 only)

### Script
- **`v1/filter_years.py`** - Python script that performs year filtering

## What the Script Does

1. **Reads** cleaned dataset from step 2
2. **Filters** records to keep only years 2012, 2013, 2014, 2015
3. **Reports** statistics:
   - Records removed/kept
   - CWUR data availability
   - Distribution by year
4. **Saves** filtered dataset to CSV

## Usage

```bash
cd 3rd_step-filtering_years/v1
python3 filter_years.py
```

### Expected Output
```
Original dataset shape: (2603, 25)
Years in original data: [2011, 2012, 2013, 2014, 2015, 2016]

============================================================
FILTERING: Keeping only years 2012-2015
============================================================

Filtered dataset shape: (~1700+, 25)
Years in filtered data: [2012, 2013, 2014, 2015]

Removed ~900 records (~35%)
Kept ~1700 records (~65%)

✓ Filtered dataset saved to: filtered_university_data.csv
```

## Data Statistics

### Before Filtering
- **Total records**: 2,603
- **Years**: 2011-2016 (6 years)
- **Missing CWUR**: All 2011 and 2016 records

### After Filtering
- **Total records**: ~1,700+
- **Years**: 2012-2015 (4 years)
- **More complete data** for both ranking systems

## Next Steps for Regional Comparison

After filtering, the following steps remain:

1. **Country/Region Grouping**
   - Standardize country names
   - Map countries to continents
   - Create regional aggregations

2. **Missing Value Treatment**
   - Analyze remaining missing CWUR values
   - Decide on imputation strategy
   - Handle missing THE metrics

3. **Feature Engineering for Regional Analysis**
   - Create regional performance scores
   - Calculate country averages
   - Identify top performers by region

4. **Aggregation & Comparison**
   - Group by country/continent
   - Calculate statistical summaries
   - Compare regional metrics

5. **Visualization**
   - Regional performance heatmaps
   - Country comparison charts
   - Continental trend analysis
   - Top universities by region

## Column Reference

The filtered dataset maintains all 25 columns:

**Core columns**: world_rank, university_name, country, year, total_score  
**THE metrics**: teaching, international, research, citations, income  
**Student data**: num_students, student_staff_ratio, international_students, female_male_percent  
**CWUR metrics**: cwur_world_rank, cwur_national_rank, cwur_quality_of_education, cwur_alumni_employment, cwur_quality_of_faculty, cwur_publications, cwur_influence, cwur_citations, cwur_broad_impact, cwur_patents, cwur_score

---

**Created**: October 2024  
**Purpose**: Data filtering for regional comparison analysis  
**Python Version**: 3.x  
**Dependencies**: pandas

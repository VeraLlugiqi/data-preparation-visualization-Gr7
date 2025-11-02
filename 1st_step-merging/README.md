# University Rankings Data Merge

This project merges two university ranking datasets into a single comprehensive file while preserving data integrity and handling missing values gracefully.

## Files

### Input Files
- **`timesData.csv`** - Times Higher Education World University Rankings
- **`cwurData.csv`** - Center for World University Rankings (CWUR) data

### Output File
- **`merged_university_data.csv`** - Combined dataset with all information from both sources

### Script
- **`merge_university_data.py`** - Python script that performs the merge operation

## Dataset Information

### timesData.csv Columns (14)
Contains performance scores and metrics:
- `world_rank` - World ranking position
- `university_name` - Name of the university
- `country` - Country of the university
- `teaching` - Teaching score (0-100)
- `international` - International outlook score (0-100)
- `research` - Research score (0-100)
- `citations` - Citations score (0-100)
- `income` - Industry income score (0-100)
- `total_score` - Overall score (0-100)
- `num_students` - Number of students
- `student_staff_ratio` - Student to staff ratio (e.g., 8.9)
- `international_students` - Percentage of international students (e.g., 25%)
- `female_male_ratio` - Gender ratio (e.g., 42:58:00)
- `year` - Year of the ranking (2011-2016)

### cwurData.csv Columns (14)
Contains ranking positions across different criteria:
- `world_rank` - World ranking position
- `institution` - Name of the institution
- `country` - Country (abbreviated, e.g., USA)
- `national_rank` - National ranking position
- `quality_of_education` - Ranking for quality of education
- `alumni_employment` - Ranking for alumni employment
- `quality_of_faculty` - Ranking for faculty quality
- `publications` - Ranking for publications
- `influence` - Ranking for influence
- `citations` - Ranking for citations
- `broad_impact` - Ranking for broad impact
- `patents` - Ranking for patents
- `score` - Overall CWUR score
- `year` - Year of the ranking (2012-2015)

**Note:** cwurData rankings represent positions (lower is better), while timesData scores represent performance (higher is better).

### University Name Normalization and Merge Accuracy

During the merging of Times and CWUR university datasets, some universities appeared as separate entries due to small differences in their names. Examples include:

- "Ohio State University" vs "Ohio State University, Columbus"  
- "University of Illinois at Urbana-Champaign" vs "University of Illinois at Urbana–Champaign"  
- Differences in punctuation, accents, or added city names.

To solve this, a normalization step was added before merging:

- Names are converted to lowercase and stripped of leading/trailing whitespace.  
- Punctuation is removed and city suffixes after commas are stripped.  
- Accented characters are normalized to ASCII.  
- Optionally, fuzzy matching can be used to catch less obvious differences.

This ensures that each university is counted as a single row in the merged dataset, improving merge quality and avoiding duplicate or fragmented records.

## Merge Process

### How It Works
1. **Reads both CSV files** using pandas
2. **Normalizes university names** for better matching:
   - Converts to lowercase
   - Standardizes country names (e.g., "United States of America" → "USA")
3. **Performs a left join** on `year` and normalized `university_name`
   - Keeps all records from timesData (primary dataset)
   - Adds cwurData where matches are found
4. **Prefixes cwurData columns** with `cwur_` to avoid naming conflicts
5. **Excludes duplicate columns** (institution and country) since they're already in timesData
6. **Replaces empty cells** with `-` for clarity
7. **Preserves the original order** from timesData

### Merge Key
Records are matched based on:
- **Year** (exact match)
- **University name** (normalized for matching)

## Output Structure

### merged_university_data.csv (25 columns)

**Original timesData columns (14):**
```
world_rank, university_name, country, teaching, international, research, 
citations, income, total_score, num_students, student_staff_ratio, 
international_students, female_male_ratio, year
```

**Added cwurData columns (11):**
```
cwur_world_rank, cwur_national_rank, cwur_quality_of_education, 
cwur_alumni_employment, cwur_quality_of_faculty, cwur_publications, 
cwur_influence, cwur_citations, cwur_broad_impact, cwur_patents, cwur_score
```

### Missing Data Handling
- **Empty cells display `-`** instead of being blank
- **Year 2011**: All cwur columns show `-` (no cwurData available for 2011)
- **Year 2016**: All cwur columns show `-` (no cwurData available for 2016)
- **Unmatched universities**: cwur columns show `-` even in years 2012-2015

## Usage

### Prerequisites
```bash
# Install pandas (if not already installed)
pip3 install --break-system-packages pandas
```

### Running the Script
```bash
python3 merge_university_data.py
```

The script will:
1. Read `timesData.csv` and `cwurData.csv`
2. Display dataset information and statistics
3. Perform the merge operation
4. Generate `merged_university_data.csv`
5. Show sample output and merge statistics

### Example Output
```
Reading timesData.csv...
Reading cwurData.csv...

timesData shape: (2603, 14)
cwurData shape: (2200, 14)

timesData years: [2011, 2012, 2013, 2014, 2015, 2016]
cwurData years: [2012, 2013, 2014, 2015]

Merging datasets...
Saving merged data to merged_university_data.csv...

Merge complete!
Output shape: (2603, 25)
```

## Statistics

- **Total records:** 2,603 (same as timesData)
- **Total columns:** 25
- **Records with cwurData:** ~807
- **Records without cwurData:** ~1,796 (includes all 2011 and 2016 data, plus unmatched universities)
- **Year coverage:**
  - timesData: 2011-2016
  - cwurData: 2012-2015
  - merged: 2011-2016 (with gaps filled by `-`)

## Key Features

- **Preserves timesData order** - Original sequence maintained  
- **No duplicate columns** - Institution and country not duplicated  
- **Handles missing years** - 2011 and 2016 preserved with `-` for cwur columns  
- **Intelligent matching** - Normalizes names for better match rates  
- **Clear empty indicators** - Uses `-` instead of blank cells  
- **Non-destructive** - Original files remain unchanged  
- **Automatic dependencies** - Installs pandas if needed (with user confirmation)

## Use Cases

This merged dataset is useful for:
- **Comprehensive analysis** of university rankings across different methodologies
- **Comparing** scoring systems (Times scores vs CWUR rankings)
- **Trend analysis** over multiple years
- **Identifying** universities that perform well in both ranking systems
- **Research** on higher education metrics and evaluation methods

## Important Notes

1. **Different metrics:** timesData uses scores (higher is better), cwurData uses rankings (lower is better)
2. **Country names:** May vary between datasets (e.g., "USA" vs "United States of America")
3. **Coverage gaps:** Not all universities appear in both datasets
4. **Year availability:** 2011 has no cwur data, 2016 has no cwur data
5. **Original files:** The merge script does NOT modify the original CSV files

## Customization

To modify the merge behavior, edit `merge_university_data.py`:

- **Change output filename:** Modify `output_file` variable (line 117)
- **Adjust empty cell indicator:** Change `fillna('-')` to use a different value (line 114)
- **Add more normalizations:** Update `normalize_university_name()` function (line 18)
- **Include dropped columns:** Modify the `cwur_df.drop()` line (line 72)

## Data Sources

- **Times Higher Education (THE)** - World University Rankings
- **Center for World University Rankings (CWUR)** - Global university rankings

---

**Created:** October 2025  
**Script Version:** 1.0  
**Python Version:** 3.13+  
**Required Package:** pandas 2.x




#  Dataset Cleaning and Type Conversion

 - **`change_type.py` script cleans the university dataset without changing the original column order. The cleaned dataset is saved as **`merged_university_data_cleaned.csv`**.

## Main Changes

- **`female_male_ratio` → `female_male_percent`**: Converted female-to-male ratio values into the percentage of female students (e.g., `24%` → `0.24`). The male percentage can be calculated later if needed.  
- **Numeric columns converted**: Columns such as `world_rank`, `teaching`, `research`, `citations`, `income`, `total_score`, `num_students`, `student_staff_ratio`, `international_students`, and CWUR columns (`cwur_world_rank`, `cwur_quality_of_education`, `cwur_alumni_employment`, etc.) are now numeric (`int` or `float`) for easier analysis.  
- **Value cleaning**: Percentages, commas, or numeric ranges were cleaned; any unparsable values were set to `NaN`.  

The dataset keeps its original structure, is numerically usable, and ready for analysis or visualization.


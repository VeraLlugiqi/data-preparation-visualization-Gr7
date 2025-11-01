# Step 5 – Sampling & Feature Engineering

This step keeps the workflow consistent with earlier stages: one script for sampling, one for feature creation, and clearly documented outputs.

---

## Scripts

### sampling.py
- **Purpose:** Load `../4th-step-data_cleaning/cleaned_university_data.csv`, draw a 20% stratified sample per year (seeded with 42), and expose the sampled/full DataFrames for reuse.
- **Run:**  
  ```bash
  python3 sampling.py
  ```
- **Output:** `sampled_dataset.csv`
- **Extra:** Provides `get_datasets()` so other scripts can load the full and sampled data without repeating logic.

### feature_engineering.py
- **Purpose:** Use `get_datasets()` to derive new analytic features, standardize key metrics, bucket rankings/sizes, and create binary indicators.
- **Run:**  
  ```bash
  python3 feature_engineering.py
  ```
- **Output:** `university_data_engineered.csv` – full dataset with engineered columns

---

## Features Added
- `rank_consistency_std` / `consistency_score`: variability of world rank and its inverse stability score.
- `research_index`, `teaching_index`, `global_index`: averaged performance metrics.
- `rank_change`, `trajectory`: year-over-year rank delta and trend class (rising/stable/declining).
- `region`, `diversity_index`: continent mapping and blended diversity measure.
- `research_index_z`, `teaching_index_z`: z-score standardized versions of the indices.
- `rank_tier`, `performance_category`, `size_category`: discrete buckets for rank, teaching strength, and university size.
- `is_top_100`, `is_research_intensive`, `is_rising`: binary flags for key analytical segments.

These outputs feed the dimensionality-reduction step and any downstream visualizations.

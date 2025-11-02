# Step 7–8: Discretization, Binarization & Transformation

This step enhances the dataset from the previous **Feature Selection & Creation** phase by adding new categorical and standardized features for better interpretability and analysis.  
It keeps all university rows (no aggregation) and prepares the data for further visualization or modeling.

---

## Overview of Operations

### 1. Discretization
Converts continuous numeric values into ordered categories for easier comparison.

- **`teaching_level`** → Categorized into `Low`, `Medium`, `High` based on quantiles of the `teaching` score.  
- **`citations_level`** → Categorized into `Low`, `Medium`, `High` based on quantiles of the `citations` score.

*Purpose:* Makes continuous scores interpretable in reports and charts.

---

### 2. Binarization
Creates binary indicators (0 or 1) for specific ranking and student metrics.

| Column | Meaning |
|---------|----------|
| **`top100_the`** | 1 if `world_rank` ≤ 100, else 0 (Times Higher Education) |
| **`top100_cwur`** | 1 if `cwur_world_rank` ≤ 100, else 0 (CWUR ranking) |
| **`high_international_ratio`** | 1 if >30% of students are international, else 0 (kept from previous step) |

*Purpose:* Enables quick identification of top universities and highly international institutions.

---

### 3. Contextual Transformations
Adds new features that compare each university’s performance relative to the **average of its country and year**.

| Column | Description |
|---------|-------------|
| **`country_year_teaching_mean`** | Average teaching score in the same country and year. |
| **`country_year_citations_mean`** | Average citations score in the same country and year. |
| **`country_year_cwur_score_mean`** | Average CWUR score in the same country and year. |
| **`relative_teaching`** | Ratio = `teaching / country_year_teaching_mean` → How much higher/lower a university’s teaching score is compared to its national yearly average. |
| **`relative_citations`** | Ratio = `citations / country_year_citations_mean` → How much higher/lower a university’s citation impact is compared to its national yearly average. |

*Purpose:* Adjusts for country and year differences, showing relative performance within the same context.

---

### 4. Standardization (Z-score Normalization)
Applies **Z-score normalization** to selected numeric features to make them comparable on the same scale.

| Column | Meaning |
|---------|----------|
| **`teaching_z`** | Standardized (mean=0, std=1) version of teaching. |
| **`citations_z`** | Standardized version of citations. |
| **`num_students_z`** | Standardized version of university size. |
| **`relative_teaching_z`** | Standardized version of relative teaching. |
| **`relative_citations_z`** | Standardized version of relative citations. |

 *Purpose:* Normalizes values for fair comparison and analytical consistency.

 *Formula used:*  
\[
z = \frac{x - \mu}{\sigma}
\]  
where \( \mu \) = mean and \( \sigma \) = standard deviation.

---

## Output Summary

- All numeric values are **rounded to two decimals**.  
- Unnecessary Z-columns (`cwur_score_z`, `student_staff_ratio_z`, `relative_cwur_score_z`) are **excluded**.  
- Keeps all existing columns (e.g., `rank_gap`, `global_influence_index`, etc.).  

---

## Input & Output Files

| File | Description |
|------|--------------|
| **Input:** `../6th-step-feature_selection_creation/feature_selected_created_university_data.csv` | Dataset from feature selection & creation step |
| **Output:** `university_data_discretized_transformed.csv` | Final dataset after discretization, binarization, and transformation |

---

## Purpose of This Step
This step:
- Makes numeric data easier to interpret,
- Adds context-aware relative comparisons,
- Normalizes values for fair scaling,
- And prepares the dataset for visualization or advanced analytics.


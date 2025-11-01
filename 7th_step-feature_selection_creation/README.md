# 7th Step — Feature Subset Selection & Feature Creation

This step refines the cleaned university dataset by keeping the most relevant columns and adding new, more informative features.  
It prepares the data for discretization and transformation in the next step.

---

##  Changes Made

- Dropped redundant or low-quality CWUR columns:
  - `cwur_national_rank` — duplicated information from global rank  
  - `cwur_broad_impact` — inconsistent or mostly zeros  
  - `cwur_patents` — sparse or unreliable data  

- Added new derived features that capture efficiency and influence metrics.

---

## New Columns and Their Meaning

| Column | Description |
|--------|-------------|
| **`rank_gap`** | Difference between Times and CWUR ranks. Negative = ranked better in Times. |
| **`research_efficiency`** | Research score per student — shows research productivity relative to university size. |
| **`faculty_efficiency`** | Faculty quality adjusted for teaching load (student–staff ratio). |
| **`global_influence_index`** | Combined measure of research and reputation impact using citations and influence scores. |
| **`high_international_ratio`** | Binary flag (1 if >30% of students are international, else 0). |

---

## Output

**File created:**  
`feature_selected_created_university_data.csv`  


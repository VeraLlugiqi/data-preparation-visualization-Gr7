# 5th Step – Data Aggregation (by Country and Year)


This script aggregates a cleaned dataset of university rankings (from THE and CWUR) by **country** and **year**.  
It calculates key statistics and derived metrics that describe each country's average performance across universities.

---

Column rank_gap = world_rank - cwur_world_rank

- Negative values mean **Times** ranked the university better (a smaller rank number).  
- Positive values mean **CWUR** ranked the university better.

#### **Faculty Efficiency**
Measures teaching quality adjusted by the student–staff ratio:

faculty_efficiency = cwur_quality_of_faculty / student_staff_ratio


This shows how efficiently faculty quality scales with the teaching workload.

#### **Global Influence Index**
Combines three related indicators — `citations`, `cwur_influence`, and `cwur_citations` — into one normalized index.

Each column is converted into a **z-score** (standardized within each year):


**Interpretation:**
- Positive → Above-average influence in that year  
- Negative → Below-average influence (normal for z-scores)

 ## Aggregation

The script groups the dataset by **country** and **year**, calculating averages, medians, and best (minimum) ranks for each group.

It includes:

-  **Rank statistics:**  
  - `world_rank_mean`, `world_rank_median`, `best_the_world_rank`  
  - `cwur_world_rank_mean`, `cwur_world_rank_median`, `best_cwur_world_rank`



- **Performance metrics:**  
  - `teaching_mean`, `international_mean`, `citations_mean`, `cwur_score_mean`

- **CWUR components:**  
  - `cwur_quality_of_education_mean`, `cwur_alumni_employment_mean`, `cwur_quality_of_faculty_mean`,  
    `cwur_publications_mean`, `cwur_influence_mean`, `cwur_citations_mean`

- **Derived metrics:**  
  - `rank_gap_mean`, `faculty_efficiency_mean`, `global_influence_index_mean`

- **Student data:**  
  - `total_students_covered`, `avg_students_per_university`, `avg_international_student_share`, `student_staff_ratio_mean`

---

### 5. Rounding and Saving

- All numeric values are rounded to **two decimals** for readability.  
- The script saves the final output file as:



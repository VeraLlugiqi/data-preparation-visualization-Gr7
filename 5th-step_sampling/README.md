# Step 5 – Sampling

This step performs **stratified random sampling** to create a representative subset of the cleaned university dataset.

---

## Objective

The goal of this step is to extract a smaller yet balanced sample from the dataset, ensuring that **each year** is proportionally represented.  
This helps in reducing data size for faster analysis while maintaining fairness across different time periods.

---

## Method Used

**Stratified Random Sampling by Year (20%)**

- The dataset is grouped by the `year` column.
- From each group (year), **20%** of the rows are selected randomly.
- The `random_state=42` parameter ensures reproducibility, so the same random sample is produced every time the code runs.
- The resulting subset is saved as `sampled_dataset.csv`.


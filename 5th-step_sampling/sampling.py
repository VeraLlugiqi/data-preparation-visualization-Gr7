import pandas as pd

# Load the cleaned dataset
df = pd.read_csv("../4th-step-data_cleaning/cleaned_university_data.csv")

# Stratified random sampling by year (20%)
sample = df.groupby('year', group_keys=False).apply(lambda x: x.sample(frac=0.2, random_state=42))
sample.to_csv("dataset_sampled_by_year.csv", index=False)


# Save sample
sample.to_csv("sampled_dataset.csv", index=False)

print(f"Sample size: {len(sample)} rows from {df['year'].nunique()} years")




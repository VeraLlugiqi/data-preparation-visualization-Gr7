import pandas as pd

# Load cleaned dataset
df = pd.read_csv("../4th-step-data_cleaning/cleaned_university_data.csv")

print("----- Aggregation by Country and Year -----")


df.columns = df.columns.str.lower().str.strip()


aggregated = (
    df.groupby(["country", "year"])
    .agg(
        {
            "world_rank": "mean",
            "cwur_world_rank": "mean",
            "teaching": "mean",
            "international": "mean",
            "research": "mean",
            "citations": "mean",
            "num_students": "mean",
            "student_staff_ratio": "mean",
            "international_students": "mean",
            "cwur_quality_of_education": "mean",
            "cwur_alumni_employment": "mean",
            "cwur_quality_of_faculty": "mean",
            "cwur_publications": "sum",
            "cwur_influence": "sum",
            "cwur_citations": "sum",
            "cwur_broad_impact": "sum",
            "cwur_patents": "sum",
            "cwur_score": "mean",
        }
    )
    .reset_index()
)


aggregated = aggregated.round(2)


aggregated.to_csv("aggregated_country_year.csv", index=False)

print(
    "Aggregation by country and year completed and saved as 'aggregated_country_year.csv'"
)

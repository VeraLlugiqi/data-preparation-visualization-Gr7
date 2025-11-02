import pandas as pd
import numpy as np
import os

df = pd.read_csv("../4th_step-data_cleaning/cleaned_university_data.csv")

country_replacements = {"USA": "United States of America"}
df["country"] = df["country"].replace(country_replacements)


df = df.dropna(subset=["country", "year"])

df["rank_gap"] = df["world_rank"] - df["cwur_world_rank"]

df["faculty_efficiency"] = df["cwur_quality_of_faculty"] / df[
    "student_staff_ratio"
].replace({0: np.nan})


def zscore(s):
    return (s - s.mean()) / s.std(ddof=0)


for col in ["citations", "cwur_influence", "cwur_citations"]:
    if col in df.columns:
        df[f"{col}_z"] = df.groupby("year")[col].transform(zscore)

df["global_influence_index"] = df[
    [
        c
        for c in ["citations_z", "cwur_influence_z", "cwur_citations_z"]
        if c in df.columns
    ]
].mean(axis=1)


agg = {
    "world_rank": ["mean", "median", "min"],
    "cwur_world_rank": ["mean", "median", "min"],
    "teaching": "mean",
    "international": "mean",
    "citations": "mean",
    "cwur_score": "mean",
    "num_students": ["sum", "mean"],
    "international_students": "mean",
    "student_staff_ratio": "mean",
    "cwur_quality_of_education": "mean",
    "cwur_alumni_employment": "mean",
    "cwur_quality_of_faculty": "mean",
    "cwur_publications": "mean",
    "cwur_influence": "mean",
    "cwur_citations": "mean",
    "rank_gap": "mean",
    "faculty_efficiency": "mean",
    "global_influence_index": "mean",
}

country_year_summary = df.groupby(["country", "year"]).agg(agg).reset_index()

country_year_summary.columns = [
    "_".join([c for c in col if c]).rstrip("_")
    for col in country_year_summary.columns.values
]

rename_map = {
    "world_rank_min": "the_best_world_rank",
    "cwur_world_rank_min": "the_best_cwur_world_rank",
    "num_students_sum": "total_students_covered",
    "num_students_mean": "avg_students_per_university",
    "international_students_mean": "avg_international_student_share",
}
country_year_summary = country_year_summary.rename(columns=rename_map)

country_year_summary = country_year_summary.round(2)

output_dir = os.getcwd()
country_year_summary.to_csv(
    os.path.join(output_dir, "country_year_summary.csv"), index=False
)

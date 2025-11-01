import pandas as pd
import numpy as np
from pathlib import Path

# Load the cleaned dataset
df = pd.read_csv(Path("../4th-step-data_cleaning/cleaned_university_data.csv"))


to_drop = ["cwur_national_rank", "cwur_broad_impact", "cwur_patents"]
df = df.drop(columns=[c for c in to_drop if c in df.columns], errors="ignore")

# Feature Creation ---
# Rank gap (THE vs CWUR)
df["rank_gap"] = df["world_rank"] - df["cwur_world_rank"]

# Research efficiency (scaled so it’s readable when rounded) 
df["research_efficiency_per_1k"] = (
    df["research"] / df["num_students"].replace({0: np.nan})
) * 1000

# Faculty efficiency
df["faculty_efficiency"] = df["cwur_quality_of_faculty"] / df["student_staff_ratio"].replace({0: np.nan})

# Global influence index 
df["global_influence_index"] = df[["citations", "cwur_influence", "cwur_citations"]].mean(axis=1)

# Highly international universities ( > 30% )
df["high_international_ratio"] = (df["international_students"] > 0.30).astype(int)


df = df.replace([np.inf, -np.inf], np.nan)



out_path = Path("feature_selected_created_university_data.csv")

rounded = df.copy()
if "research_efficiency_per_1k" in rounded.columns:
    rounded["research_efficiency_per_1k"] = rounded["research_efficiency_per_1k"].round(3)
rounded = rounded.round(2)

rounded.to_csv(out_path, index=False)
print(f"💾 Saved: {out_path.resolve()}")

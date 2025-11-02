# 7th–8th steps: Discretization, Binarization, + Transformation (keeps all rows)
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler


in_path = Path("../7th_step-feature-selection-creation/feature_selected_created_university_data.csv")
df = pd.read_csv(in_path)

# STEP 8: DISCRETIZATION & BINARIZATION

def safe_qcut(series, q, labels):
    try:
        return pd.qcut(series, q=q, labels=labels, duplicates="drop")
    except ValueError:
        return pd.cut(series, bins=q, labels=labels, include_lowest=True)

# Teaching and Citations → Low / Medium / High
if "teaching" in df.columns:
    df["teaching_level"] = safe_qcut(df["teaching"], q=3, labels=["Low", "Medium", "High"])

if "citations" in df.columns:
    df["citations_level"] = safe_qcut(df["citations"], q=3, labels=["Low", "Medium", "High"])

# Binarize: Top 100 universities (Times / CWUR)
if "world_rank" in df.columns:
    df["top100_times"] = (df["world_rank"].astype(float) <= 100).astype(int)

if "cwur_world_rank" in df.columns:
    df["top100_cwur"] = (df["cwur_world_rank"].astype(float) <= 100).astype(int)

# Do NOT recreate high_international_ratio if it already exists
if "high_international_ratio" not in df.columns and "international_students" in df.columns:
    df["high_international_ratio"] = (df["international_students"] > 0.30).astype(int)


# STEP 8: TRANSFORMATION (Contextual + Scaling)


# A) Add contextual means per country-year
group_keys = [c for c in ["country", "year"] if c in df.columns and df[c].notna().all()]

def add_group_mean(col):
    name = f"country_year_{col}_mean"
    if col in df.columns and len(group_keys) == 2:
        df[name] = df.groupby(group_keys)[col].transform("mean")
        return name
    return None

context_cols = []
for base_col in ["teaching", "citations", "cwur_score"]:
    ctx = add_group_mean(base_col)
    if ctx:
        context_cols.append(ctx)

# B) Relative-to-context ratios
def add_relative(col, ctx_col):
    name = f"relative_{col}"
    if col in df.columns and ctx_col in df.columns:
        df[name] = df[col] / df[ctx_col].replace({0: np.nan})
        return name
    return None

relative_cols = []
for col, ctx in [
    ("teaching", "country_year_teaching_mean"),
    ("citations", "country_year_citations_mean"),
    ("cwur_score", "country_year_cwur_score_mean"),
]:
    rn = add_relative(col, ctx)
    if rn:
        relative_cols.append(rn)

# C) Standardize (Z-score scaling)
to_scale = [c for c in [
    "teaching", "citations", "num_students",
    "relative_teaching", "relative_citations"
] if c in df.columns]

if to_scale:
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[to_scale].astype(float))
    for i, c in enumerate(to_scale):
        df[f"{c}_z"] = scaled[:, i]

# Replace infs, round numeric columns to 2 decimals
df = df.replace([np.inf, -np.inf], np.nan)
df = df.round(2)


out_path = Path("university_data_discretized_transformed.csv")
df.to_csv(out_path, index=False)

print("Discretization, binarization, and transformations complete.")
print("Z-scored columns:", [f"{c}_z" for c in to_scale])

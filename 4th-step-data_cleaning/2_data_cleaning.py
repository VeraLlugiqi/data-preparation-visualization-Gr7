import pandas as pd
import numpy as np

df = pd.read_csv(r"../3rd_step-filtering_years/v1/filtered_university_data.csv")

print("----- Faza e pastrimit dhe imputimit të avancuar -----")

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

cols_to_remove = ['total_score', 'female_male_percent', 'income']
cols_removed = [col for col in cols_to_remove if col in df.columns]
df = df.drop(columns=cols_removed)
print(f"🗑️ Kolonat e larguara (shumë mungesa): {cols_removed}\n")

if 'world_rank' in df.columns and 'cwur_world_rank' in df.columns:
    before_fill_world = df['world_rank'].isna().sum()
    before_fill_cwur = df['cwur_world_rank'].isna().sum()

    df['world_rank'] = df['world_rank'].fillna(df['cwur_world_rank'])
    df['cwur_world_rank'] = df['cwur_world_rank'].fillna(df['world_rank'])

    after_fill_world = df['world_rank'].isna().sum()
    after_fill_cwur = df['cwur_world_rank'].isna().sum()

    print(f"✅ 'world_rank' u plotësua me 'cwur_world_rank' për {before_fill_world - after_fill_world} raste")
    print(f"✅ 'cwur_world_rank' u plotësua me 'world_rank' për {before_fill_cwur - after_fill_cwur} raste\n")

#  Imputimi me medianë për çdo universitet
numeric_cols = df.select_dtypes(include=[np.number]).columns
print("📊 Fillimi i imputimit për çdo universitet...")
df[numeric_cols] = df.groupby('university_name')[numeric_cols].transform(lambda x: x.fillna(x.median()))

# Imputimi global me medianë për kolonat që kanë ende mungesa
for col in numeric_cols:
    missing_before = df[col].isna().sum()
    if missing_before > 0:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"⚙️ Kolona '{col}' u plotësua me medianën ({median_val:.2f}) për {missing_before} raste që mungonin pas imputimit me medianë të brendshme")

# Konvertimi i të gjitha kolonave që fillojnë me 'cwur_' në integer (pa humbje të NaN)
cwur_cols = [col for col in df.columns if col.startswith('cwur_')]
for col in cwur_cols:
    df[col] = df[col].round().astype('Int64')
print(f"\n🔢 Kolonat e konvertuara në integer: {cwur_cols}\n")

# Heq rreshtat që janë bosh në të dy renditjet
df = df.dropna(subset=['world_rank', 'cwur_world_rank'], how='all')

df.to_csv("cleaned_university_data.csv", index=False)

print("\n📋 Përmbledhje pas pastrimit:")
print(df.isnull().sum())

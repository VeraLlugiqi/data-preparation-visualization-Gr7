import pandas as pd
import numpy as np
from pathlib import Path

print("Hapi 10: Mënjanimi i Zbulimeve Jo të Sakta")
print("=" * 70)

input_path = Path("C:/Users/NB/Desktop/Master/Data preparation and visualization/Faza 1/data-preparation-visualization-Gr7/8th-step-discret_binar_transform/university_data_discretized_transformed.csv")

if not input_path.exists():
    print(f"Gabim: Skedari {input_path} nuk u gjet!")
    print("Sigurohuni që keni ekzekutuar Hapin 8 më parë.")
    exit(1)

df = pd.read_csv(input_path)
print(f"\nDataset i ngarkuar: {len(df)} rreshta, {len(df.columns)} kolona")

print("\n1. KONTROLLIMI I VLERAVE NEGATIVE OSE ZERO")
print("-" * 70)

invalid_cols = [
    "international",
    "research",
    "citations",
    "num_students",
    "student_staff_ratio",
]

for col in invalid_cols:
    if col in df.columns:
        invalid_rows = df[df[col] <= 0]
        if len(invalid_rows) > 0:
            print(f"Kolona '{col}' ka {len(invalid_rows)} vlera jo të sakta (<= 0).")

df_clean = df.copy()
for col in invalid_cols:
    if col in df_clean.columns:
        before = len(df_clean)
        df_clean = df_clean[df_clean[col] > 0]
        removed = before - len(df_clean)
        if removed > 0:
            print(f"  Hequr {removed} rreshta për shkak të kolonës '{col}'")

print("\n2. KONTROLLIMI I VLERAVE TË PAMUNDURA PËR INTERNATIONAL_STUDENTS")
print("-" * 70)

if "international_students" in df_clean.columns:
    invalid_int_students = df_clean[df_clean["international_students"] > 1]
    print(f"Vlera >1 në international_students: {len(invalid_int_students)}")
    
    if len(invalid_int_students) > 0:
        before = len(df_clean)
        df_clean = df_clean[df_clean["international_students"] <= 1]
        removed = before - len(df_clean)
        print(f"  Hequr {removed} rreshta me international_students > 1")

print("\n3. HEQJA E RRESHTAVE DUPLIKATË")
print("-" * 70)

before = len(df_clean)
duplicates = df_clean.duplicated().sum()
print(f"Numri i rreshtave të përsëritur: {duplicates}")

if duplicates > 0:
    df_clean = df_clean.drop_duplicates()
    print(f"  Hequr {duplicates} rreshta duplikatë")

print("\n4. KONTROLLIMI I VLERAVE NULL (MUNGESË)")
print("-" * 70)

missing_per_col = df_clean.isna().sum()
total_missing = missing_per_col.sum()
print(f"Total vlera munguese: {total_missing}")

if total_missing > 0:
    cols_with_missing = missing_per_col[missing_per_col > 0]
    print(f"\nKolonat me vlera munguese:")
    for col, count in cols_with_missing.items():
        pct = (count / len(df_clean)) * 100
        print(f"  {col}: {count} ({pct:.2f}%)")
    
    print("\nHeqja e rreshtave ku mungojnë të dhëna kritike...")
    before = len(df_clean)
    
    critical_cols = ['university_name', 'country', 'year', 'world_rank', 'teaching', 'research']
    critical_cols = [col for col in critical_cols if col in df_clean.columns]
    
    df_clean = df_clean.dropna(subset=critical_cols)
    removed = before - len(df_clean)
    print(f"  Hequr {removed} rreshta me të dhëna kritike munguese")

print("\n5. KONTROLLIMI I VLERAVE LOGJIKE (RENDITJE)")
print("-" * 70)

if 'world_rank' in df_clean.columns:
    invalid_ranks = df_clean[df_clean['world_rank'] <= 0]
    if len(invalid_ranks) > 0:
        print(f"Renditje <= 0: {len(invalid_ranks)}")
        df_clean = df_clean[df_clean['world_rank'] > 0]

if 'cwur_world_rank' in df_clean.columns:
    invalid_cwur = df_clean[df_clean['cwur_world_rank'] <= 0]
    if len(invalid_cwur) > 0:
        print(f"Renditje CWUR <= 0: {len(invalid_cwur)}")
        df_clean = df_clean[df_clean['cwur_world_rank'] > 0]

print("\n6. REZULTATI PËRFUNDIMTAR")
print("=" * 70)

total_removed = len(df) - len(df_clean)
removal_percentage = (total_removed / len(df)) * 100

print(f"Dataset origjinal: {len(df)} rreshta")
print(f"Dataset i pastër: {len(df_clean)} rreshta")
print(f"Total i hequr: {total_removed} rreshta ({removal_percentage:.2f}%)")

output_path = Path("university_data_final_cleaned.csv")
df_clean.to_csv(output_path, index=False)
print(f"\nDataset i pastër i ruajtur: {output_path}")

print("\nStatistika përmbledhëse për kolonat kryesore:")
summary_cols = ['world_rank', 'teaching', 'research', 'citations', 'num_students']
summary_cols = [col for col in summary_cols if col in df_clean.columns]
print(df_clean[summary_cols].describe().round(2))

print("\n" + "=" * 70)
print("Hapi 10 i kompletuar me sukses!")


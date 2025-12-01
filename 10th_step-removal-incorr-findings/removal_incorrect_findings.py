import pandas as pd

print("=" * 70)
print("KRAHASIMI I METODAVE TË DETEKTIMIT TË PËRJASHTUESVE")
print("Z-Score vs IQR vs Isolation Forest")
print("=" * 70)

# 1. Leximi i fajllave të outliers dhe datasetit origjinal
# RREGULLO PATH-IN NËSE DUHET (p.sh. '../final_dataset.csv')
df_z = pd.read_csv('../9th_step-outlier_detection/zscore/outliers_zscore.csv')
df_iqr = pd.read_csv('../9th_step-outlier_detection/iqr/outliers_iqr.csv')
df_if = pd.read_csv('../9th_step-outlier_detection/isolation_forest/outliers_isolation_forest.csv')
df_full = pd.read_csv('../final_dataset.csv')

# 2. Krijojmë një ID unike për çdo rresht: universitet | country | year
def make_id(df):
    return (
        df['university_name'].astype(str) + " | " +
        df['country'].astype(str) + " | " +
        df['year'].astype(str)
    )

df_z['entity_id'] = make_id(df_z)
df_iqr['entity_id'] = make_id(df_iqr)
df_if['entity_id'] = make_id(df_if)
df_full['entity_id'] = make_id(df_full)

# 3. Marrim set-in unik të ID-ve për secilën metodë
set_z = set(df_z['entity_id'].unique())
set_iqr = set(df_iqr['entity_id'].unique())
set_if = set(df_if['entity_id'].unique())

print(f"Outliers (Z-score): {len(set_z)} raste unike")
print(f"Outliers (IQR): {len(set_iqr)} raste unike")
print(f"Outliers (Isolation Forest): {len(set_if)} raste unike\n")

# 4. Krijojmë një listë me të gjitha ID-të që janë outlier në të paktën 1 metodë
all_ids = sorted(set_z | set_iqr | set_if)

rows = []
for eid in all_ids:
    in_z = int(eid in set_z)
    in_i = int(eid in set_iqr)
    in_if = int(eid in set_if)
    total = in_z + in_i + in_if

    rows.append({
        'entity_id': eid,
        'in_zscore': in_z,
        'in_iqr': in_i,
        'in_isolation_forest': in_if,
        'methods_flagged': total
    })

comparison_df = pd.DataFrame(rows)

# 5. Ndahet entity_id përsëri në kolonat origjinale për lehtësi
comparison_df[['university_name', 'country', 'year']] = (
    comparison_df['entity_id'].str.split(' \| ', expand=True)
)
comparison_df['year'] = comparison_df['year'].astype(int)

# 6. Outliers të "vërtetë" = të kapur nga >= 2 metoda
consensus_df = comparison_df[comparison_df['methods_flagged'] >= 2].copy()
false_df = comparison_df[comparison_df['methods_flagged'] == 1].copy()

print("PËRMBLEDHJE:")
print("-" * 70)
print(f"Totali i entiteteve (uni+vend+vit) që janë outlier në të paktën një metodë: {len(comparison_df)}")
print(f"Outliers 'të vërtetë' (>=2 metoda): {len(consensus_df)}")
print(f"Outliers të dyshimtë / jo të sakta (vetëm 1 metodë): {len(false_df)}\n")

# 7. Ruajmë fajllat e përmbledhjes
comparison_df.to_csv('outliers_all_methods_comparison.csv', index=False)
consensus_df.to_csv('outliers_consensus.csv', index=False)
false_df.to_csv('outliers_false_detected.csv', index=False)

print("✓ Ruajtur 'outliers_all_methods_comparison.csv'")
print("✓ Ruajtur 'outliers_consensus.csv' (>= 2 metoda)")
print("✓ Ruajtur 'outliers_false_detected.csv' (= 1 metodë)\n")

# 8. Largimi i outliers nga final_dataset.csv
#    (këtu po heqim OUTLIERS 'TË VËRTETË' = ata që dalin në >= 2 metoda)

consensus_ids = set(consensus_df['entity_id'])

df_full['is_outlier_consensus'] = df_full['entity_id'].isin(consensus_ids).astype(int)

# Dataset i pastruar: pa outliers të konsensusit
df_clean = df_full[df_full['is_outlier_consensus'] == 0].copy()

# Hiq kolonën teknike entity_id në datasetin e pastruar
df_clean = df_clean.drop(columns=['entity_id', 'is_outlier_consensus'])

# Ruaj datasetin e pastruar
df_clean.to_csv('final_dataset_no_outliers.csv', index=False)

# Opsionale: ruaj edhe datasetin me flag për referencë
df_full.to_csv('final_dataset_with_outlier_flags.csv', index=False)

print("DATASET I PASTRUAR:")
print("-" * 70)
print(f"Rreshta origjinalë në final_dataset: {len(df_full)}")
print(f"Rreshta të hequr si outliers 'konsensus': {len(consensus_ids)} (sipas entity_id)")
print(f"Rreshta të mbetur në 'final_dataset_no_outliers.csv': {len(df_clean)}")
print("\n✓ Ruajtur 'final_dataset_no_outliers.csv' (pa outliers konsensus)")
print("✓ Ruajtur 'final_dataset_with_outlier_flags.csv' (me kolonë is_outlier_consensus)")
print("=" * 70)





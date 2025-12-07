import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Leximi i datasetit
df = pd.read_csv('../../final_dataset.csv')

# Zgjedhja e kolonave numerike (përjashtojmë flagjet binare dhe identifikuesit)
exclude_cols = ['year', 'world_rank', 'cwur_world_rank', 'top100_times', 'top100_cwur',
                'high_international_ratio', 'cwur_quality_of_education', 'cwur_alumni_employment',
                'cwur_quality_of_faculty', 'cwur_publications', 'cwur_influence', 'cwur_citations']
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
numeric_cols = [col for col in numeric_cols if col not in exclude_cols]

print(f"Duke analizuar {len(numeric_cols)} kolona numerike për përjashtues me metodën Z-Score...")
print(f"Threshold: |Z-score| > 3\n")

# Dictionary për të ruajtur përjashtuesit
outliers_data = []
outlier_counts = {}

# Detektimi i përjashtuesve për çdo kolonë numerike
for col in numeric_cols:
    col_data = df[col].dropna()

    mean_val = col_data.mean()
    std_val = col_data.std()

    if std_val == 0:
        print(f"Kolona '{col}': U anashkalua (std = 0)")
        outlier_counts[col] = 0
        continue

    z_scores = np.abs((df[col] - mean_val) / std_val)

    outlier_mask = z_scores > 3
    outlier_indices = df[outlier_mask].index.tolist()
    outlier_counts[col] = len(outlier_indices)

    for idx in outlier_indices:
        outliers_data.append({
            'row_index': idx,
            'university_name': df.loc[idx, 'university_name'],
            'country': df.loc[idx, 'country'],
            'year': df.loc[idx, 'year'],
            'feature': col,
            'value': df.loc[idx, col],
            'z_score': z_scores[idx],
            'mean': mean_val,
            'std': std_val
        })

    print(f"Kolona '{col}': {outlier_counts[col]} përjashtues")
    print(f"  Mean: {mean_val:.2f}, Std: {std_val:.2f}")
    if len(outlier_indices) > 0:
        print(f"  Max |Z-score|: {z_scores[outlier_indices].max():.2f}")
    print()

# Ruaje DataFrame – FIXED PATH
outliers_df = pd.DataFrame(outliers_data)
outliers_df.to_csv('outliers_zscore.csv', index=False)
print(f"\n✓ Ruajtur {len(outliers_df)} përjashtues në 'outliers_zscore.csv'")

# Përmbledhje për kolonë
summary_df = pd.DataFrame([
    {
        'feature': col,
        'outlier_count': count,
        'percentage': (count / len(df)) * 100
    }
    for col, count in outlier_counts.items()
]).sort_values('outlier_count', ascending=False)

summary_df.to_csv('outliers_zscore_summary.csv', index=False)
print(f"✓ Ruajtur përmbledhje në 'outliers_zscore_summary.csv'\n")

# Vizualizime — FIXED PATHS
print("Duke krijuar vizualizime...")

# 1. Histogram i outliers per kolonë
plt.figure(figsize=(12, 6))
plt.bar(summary_df['feature'], summary_df['outlier_count'], color='steelblue')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Feature')
plt.ylabel('Number of Outliers')
plt.title('Outlier Count per Feature (Z-Score Method, |Z| > 3)')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('outliers_zscore_counts.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Ruajtur 'outliers_zscore_counts.png'")

# 2. Distribucione për kolonat me më shumë outliers
top_outlier_cols = summary_df[summary_df['outlier_count'] > 0].head(8)['feature'].tolist()

if len(top_outlier_cols) > 0:
    fig, axes = plt.subplots(4, 2, figsize=(14, 16))
    axes = axes.ravel()

    for i, col in enumerate(top_outlier_cols):
        ax = axes[i]
        col_data = df[col].dropna()
        z_scores = np.abs((col_data - col_data.mean()) / col_data.std())

        ax.hist(z_scores, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
        ax.axvline(x=3, color='red', linestyle='--', linewidth=2, label='Threshold (|Z| = 3)')
        ax.set_xlabel('|Z-Score|')
        ax.set_ylabel('Frequency')
        ax.set_title(f'{col}\n({outlier_counts[col]} outliers)', fontsize=10)
        ax.legend()
        ax.grid(True, alpha=0.3)

    for i in range(len(top_outlier_cols), len(axes)):
        fig.delaxes(axes[i])

    plt.tight_layout()
    plt.savefig('outliers_zscore_distributions.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Ruajtur 'outliers_zscore_distributions.png'")

# 3. Top 10 universitete me më shumë outliers
if len(outliers_df) > 0:
    university_outlier_counts = (
        outliers_df.groupby(['university_name', 'country'])
        .size()
        .reset_index(name='outlier_count')
        .sort_values('outlier_count', ascending=False)
        .head(10)
    )

    plt.figure(figsize=(12, 6))
    plt.barh(range(len(university_outlier_counts)), university_outlier_counts['outlier_count'], color='coral')
    plt.yticks(
        range(len(university_outlier_counts)),
        [f"{row['university_name'][:30]} ({row['country']})"
         for _, row in university_outlier_counts.iterrows()]
    )
    plt.xlabel('Number of Outlier Features')
    plt.title('Top 10 Universities with Most Outlier Features (Z-Score Method)')
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('outliers_zscore_top_universities.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Ruajtur 'outliers_zscore_top_universities.png'")

# 4. Heatmap për 10 universitetet me më shumë outliers
if len(outliers_df) > 0:
    top_unis = outliers_df.groupby('university_name').size().nlargest(10).index.tolist()
    top_features = summary_df[summary_df['outlier_count'] > 0].head(10)['feature'].tolist()

    z_matrix = pd.DataFrame(index=top_unis, columns=top_features)

    for uni in top_unis:
        for feat in top_features:
            uni_data = df[df['university_name'] == uni]
            if len(uni_data) > 0:
                val = uni_data[feat].iloc[0]
                mean_val = df[feat].mean()
                std_val = df[feat].std()
                if std_val > 0:
                    z_matrix.loc[uni, feat] = (val - mean_val) / std_val

    z_matrix = z_matrix.astype(float)

    plt.figure(figsize=(12, 8))
    sns.heatmap(z_matrix, annot=True, fmt='.1f', cmap='RdYlBu_r', center=0,
                cbar_kws={'label': 'Z-Score'}, linewidths=0.5)
    plt.title('Z-Scores for Top Outlier Universities and Features')
    plt.xlabel('Feature')
    plt.ylabel('University')
    plt.tight_layout()
    plt.savefig('outliers_zscore_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Ruajtur 'outliers_zscore_heatmap.png'")

print("\n" + "=" * 60)
print("PËRMBLEDHJE E DETEKTIMIT ME METODËN Z-SCORE")
print("=" * 60)
print(f"Total përjashtues të detektuar: {len(outliers_df)}")

if len(outliers_df) > 0:
    print(f"Universitete unike me përjashtues: {outliers_df['university_name'].nunique()}")
    print("Kolona me më shumë përjashtues:")
    for _, row in summary_df[summary_df['outlier_count'] > 0].head(5).iterrows():
        print(f"  - {row['feature']}: {int(row['outlier_count'])} ({row['percentage']:.1f}%)")
else:
    print("Asnjë përjashtues i detektuar me threshold |Z| > 3")

print("=" * 60)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Leximi i datasetit
df = pd.read_csv('../final_dataset.csv')

# Zgjedhja e kolonave numerike (përjashtojmë flagjet binare dhe identifikuesit)
exclude_cols = ['year', 'world_rank', 'cwur_world_rank', 'top100_times', 'top100_cwur', 
                'high_international_ratio', 'cwur_quality_of_education', 'cwur_alumni_employment',
                'cwur_quality_of_faculty', 'cwur_publications', 'cwur_influence', 'cwur_citations']
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
numeric_cols = [col for col in numeric_cols if col not in exclude_cols]

print(f"Duke analizuar {len(numeric_cols)} kolona numerike për përjashtues me metodën IQR...")
print(f"Kolona: {', '.join(numeric_cols)}\n")

# Dictionary për të ruajtur përjashtuesit
outliers_data = []
outlier_counts = {}

# Detektimi i përjashtuesve për çdo kolonë numerike
for col in numeric_cols:
    # Heq NaN values
    col_data = df[col].dropna()
    
    Q1 = col_data.quantile(0.25)
    Q3 = col_data.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Gjej rreshtat që janë përjashtues
    outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
    outlier_indices = df[outlier_mask].index.tolist()
    
    # Ruaj informacionin
    outlier_counts[col] = len(outlier_indices)
    
    for idx in outlier_indices:
        outliers_data.append({
            'row_index': idx,
            'university_name': df.loc[idx, 'university_name'],
            'country': df.loc[idx, 'country'],
            'year': df.loc[idx, 'year'],
            'feature': col,
            'value': df.loc[idx, col],
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'Q1': Q1,
            'Q3': Q3,
            'IQR': IQR
        })
    
    print(f"Kolona '{col}': {outlier_counts[col]} përjashtues")
    print(f"  Range: [{lower_bound:.2f}, {upper_bound:.2f}]")
    print(f"  Q1: {Q1:.2f}, Q3: {Q3:.2f}, IQR: {IQR:.2f}\n")

# Krijo DataFrame dhe ruaj në CSV
outliers_df = pd.DataFrame(outliers_data)
outliers_df.to_csv('outliers_iqr.csv', index=False)
print(f"\n✓ Ruajtur {len(outliers_df)} detaje përjashtuesish në 'outliers_iqr.csv'")

# Krijo një përmbledhje të përjashtuesve për kolonë
summary_df = pd.DataFrame([
    {
        'feature': col,
        'outlier_count': count,
        'percentage': (count / len(df)) * 100
    }
    for col, count in outlier_counts.items()
]).sort_values('outlier_count', ascending=False)

summary_df.to_csv('outliers_iqr_summary.csv', index=False)
print(f"✓ Ruajtur përmbledhje në 'outliers_iqr_summary.csv'\n")

# Vizualizime: Boxplots për kolonat me më shumë përjashtues
print("Duke krijuar vizualizime...")
top_outlier_cols = summary_df.head(8)['feature'].tolist()

fig, axes = plt.subplots(4, 2, figsize=(14, 16))
axes = axes.ravel()

for i, col in enumerate(top_outlier_cols):
    ax = axes[i]
    df.boxplot(column=col, ax=ax)
    ax.set_title(f'{col}\n({outlier_counts[col]} outliers)', fontsize=10)
    ax.set_ylabel('Value')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outliers_iqr_boxplots.png', dpi=300, bbox_inches='tight')
print("✓ Ruajtur boxplots në 'outliers_iqr_boxplots.png'")
plt.close()

# Histogram i numrit të përjashtuesve për kolonë
plt.figure(figsize=(12, 6))
plt.bar(summary_df['feature'], summary_df['outlier_count'])
plt.xticks(rotation=45, ha='right')
plt.xlabel('Feature')
plt.ylabel('Number of Outliers')
plt.title('Outlier Count per Feature (IQR Method)')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('outliers_iqr_counts.png', dpi=300, bbox_inches='tight')
print("✓ Ruajtur histogram në 'outliers_iqr_counts.png'")
plt.close()

# Top 10 universitete me më shumë përjashtues
university_outlier_counts = outliers_df.groupby(['university_name', 'country']).size().reset_index(name='outlier_count')
university_outlier_counts = university_outlier_counts.sort_values('outlier_count', ascending=False).head(10)

plt.figure(figsize=(12, 6))
plt.barh(range(len(university_outlier_counts)), university_outlier_counts['outlier_count'])
plt.yticks(range(len(university_outlier_counts)), 
           [f"{row['university_name'][:30]} ({row['country']})" 
            for _, row in university_outlier_counts.iterrows()])
plt.xlabel('Number of Outlier Features')
plt.title('Top 10 Universities with Most Outlier Features (IQR Method)')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('outliers_iqr_top_universities.png', dpi=300, bbox_inches='tight')
print("✓ Ruajtur top universities në 'outliers_iqr_top_universities.png'")
plt.close()

print("\n" + "="*60)
print("PËRMBLEDHJE E DETEKTIMIT ME METODËN IQR")
print("="*60)
print(f"Total përjashtues të detektuar: {len(outliers_df)}")
print(f"Universitete unike me përjashtues: {outliers_df['university_name'].nunique()}")
print(f"Kolona me më shumë përjashtues:")
for _, row in summary_df.head(5).iterrows():
    print(f"  - {row['feature']}: {int(row['outlier_count'])} ({row['percentage']:.1f}%)")
print("="*60)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Leximi i datasetit
df = pd.read_csv('../../final_dataset.csv')

print("DETEKTIMI I PËRJASHTUESVE ME ISOLATION FOREST (Multivariate)")
print("="*60)

# Zgjedhja e kolonave numerike për analiza multivariate
feature_cols = [
    'teaching', 'international', 'research', 'citations',
    'num_students', 'student_staff_ratio', 'international_students',
    'cwur_score', 'rank_gap', 'research_efficiency_per_1k',
    'faculty_efficiency', 'global_influence_index',
    'relative_teaching', 'relative_citations', 'relative_cwur_score'
]

# Heq rreshta me NaN në këto kolona
df_clean = df[feature_cols + ['university_name', 'country', 'year']].dropna()
print(f"Dataset pas heqjes së NaN: {len(df_clean)} rreshta\n")

# Standardizim i të dhënave
X = df_clean[feature_cols].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apliko Isolation Forest
print("Duke trajnuar modelin Isolation Forest...")
iso_forest = IsolationForest(
    contamination=0.1,
    random_state=42,
    n_estimators=100
)

predictions = iso_forest.fit_predict(X_scaled)
anomaly_scores = iso_forest.score_samples(X_scaled)

df_clean['is_outlier'] = predictions
df_clean['anomaly_score'] = anomaly_scores

# Gjej outliers dhe inliers
outliers_df = df_clean[df_clean['is_outlier'] == -1].copy()
inliers_df = df_clean[df_clean['is_outlier'] == 1].copy()

print(f"✓ Trajnim i përfunduar")
print(f"  Outliers të detektuar: {len(outliers_df)} ({len(outliers_df)/len(df_clean)*100:.1f}%)")
print(f"  Inliers: {len(inliers_df)} ({len(inliers_df)/len(df_clean)*100:.1f}%)\n")

# Ruaj rezultatet – FIXED PATHS
outliers_result = outliers_df[['university_name', 'country', 'year', 'anomaly_score'] + feature_cols].copy()
outliers_result = outliers_result.sort_values('anomaly_score')
outliers_result.to_csv('outliers_isolation_forest.csv', index=False)
print(f"✓ Ruajtur {len(outliers_result)} përjashtues në 'outliers_isolation_forest.csv'\n")

print("ANALIZA E OUTLIERS:")
print("-" * 60)

# Outliers sipas shtetit
country_counts = outliers_df['country'].value_counts().head(10)
print("\nTop 10 shtete me më shumë outliers:")
for country, count in country_counts.items():
    print(f"  {country}: {count}")

# Outliers sipas vitit
year_counts = outliers_df['year'].value_counts().sort_index()
print("\nOutliers sipas vitit:")
for year, count in year_counts.items():
    print(f"  {year}: {count}")

# VIZUALIZIME — FIXED PATHS
print("\nDuke krijuar vizualizime...")

# 1. Distribucion i anomaly scores
plt.figure(figsize=(12, 6))
plt.hist(inliers_df['anomaly_score'], bins=50, alpha=0.6, label='Inliers', color='green')
plt.hist(outliers_df['anomaly_score'], bins=50, alpha=0.6, label='Outliers', color='red')
plt.xlabel('Anomaly Score')
plt.ylabel('Frequency')
plt.title('Distribution of Anomaly Scores (Isolation Forest)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('outliers_isolation_forest_scores.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Ruajtur 'outliers_isolation_forest_scores.png'")

# 2. Top 20 outliers
top_outliers = outliers_result.head(20)

plt.figure(figsize=(12, 8))
plt.barh(range(len(top_outliers)), top_outliers['anomaly_score'], color='crimson')
plt.yticks(range(len(top_outliers)),
           [f"{row['university_name'][:25]} ({row['country']})"
            for _, row in top_outliers.iterrows()])
plt.xlabel('Anomaly Score (more negative = more anomalous)')
plt.title('Top 20 Most Anomalous Universities (Isolation Forest)')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('outliers_isolation_forest_top20.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Ruajtur 'outliers_isolation_forest_top20.png'")

# 3. Scatter plots
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

scatter_pairs = [
    ('teaching', 'research'),
    ('citations', 'num_students'),
    ('research_efficiency_per_1k', 'faculty_efficiency'),
    ('relative_teaching', 'relative_citations')
]

for idx, (feat1, feat2) in enumerate(scatter_pairs):
    ax = axes[idx // 2, idx % 2]
    ax.scatter(inliers_df[feat1], inliers_df[feat2], c='blue', alpha=0.3, s=20, label='Inliers')
    ax.scatter(outliers_df[feat1], outliers_df[feat2], c='red', alpha=0.7, s=50, marker='x', label='Outliers')
    ax.set_xlabel(feat1)
    ax.set_ylabel(feat2)
    ax.set_title(f'{feat1} vs {feat2}')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outliers_isolation_forest_scatter.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Ruajtur 'outliers_isolation_forest_scatter.png'")

# 4. Heatmap comparison
comparison_data = {
    'Outliers': outliers_df[feature_cols].mean(),
    'Inliers': inliers_df[feature_cols].mean()
}
comparison_df = pd.DataFrame(comparison_data).T
comparison_normalized = (comparison_df - comparison_df.mean()) / comparison_df.std()

plt.figure(figsize=(14, 4))
sns.heatmap(comparison_normalized, annot=True, fmt='.2f', cmap='RdYlGn_r',
            center=0, cbar_kws={'label': 'Normalized Mean'}, linewidths=0.5)
plt.title('Feature Means: Outliers vs Inliers (Normalized)')
plt.xlabel('Feature')
plt.ylabel('Group')
plt.tight_layout()
plt.savefig('outliers_isolation_forest_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Ruajtur 'outliers_isolation_forest_comparison.png'")

# 5. Outliers by country
plt.figure(figsize=(12, 6))
country_counts.plot(kind='bar', color='darkorange')
plt.xlabel('Country')
plt.ylabel('Number of Outliers')
plt.title('Outlier Count by Country (Top 10)')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('outliers_isolation_forest_by_country.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Ruajtur 'outliers_isolation_forest_by_country.png'")

# Statistical summary — FIXED PATH
summary_stats = {
    'total_records': len(df_clean),
    'outliers_detected': len(outliers_df),
    'outliers_percentage': (len(outliers_df) / len(df_clean)) * 100,
    'mean_anomaly_score_outliers': outliers_df['anomaly_score'].mean(),
    'mean_anomaly_score_inliers': inliers_df['anomaly_score'].mean(),
    'min_anomaly_score': df_clean['anomaly_score'].min(),
    'max_anomaly_score': df_clean['anomaly_score'].max(),
    'features_used': len(feature_cols)
}

summary_df = pd.DataFrame([summary_stats])
summary_df.to_csv('outliers_isolation_forest_summary.csv', index=False)
print("✓ Ruajtur 'outliers_isolation_forest_summary.csv'")

print("\n" + "="*60)
print("PËRMBLEDHJE E DETEKTIMIT ME ISOLATION FOREST")
print("="*60)
print(f"Total rreshta të analizuara: {len(df_clean)}")
print(f"Outliers të detektuar: {len(outliers_df)} ({len(outliers_df)/len(df_clean)*100:.1f}%)")
print(f"Karakteristika të përdorura: {len(feature_cols)}")
print(f"Mean anomaly score (outliers): {outliers_df['anomaly_score'].mean():.4f}")
print(f"Mean anomaly score (inliers): {inliers_df['anomaly_score'].mean():.4f}")
print(f"\nTop 5 universitete më anomale:")
for i, (_, row) in enumerate(outliers_result.head(5).iterrows(), 1):
    print(f"  {i}. {row['university_name']} ({row['country']}, {int(row['year'])}) - Score: {row['anomaly_score']:.4f}")
print("="*60)

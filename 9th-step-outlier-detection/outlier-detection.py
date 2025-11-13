import pandas as pd

# Leximi i datasetit
df = pd.read_csv('../final_dataset.csv')

# Zgjedhja e kolonave numerike
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

outliers = {}

# Detektimi i përjashtuesve për çdo kolonë numerike
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Gjej rreshtat që janë përjashtues
    outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
    
    outliers[col] = df[col][outlier_mask]

# Printo numrin e përjashtuesve për çdo kolonë
for col in numeric_cols:
    print(f"Kolona '{col}' ka {outliers[col].count()} përjashtues.")


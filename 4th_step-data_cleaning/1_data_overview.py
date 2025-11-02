import pandas as pd


df = pd.read_csv(r"../3rd_step-filtering_years/v1/filtered_university_data.csv")

print("Informata për datasetin:")
print(df.info())
print("\n---------------------------------------\n")


print(f"Numri i rreshtave: {df.shape[0]}")
print(f"Numri i kolonave: {df.shape[1]}")
print("\n---------------------------------------\n")

print("Numri i vlerave që mungojnë për kolonë:")
print(df.isnull().sum().sort_values(ascending=False))
print("\n---------------------------------------\n")

print("Përqindja e vlerave që mungojnë (%):")
missing_percentage = (df.isnull().sum() / len(df)) * 100
print(missing_percentage.sort_values(ascending=False))
print("\n---------------------------------------\n")

duplicates = df.duplicated().sum()
print(f"Numri i rreshtave duplikatë: {duplicates}")
print("\n---------------------------------------\n")

print("Statistika për kolonat numerike:")
print(df.describe())
print("\n---------------------------------------\n")

print("Disa rreshta të parë të datasetit:")
print(df.head())

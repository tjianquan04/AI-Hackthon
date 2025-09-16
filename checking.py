import pandas as pd

# Load dataset (⚠️ use raw string r"" to avoid path errors in Windows)
df = pd.read_csv(r"data\bank_churn_cleaned.csv")

# 1. Quick info about dataset
print("\n📊 Dataset Info:")
print(df.info())

# 2. Show first 5 rows
print("\n👀 First 5 rows:")
print(df.head())

# 3. Show all column names
print("\n📋 Columns in dataset:")
print(df.columns.tolist())

# 4. Check for missing values
print("\n🔎 Missing values per column:")
print(df.isnull().sum())

# 5. For each column, show unique values (for categorical columns) or stats (for numeric columns)
print("\n🔍 Unique values / stats per column:")
for col in df.columns:
    if df[col].dtype == "object":
        print(f"\n➡️ {col} (categorical) unique values:")
        print(df[col].unique())
    else:
        print(f"\n➡️ {col} (numeric) stats:")
        print(df[col].describe())

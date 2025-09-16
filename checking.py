import pandas as pd

df_clean = pd.read_csv("bank_churn_cleaned.csv")

# Total missing values
print("Total missing values:", df_clean.isnull().sum().sum())

# If you want just the columns that have missing values:
missing_cols = df_clean.columns[df_clean.isnull().any()]
if len(missing_cols) == 0:
    print("✅ No missing values in any column")
else:
    print("⚠️ Columns with missing values:")
    print(df_clean[missing_cols].isnull().sum())

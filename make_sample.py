import pandas as pd

# Load your cleaned dataset
df = pd.read_csv(r"D:\AI Hackathon\data\bank_churn_cleaned.csv")

# Drop target column (since we want to predict it)
X = df.drop(columns=["Attrition_Flag"])

# Take 8 sample rows for demo
sample = X.sample(n=8, random_state=42)

# Save as new_customers.csv
sample.to_csv(r"D:\AI Hackathon\data\new_customers.csv", index=False)

print("✅ Created new_customers.csv with 8 sample rows for demo.")

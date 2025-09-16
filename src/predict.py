import pandas as pd
import joblib

# Load model
pipeline = joblib.load("D:\\AI Hackathon\\models\\best_model.pkl")

# Load new customers dataset
new_customers = pd.read_csv("D:\\AI Hackathon\\data\\new_customers.csv")

# Predict churn probabilities
probs = pipeline.predict_proba(new_customers)[:, 1]

# ---- Custom Threshold ----
threshold = 0.35   # lower than default 0.5
y_pred = (probs >= threshold).astype(int)

# Add results to DataFrame
new_customers["Churn_Probability"] = probs.round(3)
new_customers["Predicted_Label"] = y_pred
new_customers["Recommended_Action"] = new_customers["Predicted_Label"].map({
    1: "Offer retention benefits",
    0: "No action needed"
})

# Save output
new_customers.to_csv("predictions_with_actions.csv", index=False)
print("✅ Predictions saved to predictions_with_actions.csv")

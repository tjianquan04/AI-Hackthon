# -----------------------------------------
# Bank Customer Churn Prediction Pipeline
# Works with BankChurners.csv
# -----------------------------------------

# (optional: install if not available locally)
# pip install imbalanced-learn joblib matplotlib seaborn packaging

import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report, RocCurveDisplay, confusion_matrix

# version check for OneHotEncoder
from sklearn import __version__ as sklearn_version
from packaging import version

# 1) Load dataset (adjust path if needed)
df = pd.read_csv(r"D:\AI Hackathon\BankChurners.csv")

# Drop customer ID and weird Naive Bayes columns
df = df.drop(columns=["CLIENTNUM"], errors="ignore")
df = df.drop(columns=[col for col in df.columns if col.startswith("Naive_Bayes_Classifier")], errors="ignore")

print("Dataset shape:", df.shape)
print("Missing values:\n", df.isnull().sum())

# 2) Define features and target
X = df.drop("Attrition_Flag", axis=1)
y = df["Attrition_Flag"]

# Convert target into binary
y = y.map({"Existing Customer": 0, "Attrited Customer": 1})

# 3) Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=42
)

# 4) Identify numeric and categorical columns
numeric_feats = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_feats = X.select_dtypes(include=["object", "category"]).columns.tolist()

if "Attrition_Flag" in categorical_feats:
    categorical_feats.remove("Attrition_Flag")

# 5) Transformers
numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# choose correct OneHotEncoder param depending on sklearn version
if version.parse(sklearn_version) >= version.parse("1.2"):
    onehot = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
else:
    onehot = OneHotEncoder(handle_unknown="ignore", sparse=False)

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", onehot)
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_feats),
    ("cat", categorical_transformer, categorical_feats)
])

# 6) Model pipeline
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

pipeline = ImbPipeline(steps=[
    ("preproc", preprocessor),
    ("smote", SMOTE(random_state=42)),
    ("clf", model)
])

# 7) Fit model
pipeline.fit(X_train, y_train)

# 8) Evaluate
probs = pipeline.predict_proba(X_test)[:, 1]
y_pred = pipeline.predict(X_test)

roc = roc_auc_score(y_test, probs)
print("ROC AUC:", roc)
print(classification_report(y_test, y_pred))

# -----------------------------------------
# SAVE OUTPUTS
# -----------------------------------------

# a) Save cleaned dataset
df.to_csv("bank_churn_cleaned.csv", index=False)

# b) Save evaluation metrics
report = classification_report(y_test, y_pred, output_dict=True)
pd.DataFrame(report).to_csv("model_metrics.csv")

# c) Save trained pipeline
joblib.dump(pipeline, "bank_churn_model.pkl")

# d) Save ROC curve plot
RocCurveDisplay.from_estimator(pipeline, X_test, y_test)
plt.title(f"ROC Curve (AUC={roc:.3f})")
plt.savefig("roc_curve.png")
plt.close()

# e) Save confusion matrix heatmap
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["No Churn", "Churn"],
            yticklabels=["No Churn", "Churn"])
plt.title("Confusion Matrix")
plt.savefig("confusion_matrix.png")
plt.close()

print("✅ Outputs saved: cleaned CSV, metrics CSV, model.pkl, ROC curve, confusion matrix.")

#!/usr/bin/env python3
"""
train.py
Train a churn model from a cleaned CSV and save artifacts:
- models/best_model.pkl
- outputs/model_metrics.csv
- outputs/roc_curve.png
- outputs/confusion_matrix.png
- outputs/X_train_transformed.csv / X_test_transformed.csv
"""

import argparse
import os
import json
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from packaging import version
from sklearn import __version__ as sklearn_version

from sklearn.model_selection import train_test_split, StratifiedKFold, RandomizedSearchCV
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score, average_precision_score,
    classification_report, confusion_matrix, roc_curve
)

import warnings
warnings.filterwarnings("ignore")

def precision_at_k(y_true, y_scores, k=0.05):
    y_true = np.array(y_true)
    kN = max(int(len(y_scores)*k), 1)
    order = np.argsort(y_scores)[::-1][:kN]
    return float(np.mean(y_true[order]))  # fraction of positives among top k

def main(args):
    os.makedirs(args.outdir, exist_ok=True)
    os.makedirs(args.modeldir, exist_ok=True)

    # 1) Load
    df = pd.read_csv(args.data)
    # drop ID if present (won't error if not there)
    df = df.drop(columns=["CLIENTNUM"], errors="ignore")
    # drop any auto Naive Bayes cols if still present
    df = df.drop(columns=[c for c in df.columns if c.startswith("Naive_Bayes_Classifier")], errors="ignore")

    # target
    if "Attrition_Flag" not in df.columns:
        raise ValueError("Expected 'Attrition_Flag' column in cleaned CSV.")
    X = df.drop("Attrition_Flag", axis=1)
    y = df["Attrition_Flag"].map({"Existing Customer": 0, "Attrited Customer": 1})

    # 2) train/test split (stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, stratify=y, random_state=args.random_state
    )

    # 3) features identification
    numeric_feats = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_feats = X.select_dtypes(include=["object", "category"]).columns.tolist()
    # ensure target not listed
    for t in ["Attrition_Flag"]:
        if t in categorical_feats: categorical_feats.remove(t)

    # 4) build transformers
    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    # choose OneHotEncoder param depending on sklearn version
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
    ], remainder="drop")

    # 5) modeling pipeline (imblearn pipeline to include SMOTE)
    clf = RandomForestClassifier(class_weight="balanced", random_state=args.random_state)
    pipeline = ImbPipeline(steps=[
        ("preproc", preprocessor),
        ("smote", SMOTE(random_state=args.random_state)),
        ("clf", clf)
    ])

    # 6) hyperparameter search space (RandomForest)
    param_dist = {
        "clf__n_estimators": [100, 200, 300, 500],
        "clf__max_depth": [None, 6, 12, 20],
        "clf__min_samples_split": [2, 5, 10],
        "clf__min_samples_leaf": [1, 2, 4],
        "clf__max_features": ["sqrt", "log2", None]
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=args.random_state)
    rs = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=param_dist,
        n_iter=args.n_iter,
        scoring="roc_auc",
        cv=cv,
        verbose=2,
        n_jobs=args.n_jobs,
        random_state=args.random_state,
        refit=True
    )

    # 7) fit
    print("Fitting RandomizedSearchCV...")
    rs.fit(X_train, y_train)

    print("Best params:", rs.best_params_)
    best = rs.best_estimator_

    # 8) evaluate on test
    probs = best.predict_proba(X_test)[:, 1]
    y_pred = best.predict(X_test)

    roc = roc_auc_score(y_test, probs)
    pr_auc = average_precision_score(y_test, probs)
    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred)

    # precision@k
    p_at_5 = precision_at_k(y_test, probs, k=0.05)
    p_at_10 = precision_at_k(y_test, probs, k=0.10)

    metrics = {
        "roc_auc": roc,
        "pr_auc": pr_auc,
        "precision_at_5pct": p_at_5,
        "precision_at_10pct": p_at_10,
        "classification_report": report,
        "best_params": rs.best_params_
    }

    # 9) save artifacts
    model_path = os.path.join(args.modeldir, "best_model.pkl")
    joblib.dump(best, model_path)

    # save metrics json & csv
    with open(os.path.join(args.outdir, "model_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    pd.DataFrame(report).transpose().to_csv(os.path.join(args.outdir, "model_metrics.csv"))

    # save roc curve
    fpr, tpr, _ = roc_curve(y_test, probs)
    plt.figure()
    plt.plot(fpr, tpr, label=f"AUC={roc:.3f}")
    plt.plot([0,1],[0,1],"--", color="grey")
    plt.xlabel("FPR"); plt.ylabel("TPR"); plt.title("ROC Curve"); plt.legend(loc="lower right")
    plt.savefig(os.path.join(args.outdir, "roc_curve.png"))
    plt.close()

    # save confusion matrix heatmap
    plt.figure(figsize=(5,4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["No Churn","Churn"], yticklabels=["No Churn","Churn"])
    plt.title("Confusion Matrix")
    plt.savefig(os.path.join(args.outdir, "confusion_matrix.png"))
    plt.close()

    # save transformed train/test sets (column names best-effort)
    preproc = best.named_steps["preproc"]
    X_train_trans = preproc.transform(X_train)
    X_test_trans = preproc.transform(X_test)

    # try to get feature names; fallback to generic names
    try:
        feature_names = preproc.get_feature_names_out()
    except Exception:
        feature_names = [f"feat_{i}" for i in range(X_train_trans.shape[1])]

    pd.DataFrame(X_train_trans, columns=feature_names).to_csv(os.path.join(args.outdir, "X_train_transformed.csv"), index=False)
    pd.DataFrame(X_test_trans, columns=feature_names).to_csv(os.path.join(args.outdir, "X_test_transformed.csv"), index=False)

    print("Saved model:", model_path)
    print("Saved metrics + plots in:", args.outdir)
    print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default="D:\\AI Hackathon\\data\\bank_churn_cleaned.csv", help="Path to cleaned CSV")
    parser.add_argument("--outdir", type=str, default="outputs", help="Folder to save metrics/plots/transformed")
    parser.add_argument("--modeldir", type=str, default="models", help="Folder to save model pickle")
    parser.add_argument("--test_size", type=float, default=0.20)
    parser.add_argument("--n_iter", type=int, default=20, help="Number of RandomizedSearch iterations")
    parser.add_argument("--n_jobs", type=int, default=-1)
    parser.add_argument("--random_state", type=int, default=42)
    args = parser.parse_args()
    main(args)

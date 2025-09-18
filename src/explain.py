#!/usr/bin/env python3
"""
Explain churn predictions using SHAP.

Outputs in outputs/explanations:
- per_customer_reasons.csv: top positive SHAP reasons per customer
- shap_values_summary_by_income.csv: mean |SHAP| per feature within Income_Category
- plots: bar charts per income group and example waterfall plots
"""

import os
import argparse
import json
import numpy as np
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt
import seaborn as sns


def get_feature_names_from_preprocessor(preproc) -> list:
    try:
        names = preproc.get_feature_names_out()
        try:
            return names.tolist()
        except Exception:
            return list(names)
    except Exception:
        # Fallback: unknown names
        return None


def compute_shap_for_pipeline(pipeline, X: pd.DataFrame):
    # Access steps
    preproc = pipeline.named_steps.get("preproc")
    model = pipeline.named_steps.get("clf")

    # Transform features like during training
    X_trans = preproc.transform(X)
    feature_names = get_feature_names_from_preprocessor(preproc)

    # Build TreeExplainer for tree-based model
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_trans)

    # If list per class, take class 1 (churn)
    if isinstance(shap_values, list) and len(shap_values) >= 2:
        shap_for_positive = np.asarray(shap_values[1])
        try:
            base_value = explainer.expected_value[1]
        except Exception:
            base_value = None
    else:
        shap_for_positive = np.asarray(shap_values)
        # Handle 3D array (n_samples, n_features, n_outputs) by selecting class 1 if present
        if shap_for_positive.ndim == 3:
            class_axis = shap_for_positive.shape[-1]
            idx = 1 if class_axis >= 2 else 0
            shap_for_positive = shap_for_positive[:, :, idx]
        try:
            base_value = explainer.expected_value
            if isinstance(base_value, (list, tuple, np.ndarray)):
                if len(base_value) >= 2:
                    base_value = base_value[1]
                else:
                    base_value = base_value[0]
        except Exception:
            base_value = None
    return shap_for_positive, base_value, feature_names


def top_positive_reasons(shap_row: np.ndarray, feature_names: list, top_k: int = 3):
    shap_row = np.asarray(shap_row).reshape(-1)
    indices = np.argsort(shap_row)[::-1]  # descending contributions
    top_indices = indices[:top_k]
    reasons = [
        {
            "feature": feature_names[i] if feature_names else f"feat_{i}",
            "shap_value": float(np.squeeze(shap_row[i]))
        }
        for i in top_indices if float(np.squeeze(shap_row[i])) > 0
    ]
    return reasons


def summarize_by_income(abs_shap: np.ndarray, feature_names: list, income_series: pd.Series, top_n: int = 10):
    df_abs = pd.DataFrame(abs_shap, columns=feature_names)
    df_abs["Income_Category"] = income_series.values
    grouped = df_abs.groupby("Income_Category").mean(numeric_only=True)
    summaries = {}
    for income_cat, row in grouped.iterrows():
        s = row.sort_values(ascending=False).head(top_n)
        summaries[income_cat] = s
    return grouped, summaries


def map_reason_for_feature(feature_name: str, shap_value: float) -> str:
    name = feature_name
    val = float(shap_value)
    positive = val > 0
    # Numeric drivers
    if name.endswith("num__Avg_Utilization_Ratio") or name == "num__Avg_Utilization_Ratio" or "Avg_Utilization_Ratio" in name:
        return "high credit utilization" if positive else "low utilization"
    if name.endswith("num__Months_Inactive_12_mon") or "Months_Inactive_12_mon" in name:
        return "recent inactivity" if positive else "recent activity"
    if name.endswith("num__Contacts_Count_12_mon") or "Contacts_Count_12_mon" in name:
        return "frequent service contacts" if positive else "few service contacts"
    if name.endswith("num__Total_Trans_Ct") or "Total_Trans_Ct" in name:
        return "low transaction count" if positive else "high transaction count"
    if name.endswith("num__Total_Trans_Amt") or "Total_Trans_Amt" in name:
        return "lower total spend" if positive else "higher total spend"
    if name.endswith("num__Total_Ct_Chng_Q4_Q1") or "Total_Ct_Chng_Q4_Q1" in name:
        return "drop in recent activity" if positive else "rise in recent activity"
    if name.endswith("num__Total_Revolving_Bal") or "Total_Revolving_Bal" in name:
        return "high revolving balance" if positive else "low revolving balance"
    if name.endswith("num__Credit_Limit") or "Credit_Limit" in name:
        return "lower credit limit" if positive else "higher credit limit"
    if name.endswith("num__Total_Relationship_Count") or "Total_Relationship_Count" in name:
        return "fewer products with bank" if positive else "more products with bank"

    # Categorical examples
    if name.startswith("cat__Marital_Status_"):
        label = name.split("cat__Marital_Status_")[-1]
        return f"marital status: {label}"
    if name.startswith("cat__Education_Level_"):
        label = name.split("cat__Education_Level_")[-1]
        return f"education level: {label}"
    if name.startswith("cat__Income_Category_"):
        label = name.split("cat__Income_Category_")[-1]
        return f"income segment: {label}"
    if name.startswith("cat__Gender_"):
        label = name.split("cat__Gender_")[-1]
        return f"gender: {label}"
    if name.startswith("cat__Card_Category_"):
        label = name.split("cat__Card_Category_")[-1]
        return f"card type: {label}"

    # Fallback
    # Clean generic name
    generic = name.replace("num__", "").replace("cat__", "").replace("_", " ")
    return f"{generic} contributes to churn"


def build_reason_comment(top_reasons: list) -> str:
    # Deduplicate by phrase order, keep first 3
    phrases = []
    seen = set()
    for r in top_reasons:
        phrase = map_reason_for_feature(r["feature"], r["shap_value"])
        if phrase not in seen:
            seen.add(phrase)
            phrases.append(phrase)
        if len(phrases) >= 3:
            break
    if not phrases:
        return "No strong drivers detected."
    if len(phrases) == 1:
        return f"Likely driver: {phrases[0]}."
    if len(phrases) == 2:
        return f"Likely drivers: {phrases[0]} and {phrases[1]}."
    return f"Likely drivers: {phrases[0]}, {phrases[1]}, and {phrases[2]}."


def get_base_feature_name(feature_name: str) -> str:
    # Remove pipeline prefixes and one-hot category suffixes where possible
    name = feature_name
    if name.startswith("num__"):
        return name[len("num__"):]
    if name.startswith("cat__"):
        trimmed = name[len("cat__"):]
        # drop last category token for one-hot columns
        if "_" in trimmed:
            return trimmed.rsplit("_", 1)[0]
        return trimmed
    return name


def describe_reason(base, shap_val):
    """Generate business-oriented explanations based on feature and SHAP value direction"""

    # Age
    if base == "Customer_Age":
        return "Older customer group may be less tolerant of fees/service issues" if shap_val > 0 else "Younger age group tends to stay engaged"

    # Dependents
    elif base == "Dependent_count":
        return "Fewer dependents may allow more flexibility to switch banks" if shap_val > 0 else "More dependents may indicate stability in banking needs"

    # Utilization
    elif base == "Avg_Utilization_Ratio":
        return "High credit utilization suggests financial stress, increasing churn risk" if shap_val > 0 else "Low utilization indicates healthy credit behavior"

    # Transactions (count + amount)
    elif base == "Total_Trans_Ct":
        return "Very frequent transactions may reflect rising expectations or shopping for alternatives" if shap_val > 0 else "Low transaction activity indicates less engagement"
    elif base == "Total_Trans_Amt":
        return "High spending volume can raise sensitivity to better offers elsewhere" if shap_val > 0 else "Low spending volume shows limited engagement"

    # Balances & limits
    elif base == "Total_Revolving_Bal":
        return "Carrying a high revolving balance can create financial strain" if shap_val > 0 else "Low revolving balance suggests financial stability"
    elif base == "Credit_Limit":
        return "Low credit limit compared to needs may push customer to seek better options" if shap_val > 0 else "High credit limit provides flexibility, reducing churn risk"
    elif base == "Avg_Open_To_Buy":
        return "Limited available credit may create dissatisfaction" if shap_val > 0 else "High available credit supports satisfaction"

    # Relationship & tenure
    elif base == "Months_on_book":
        return "Short tenure with the bank means weaker loyalty" if shap_val > 0 else "Long tenure indicates established loyalty"
    elif base == "Total_Relationship_Count":
        return "Few banking products may cause customer to explore competitors" if shap_val > 0 else "Multiple products create stickiness with the bank"

    # Inactivity & service contacts
    elif base == "Months_Inactive_12_mon":
        return "Recent inactivity signals disengagement risk" if shap_val > 0 else "Consistent activity shows ongoing engagement"
    elif base == "Contacts_Count_12_mon":
        return "Frequent service contacts suggest frustration or unresolved issues" if shap_val > 0 else "Minimal service contacts indicate satisfaction"

    # Behavior changes
    elif base == "Total_Amt_Chng_Q4_Q1":
        return "Declining spend compared to prior periods suggests reduced engagement" if shap_val > 0 else "Rising spend signals deeper engagement"
    elif base == "Total_Ct_Chng_Q4_Q1":
        return "Declining transaction frequency is a churn warning" if shap_val > 0 else "Increasing transaction frequency indicates stronger engagement"

    # Demographics & card
    elif base == "Income_Category":
        return "Lower income bracket may be more price-sensitive" if shap_val > 0 else "Higher income bracket often indicates more stable relationships"
    elif base == "Gender":
        return "Gender pattern observed as churn risk" if shap_val > 0 else "Gender pattern observed as retention factor"
    elif base == "Education_Level":
        return "Certain education levels show higher churn risk" if shap_val > 0 else "Certain education levels are more stable"
    elif base == "Marital_Status":
        return "Marital status associated with higher churn risk" if shap_val > 0 else "Marital status linked with stability"
    elif base == "Card_Category":
        return "Card tier mismatch may push customer to competitors" if shap_val > 0 else "Appropriate card tier supports satisfaction"

    # Fallback
    else:
        return f"{base.replace('',' ').title()} contributes to churn risk" if shap_val > 0 else f"{base.replace('',' ').title()} supports retention"


def main(args):
    os.makedirs(args.outdir, exist_ok=True)
    exp_dir = os.path.join(args.outdir, "explanations")
    os.makedirs(exp_dir, exist_ok=True)

    # Load pipeline and data
    pipeline = joblib.load(args.model)
    data = pd.read_csv(args.data)

    # If Attrition_Flag exists, drop it to simulate prediction-time features
    if "Attrition_Flag" in data.columns:
        data_features = data.drop(columns=["Attrition_Flag"])  # retain raw for inspection if needed
    else:
        data_features = data.copy()

    # Drop known ID/noise columns if present (consistent with training)
    data_features = data_features.drop(columns=["CLIENTNUM"], errors="ignore")
    data_features = data_features.drop(
        columns=[c for c in data_features.columns if c.startswith("Naive_Bayes_Classifier")], errors="ignore"
    )

    # Compute SHAP values on transformed features
    shap_pos, base_value, feature_names = compute_shap_for_pipeline(pipeline, data_features)
    if feature_names is None:
        feature_names = [f"feat_{i}" for i in range(shap_pos.shape[1])]

    # Predicted churn probability to align reasons toward churn
    probs = pipeline.predict_proba(data_features)[:, 1]
    high_risk = (probs >= args.threshold).astype(int)

    # Build per-customer reasons table ONLY for churn (Predicted_Label==1)
    churn_indices = np.where(high_risk == 1)[0]
    records = []
    for idx in churn_indices:
        reasons = top_positive_reasons(shap_pos[idx], feature_names, top_k=args.top_k)
        # Enrich reasons with business-oriented descriptions
        enriched = []
        for r in reasons:
            base = get_base_feature_name(r["feature"])
            r_desc = describe_reason(base, r["shap_value"])
            enriched.append({**r, "reason": r_desc})
        # Build natural language comment
        reason_comment = build_reason_comment(reasons)
        key_factors = "; ".join([describe_reason(get_base_feature_name(r['feature']), r['shap_value']) for r in reasons])
        records.append({
            "index": int(idx),
            "Churn_Probability": float(probs[idx]),
            "Predicted_Label": 1,
            "Recommended_Action": "Offer retention benefits",
            "Top_Reasons": "; ".join([f"{r['feature']} (+{r['shap_value']:.3f}) — {get_base_feature_name(r['feature'])}: {describe_reason(get_base_feature_name(r['feature']), r['shap_value'])}" for r in reasons]),
            "Reason_Comment": reason_comment,
            "Key_Factors": key_factors
        })

    reasons_df = pd.DataFrame(records) if records else pd.DataFrame(columns=[
        "index","Churn_Probability","Predicted_Label","Recommended_Action","Top_Reasons","Reason_Comment","Key_Factors"
    ])
    # If original data has a stable key, attach it
    key_cols = [c for c in ["CLIENTNUM"] if c in data.columns]
    if key_cols:
        reasons_df = reasons_df.join(data[key_cols], how="left")

    reasons_csv = os.path.join(exp_dir, "per_customer_reasons.csv")
    # Build a reasons file that includes ALL customers with blanks for non-churn
    reasons_complete = pd.DataFrame({
        "index": np.arange(len(data_features), dtype=int),
        "Churn_Probability": probs,
        "Predicted_Label": high_risk,
        "Recommended_Action": np.where(high_risk == 1, "Offer retention benefits", "No action needed"),
    })
    if not reasons_df.empty:
        reasons_complete = reasons_complete.merge(
            reasons_df[["index","Top_Reasons","Reason_Comment","Key_Factors"]], on="index", how="left"
        )
    else:
        reasons_complete["Top_Reasons"] = ""
        reasons_complete["Reason_Comment"] = ""
        reasons_complete["Key_Factors"] = ""
    reasons_complete["Top_Reasons"] = reasons_complete["Top_Reasons"].fillna("")
    reasons_complete["Reason_Comment"] = reasons_complete["Reason_Comment"].fillna("")
    reasons_complete["Key_Factors"] = reasons_complete["Key_Factors"].fillna("")
    reasons_complete.to_csv(reasons_csv, index=False)

    # Create merged predictions file with reasons
    merged = data.copy()
    merged["Churn_Probability"] = probs.round(3)
    merged["Predicted_Label"] = high_risk
    merged["Recommended_Action"] = np.where(merged["Predicted_Label"] == 1, "Offer retention benefits", "No action needed")
    merged = merged.reset_index(drop=True).join(reasons_df.set_index("index")[ ["Top_Reasons","Reason_Comment","Key_Factors"] ], how="left")
    # Ensure non-churn rows have empty reason fields (not NaN)
    if "Top_Reasons" in merged.columns:
        merged["Top_Reasons"] = merged["Top_Reasons"].fillna("")
    if "Reason_Comment" in merged.columns:
        merged["Reason_Comment"] = merged["Reason_Comment"].fillna("")
    if "Key_Factors" in merged.columns:
        merged["Key_Factors"] = merged["Key_Factors"].fillna("")
    merged_csv = os.path.join(exp_dir, "predictions_with_reasons.csv")
    merged.to_csv(merged_csv, index=False)

    # Aggregate by Income_Category for churn-only (if present)
    if "Income_Category" in data_features.columns and len(churn_indices) > 0:
        abs_shap = np.abs(shap_pos[churn_indices])
        grouped, summaries = summarize_by_income(abs_shap, feature_names, data_features.loc[churn_indices, "Income_Category"], top_n=10)
        grouped_csv = os.path.join(exp_dir, "shap_values_summary_by_income.csv")
        grouped.to_csv(grouped_csv)

        # Plot top features per income category
        for income_cat, s in summaries.items():
            plt.figure(figsize=(8, 4))
            sns.barplot(x=s.values, y=s.index, color="#4F46E5")
            plt.title(f"Top mean |SHAP| (churn-only) — {income_cat}")
            plt.xlabel("Mean |SHAP|")
            plt.ylabel("Feature")
            plt.tight_layout()
            plt.savefig(os.path.join(exp_dir, f"top_shap_{income_cat.replace(' ', '_').replace('>','gt').replace('<','lt')}.png"))
            plt.close()

    # Example waterfall plots for a few high-risk customers
    try:
        preproc = pipeline.named_steps["preproc"]
        X_trans = preproc.transform(data_features)
        explainer = shap.TreeExplainer(pipeline.named_steps["clf"])
        shap_values = explainer.shap_values(X_trans)
        if isinstance(shap_values, list) and len(shap_values) == 2:
            shap_for_positive = shap_values[1]
            expected_value = explainer.expected_value[1]
        else:
            shap_for_positive = shap_values
            expected_value = explainer.expected_value

        # pick top-N by probability
        top_idx = np.argsort(probs)[::-1][: min(5, len(probs))]
        for i in top_idx:
            try:
                shap.plots.waterfall(
                    shap.Explanation(values=shap_for_positive[i], base_values=expected_value, feature_names=feature_names)
                )
                plt.tight_layout()
                plt.savefig(os.path.join(exp_dir, f"waterfall_{i}.png"))
                plt.close()
            except Exception:
                # Waterfall sometimes fails with dense arrays; skip gracefully
                pass
    except Exception:
        pass

    # Save a minimal metadata file
    meta = {
        "model_path": os.path.abspath(args.model),
        "data_path": os.path.abspath(args.data),
        "num_rows": int(data_features.shape[0]),
        "num_features_transformed": int(len(feature_names)),
        "top_k": int(args.top_k)
    }
    with open(os.path.join(exp_dir, "explain_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    print(f"Saved per-customer reasons to: {reasons_csv}")
    print(f"Saved merged predictions with reasons to: {merged_csv}")
    if os.path.exists(os.path.join(exp_dir, "shap_values_summary_by_income.csv")):
        print("Saved income-segment SHAP summary and plots.")
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="D:\\AI Hackathon\\models\\best_model.pkl")
    parser.add_argument("--data", type=str, default="D:\\AI Hackathon\\data\\new_customers.csv")
    parser.add_argument("--outdir", type=str, default="outputs")
    parser.add_argument("--top_k", type=int, default=3)
    parser.add_argument("--threshold", type=float, default=0.35)
    args = parser.parse_args()
    main(args)



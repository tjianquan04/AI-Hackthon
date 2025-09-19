#!/usr/bin/env python3
"""
Dashboard EDA Script for Bank Churn Analysis
Generates comprehensive business-oriented analysis for UI dashboard
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import math
from pathlib import Path

# Set style for better-looking plots
plt.style.use('default')
sns.set_palette("husl")

def clean_for_json(obj):
    """Recursively clean NaN, infinity values for JSON serialization"""
    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(v) for v in obj]
    elif isinstance(obj, np.ndarray):
        return clean_for_json(obj.tolist())
    elif isinstance(obj, (np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32)):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return float(obj)
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    elif pd.isna(obj):
        return None
    else:
        return obj

def load_and_clean_data():
    """Load and clean the raw bank churners data"""
    print("📊 Loading and cleaning data...")
    
    # Load data
    df = pd.read_csv("../data/raw_BankChurners.csv")
    
    # Remove Naive Bayes columns (synthetic features)
    df = df.drop(columns=[col for col in df.columns if col.startswith("Naive_Bayes")])
    
    # Create binary churn flag
    df['Churned'] = (df['Attrition_Flag'] == 'Attrited Customer').astype(int)
    
    # Clean categorical variables
    df['Income_Category'] = df['Income_Category'].replace('Unknown', 'Unknown Income')
    df['Education_Level'] = df['Education_Level'].replace('Unknown', 'Unknown Education')
    df['Marital_Status'] = df['Marital_Status'].replace('Unknown', 'Unknown Status')
    
    print(f"✅ Data loaded: {len(df):,} customers, {df['Churned'].sum():,} churned ({df['Churned'].mean():.1%})")
    return df

def churn_overview_analysis(df):
    """Generate churn overview analytics"""
    print("🔍 Analyzing churn overview...")
    
    results = {}
    
    # Overall churn rate
    results['overall_churn_rate'] = {
        'total_customers': len(df),
        'churned_customers': df['Churned'].sum(),
        'churn_rate': df['Churned'].mean(),
        'retention_rate': 1 - df['Churned'].mean()
    }
    
    # Churn by age groups
    df['Age_Group'] = pd.cut(df['Customer_Age'], 
                            bins=[0, 30, 40, 50, 60, 100], 
                            labels=['<30', '30-40', '40-50', '50-60', '60+'])
    
    age_churn = df.groupby('Age_Group')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    age_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_age'] = age_churn.to_dict('index')
    
    # Churn by income category
    income_churn = df.groupby('Income_Category')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    income_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_income'] = income_churn.to_dict('index')
    
    # Churn by card type
    card_churn = df.groupby('Card_Category')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    card_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_card_type'] = card_churn.to_dict('index')
    
    # Churn by tenure groups (enhanced with business-friendly labels)
    df['Tenure_Group'] = pd.cut(df['Months_on_book'], 
                               bins=[0, 12, 24, 36, 48, 100], 
                               labels=['New (0-12m)', 'Early Stage (13-24m)', 'Mid Stage (25-36m)', 
                                      'Established (37-48m)', 'Long-term (49m+)'])
    
    tenure_churn = df.groupby('Tenure_Group')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    tenure_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_tenure'] = tenure_churn.to_dict('index')
    
    # Additional tenure insights
    results['tenure_insights'] = {
        'avg_tenure_months': df['Months_on_book'].mean(),
        'avg_tenure_churned': df[df['Churned'] == 1]['Months_on_book'].mean(),
        'avg_tenure_retained': df[df['Churned'] == 0]['Months_on_book'].mean(),
        'newest_customers_churn': tenure_churn.loc['New (0-12m)', 'Churn_Rate'] if 'New (0-12m)' in tenure_churn.index else 0,
        'longest_customers_churn': tenure_churn.loc['Long-term (49m+)', 'Churn_Rate'] if 'Long-term (49m+)' in tenure_churn.index else 0
    }
    
    return results

def demographics_analysis(df):
    """Generate demographic analytics"""
    print("👥 Analyzing customer demographics...")
    
    results = {}
    
    # Churn by gender
    gender_churn = df.groupby('Gender')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    gender_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_gender'] = gender_churn.to_dict('index')
    
    # Churn by education level
    education_churn = df.groupby('Education_Level')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    education_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_education'] = education_churn.to_dict('index')
    
    # Churn by marital status
    marital_churn = df.groupby('Marital_Status')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    marital_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_marital_status'] = marital_churn.to_dict('index')
    
    # Age distribution stats
    age_stats = df.groupby('Churned')['Customer_Age'].agg(['mean', 'median', 'std']).round(2)
    age_stats.index = ['Retained', 'Churned']
    results['age_distribution_stats'] = age_stats.to_dict('index')
    
    return results

def product_engagement_analysis(df):
    """Analyze product engagement patterns"""
    print("🏦 Analyzing product engagement...")
    
    results = {}
    
    # Relationship count vs churn
    relationship_churn = df.groupby('Total_Relationship_Count')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    relationship_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_relationship_count'] = relationship_churn.to_dict('index')
    
    # Product engagement segments
    df['Product_Engagement'] = pd.cut(df['Total_Relationship_Count'], 
                                     bins=[0, 2, 4, 10], 
                                     labels=['Low (1-2)', 'Medium (3-4)', 'High (5+)'])
    
    engagement_churn = df.groupby('Product_Engagement')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    engagement_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_product_engagement'] = engagement_churn.to_dict('index')
    
    return results

def customer_activity_analysis(df):
    """Analyze customer activity patterns"""
    print("📈 Analyzing customer activity...")
    
    results = {}
    
    # Months inactive analysis
    inactive_churn = df.groupby('Months_Inactive_12_mon')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    inactive_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_months_inactive'] = inactive_churn.to_dict('index')
    
    # Service contacts analysis
    contacts_churn = df.groupby('Contacts_Count_12_mon')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    contacts_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_service_contacts'] = contacts_churn.to_dict('index')
    
    # Transaction volume segments
    df['Transaction_Volume'] = pd.qcut(df['Total_Trans_Amt'], 
                                      q=4, 
                                      labels=['Low', 'Medium', 'High', 'Very High'])
    
    volume_churn = df.groupby('Transaction_Volume')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    volume_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_transaction_volume'] = volume_churn.to_dict('index')
    
    # Transaction count segments
    df['Transaction_Count'] = pd.qcut(df['Total_Trans_Ct'], 
                                     q=4, 
                                     labels=['Low', 'Medium', 'High', 'Very High'])
    
    count_churn = df.groupby('Transaction_Count')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    count_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_transaction_count'] = count_churn.to_dict('index')
    
    # Transaction change analysis
    df['Transaction_Change'] = pd.cut(df['Total_Ct_Chng_Q4_Q1'], 
                                     bins=[0, 0.5, 1.0, 1.5, 5.0], 
                                     labels=['Declining', 'Stable', 'Growing', 'High Growth'])
    
    change_churn = df.groupby('Transaction_Change')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    change_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_transaction_change'] = change_churn.to_dict('index')
    
    return results

def financial_behavior_analysis(df):
    """Analyze financial behavior patterns"""
    print("💰 Analyzing financial behavior...")
    
    results = {}
    
    # Credit limit segments
    df['Credit_Limit_Segment'] = pd.qcut(df['Credit_Limit'], 
                                        q=4, 
                                        labels=['Low', 'Medium', 'High', 'Premium'])
    
    credit_churn = df.groupby('Credit_Limit_Segment')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    credit_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_credit_limit'] = credit_churn.to_dict('index')
    
    # Revolving balance analysis
    df['Revolving_Balance_Segment'] = pd.cut(df['Total_Revolving_Bal'], 
                                           bins=[0, 500, 1500, 3000, 10000], 
                                           labels=['None/Low', 'Medium', 'High', 'Very High'])
    
    revolving_churn = df.groupby('Revolving_Balance_Segment')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    revolving_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_revolving_balance'] = revolving_churn.to_dict('index')
    
    # Utilization ratio analysis
    df['Utilization_Category'] = pd.cut(df['Avg_Utilization_Ratio'], 
                                       bins=[0, 0.1, 0.3, 0.7, 1.0], 
                                       labels=['Very Low', 'Low', 'Medium', 'High'])
    
    utilization_churn = df.groupby('Utilization_Category')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    utilization_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_utilization'] = utilization_churn.to_dict('index')
    
    # Available credit analysis
    df['Available_Credit_Segment'] = pd.qcut(df['Avg_Open_To_Buy'], 
                                           q=4, 
                                           labels=['Low', 'Medium', 'High', 'Very High'])
    
    available_churn = df.groupby('Available_Credit_Segment')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    available_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_available_credit'] = available_churn.to_dict('index')
    
    return results

def customer_value_analysis(df):
    """Analyze customer value patterns"""
    print("💎 Analyzing customer value...")
    
    results = {}
    
    # Create customer value score (combination of transaction amount and credit usage)
    df['Value_Score'] = (df['Total_Trans_Amt'].rank(pct=True) * 0.6 + 
                        df['Credit_Limit'].rank(pct=True) * 0.4)
    
    df['Customer_Value'] = pd.qcut(df['Value_Score'], 
                                  q=4, 
                                  labels=['Low Value', 'Medium Value', 'High Value', 'Premium Value'])
    
    value_churn = df.groupby('Customer_Value')['Churned'].agg(['count', 'sum', 'mean']).round(3)
    value_churn.columns = ['Total_Customers', 'Churned_Count', 'Churn_Rate']
    results['churn_by_customer_value'] = value_churn.to_dict('index')
    
    # High-value customer analysis
    high_value_customers = df[df['Customer_Value'].isin(['High Value', 'Premium Value'])]
    results['high_value_churn_stats'] = {
        'total_high_value': len(high_value_customers),
        'churned_high_value': high_value_customers['Churned'].sum(),
        'high_value_churn_rate': high_value_customers['Churned'].mean(),
        'revenue_at_risk_pct': high_value_customers['Churned'].sum() / len(high_value_customers)
    }
    
    # Card tier and income analysis
    card_income_churn = df.groupby(['Card_Category', 'Income_Category'])['Churned'].agg(['count', 'mean']).round(3)
    card_income_churn.columns = ['Customer_Count', 'Churn_Rate']
    # Convert multi-index to string keys for JSON serialization
    card_income_dict = {}
    for (card, income), values in card_income_churn.iterrows():
        key = f"{card}_{income}"
        card_income_dict[key] = {
            'Card_Category': card,
            'Income_Category': income,
            'Customer_Count': values['Customer_Count'],
            'Churn_Rate': values['Churn_Rate']
        }
    results['churn_by_card_income'] = card_income_dict
    
    return results

def generate_feature_importance_insights(df):
    """Generate insights about key churn drivers"""
    print("🎯 Analyzing churn drivers...")
    
    results = {}
    
    # Calculate correlation with churn for numerical features
    numerical_features = ['Customer_Age', 'Dependent_count', 'Months_on_book', 
                         'Total_Relationship_Count', 'Months_Inactive_12_mon', 
                         'Contacts_Count_12_mon', 'Credit_Limit', 'Total_Revolving_Bal',
                         'Total_Trans_Amt', 'Total_Trans_Ct', 'Avg_Utilization_Ratio']
    
    correlations = df[numerical_features + ['Churned']].corr()['Churned'].abs().sort_values(ascending=False)
    correlations = correlations.drop('Churned').head(10)
    
    results['top_numerical_drivers'] = correlations.to_dict()
    
    # Key insights for dashboard
    insights = []
    
    # Inactivity insight
    inactive_customers = df[df['Months_Inactive_12_mon'] >= 3]
    if len(inactive_customers) > 0:
        inactive_churn_rate = inactive_customers['Churned'].mean()
        insights.append({
            'category': 'Inactivity Risk',
            'insight': f"Customers inactive for 3+ months have {inactive_churn_rate:.1%} churn rate",
            'risk_level': 'High' if inactive_churn_rate > 0.25 else 'Medium'
        })
    
    # Service contacts insight
    frequent_contacts = df[df['Contacts_Count_12_mon'] >= 4]
    if len(frequent_contacts) > 0:
        contact_churn_rate = frequent_contacts['Churned'].mean()
        insights.append({
            'category': 'Service Issues',
            'insight': f"Customers with 4+ service contacts have {contact_churn_rate:.1%} churn rate",
            'risk_level': 'High' if contact_churn_rate > 0.25 else 'Medium'
        })
    
    # Utilization insight
    high_utilization = df[df['Avg_Utilization_Ratio'] > 0.7]
    if len(high_utilization) > 0:
        util_churn_rate = high_utilization['Churned'].mean()
        insights.append({
            'category': 'Financial Stress',
            'insight': f"High utilization customers (>70%) have {util_churn_rate:.1%} churn rate",
            'risk_level': 'High' if util_churn_rate > 0.25 else 'Medium'
        })
    
    # Transaction decline insight
    declining_transactions = df[df['Total_Ct_Chng_Q4_Q1'] < 0.5]
    if len(declining_transactions) > 0:
        decline_churn_rate = declining_transactions['Churned'].mean()
        insights.append({
            'category': 'Engagement Decline',
            'insight': f"Customers with declining transactions have {decline_churn_rate:.1%} churn rate",
            'risk_level': 'High' if decline_churn_rate > 0.25 else 'Medium'
        })
    
    results['key_insights'] = insights
    
    return results

def create_summary_dashboard_data(df):
    """Create summary data for dashboard KPIs"""
    print("📋 Creating dashboard summary...")
    
    summary = {
        'kpi_metrics': {
            'total_customers': len(df),
            'churned_customers': df['Churned'].sum(),
            'overall_churn_rate': df['Churned'].mean(),
            'retention_rate': 1 - df['Churned'].mean(),
            'avg_customer_age': df['Customer_Age'].mean(),
            'avg_tenure_months': df['Months_on_book'].mean(),
            'avg_credit_limit': df['Credit_Limit'].mean(),
            'avg_transaction_amount': df['Total_Trans_Amt'].mean()
        },
        'risk_segments': {
            'high_risk_customers': len(df[(df['Months_Inactive_12_mon'] >= 3) | 
                                         (df['Contacts_Count_12_mon'] >= 4) | 
                                         (df['Avg_Utilization_Ratio'] > 0.7)]),
            'medium_risk_customers': len(df[(df['Months_Inactive_12_mon'] == 2) | 
                                           (df['Contacts_Count_12_mon'] == 3) | 
                                           (df['Avg_Utilization_Ratio'] > 0.5)]),
            'low_risk_customers': len(df[(df['Months_Inactive_12_mon'] <= 1) & 
                                        (df['Contacts_Count_12_mon'] <= 2) & 
                                        (df['Avg_Utilization_Ratio'] <= 0.5)])
        }
    }
    
    return summary

def main():
    """Main function to run all analyses"""
    print("🚀 Starting Bank Churn EDA for Dashboard...")
    
    # Create output directory
    os.makedirs("../outputs/dashboard_data", exist_ok=True)
    
    # Load and clean data
    df = load_and_clean_data()
    
    # Run all analyses
    analyses = {
        'churn_overview': churn_overview_analysis(df),
        'demographics': demographics_analysis(df),
        'product_engagement': product_engagement_analysis(df),
        'customer_activity': customer_activity_analysis(df),
        'financial_behavior': financial_behavior_analysis(df),
        'customer_value': customer_value_analysis(df),
        'churn_drivers': generate_feature_importance_insights(df),
        'summary_kpis': create_summary_dashboard_data(df)
    }
    
    # Clean data for JSON serialization (remove NaN, infinity values)
    clean_analyses = clean_for_json(analyses)
    
    # Save results to JSON for dashboard consumption
    output_file = "../outputs/dashboard_data/churn_analysis.json"
    with open(output_file, 'w') as f:
        json.dump(clean_analyses, f, indent=2)
    
    print(f"✅ Analysis complete! Results saved to: {output_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 DASHBOARD EDA SUMMARY")
    print("="*60)
    
    summary = analyses['summary_kpis']['kpi_metrics']
    print(f"Total Customers: {summary['total_customers']:,}")
    print(f"Churned Customers: {summary['churned_customers']:,}")
    print(f"Overall Churn Rate: {summary['overall_churn_rate']:.1%}")
    print(f"Retention Rate: {summary['retention_rate']:.1%}")
    
    print("\n🎯 Key Insights:")
    for insight in analyses['churn_drivers']['key_insights']:
        print(f"• {insight['category']}: {insight['insight']}")
    
    print(f"\n📁 Data files created for dashboard:")
    print(f"• {output_file}")
    print("• Ready for UI integration!")

if __name__ == "__main__":
    main()

# Customer Data Service - Streamlit version
import pandas as pd
import numpy as np
import os
from typing import List, Dict, Any, Optional

class CustomerDataService:
    def __init__(self):
        self.customers_df = None
        self.predictions_df = None
        self._load_data()

    def _load_data(self):
        """Load customer data and predictions"""
        try:
            # Try multiple paths to find the data files
            data_paths = [
                '../data/bank_churn_cleaned.csv',
                '../../data/bank_churn_cleaned.csv',
                '../UI/public/data/bank_churn_cleaned.csv'
            ]
            
            prediction_paths = [
                '../outputs/explanations/predictions_with_reasons.csv',
                '../../outputs/explanations/predictions_with_reasons.csv',
                '../UI/public/data/predictions_with_reasons.csv'
            ]
            
            # Load customer data
            for path in data_paths:
                try:
                    self.customers_df = pd.read_csv(path)
                    break
                except FileNotFoundError:
                    continue
            
            # Load predictions data
            for path in prediction_paths:
                try:
                    self.predictions_df = pd.read_csv(path)
                    break
                except FileNotFoundError:
                    continue
                    
            # If files not found, create sample data
            if self.customers_df is None:
                self.customers_df = self._create_sample_customer_data()
            
            if self.predictions_df is None:
                self.predictions_df = self._create_sample_prediction_data()
                
        except Exception as e:
            print(f"Error loading customer data: {e}")
            self.customers_df = self._create_sample_customer_data()
            self.predictions_df = self._create_sample_prediction_data()

    def _create_sample_customer_data(self) -> pd.DataFrame:
        """Create sample customer data if files are not available"""
        np.random.seed(42)
        n_customers = 100
        
        return pd.DataFrame({
            'CLIENTNUM': range(100000, 100000 + n_customers),
            'Customer_Age': np.random.randint(20, 80, n_customers),
            'Gender': np.random.choice(['M', 'F'], n_customers),
            'Dependent_count': np.random.randint(0, 6, n_customers),
            'Education_Level': np.random.choice(['High School', 'Graduate', 'College', 'Post-Graduate'], n_customers),
            'Marital_Status': np.random.choice(['Single', 'Married', 'Divorced'], n_customers),
            'Income_Category': np.random.choice(['Less than $40K', '$40K - $60K', '$60K - $80K', '$80K - $120K', '$120K +'], n_customers),
            'Card_Category': np.random.choice(['Blue', 'Gold', 'Silver', 'Platinum'], n_customers),
            'Months_on_book': np.random.randint(12, 60, n_customers),
            'Total_Relationship_Count': np.random.randint(1, 7, n_customers),
            'Months_Inactive_12_mon': np.random.randint(0, 6, n_customers),
            'Contacts_Count_12_mon': np.random.randint(0, 7, n_customers),
            'Credit_Limit': np.random.uniform(1000, 35000, n_customers),
            'Total_Revolving_Bal': np.random.uniform(0, 2500, n_customers),
            'Avg_Open_To_Buy': np.random.uniform(500, 20000, n_customers),
            'Total_Trans_Amt': np.random.uniform(500, 20000, n_customers),
            'Total_Trans_Ct': np.random.randint(10, 150, n_customers),
            'Avg_Utilization_Ratio': np.random.uniform(0, 1, n_customers),
            'Attrition_Flag': np.random.choice(['Existing Customer', 'Attrited Customer'], n_customers, p=[0.84, 0.16])
        })

    def _create_sample_prediction_data(self) -> pd.DataFrame:
        """Create sample prediction data if files are not available"""
        np.random.seed(42)
        n_predictions = 50
        
        return pd.DataFrame({
            'Churn_Probability': np.random.uniform(0, 1, n_predictions),
            'Predicted_Label': np.random.choice(['Churn', 'No Churn'], n_predictions, p=[0.3, 0.7]),
            'Recommended_Action': [f'Action {i}' for i in range(n_predictions)],
            'Top_Reasons': [f'Reason {i}' for i in range(n_predictions)],
            'Reason_Comment': [f'Comment {i}' for i in range(n_predictions)]
        })

    def get_customers(self, limit: Optional[int] = None) -> pd.DataFrame:
        """Get customer data with optional limit"""
        if limit:
            return self.customers_df.head(limit)
        return self.customers_df

    def get_predictions(self, limit: Optional[int] = None) -> pd.DataFrame:
        """Get prediction data with optional limit"""
        if limit:
            return self.predictions_df.head(limit)
        return self.predictions_df

    def calculate_churn_risk(self, customer: Dict[str, Any]) -> float:
        """Calculate churn risk score for a customer"""
        risk_score = 0
        
        # Age factor
        age = customer.get('Customer_Age', 0)
        if age > 60:
            risk_score += 10
        elif age < 30:
            risk_score += 15
        
        # Inactivity factor
        inactive_months = customer.get('Months_Inactive_12_mon', 0)
        if inactive_months > 3:
            risk_score += 20
        
        # Contact frequency factor
        contacts = customer.get('Contacts_Count_12_mon', 0)
        if contacts > 4:
            risk_score += 15
        
        # Utilization factor
        utilization = customer.get('Avg_Utilization_Ratio', 0)
        if utilization > 0.7:
            risk_score += 25
        elif utilization < 0.1:
            risk_score += 10
        
        # Transaction factor
        transactions = customer.get('Total_Trans_Ct', 0)
        if transactions < 20:
            risk_score += 20
        
        # Income factor
        income = customer.get('Income_Category', '')
        if income == 'Less than $40K':
            risk_score += 10
        
        return min(risk_score, 100)

    def get_risk_level(self, risk_score: float) -> Dict[str, str]:
        """Get risk level and color based on risk score"""
        if risk_score <= 20:
            return {'level': 'Low', 'color': 'green'}
        elif risk_score <= 50:
            return {'level': 'Medium', 'color': 'orange'}
        else:
            return {'level': 'High', 'color': 'red'}

    def format_currency(self, amount: float) -> str:
        """Format amount as currency"""
        return f"${amount:,.0f}"

    def search_customers(self, search_term: str = '', risk_filter: str = 'all', 
                        status_filter: str = 'all') -> pd.DataFrame:
        """Search and filter customers"""
        df = self.customers_df.copy()
        
        # Add calculated risk scores
        df['churn_risk'] = df.apply(lambda row: self.calculate_churn_risk(row.to_dict()), axis=1)
        df['risk_level'] = df['churn_risk'].apply(lambda x: self.get_risk_level(x)['level'])
        
        # Apply search filter
        if search_term:
            mask = (
                df['CLIENTNUM'].astype(str).str.contains(search_term, case=False, na=False) |
                df['Income_Category'].str.contains(search_term, case=False, na=False) |
                df['Education_Level'].str.contains(search_term, case=False, na=False)
            )
            df = df[mask]
        
        # Apply risk filter
        if risk_filter != 'all':
            if risk_filter == 'low':
                df = df[df['churn_risk'] <= 20]
            elif risk_filter == 'medium':
                df = df[(df['churn_risk'] > 20) & (df['churn_risk'] <= 50)]
            elif risk_filter == 'high':
                df = df[df['churn_risk'] > 50]
        
        # Apply status filter
        if status_filter != 'all':
            if status_filter == 'existing':
                df = df[df['Attrition_Flag'] == 'Existing Customer']
            elif status_filter == 'attrited':
                df = df[df['Attrition_Flag'] == 'Attrited Customer']
        
        return df

    def get_customer_stats(self, filtered_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate statistics for filtered customer data"""
        total = len(filtered_df)
        if total == 0:
            return {
                'total': 0,
                'attrited': 0,
                'high_risk': 0,
                'avg_credit_limit': '$0',
                'churn_rate': '0.0'
            }
        
        attrited = len(filtered_df[filtered_df['Attrition_Flag'] == 'Attrited Customer'])
        high_risk = len(filtered_df[filtered_df['churn_risk'] > 50])
        avg_credit_limit = filtered_df['Credit_Limit'].mean()
        churn_rate = (attrited / total) * 100
        
        return {
            'total': total,
            'attrited': attrited,
            'high_risk': high_risk,
            'avg_credit_limit': self.format_currency(avg_credit_limit),
            'churn_rate': f'{churn_rate:.1f}'
        }

# Create singleton instance
customer_data = CustomerDataService()



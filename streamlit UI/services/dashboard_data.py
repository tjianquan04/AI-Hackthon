# Dashboard Data Service - Streamlit version
import json
import os
import pandas as pd
from typing import Dict, Any, Optional

class DashboardDataService:
    def __init__(self):
        self.data = None
        self._load_data()

    def _load_data(self):
        """Load churn analysis data from JSON file"""
        try:
            # Try multiple paths to find the churn analysis JSON
            json_paths = [
                'services/churn_analysis.json',
                '../outputs/dashboard_data/churn_analysis.json',
                '../../outputs/dashboard_data/churn_analysis.json',
                '../UI/src/services/churn_analysis.json'
            ]
            
            for path in json_paths:
                try:
                    with open(path, 'r') as f:
                        self.data = json.load(f)
                    break
                except FileNotFoundError:
                    continue
                    
            # If no file found, create sample data
            if self.data is None:
                self.data = self._create_sample_data()
                
        except Exception as e:
            print(f"Error loading dashboard data: {e}")
            self.data = self._create_sample_data()

    def _create_sample_data(self) -> Dict[str, Any]:
        """Create sample dashboard data if JSON file is not available"""
        return {
            "summary_kpis": {
                "kpi_metrics": {
                    "total_customers": 10127,
                    "churned_customers": 1627,
                    "overall_churn_rate": 0.1607,
                    "retention_rate": 0.8393,
                    "avg_customer_age": 46.33,
                    "avg_tenure_months": 35.93,
                    "avg_credit_limit": 8631.95,
                    "avg_transaction_amount": 4404.09
                },
                "risk_segments": {
                    "high_risk_customers": 2532,
                    "medium_risk_customers": 3795,
                    "low_risk_customers": 3800
                }
            },
            "churn_overview": {
                "overall_churn_rate": {
                    "total_customers": 10127,
                    "churned_customers": 1627,
                    "churn_rate": 0.1607,
                    "retention_rate": 0.8393
                },
                "churn_by_age": {
                    "<30": {"Total_Customers": 265, "Churned_Count": 32, "Churn_Rate": 0.121},
                    "30-40": {"Total_Customers": 2132, "Churned_Count": 310, "Churn_Rate": 0.145},
                    "40-50": {"Total_Customers": 4652, "Churned_Count": 779, "Churn_Rate": 0.167},
                    "50-60": {"Total_Customers": 2673, "Churned_Count": 448, "Churn_Rate": 0.168},
                    "60+": {"Total_Customers": 405, "Churned_Count": 58, "Churn_Rate": 0.143}
                },
                "churn_by_income": {
                    "$120K +": {"Total_Customers": 727, "Churned_Count": 126, "Churn_Rate": 0.173},
                    "$40K - $60K": {"Total_Customers": 1790, "Churned_Count": 271, "Churn_Rate": 0.151},
                    "$60K - $80K": {"Total_Customers": 1402, "Churned_Count": 189, "Churn_Rate": 0.135},
                    "$80K - $120K": {"Total_Customers": 1535, "Churned_Count": 242, "Churn_Rate": 0.158},
                    "Less than $40K": {"Total_Customers": 3561, "Churned_Count": 612, "Churn_Rate": 0.172},
                    "Unknown Income": {"Total_Customers": 1112, "Churned_Count": 187, "Churn_Rate": 0.168}
                }
            },
            "churn_drivers": {
                "key_insights": [
                    {
                        "category": "Inactivity Risk",
                        "insight": "Customers inactive for 3+ months have 22.0% churn rate",
                        "risk_level": "Medium"
                    },
                    {
                        "category": "Service Issues",
                        "insight": "Customers with 4+ service contacts have 26.4% churn rate",
                        "risk_level": "High"
                    }
                ]
            }
        }

    def get_kpi_metrics(self) -> Dict[str, Any]:
        """Get KPI metrics for dashboard cards"""
        kpis = self.data.get('summary_kpis', {}).get('kpi_metrics', {})
        risk_segments = self.data.get('summary_kpis', {}).get('risk_segments', {})
        
        return {
            'total_customers': kpis.get('total_customers', 0),
            'churned_customers': kpis.get('churned_customers', 0),
            'churn_rate': round(kpis.get('overall_churn_rate', 0) * 100, 1),
            'retention_rate': round(kpis.get('retention_rate', 0) * 100, 1),
            'avg_customer_age': round(kpis.get('avg_customer_age', 0)),
            'avg_tenure': round(kpis.get('avg_tenure_months', 0)),
            'avg_credit_limit': round(kpis.get('avg_credit_limit', 0)),
            'avg_transaction_amount': round(kpis.get('avg_transaction_amount', 0)),
            'high_risk_customers': risk_segments.get('high_risk_customers', 0),
            'medium_risk_customers': risk_segments.get('medium_risk_customers', 0),
            'low_risk_customers': risk_segments.get('low_risk_customers', 0)
        }

    def get_churn_overview(self) -> Dict[str, Any]:
        """Get churn overview data for charts"""
        return self.data.get('churn_overview', {})

    def get_demographics(self) -> Dict[str, Any]:
        """Get demographic data"""
        return self.data.get('demographics', {})

    def get_financial_behavior(self) -> Dict[str, Any]:
        """Get financial behavior data"""
        return self.data.get('financial_behavior', {})

    def get_customer_activity(self) -> Dict[str, Any]:
        """Get customer activity data"""
        return self.data.get('customer_activity', {})

    def get_product_engagement(self) -> Dict[str, Any]:
        """Get product engagement data"""
        return self.data.get('product_engagement', {})

    def get_customer_value(self) -> Dict[str, Any]:
        """Get customer value data"""
        return self.data.get('customer_value', {})

    def get_churn_drivers(self) -> Dict[str, Any]:
        """Get churn drivers and insights"""
        return self.data.get('churn_drivers', {})

    def get_age_group_chart_data(self) -> Dict[str, Any]:
        """Get age group data formatted for charts"""
        churn_by_age = self.get_churn_overview().get('churn_by_age', {})
        
        age_groups = []
        for group, data in churn_by_age.items():
            age_groups.append({
                'ageGroup': group,
                'totalCustomers': data.get('Total_Customers', 0),
                'churnedCustomers': data.get('Churned_Count', 0),
                'churnRate': round(data.get('Churn_Rate', 0) * 100, 1)
            })
        
        return {'ageGroups': age_groups}

    def get_income_chart_data(self) -> Dict[str, Any]:
        """Get income data formatted for charts"""
        churn_by_income = self.get_churn_overview().get('churn_by_income', {})
        
        income_groups = []
        for group, data in churn_by_income.items():
            income_groups.append({
                'incomeCategory': group,
                'totalCustomers': data.get('Total_Customers', 0),
                'churnedCustomers': data.get('Churned_Count', 0),
                'churnRate': round(data.get('Churn_Rate', 0) * 100, 1)
            })
        
        return {'incomeGroups': income_groups}

    def get_card_category_data(self) -> Dict[str, Any]:
        """Get card category data"""
        churn_by_card = self.get_churn_overview().get('churn_by_card_type', {})
        
        labels = []
        customer_counts = []
        churn_rates = []
        
        for card_type, data in churn_by_card.items():
            labels.append(card_type)
            customer_counts.append(data.get('Total_Customers', 0))
            churn_rates.append(round(data.get('Churn_Rate', 0) * 100, 1))
        
        return {
            'labels': labels,
            'customer_counts': customer_counts,
            'churn_rates': churn_rates
        }

    def get_activity_chart_data(self) -> Dict[str, Any]:
        """Get activity data for charts"""
        activity_data = self.get_customer_activity()
        
        # Process contact data
        contacts_data = activity_data.get('churn_by_service_contacts', {})
        contact_labels = []
        contact_churn_rates = []
        for contacts, data in contacts_data.items():
            contact_labels.append(contacts)
            contact_churn_rates.append(round(data.get('Churn_Rate', 0) * 100, 1))
        
        # Process inactive months data
        inactive_data = activity_data.get('churn_by_months_inactive', {})
        inactive_labels = []
        inactive_churn_rates = []
        for months, data in inactive_data.items():
            inactive_labels.append(months)
            inactive_churn_rates.append(round(data.get('Churn_Rate', 0) * 100, 1))
        
        return {
            'inactivity': {
                'labels': inactive_labels,
                'data': inactive_churn_rates
            },
            'service_contacts': {
                'labels': contact_labels,
                'data': contact_churn_rates
            }
        }

    def get_financial_chart_data(self) -> Dict[str, Any]:
        """Get financial data for charts"""
        financial_data = self.get_financial_behavior()
        
        # Process credit limit data
        credit_data = financial_data.get('churn_by_credit_limit', {})
        credit_labels = []
        credit_churn_rates = []
        for category, data in credit_data.items():
            credit_labels.append(category)
            credit_churn_rates.append(round(data.get('Churn_Rate', 0) * 100, 1))
        
        # Process utilization data
        utilization_data = financial_data.get('churn_by_utilization', {})
        utilization_labels = []
        utilization_churn_rates = []
        for category, data in utilization_data.items():
            utilization_labels.append(category)
            utilization_churn_rates.append(round(data.get('Churn_Rate', 0) * 100, 1))
        
        return {
            'utilization': {
                'labels': utilization_labels,
                'data': utilization_churn_rates
            },
            'credit_limit': {
                'labels': credit_labels,
                'data': credit_churn_rates
            }
        }

    def get_customer_segments(self) -> Dict[str, Any]:
        """Get customer segmentation data"""
        product_engagement = self.get_product_engagement()
        customer_value = self.get_customer_value()
        
        # Process engagement data
        engagement_data = product_engagement.get('churn_by_product_engagement', {})
        engagement_segments = []
        for segment, data in engagement_data.items():
            engagement_segments.append({
                'segment': segment,
                'totalCustomers': data.get('Total_Customers', 0),
                'churnedCustomers': data.get('Churned_Count', 0),
                'churnRate': round(data.get('Churn_Rate', 0) * 100, 1)
            })
        
        # Process value data
        value_data = customer_value.get('churn_by_customer_value', {})
        value_segments = []
        for segment, data in value_data.items():
            value_segments.append({
                'valueSegment': segment,
                'totalCustomers': data.get('Total_Customers', 0),
                'churnedCustomers': data.get('Churned_Count', 0),
                'churnRate': round(data.get('Churn_Rate', 0) * 100, 1)
            })
        
        return {
            'engagementSegments': engagement_segments,
            'valueSegments': value_segments
        }

    def get_risk_insights_summary(self) -> Dict[str, Any]:
        """Get risk insights and recommendations"""
        churn_drivers = self.get_churn_drivers()
        insights = churn_drivers.get('key_insights', [])
        
        return {
            'insights': insights,
            'totalInsights': len(insights),
            'highRiskInsights': len([i for i in insights if i.get('risk_level') == 'High']),
            'mediumRiskInsights': len([i for i in insights if i.get('risk_level') == 'Medium'])
        }

    def get_tenure_chart_data(self) -> Dict[str, Any]:
        """Get tenure analysis data"""
        churn_by_tenure = self.get_churn_overview().get('churn_by_tenure', {})
        
        chart_data = []
        for group, data in churn_by_tenure.items():
            if data.get('Total_Customers', 0) > 0:  # Skip empty groups
                chart_data.append({
                    'name': group,
                    'customers': data.get('Total_Customers', 0),
                    'churned': data.get('Churned_Count', 0),
                    'churn_rate': round(data.get('Churn_Rate', 0) * 100, 1) if data.get('Churn_Rate') else 0
                })
        
        return {'chart_data': chart_data}

    def get_widget_data(self, widget_type: str) -> Optional[Dict[str, Any]]:
        """Get data for specific dashboard widgets"""
        widget_map = {
            'kpi': self.get_kpi_metrics,
            'ageGroup': self.get_age_group_chart_data,
            'income': self.get_income_chart_data,
            'cardCategory': self.get_card_category_data,
            'activity': self.get_activity_chart_data,
            'financial': self.get_financial_chart_data,
            'segments': self.get_customer_segments,
            'insights': self.get_risk_insights_summary,
            'tenure': self.get_tenure_chart_data
        }
        
        if widget_type in widget_map:
            return widget_map[widget_type]()
        return None

    def get_key_insights(self) -> Dict[str, Any]:
        """Get key insights data for the insights component"""
        churn_drivers = self.get_churn_drivers()
        insights = churn_drivers.get('key_insights', [])
        
        # Format insights for the component
        formatted_insights = []
        for insight in insights:
            formatted_insights.append({
                'category': insight.get('category', 'General'),
                'description': insight.get('insight', 'No description available'),
                'risk_level': insight.get('risk_level', 'Medium')
            })
        
        # Generate top features data (placeholder)
        top_features = [
            {'feature': 'Total_Trans_Ct', 'importance': 37.1},
            {'feature': 'Total_Revolving_Bal', 'importance': 26.3},
            {'feature': 'Contacts_Count_12_mon', 'importance': 20.4},
            {'feature': 'Avg_Utilization_Ratio', 'importance': 17.8},
            {'feature': 'Total_Trans_Amt', 'importance': 16.9}
        ]
        
        return {
            'insights': formatted_insights,
            'top_features': top_features
        }

    def get_age_chart_data(self) -> Dict[str, Any]:
        """Get age chart data formatted for components"""
        age_data = self.get_age_group_chart_data()
        
        # Convert to format expected by component
        labels = [group['ageGroup'] for group in age_data['ageGroups']]
        churn_rates = [group['churnRate'] for group in age_data['ageGroups']]
        customer_counts = [group['totalCustomers'] for group in age_data['ageGroups']]
        
        return {
            'labels': labels,
            'churn_rates': churn_rates,
            'customer_counts': customer_counts
        }

    def get_customer_segments(self) -> Dict[str, Any]:
        """Get customer segments data formatted for components"""
        # Get the raw segments data using the existing method
        product_engagement = self.get_product_engagement()
        customer_value = self.get_customer_value()
        
        # Process engagement data
        engagement_data = product_engagement.get('churn_by_product_engagement', {})
        engagement_labels = list(engagement_data.keys())
        engagement_churn_rates = [data.get('Churn_Rate', 0) * 100 for data in engagement_data.values()]
        engagement_counts = [data.get('Total_Customers', 0) for data in engagement_data.values()]
        
        # Process value data
        value_data = customer_value.get('churn_by_customer_value', {})
        value_labels = list(value_data.keys())
        value_churn_rates = [data.get('Churn_Rate', 0) * 100 for data in value_data.values()]
        value_counts = [data.get('Total_Customers', 0) for data in value_data.values()]
        
        return {
            'by_engagement': {
                'labels': engagement_labels,
                'churn_rates': engagement_churn_rates,
                'customer_counts': engagement_counts
            },
            'by_value': {
                'labels': value_labels,
                'churn_rates': value_churn_rates,
                'customer_counts': value_counts
            }
        }

    # Add missing methods for churn_charts.py compatibility
    def get_income_chart_data(self) -> Dict[str, Any]:
        """Get income chart data formatted for charts component"""
        # Get income data from existing method and reformat
        churn_by_income = self.get_churn_overview().get('churn_by_income', {})
        
        labels = list(churn_by_income.keys())
        churn_rates = [round(data.get('Churn_Rate', 0) * 100, 1) for data in churn_by_income.values()]
        customer_counts = [data.get('Total_Customers', 0) for data in churn_by_income.values()]
        
        return {
            'labels': labels,
            'churn_rates': churn_rates,
            'customer_counts': customer_counts
        }

# Create singleton instance
dashboard_data = DashboardDataService()

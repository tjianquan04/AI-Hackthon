# Main Streamlit Application - Customer Churn Analytics Dashboard
import streamlit as st
import sys
import os

# Add the current directory to the Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import components
from components.kpi_cards import render_kpi_cards, render_additional_kpis
from components.churn_charts import (
    render_income_analysis, render_age_analysis, render_card_category_analysis,
    render_activity_analysis, render_financial_analysis, render_tenure_analysis
)
from components.customer_segments import render_customer_segments, render_actionable_insights
from components.insights import render_churn_insights, render_action_recommendations

# Import pages
from pages.customers import render_customer_page
from pages.predictions import render_predictions_page

def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Customer Churn Analytics",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main > div {
        padding-top: 1rem;
    }
    
    .stMetric {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    .stPlotlyChart {
        background-color: white;
        border-radius: 0.5rem;
    }
    
    .css-1d391kg {
        padding-top: 1rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #f1f5f9;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-left: 20px;
        padding-right: 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6;
        color: white;
    }
    
    h1 {
        color: #1f2937;
        font-weight: 700;
    }
    
    h2 {
        color: #374151;
        font-weight: 600;
    }
    
    h3 {
        color: #4b5563;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        st.title("🏦 Bank Churn Analytics")
        st.markdown("---")
        
        # Navigation
        page = st.selectbox(
            "📍 Navigate to:",
            options=["Dashboard", "Customer Database", "Predictions"],
            index=0
        )
        
        st.markdown("---")
        
        # Quick stats or info
        st.markdown("""
        **📊 Dashboard Features:**
        - Real-time churn analytics
        - Customer risk assessment
        - Predictive insights
        - Actionable recommendations
        
        **💡 Quick Actions:**
        - Filter high-risk customers
        - Download reports
        - Export predictions
        """)
        
        st.markdown("---")
        st.caption("📈 AI-Powered Customer Analytics")
        
    return page

def render_dashboard():
    """Render the main dashboard page"""
    # Header
    st.title("📊 Customer Churn Analytics Dashboard")
    st.markdown("""
    <div style='background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%); 
                color: white; 
                padding: 1rem; 
                border-radius: 0.5rem; 
                margin-bottom: 2rem;'>
        <h3 style='margin: 0; color: white;'>🔴 Live Analytics Dashboard</h3>
        <p style='margin: 0.5rem 0 0 0; color: #dbeafe;'>
            Advanced EDA insights from 10,127+ customers • Real-time business intelligence for data-driven retention strategies
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Cards
    st.subheader("📈 Key Performance Indicators")
    render_kpi_cards()
    
    # Additional KPIs in expander
    render_additional_kpis()
    
    st.markdown("---")
    
    # Main Analytics Section
    st.subheader("🎯 Core Analytics")
    
    # Create tabs for different analysis sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Demographic Analysis", 
        "💰 Financial Analysis", 
        "🎯 Customer Segments", 
        "🧠 Insights & Actions"
    ])
    
    with tab1:
        st.markdown("### 👥 Demographic Churn Patterns")
        
        # Income and Age Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            render_income_analysis()
        
        with col2:
            render_age_analysis()
        
        st.markdown("---")
        
        # Card Category and Tenure Analysis
        render_card_category_analysis()
        
        st.markdown("---")
        
        render_tenure_analysis()
    
    with tab2:
        st.markdown("### 💰 Financial Behavior Analysis")
        
        render_financial_analysis()
        
        st.markdown("---")
        
        render_activity_analysis()
    
    with tab3:
        st.markdown("### 🎯 Customer Segmentation")
        
        render_customer_segments()
        
        st.markdown("---")
        
        render_actionable_insights()
    
    with tab4:
        st.markdown("### 🧠 AI-Driven Insights")
        
        render_churn_insights()
        
        st.markdown("---")
        
        render_action_recommendations()

def main():
    """Main application entry point"""
    # Configure page
    configure_page()
    
    # Render sidebar and get selected page
    selected_page = render_sidebar()
    
    # Route to appropriate page
    if selected_page == "Dashboard":
        render_dashboard()
    elif selected_page == "Customer Database":
        render_customer_page()
    elif selected_page == "Predictions":
        render_predictions_page()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6b7280; font-size: 0.875rem; padding: 1rem;'>
        🤖 Powered by Advanced Machine Learning & SHAP Explanations<br>
        📊 Customer Churn Analytics Dashboard v2.0
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()



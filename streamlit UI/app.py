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
    
    # Enhanced Custom CSS for modern dark theme
    st.markdown("""
    <style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    .main > div {
        padding-top: 1rem;
    }
    
    /* Content container styling */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Enhanced Metric Cards */
    .stMetric {
        background: linear-gradient(145deg, #1e293b, #334155);
        border: 1px solid #475569;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        color: #f1f5f9;
        transition: transform 0.2s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    }
    
    .stMetric label {
        color: #94a3b8 !important;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    .stMetric div[data-testid="metric-value"] {
        color: #f1f5f9 !important;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    .stMetric div[data-testid="metric-delta"] {
        font-weight: 500;
    }
    
    /* Chart containers */
    .stPlotlyChart {
        background: linear-gradient(145deg, #1e293b, #334155);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid #334155;
    }
    
    .sidebar .sidebar-content {
        background: transparent;
    }
    
    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(30, 41, 59, 0.5);
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid #334155;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background: rgba(51, 65, 85, 0.6);
        border-radius: 8px;
        border: 1px solid transparent;
        color: #94a3b8;
        font-weight: 500;
        padding-left: 20px;
        padding-right: 20px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(71, 85, 105, 0.8);
        color: #e2e8f0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white !important;
        font-weight: 600;
        border: 1px solid #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Typography */
    h1 {
        color: #f1f5f9 !important;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    h2 {
        color: #e2e8f0 !important;
        font-weight: 600;
    }
    
    h3 {
        color: #cbd5e1 !important;
        font-weight: 600;
    }
    
    /* Text elements */
    .stMarkdown p, .stText {
        color: #cbd5e1;
    }
    
    .stCaption {
        color: #94a3b8 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(145deg, #1e293b, #334155) !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        color: #f1f5f9 !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid #334155 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }
    
    /* Alert boxes */
    .stAlert {
        background: rgba(30, 41, 59, 0.9) !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        color: #f1f5f9 !important;
    }
    
    /* Success, warning, error alerts */
    .stAlert[data-baseweb="notification"] > div {
        background: transparent !important;
    }
    
    /* Columns spacing */
    .row-widget.stHorizontal > div {
        padding: 0 0.5rem;
    }
    
    /* Selectbox and other inputs */
    .stSelectbox > div > div {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        color: #f1f5f9 !important;
    }
    
    /* Progress indicators */
    .stProgress > div > div {
        background: linear-gradient(90deg, #3b82f6, #1d4ed8) !important;
    }
    
    /* Custom gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    /* Modern card styling */
    .metric-card {
        background: linear-gradient(145deg, #1e293b, #334155);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    }
    
    /* Header gradient */
    .dashboard-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #1d4ed8 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the enhanced sidebar navigation"""
    with st.sidebar:
        # Enhanced sidebar header
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0; margin-bottom: 1rem;'>
            <h2 style='color: #f1f5f9; margin: 0; font-size: 1.5rem;'>🏦 Bank Churn Analytics</h2>
            <p style='color: #94a3b8; margin: 0.5rem 0 0 0; font-size: 0.85rem;'>AI-Powered Insights</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Enhanced Navigation
        st.markdown("### 📍 Navigation")
        page = st.selectbox(
            "Choose a view:",
            options=["Dashboard", "Customer Database", "Predictions"],
            index=0
        )
        
        st.markdown("---")
        
        # Enhanced Features section
        st.markdown("### 📊 Dashboard Features")
        
        features = [
            ("🔴", "Real-time Analytics", "Live churn monitoring"),
            ("🎯", "Risk Assessment", "Customer risk scoring"),
            ("🧠", "AI Insights", "Predictive analytics"),
            ("📈", "Recommendations", "Actionable strategies")
        ]
        
        for icon, title, desc in features:
            st.markdown(f"""
            <div style='margin-bottom: 0.75rem; padding: 0.5rem; background: rgba(51, 65, 85, 0.3); border-radius: 8px;'>
                <div style='color: #f1f5f9; font-weight: 600; margin-bottom: 0.25rem;'>
                    {icon} {title}
                </div>
                <div style='color: #94a3b8; font-size: 0.8rem;'>
                    {desc}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("### 💡 Quick Actions")
        
        actions = [
            "🔍 Filter high-risk customers",
            "📊 Download reports", 
            "📤 Export predictions",
            "⚙️ Configure alerts"
        ]
        
        for action in actions:
            st.markdown(f"<div style='color: #cbd5e1; margin-bottom: 0.5rem; padding: 0.25rem 0;'>{action}</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Status indicator
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: rgba(34, 197, 94, 0.1); border: 1px solid #22c55e; border-radius: 8px; margin-top: 1rem;'>
            <div style='color: #22c55e; font-weight: 600; margin-bottom: 0.25rem;'>✅ System Status</div>
            <div style='color: #94a3b8; font-size: 0.8rem;'>All systems operational</div>
        </div>
        """, unsafe_allow_html=True)
        
    return page

def render_dashboard():
    """Render the main dashboard page"""
    # Enhanced Header with modern styling
    st.markdown("""
    <div class="dashboard-header">
        <h1 style='margin: 0; color: white; font-size: 2.5rem;'>📊 Customer Churn Analytics Dashboard</h1>
        <div style='margin-top: 1rem; display: flex; align-items: center; gap: 1rem;'>
            <div style='background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; display: inline-flex; align-items: center; gap: 0.5rem;'>
                <div style='width: 8px; height: 8px; background: #22c55e; border-radius: 50%; animation: pulse 2s infinite;'></div>
                <span style='color: white; font-weight: 600; font-size: 0.9rem;'>Live Analytics</span>
            </div>
            <span style='color: #dbeafe; font-size: 1rem;'>
                Advanced EDA insights from <strong>10,127+</strong> customers • Real-time business intelligence for data-driven retention strategies
            </span>
        </div>
    </div>
    <style>
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    </style>
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
    
    # Enhanced Footer
    st.markdown("""
    <div style='margin-top: 3rem; padding: 2rem 0; border-top: 1px solid #334155; background: rgba(15, 23, 42, 0.8);'>
        <div style='text-align: center;'>
            <div style='display: flex; justify-content: center; align-items: center; gap: 2rem; margin-bottom: 1rem; flex-wrap: wrap;'>
                <div style='display: flex; align-items: center; gap: 0.5rem;'>
                    <span style='color: #3b82f6; font-size: 1.2rem;'>🤖</span>
                    <span style='color: #e2e8f0; font-weight: 500;'>Advanced ML</span>
                </div>
                <div style='display: flex; align-items: center; gap: 0.5rem;'>
                    <span style='color: #10b981; font-size: 1.2rem;'>🧠</span>
                    <span style='color: #e2e8f0; font-weight: 500;'>SHAP Explanations</span>
                </div>
                <div style='display: flex; align-items: center; gap: 0.5rem;'>
                    <span style='color: #f59e0b; font-size: 1.2rem;'>📊</span>
                    <span style='color: #e2e8f0; font-weight: 500;'>Real-time Analytics</span>
                </div>
            </div>
            <div style='color: #94a3b8; font-size: 0.9rem; margin-bottom: 0.5rem;'>
                Customer Churn Analytics Dashboard v2.0
            </div>
            <div style='color: #64748b; font-size: 0.8rem;'>
                Built with ❤️ using Streamlit • Powered by Python & Machine Learning
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()



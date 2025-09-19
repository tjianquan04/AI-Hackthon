# KPI Cards Component - Streamlit version
import streamlit as st
from services.dashboard_data import dashboard_data

def render_kpi_cards():
    """Render KPI cards with responsive layout"""
    
    # Get KPI metrics
    metrics = dashboard_data.get_kpi_metrics()
    
    # Create responsive columns (2x2 on mobile, 1x4 on desktop)
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap="medium")
    
    with col1:
        st.metric(
            label="👥 Total Customers",
            value=f"{metrics['total_customers']:,}",
            help=f"Average Age: {metrics['avg_customer_age']:.1f} years"
        )
        st.caption(f"🎂 Avg Age: {metrics['avg_customer_age']:.1f}y")
    
    with col2:
        st.metric(
            label="⚠️ Churned", 
            value=f"{metrics['churned_customers']:,}",
            delta=f"{metrics['churn_rate']:.1f}% rate",
            delta_color="inverse"
        )
        st.caption("📉 Lost customers")
    
    with col3:
        st.metric(
            label="📊 Churn Rate",
            value=f"{metrics['churn_rate']:.1f}%",
            delta=f"{metrics['retention_rate']:.1f}% retained",
            delta_color="inverse"
        )
        st.caption("🎯 Above target")
    
    with col4:
        st.metric(
            label="🛡️ High-Risk",
            value=f"{metrics['high_risk_customers']:,}",
            delta="Priority attention",
            delta_color="off"
        )
        st.caption("⚡ Requiring action")

def render_additional_kpis():
    """Render additional KPI metrics in an expander"""
    with st.expander("📈 Additional Metrics", expanded=False):
        metrics = dashboard_data.get_kpi_metrics()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="💰 Avg Credit Limit",
                value=f"${metrics['avg_credit_limit']:,}",
                help="Average credit limit across all customers"
            )
        
        with col2:
            st.metric(
                label="🕐 Avg Tenure",
                value=f"{metrics['avg_tenure']} months",
                help="Average months on book"
            )
        
        with col3:
            st.metric(
                label="💳 Avg Transaction Amount",
                value=f"${metrics['avg_transaction_amount']:,}",
                help="Average transaction amount per customer"
            )
        
        # Risk distribution
        st.subheader("🎯 Risk Distribution")
        risk_col1, risk_col2, risk_col3 = st.columns(3)
        
        with risk_col1:
            st.metric("🟢 Low Risk", f"{metrics['low_risk_customers']:,}")
        with risk_col2:
            st.metric("🟡 Medium Risk", f"{metrics['medium_risk_customers']:,}")
        with risk_col3:
            st.metric("🔴 High Risk", f"{metrics['high_risk_customers']:,}")



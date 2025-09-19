# Customer Segments Analysis - Streamlit version
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from services.dashboard_data import dashboard_data

def render_customer_segments():
    """Render customer segmentation analysis"""
    st.subheader("🎯 Customer Segmentation Analysis")
    st.caption("Value-based and engagement-based customer segments")
    
    # Get segments data
    segments_data = dashboard_data.get_customer_segments()
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_value_segments(segments_data['by_value'])
    
    with col2:
        render_engagement_segments(segments_data['by_engagement'])

def render_value_segments(value_data):
    """Render customer value segments"""
    st.write("**🏆 Customer Value Segments**")
    
    # Create DataFrame
    df = pd.DataFrame({
        'Value Segment': value_data['labels'],
        'Churn Rate (%)': value_data['churn_rates'],
        'Customer Count': value_data['customer_counts']
    })
    
    # Create horizontal bar chart
    fig = px.bar(
        df,
        x='Churn Rate (%)',
        y='Value Segment',
        orientation='h',
        title='Churn Rate by Customer Value',
        color='Churn Rate (%)',
        color_continuous_scale='RdYlGn_r',
        hover_data=['Customer Count']
    )
    
    fig.update_layout(
        height=350,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Value insights
    if len(df) > 0:
        highest_value_churn = df.loc[df['Churn Rate (%)'].idxmax()]
        st.warning(f"⚠️ **Highest Risk**: {highest_value_churn['Value Segment']} ({highest_value_churn['Churn Rate (%)']:.1f}%)")

def render_engagement_segments(engagement_data):
    """Render product engagement segments"""
    st.write("**📱 Product Engagement Segments**")
    
    # Create DataFrame
    df = pd.DataFrame({
        'Engagement Level': engagement_data['labels'],
        'Churn Rate (%)': engagement_data['churn_rates'],
        'Customer Count': engagement_data['customer_counts']
    })
    
    # Create donut chart for customer distribution
    fig_donut = px.pie(
        df,
        values='Customer Count',
        names='Engagement Level',
        title='Customer Distribution by Engagement',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
    fig_donut.update_layout(height=350)
    
    st.plotly_chart(fig_donut, use_container_width=True)
    
    # Engagement insights
    if len(df) > 0:
        lowest_engagement_churn = df.loc[df['Churn Rate (%)'].idxmin()]
        st.success(f"✅ **Best Retention**: {lowest_engagement_churn['Engagement Level']} ({lowest_engagement_churn['Churn Rate (%)']:.1f}%)")

def render_segment_comparison():
    """Render segment comparison analysis"""
    with st.expander("🔍 Detailed Segment Analysis", expanded=False):
        st.subheader("Customer Segment Comparison")
        
        segments_data = dashboard_data.get_customer_segments()
        
        # Combined analysis
        tab1, tab2 = st.tabs(["📊 Value Analysis", "📱 Engagement Analysis"])
        
        with tab1:
            value_df = pd.DataFrame({
                'Segment': segments_data['by_value']['labels'],
                'Churn Rate (%)': segments_data['by_value']['churn_rates'],
                'Customer Count': segments_data['by_value']['customer_counts']
            })
            
            # Scatter plot: Customer Count vs Churn Rate
            fig_scatter = px.scatter(
                value_df,
                x='Customer Count',
                y='Churn Rate (%)',
                size='Customer Count',
                color='Segment',
                title='Customer Value: Count vs Churn Risk',
                hover_name='Segment'
            )
            
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Value metrics
            col1, col2, col3 = st.columns(3)
            
            total_customers = sum(value_df['Customer Count'])
            avg_churn_rate = sum(value_df['Churn Rate (%)']) / len(value_df)
            
            with col1:
                st.metric("Total Customers", f"{total_customers:,}")
            with col2:
                st.metric("Avg Churn Rate", f"{avg_churn_rate:.1f}%")
            with col3:
                high_value_customers = value_df[value_df['Segment'].str.contains('High', case=False)]
                if not high_value_customers.empty:
                    st.metric("High Value Churn", f"{high_value_customers['Churn Rate (%)'].iloc[0]:.1f}%")
        
        with tab2:
            engagement_df = pd.DataFrame({
                'Engagement': segments_data['by_engagement']['labels'],
                'Churn Rate (%)': segments_data['by_engagement']['churn_rates'],
                'Customer Count': segments_data['by_engagement']['customer_counts']
            })
            
            # Bar chart for engagement
            fig_engagement = px.bar(
                engagement_df,
                x='Engagement',
                y=['Churn Rate (%)', 'Customer Count'],
                title='Engagement Analysis: Churn vs Volume',
                barmode='group'
            )
            
            fig_engagement.update_layout(height=400)
            st.plotly_chart(fig_engagement, use_container_width=True)
            
            # Engagement metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Engagement Segments", len(engagement_df))
            with col2:
                if not engagement_df.empty:
                    best_engagement = engagement_df.loc[engagement_df['Churn Rate (%)'].idxmin()]
                    st.metric("Best Engagement", best_engagement['Engagement'])
            with col3:
                if not engagement_df.empty:
                    worst_engagement = engagement_df.loc[engagement_df['Churn Rate (%)'].idxmax()]
                    st.metric("Worst Engagement", worst_engagement['Engagement'])

def render_actionable_insights():
    """Render actionable insights from segmentation"""
    st.subheader("💡 Actionable Insights")
    
    segments_data = dashboard_data.get_customer_segments()
    
    # Generate insights based on data
    insights = []
    
    # Value-based insights
    value_data = segments_data['by_value']
    if value_data['labels'] and value_data['churn_rates']:
        max_churn_idx = value_data['churn_rates'].index(max(value_data['churn_rates']))
        high_risk_segment = value_data['labels'][max_churn_idx]
        high_risk_rate = value_data['churn_rates'][max_churn_idx]
        
        insights.append({
            'type': 'warning',
            'title': 'High-Risk Value Segment',
            'message': f'{high_risk_segment} customers have {high_risk_rate:.1f}% churn rate - immediate intervention needed'
        })
    
    # Engagement-based insights
    engagement_data = segments_data['by_engagement']
    if engagement_data['labels'] and engagement_data['churn_rates']:
        min_churn_idx = engagement_data['churn_rates'].index(min(engagement_data['churn_rates']))
        best_segment = engagement_data['labels'][min_churn_idx]
        best_rate = engagement_data['churn_rates'][min_churn_idx]
        
        insights.append({
            'type': 'success',
            'title': 'Best Practice Segment',
            'message': f'{best_segment} customers show {best_rate:.1f}% churn rate - replicate engagement strategies'
        })
    
    # Display insights
    for insight in insights:
        if insight['type'] == 'warning':
            st.warning(f"⚠️ **{insight['title']}**: {insight['message']}")
        elif insight['type'] == 'success':
            st.success(f"✅ **{insight['title']}**: {insight['message']}")
        else:
            st.info(f"ℹ️ **{insight['title']}**: {insight['message']}")
    
    # Recommendations
    with st.expander("📋 Strategic Recommendations", expanded=False):
        st.markdown("""
        **Customer Value Optimization:**
        - 🎯 Focus retention efforts on high-value segments with elevated churn rates
        - 💰 Implement tiered loyalty programs based on customer value
        - 📈 Upsell low-value customers to higher tiers
        
        **Engagement Enhancement:**
        - 📱 Increase product adoption for low-engagement segments
        - 🎓 Provide training and onboarding for complex products
        - 🔄 Create feedback loops to improve user experience
        
        **Risk Mitigation:**
        - 🚨 Set up automated alerts for high-risk segment behaviors
        - 🤝 Assign dedicated relationship managers to top-tier customers
        - 📊 Regular segment performance reviews and strategy adjustments
        """)



# Churn Analysis Charts - Streamlit version
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from services.dashboard_data import dashboard_data

def render_income_analysis():
    """Render churn analysis by income"""
    st.subheader("📊 Churn Analysis by Income")
    st.caption("Customer retention rates across income segments • EDA Insights")
    
    # Get income data
    income_data = dashboard_data.get_income_chart_data()
    
    # Create DataFrame for plotting
    df = pd.DataFrame({
        'Income Category': income_data['labels'],
        'Churn Rate (%)': income_data['churn_rates'],
        'Total Customers': income_data['customer_counts']
    })
    
    # Create the bar chart
    fig = px.bar(
        df, 
        x='Income Category', 
        y='Churn Rate (%)',
        title='Churn Rate by Income Category',
        color='Churn Rate (%)',
        color_continuous_scale='Reds',
        hover_data=['Total Customers']
    )
    
    fig.update_layout(
        xaxis_title="Income Category",
        yaxis_title="Churn Rate (%)",
        showlegend=False,
        height=450,
        margin=dict(l=60, r=40, t=80, b=120),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=10),
            automargin=True
        ),
        yaxis=dict(
            tickfont=dict(size=10),
            automargin=True
        ),
        title=dict(
            font=dict(size=14),
            x=0.5,
            xanchor='center'
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    
    for i, (income, churn_rate, customers) in enumerate(zip(
        income_data['labels'], 
        income_data['churn_rates'], 
        income_data['customer_counts']
    )):
        with [col1, col2, col3, col4][i % 4]:
            # Truncate long labels for display
            display_label = income.replace('$', '').replace(' +', '+')
            if len(display_label) > 12:
                display_label = display_label[:9] + "..."
            st.metric(
                label=display_label,
                value=f"{churn_rate:.1f}%",
                help=f"{income}: {customers:,} customers"
            )

def render_age_analysis():
    """Render churn analysis by age"""
    st.subheader("👥 Churn Analysis by Age Groups")
    st.caption("Demographic churn patterns across age segments")
    
    # Get age data
    age_data = dashboard_data.get_age_chart_data()
    
    # Create DataFrame
    df = pd.DataFrame({
        'Age Group': age_data['labels'],
        'Churn Rate (%)': age_data['churn_rates'],
        'Total Customers': age_data['customer_counts']
    })
    
    # Create dual-axis chart
    fig = go.Figure()
    
    # Bar chart for churn rate
    fig.add_trace(go.Bar(
        x=df['Age Group'],
        y=df['Churn Rate (%)'],
        name='Churn Rate (%)',
        marker_color='rgba(239, 68, 68, 0.8)',
        yaxis='y',
        offsetgroup=1
    ))
    
    # Line chart for customer count
    fig.add_trace(go.Scatter(
        x=df['Age Group'],
        y=df['Total Customers'],
        mode='lines+markers',
        name='Total Customers',
        line=dict(color='rgba(59, 130, 246, 0.8)', width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text='Churn Rate and Customer Distribution by Age',
            font=dict(size=14),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(title='Age Group', tickfont=dict(size=10), automargin=True),
        yaxis=dict(title='Churn Rate (%)', side='left', tickfont=dict(size=10), automargin=True),
        yaxis2=dict(title='Total Customers', side='right', overlaying='y', tickfont=dict(size=10), automargin=True),
        height=450,
        margin=dict(l=60, r=80, t=80, b=60),
        hovermode='x',
        legend=dict(x=0, y=1, bgcolor='rgba(255,255,255,0.8)')
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_card_category_analysis():
    """Render card category analysis"""
    st.subheader("💳 Card Category Distribution")
    st.caption("Customer distribution and churn by card type")
    
    # Get card data
    card_data = dashboard_data.get_card_category_data()
    
    # Create pie chart for customer distribution
    fig_pie = px.pie(
        values=card_data['customer_counts'],
        names=card_data['labels'],
        title='Customer Distribution by Card Category',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(height=350)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart for churn rates
        df_bar = pd.DataFrame({
            'Card Type': card_data['labels'],
            'Churn Rate (%)': card_data['churn_rates']
        })
        
        fig_bar = px.bar(
            df_bar,
            x='Card Type',
            y='Churn Rate (%)',
            title='Churn Rate by Card Category',
            color='Churn Rate (%)',
            color_continuous_scale='RdYlBu_r'
        )
        
        fig_bar.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

def render_activity_analysis():
    """Render customer activity analysis"""
    st.subheader("🏃 Customer Activity Patterns")
    st.caption("Impact of customer activity on churn behavior")
    
    # Get activity data
    activity_data = dashboard_data.get_activity_chart_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Inactivity analysis
        st.write("**Churn by Months Inactive**")
        
        df_inactive = pd.DataFrame({
            'Months Inactive': activity_data['inactivity']['labels'],
            'Churn Rate (%)': activity_data['inactivity']['data']
        })
        
        fig_inactive = px.line(
            df_inactive,
            x='Months Inactive',
            y='Churn Rate (%)',
            markers=True,
            title='Churn Rate vs Inactivity Period',
            color_discrete_sequence=['#ef4444']
        )
        
        fig_inactive.update_layout(height=300)
        st.plotly_chart(fig_inactive, use_container_width=True)
    
    with col2:
        # Service contacts analysis
        st.write("**Churn by Service Contacts**")
        
        df_contacts = pd.DataFrame({
            'Service Contacts': activity_data['service_contacts']['labels'],
            'Churn Rate (%)': activity_data['service_contacts']['data']
        })
        
        fig_contacts = px.bar(
            df_contacts,
            x='Service Contacts',
            y='Churn Rate (%)',
            title='Churn Rate vs Service Contacts',
            color='Churn Rate (%)',
            color_continuous_scale='Oranges'
        )
        
        fig_contacts.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig_contacts, use_container_width=True)

def render_financial_analysis():
    """Render financial behavior analysis"""
    st.subheader("💰 Financial Behavior Impact")
    st.caption("Credit utilization and limit effects on churn")
    
    # Get financial data
    financial_data = dashboard_data.get_financial_chart_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Utilization analysis
        st.write("**Churn by Utilization Rate**")
        
        df_util = pd.DataFrame({
            'Utilization Range': financial_data['utilization']['labels'],
            'Churn Rate (%)': financial_data['utilization']['data']
        })
        
        fig_util = px.bar(
            df_util,
            x='Utilization Range',
            y='Churn Rate (%)',
            title='Churn Rate by Credit Utilization',
            color='Churn Rate (%)',
            color_continuous_scale='Blues'
        )
        
        fig_util.update_layout(height=300, showlegend=False, xaxis=dict(tickangle=45))
        st.plotly_chart(fig_util, use_container_width=True)
    
    with col2:
        # Credit limit analysis
        st.write("**Churn by Credit Limit**")
        
        df_credit = pd.DataFrame({
            'Credit Limit Range': financial_data['credit_limit']['labels'],
            'Churn Rate (%)': financial_data['credit_limit']['data']
        })
        
        fig_credit = px.bar(
            df_credit,
            x='Credit Limit Range',
            y='Churn Rate (%)',
            title='Churn Rate by Credit Limit Range',
            color='Churn Rate (%)',
            color_continuous_scale='Greens'
        )
        
        fig_credit.update_layout(height=300, showlegend=False, xaxis=dict(tickangle=45))
        st.plotly_chart(fig_credit, use_container_width=True)

def render_tenure_analysis():
    """Render tenure analysis"""
    st.subheader("📅 Customer Tenure Analysis")
    st.caption("Relationship between customer tenure and churn risk")
    
    # Get tenure data
    tenure_data = dashboard_data.get_tenure_chart_data()
    
    if tenure_data['chart_data']:
        df = pd.DataFrame(tenure_data['chart_data'])
        
        # Create combination chart
        fig = go.Figure()
        
        # Bar chart for churn rate
        fig.add_trace(go.Bar(
            x=df['name'],
            y=df['churn_rate'],
            name='Churn Rate (%)',
            marker_color='rgba(255, 99, 132, 0.7)',
            yaxis='y'
        ))
        
        # Line for customer count
        fig.add_trace(go.Scatter(
            x=df['name'],
            y=df['customers'],
            mode='lines+markers',
            name='Total Customers',
            line=dict(color='rgba(54, 162, 235, 0.8)', width=3),
            marker=dict(size=8),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Churn Rate and Customer Count by Tenure',
            xaxis=dict(title='Tenure Period', tickangle=45),
            yaxis=dict(title='Churn Rate (%)', side='left'),
            yaxis2=dict(title='Total Customers', side='right', overlaying='y'),
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tenure insights
        if len(df) > 0:
            highest_churn_tenure = df.loc[df['churn_rate'].idxmax(), 'name']
            lowest_churn_tenure = df.loc[df['churn_rate'].idxmin(), 'name']
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"🔴 **Highest Churn**: {highest_churn_tenure}")
            with col2:
                st.success(f"🟢 **Lowest Churn**: {lowest_churn_tenure}")
    else:
        st.warning("No tenure data available for analysis")

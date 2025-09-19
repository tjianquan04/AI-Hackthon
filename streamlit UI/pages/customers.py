# Customer Database Page - Streamlit version
import streamlit as st
import pandas as pd
import plotly.express as px
from services.customer_data import customer_data

def render_customer_page():
    """Render the customer database page"""
    st.title("👥 Customer Database")
    st.caption("Complete customer information with risk assessment")
    
    # Add filters in sidebar
    with st.sidebar:
        st.subheader("🔍 Filters")
        
        search_term = st.text_input(
            "Search customers",
            placeholder="ID, income, education...",
            help="Search by customer ID, income category, or education level"
        )
        
        risk_filter = st.selectbox(
            "Risk Level",
            options=['all', 'low', 'medium', 'high'],
            format_func=lambda x: {
                'all': 'All Risk Levels',
                'low': 'Low Risk',
                'medium': 'Medium Risk', 
                'high': 'High Risk'
            }[x]
        )
        
        status_filter = st.selectbox(
            "Customer Status",
            options=['all', 'existing', 'attrited'],
            format_func=lambda x: {
                'all': 'All Status',
                'existing': 'Existing Customer',
                'attrited': 'Attrited Customer'
            }[x]
        )
        
        # Data refresh button
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    # Get filtered customer data
    filtered_df = customer_data.search_customers(search_term, risk_filter, status_filter)
    stats = customer_data.get_customer_stats(filtered_df)
    
    # Display statistics
    render_customer_stats(stats)
    
    # Display customer table
    render_customer_table(filtered_df)
    
    # Customer analytics
    render_customer_analytics(filtered_df)

def render_customer_stats(stats):
    """Render customer statistics cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Total Customers",
            value=f"{stats['total']:,}",
            help="Total customers in filtered view"
        )
    
    with col2:
        st.metric(
            label="⚠️ High Risk",
            value=f"{stats['high_risk']:,}",
            delta=f"{(stats['high_risk']/max(stats['total'], 1)*100):.1f}% of total" if stats['total'] > 0 else "0%",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="📊 Churn Rate",
            value=f"{stats['churn_rate']}%",
            delta="Above average" if float(stats['churn_rate']) > 16 else "Below average",
            delta_color="inverse" if float(stats['churn_rate']) > 16 else "normal"
        )
    
    with col4:
        st.metric(
            label="💰 Avg Credit Limit",
            value=stats['avg_credit_limit'],
            help="Average credit limit for filtered customers"
        )

def render_customer_table(df):
    """Render customer data table"""
    st.subheader("📋 Customer Details")
    
    if df.empty:
        st.info("No customers found matching the current filters.")
        return
    
    # Pagination
    page_size = st.selectbox("Rows per page", [10, 20, 50, 100], index=1)
    
    total_pages = len(df) // page_size + (1 if len(df) % page_size > 0 else 0)
    
    if total_pages > 1:
        page = st.selectbox(f"Page (1-{total_pages})", range(1, total_pages + 1))
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        display_df = df.iloc[start_idx:end_idx]
    else:
        display_df = df
    
    # Format the display dataframe
    display_df = display_df.copy()
    
    # Format currency columns
    currency_cols = ['Credit_Limit', 'Total_Revolving_Bal', 'Avg_Open_To_Buy', 'Total_Trans_Amt']
    for col in currency_cols:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "N/A")
    
    # Format percentage columns
    if 'Avg_Utilization_Ratio' in display_df.columns:
        display_df['Avg_Utilization_Ratio'] = display_df['Avg_Utilization_Ratio'].apply(
            lambda x: f"{x*100:.1f}%" if pd.notna(x) else "N/A"
        )
    
    # Add risk level colors
    def color_risk_level(val):
        if pd.isna(val):
            return ''
        if val <= 20:
            return 'background-color: #dcfce7'  # Light green
        elif val <= 50:
            return 'background-color: #fef3c7'  # Light yellow
        else:
            return 'background-color: #fee2e2'  # Light red
    
    # Style the dataframe
    if 'churn_risk' in display_df.columns:
        styled_df = display_df.style.applymap(color_risk_level, subset=['churn_risk'])
    else:
        styled_df = display_df
    
    # Select columns to display
    display_columns = [
        'CLIENTNUM', 'Customer_Age', 'Gender', 'Income_Category', 
        'Education_Level', 'Card_Category', 'Credit_Limit', 
        'Total_Trans_Amt', 'Total_Trans_Ct', 'churn_risk', 
        'risk_level', 'Attrition_Flag'
    ]
    
    available_columns = [col for col in display_columns if col in display_df.columns]
    
    st.dataframe(
        styled_df[available_columns] if hasattr(styled_df, '__getitem__') else display_df[available_columns],
        use_container_width=True,
        height=400
    )
    
    # Display pagination info
    if total_pages > 1:
        st.caption(f"Showing {start_idx + 1}-{min(end_idx, len(df))} of {len(df)} customers")

def render_customer_analytics(df):
    """Render customer analytics charts"""
    if df.empty:
        return
    
    with st.expander("📊 Customer Analytics", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk distribution
            st.subheader("Risk Level Distribution")
            
            if 'risk_level' in df.columns:
                risk_counts = df['risk_level'].value_counts()
                
                fig_risk = px.pie(
                    values=risk_counts.values,
                    names=risk_counts.index,
                    title="Customer Risk Distribution",
                    color_discrete_map={
                        'Low': '#22c55e',
                        'Medium': '#f59e0b',
                        'High': '#ef4444'
                    }
                )
                
                st.plotly_chart(fig_risk, use_container_width=True)
        
        with col2:
            # Age distribution
            st.subheader("Age Distribution")
            
            if 'Customer_Age' in df.columns:
                fig_age = px.histogram(
                    df,
                    x='Customer_Age',
                    title="Customer Age Distribution",
                    nbins=20,
                    color_discrete_sequence=['#3b82f6']
                )
                
                fig_age.update_layout(showlegend=False)
                st.plotly_chart(fig_age, use_container_width=True)
        
        # Additional analytics
        col3, col4 = st.columns(2)
        
        with col3:
            # Income category distribution
            st.subheader("Income Categories")
            
            if 'Income_Category' in df.columns:
                income_counts = df['Income_Category'].value_counts()
                
                fig_income = px.bar(
                    x=income_counts.index,
                    y=income_counts.values,
                    title="Customers by Income Category",
                    color=income_counts.values,
                    color_continuous_scale='Viridis'
                )
                
                fig_income.update_layout(
                    xaxis_title="Income Category",
                    yaxis_title="Number of Customers",
                    showlegend=False,
                    xaxis=dict(tickangle=45)
                )
                
                st.plotly_chart(fig_income, use_container_width=True)
        
        with col4:
            # Card category distribution  
            st.subheader("Card Categories")
            
            if 'Card_Category' in df.columns:
                card_counts = df['Card_Category'].value_counts()
                
                fig_card = px.bar(
                    x=card_counts.index,
                    y=card_counts.values,
                    title="Customers by Card Category",
                    color=card_counts.values,
                    color_continuous_scale='Plasma'
                )
                
                fig_card.update_layout(
                    xaxis_title="Card Category",
                    yaxis_title="Number of Customers",
                    showlegend=False
                )
                
                st.plotly_chart(fig_card, use_container_width=True)

def render_export_options():
    """Render data export options"""
    with st.expander("📥 Export Data", expanded=False):
        st.subheader("Download Customer Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Download Filtered Data (CSV)"):
                # This would implement CSV download functionality
                st.success("Download functionality would be implemented here")
        
        with col2:
            if st.button("📈 Download Analytics Report"):
                # This would implement analytics report download
                st.success("Analytics report download would be implemented here")

# Main execution
if __name__ == "__main__":
    render_customer_page()



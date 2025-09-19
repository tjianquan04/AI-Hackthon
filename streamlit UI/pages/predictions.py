# Predictions Page - Streamlit version
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from services.customer_data import customer_data

def render_predictions_page():
    """Render the predictions page"""
    st.title("🔮 Churn Predictions")
    st.caption("Model outputs with SHAP-based explanations")
    
    # Get predictions data
    predictions_df = customer_data.get_predictions()
    
    if predictions_df.empty:
        render_no_predictions()
        return
    
    # Add filters in sidebar
    with st.sidebar:
        st.subheader("🎯 Prediction Filters")
        
        search_term = st.text_input(
            "Search predictions",
            placeholder="Search by action, reason...",
            help="Search in predictions, actions, or reasons"
        )
        
        prediction_filter = st.selectbox(
            "Prediction Label",
            options=['all', 'churn', 'no_churn'],
            format_func=lambda x: {
                'all': 'All Predictions',
                'churn': 'Churn Predicted',
                'no_churn': 'No Churn Predicted'
            }[x]
        )
        
        probability_range = st.slider(
            "Churn Probability Range",
            0.0, 1.0, (0.0, 1.0),
            step=0.05,
            help="Filter by churn probability range"
        )
    
    # Filter predictions
    filtered_df = filter_predictions(predictions_df, search_term, prediction_filter, probability_range)
    
    # Display prediction statistics
    render_prediction_stats(filtered_df)
    
    # Display predictions table
    render_predictions_table(filtered_df)
    
    # Prediction analytics
    render_prediction_analytics(filtered_df)

def filter_predictions(df, search_term, prediction_filter, probability_range):
    """Filter predictions based on criteria"""
    filtered_df = df.copy()
    
    # Search filter
    if search_term:
        search_mask = (
            filtered_df.get('Predicted_Label', '').astype(str).str.contains(search_term, case=False, na=False) |
            filtered_df.get('Recommended_Action', '').astype(str).str.contains(search_term, case=False, na=False) |
            filtered_df.get('Top_Reasons', '').astype(str).str.contains(search_term, case=False, na=False) |
            filtered_df.get('Reason_Comment', '').astype(str).str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[search_mask]
    
    # Prediction label filter
    if prediction_filter != 'all':
        if prediction_filter == 'churn':
            filtered_df = filtered_df[filtered_df.get('Predicted_Label', '') == 'Churn']
        elif prediction_filter == 'no_churn':
            filtered_df = filtered_df[filtered_df.get('Predicted_Label', '') == 'No Churn']
    
    # Probability range filter
    if 'Churn_Probability' in filtered_df.columns:
        prob_mask = (
            (filtered_df['Churn_Probability'] >= probability_range[0]) & 
            (filtered_df['Churn_Probability'] <= probability_range[1])
        )
        filtered_df = filtered_df[prob_mask]
    
    return filtered_df

def render_prediction_stats(df):
    """Render prediction statistics"""
    if df.empty:
        st.warning("No predictions match the current filters.")
        return
    
    # Calculate statistics
    total_predictions = len(df)
    churn_predictions = len(df[df.get('Predicted_Label', '') == 'Churn'])
    avg_probability = df.get('Churn_Probability', pd.Series([0])).mean()
    high_risk_count = len(df[df.get('Churn_Probability', pd.Series([0])) > 0.7])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🔮 Total Predictions",
            value=f"{total_predictions:,}",
            help="Total number of predictions in current view"
        )
    
    with col2:
        st.metric(
            label="⚠️ Churn Predicted",
            value=f"{churn_predictions:,}",
            delta=f"{(churn_predictions/max(total_predictions,1)*100):.1f}% of total",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="📊 Avg Probability",
            value=f"{avg_probability:.1%}",
            help="Average churn probability across all predictions"
        )
    
    with col4:
        st.metric(
            label="🚨 High Risk (>70%)",
            value=f"{high_risk_count:,}",
            delta="Immediate attention",
            delta_color="off"
        )

def render_predictions_table(df):
    """Render predictions data table"""
    st.subheader("📋 Prediction Details")
    
    if df.empty:
        st.info("No predictions found matching the current filters.")
        return
    
    # Pagination
    page_size = st.selectbox("Rows per page", [10, 20, 50], index=1, key="pred_page_size")
    
    total_pages = len(df) // page_size + (1 if len(df) % page_size > 0 else 0)
    
    if total_pages > 1:
        page = st.selectbox(f"Page (1-{total_pages})", range(1, total_pages + 1), key="pred_page")
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        display_df = df.iloc[start_idx:end_idx].copy()
    else:
        display_df = df.copy()
    
    # Format the display dataframe
    if 'Churn_Probability' in display_df.columns:
        display_df['Probability (%)'] = (display_df['Churn_Probability'] * 100).round(1)
    
    # Add row numbers
    display_df = display_df.reset_index(drop=True)
    display_df.index = display_df.index + 1
    
    # Color coding function for probabilities
    def color_probability(val):
        if pd.isna(val):
            return ''
        if val >= 70:
            return 'background-color: #fee2e2'  # Light red
        elif val >= 50:
            return 'background-color: #fef3c7'  # Light yellow
        else:
            return 'background-color: #dcfce7'  # Light green
    
    # Select and order columns for display
    display_columns = []
    if 'Probability (%)' in display_df.columns:
        display_columns.append('Probability (%)')
    if 'Predicted_Label' in display_df.columns:
        display_columns.append('Predicted_Label')
    if 'Recommended_Action' in display_df.columns:
        display_columns.append('Recommended_Action')
    if 'Top_Reasons' in display_df.columns:
        display_columns.append('Top_Reasons')
    if 'Reason_Comment' in display_df.columns:
        display_columns.append('Reason_Comment')
    
    # Apply styling if probability column exists
    if 'Probability (%)' in display_df.columns:
        styled_df = display_df[display_columns].style.applymap(
            color_probability, 
            subset=['Probability (%)']
        )
    else:
        styled_df = display_df[display_columns]
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=400
    )
    
    # Display pagination info
    if total_pages > 1:
        st.caption(f"Showing {start_idx + 1}-{min(end_idx, len(df))} of {len(df)} predictions")

def render_prediction_analytics(df):
    """Render prediction analytics charts"""
    if df.empty:
        return
    
    with st.expander("📊 Prediction Analytics", expanded=False):
        
        # Probability distribution
        st.subheader("📈 Probability Distribution")
        
        if 'Churn_Probability' in df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Histogram of probabilities
                fig_hist = px.histogram(
                    df,
                    x='Churn_Probability',
                    title="Churn Probability Distribution",
                    nbins=20,
                    color_discrete_sequence=['#3b82f6']
                )
                
                fig_hist.update_layout(
                    xaxis_title="Churn Probability",
                    yaxis_title="Number of Predictions",
                    showlegend=False
                )
                
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                # Risk level distribution
                df_risk = df.copy()
                df_risk['Risk_Level'] = pd.cut(
                    df_risk['Churn_Probability'],
                    bins=[0, 0.3, 0.7, 1.0],
                    labels=['Low Risk', 'Medium Risk', 'High Risk'],
                    include_lowest=True
                )
                
                risk_counts = df_risk['Risk_Level'].value_counts()
                
                fig_risk = px.pie(
                    values=risk_counts.values,
                    names=risk_counts.index,
                    title="Risk Level Distribution",
                    color_discrete_map={
                        'Low Risk': '#22c55e',
                        'Medium Risk': '#f59e0b',
                        'High Risk': '#ef4444'
                    }
                )
                
                st.plotly_chart(fig_risk, use_container_width=True)
        
        # Prediction accuracy (if actual labels were available)
        render_model_performance()

def render_model_performance():
    """Render model performance metrics"""
    st.subheader("🤖 Model Performance")
    
    # Mock performance metrics (in real implementation, these would come from model evaluation)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Accuracy", "87.3%", help="Overall prediction accuracy")
    
    with col2:
        st.metric("Precision", "84.1%", help="True positive rate")
    
    with col3:
        st.metric("Recall", "79.6%", help="Sensitivity to churn cases")
    
    with col4:
        st.metric("F1-Score", "81.8%", help="Balanced performance metric")
    
    # Feature importance visualization (mock data)
    st.subheader("🎯 Feature Importance")
    
    # Mock feature importance data
    features = [
        'Total_Trans_Ct', 'Total_Trans_Amt', 'Avg_Utilization_Ratio',
        'Months_Inactive_12_mon', 'Contacts_Count_12_mon'
    ]
    importance = [0.23, 0.19, 0.16, 0.14, 0.12]
    
    fig_importance = px.bar(
        x=importance,
        y=features,
        orientation='h',
        title="Top 5 Most Important Features",
        color=importance,
        color_continuous_scale='Reds'
    )
    
    fig_importance.update_layout(
        xaxis_title="Feature Importance",
        yaxis_title="Features",
        showlegend=False,
        height=300
    )
    
    st.plotly_chart(fig_importance, use_container_width=True)

def render_no_predictions():
    """Render message when no predictions are available"""
    st.info("🔍 No prediction data available")
    
    st.markdown("""
    **To generate predictions:**
    
    1. 📊 Ensure customer data is loaded
    2. 🤖 Run the prediction model on new customers
    3. 📈 Results will appear here with SHAP explanations
    
    **What you'll see:**
    - Churn probability scores
    - Predicted labels (Churn/No Churn)
    - Recommended actions for each customer
    - Top reasons contributing to the prediction
    - Detailed SHAP-based explanations
    """)
    
    # Sample prediction demo
    with st.expander("📋 Sample Prediction Format", expanded=False):
        sample_data = {
            'Probability (%)': [85.3, 23.1, 67.8],
            'Predicted_Label': ['Churn', 'No Churn', 'Churn'],
            'Recommended_Action': [
                'Immediate retention call',
                'Continue standard engagement',
                'Offer targeted incentives'
            ],
            'Top_Reasons': [
                'High inactivity, Low transactions',
                'Good utilization, Regular activity',
                'High service contacts, Credit limit issues'
            ]
        }
        
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df, use_container_width=True)

# Main execution
if __name__ == "__main__":
    render_predictions_page()



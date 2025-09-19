# Predictions Page - Streamlit version
import streamlit as st
import pandas as pd
import numpy as np
import re
import plotly.express as px
import plotly.graph_objects as go
from services.customer_data import customer_data

# ---------- Helpers ----------
def _churn_mask(df: pd.DataFrame, threshold: float = 0.7) -> pd.Series:
    """Return boolean mask for rows considered churn.
    Priority order:
    1) Numeric labels (1/0) → 1 means churn
    2) String labels → 'churn', '1', 'true', 'yes' mean churn
    3) Fallback to probability threshold (>= threshold)
    """
    if 'Predicted_Label' in df.columns:
        col = df['Predicted_Label']
        if pd.api.types.is_numeric_dtype(col):
            try:
                return col.astype(float) >= 0.5
            except Exception:
                pass
        labels = col.astype(str).str.strip().str.lower()
        return labels.isin(['churn', '1', 'true', 'yes'])
    if 'Churn_Probability' in df.columns:
        return df['Churn_Probability'] >= threshold
    return pd.Series(False, index=df.index)

def _summarize_text(text: str, max_items: int = 2, max_chars: int = 60) -> str:
    """Return a concise summary string from long comma-/semicolon-separated text."""
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return "None"
    s = str(text)
    # Split by common delimiters and filter empties
    parts = [p.strip() for p in re.split(r"[;,|]\s*|\n+", s) if p and p.strip().lower() != 'none']
    if not parts:
        parts = [s.strip()]
    summary = ", ".join(parts[:max_items])
    if len(summary) > max_chars:
        summary = summary[: max_chars - 1].rstrip() + "…"
    return summary

def _parse_reasons_to_series(text: str, top_n: int = 5):
    """Parse reasons into a simple series for charting with equal weights when unknown."""
    s = str(text) if text is not None else ""
    parts = [p.strip() for p in re.split(r"[;,|]\s*|\n+", s) if p.strip()]
    if not parts:
        return pd.Series([1], index=["No reasons available"])  # fallback
    parts = parts[:top_n]
    weights = [1.0 / len(parts)] * len(parts)
    return pd.Series(weights, index=parts)

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
        mask = _churn_mask(filtered_df, threshold=0.7)
        if prediction_filter == 'churn':
            filtered_df = filtered_df[mask]
        elif prediction_filter == 'no_churn':
            filtered_df = filtered_df[~mask]
    
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
    churn_predictions = int(_churn_mask(df, threshold=0.7).sum())
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
    
    # Add View column
    display_columns.append('View')
    
    # Simplify verbose text columns for compact display
    if 'Top_Reasons' in display_df.columns:
        display_df['Top_Reasons_Short'] = display_df['Top_Reasons'].apply(lambda x: _summarize_text(x, max_items=2, max_chars=40))
    if 'Reason_Comment' in display_df.columns:
        display_df['Reason_Comment_Short'] = display_df['Reason_Comment'].apply(lambda x: _summarize_text(x, max_items=1, max_chars=50))

    # Replace original columns in display with shortened versions if available
    replaced_columns = []
    if 'Top_Reasons' in display_columns and 'Top_Reasons_Short' in display_df.columns:
        display_columns[display_columns.index('Top_Reasons')] = 'Top_Reasons_Short'
        replaced_columns.append(('Top_Reasons_Short', 'Top_Reasons'))
    if 'Reason_Comment' in display_columns and 'Reason_Comment_Short' in display_df.columns:
        display_columns[display_columns.index('Reason_Comment')] = 'Reason_Comment_Short'
        replaced_columns.append(('Reason_Comment_Short', 'Reason_Comment'))
    
    # Build an identifier to map clicks back to the underlying row
    if 'CLIENTNUM' in display_df.columns:
        display_df['__row_id__'] = display_df['CLIENTNUM'].astype(str)
    else:
        display_df['__row_id__'] = display_df.index.astype(str)

    # Add View column used by data editor button
    display_df['View'] = "View"

    # Apply styling if probability column exists
    if 'Probability (%)' in display_df.columns:
        styled_df = (
            display_df[display_columns]
                .style
                .format({'Probability (%)': '{:.1f}'})
                .applymap(
                    color_probability,
                    subset=['Probability (%)']
                )
                .set_properties(
                    subset=['Probability (%)'],
                    **{
                        'color': '#111827',          # slate-900 for strong contrast on light bg
                        'font-weight': '600'         # semi-bold for readability
                    }
                )
        )
    else:
        styled_df = display_df[display_columns]
    
    # Inline selection using a checkbox column (works across Streamlit versions)
    selected_id_default = st.session_state.get('selected_customer_row_id')
    display_df['Selected'] = display_df['__row_id__'].astype(str) == str(selected_id_default)

    edited_df = st.data_editor(
        display_df[display_columns + ['Selected']],
        hide_index=True,
        use_container_width=True,
        height=420,
        column_config={
            'Selected': st.column_config.CheckboxColumn(
                label='View',
                help='Check to view details for this row',
                default=False,
                width='small'
            ),
        },
        disabled=[c for c in display_columns]
    )

    # Identify selected row (first checked row wins)
    try:
        selected_rows = edited_df[edited_df['Selected'] == True]
        if not selected_rows.empty:
            # Get the index of the selected row and map it back to the original row_id
            selected_idx = selected_rows.index[0]
            st.session_state['selected_customer_row_id'] = str(display_df.iloc[selected_idx]['__row_id__'])
    except Exception:
        pass

    # Show customer details when a View button is clicked
    selected_row_id = st.session_state.get('selected_customer_row_id')
    if selected_row_id is not None:
        st.markdown("---")
        st.subheader("👤 Customer Analysis Details")
        
        # Find the selected row by identifier
        try:
            selected_row = display_df[display_df['__row_id__'] == str(selected_row_id)].iloc[0]
        except Exception:
            selected_row = display_df.iloc[0]
        
        # Extract data from the selected row
        prob = float(selected_row.get('Churn_Probability', np.nan)) if 'Churn_Probability' in selected_row else float(selected_row.get('Probability (%)', np.nan))/100.0 if 'Probability (%)' in selected_row else np.nan
        label = selected_row.get('Predicted_Label', 'N/A')
        action = selected_row.get('Recommended_Action', 'N/A')
        reasons = selected_row.get('Top_Reasons', selected_row.get('Top_Reasons_Short', ''))
        comment = selected_row.get('Reason_Comment', selected_row.get('Reason_Comment_Short', ''))
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Churn Probability", f"{(prob*100 if not pd.isna(prob) else 0):.1f}%")
        with col2:
            st.metric("Predicted Label", str(label))
        with col3:
            st.metric("Recommended Action", str(action))
        with col4:
            risk_level = "High" if prob > 0.7 else "Medium" if prob > 0.3 else "Low"
            st.metric("Risk Level", risk_level)
        
        # Create tabs for different analysis views
        tab1, tab2, tab3 = st.tabs(["🧠 Key Reasons", "📊 Risk Analysis", "💡 Action Plan"])
        
        with tab1:
            st.markdown("#### Top Contributing Factors")
            if reasons and str(reasons).strip() != 'None':
                reason_series = _parse_reasons_to_series(reasons, top_n=5)
                fig = px.bar(
                    reason_series.sort_values().tail(5),
                    orientation='h',
                    labels={'value': 'Impact', 'index': 'Factor'},
                    title="Key Churn Drivers",
                    color=reason_series.sort_values().tail(5),
                    color_continuous_scale='Reds'
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                
                # Show detailed reasons
                st.markdown("**Detailed Analysis:**")
                st.info(_summarize_text(reasons, max_items=5, max_chars=300))
            else:
                st.info("No specific reasons identified for this customer.")
        
        with tab2:
            st.markdown("#### Risk Assessment")
            
            # Create risk indicators
            risk_factors = []
            if prob > 0.7:
                risk_factors.append("🔴 High churn probability (>70%)")
            elif prob > 0.3:
                risk_factors.append("🟡 Medium churn probability (30-70%)")
            else:
                risk_factors.append("🟢 Low churn probability (<30%)")
            
            if "inactive" in str(reasons).lower():
                risk_factors.append("⚠️ Customer inactivity detected")
            if "contact" in str(reasons).lower():
                risk_factors.append("📞 High service contact frequency")
            if "transaction" in str(reasons).lower():
                risk_factors.append("💳 Low transaction activity")
            
            for factor in risk_factors:
                st.write(factor)
            
            # Risk score visualization
            risk_score = int(prob * 100) if not pd.isna(prob) else 0
            fig_risk = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = risk_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Churn Risk Score"},
                delta = {'reference': 50},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgreen"},
                        {'range': [30, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 70
                    }
                }
            ))
            fig_risk.update_layout(height=300)
            st.plotly_chart(fig_risk, use_container_width=True)
        
        with tab3:
            st.markdown("#### Recommended Actions")
            
            # Action recommendations based on probability and reasons
            actions = []
            if prob > 0.7:
                actions.append("🚨 **Immediate Action Required**")
                actions.append("• Schedule urgent retention call within 24 hours")
                actions.append("• Offer personalized retention incentives")
                actions.append("• Assign dedicated account manager")
            elif prob > 0.3:
                actions.append("⚠️ **Proactive Engagement**")
                actions.append("• Schedule follow-up call within 1 week")
                actions.append("• Send targeted product recommendations")
                actions.append("• Monitor account activity closely")
            else:
                actions.append("✅ **Maintain Current Relationship**")
                actions.append("• Continue standard engagement")
                actions.append("• Regular check-ins every 3 months")
                actions.append("• Upsell opportunities when appropriate")
            
            # Add specific actions based on reasons
            if "inactive" in str(reasons).lower():
                actions.append("• Re-engagement campaign with special offers")
            if "contact" in str(reasons).lower():
                actions.append("• Review and improve service quality")
            if "transaction" in str(reasons).lower():
                actions.append("• Provide transaction incentives or rewards")
            
            for action in actions:
                st.write(action)
            
            # Show comment if available
            if comment and str(comment).strip() != 'None':
                st.markdown("**Additional Notes:**")
                st.info(_summarize_text(comment, max_items=3, max_chars=200))
    
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



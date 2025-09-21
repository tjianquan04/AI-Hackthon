# 🏦 Customer Churn Analytics - Streamlit Dashboard

A comprehensive Streamlit-based dashboard for customer churn analysis, featuring real-time analytics, predictive insights, and actionable recommendations.

## 🚀 Features

### 📊 Dashboard Analytics
- **Real-time KPI Monitoring**: Track key metrics like churn rate, customer count, and risk levels
- **Demographic Analysis**: Analyze churn patterns across age groups, income categories, and card types
- **Financial Behavior**: Understand credit utilization and transaction patterns impact on churn
- **Customer Segmentation**: Value-based and engagement-based customer analysis
- **AI-Driven Insights**: Machine learning insights with feature importance analysis

### 👥 Customer Database
- **Advanced Filtering**: Search and filter customers by risk level, status, and demographics
- **Risk Assessment**: Automated churn risk scoring for each customer
- **Interactive Tables**: Paginated, sortable customer data with color-coded risk levels
- **Export Capabilities**: Download filtered data and analytics reports

### 🔮 Churn Predictions
- **ML Model Outputs**: Display prediction results with probability scores
- **SHAP Explanations**: Detailed reasoning for each prediction
- **Recommended Actions**: Automated action suggestions for high-risk customers
- **Performance Metrics**: Model accuracy, precision, recall, and F1-score tracking

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone/Navigate to the Streamlit UI directory**
   ```bash
   cd "streamlit UI"
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare Data Files** (Optional - app includes fallback data)
   - Place `churn_analysis.json` in the services directory
   - Place customer data CSV files in appropriate locations
   - Place prediction files for the predictions page

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

5. **Access the Dashboard**
   - Open your browser to `http://localhost:8501`
   - The dashboard will load with the main analytics view

## 📁 Project Structure

```
streamlit UI/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                  # This file
│
├── components/                 # Reusable UI components
│   ├── kpi_cards.py           # KPI metrics cards
│   ├── churn_charts.py        # Chart components
│   ├── customer_segments.py   # Segmentation analysis
│   └── insights.py            # Insights and recommendations
│
├── pages/                     # Multi-page components
│   ├── customers.py           # Customer database page
│   └── predictions.py         # Predictions page
│
├── services/                  # Data services
│   ├── dashboard_data.py      # Dashboard data service
│   └── customer_data.py       # Customer data service
│
└── utils/                     # Utility functions (future use)
```

## 🎯 Usage Guide

### Navigation
- Use the sidebar to navigate between Dashboard, Customer Database, and Predictions pages
- Each page includes filters and interactive controls in the sidebar

### Dashboard Page
1. **KPI Overview**: View high-level metrics at the top
2. **Tabbed Analysis**: Switch between demographic, financial, segments, and insights tabs
3. **Interactive Charts**: Hover over charts for detailed information
4. **Expandable Sections**: Click expanders for additional details

### Customer Database Page
1. **Filter Customers**: Use sidebar filters to narrow down the customer list
2. **Search Function**: Search by ID, income, education, etc.
3. **Risk Assessment**: View calculated risk scores with color coding
4. **Analytics**: Expand the analytics section for visual insights

### Predictions Page
1. **View Predictions**: See model outputs with probability scores
2. **Filter Results**: Filter by prediction label or probability range
3. **SHAP Explanations**: Review detailed reasoning for each prediction
4. **Action Items**: View recommended actions for high-risk customers

## ⚙️ Configuration

### Data Sources
The application attempts to load data from multiple locations:
- `../UI/src/services/churn_analysis.json` (React app data)
- `../outputs/dashboard_data/churn_analysis.json` (Generated outputs)
- `../data/bank_churn_cleaned.csv` (Customer data)
- `../outputs/explanations/predictions_with_reasons.csv` (Predictions)

If data files are not found, the app will use sample/fallback data to demonstrate functionality.

### Customization
- **Styling**: Modify the CSS in `app.py` for custom styling
- **Components**: Add new chart types in the `components/` directory
- **Data Sources**: Update file paths in service files to match your data structure

## 🔧 Advanced Features

### Model Integration
- Ready for integration with ML model APIs
- SHAP explanation framework included
- Performance metrics tracking

### Export Capabilities
- CSV download functionality framework
- Analytics report generation structure
- Data filtering and export pipeline

### Responsive Design
- Mobile-friendly layout
- Adaptive chart sizing
- Collapsible sections for smaller screens

## 🤝 Contributing

To extend or modify the dashboard:
1. Add new components in the `components/` directory
2. Create new pages in the `pages/` directory  
3. Extend data services in the `services/` directory
4. Update the main `app.py` file to include new features

## 📊 Data Requirements

### Expected Data Format
- **Customer Data**: CSV with columns like CLIENTNUM, Customer_Age, Income_Category, etc.
- **Predictions**: CSV with Churn_Probability, Predicted_Label, Recommended_Action, etc.
- **Analytics**: JSON with structured EDA results and insights

### Sample Data
The application includes sample data generation if actual files are not available, allowing you to test all functionality immediately.

## 🚀 Deployment

For production deployment:
1. Install dependencies: `pip install -r requirements.txt`
2. Set up data file paths in service configurations
3. Run with: `streamlit run app.py --server.port 8501`
4. Consider using Docker for containerized deployment

## 📞 Support

For questions or issues:
- Check the component documentation in each file
- Review the data service implementations
- Ensure all required data files are accessible
- Verify Python dependencies are correctly installed





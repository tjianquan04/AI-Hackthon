// Dashboard Data Service - Integrates real EDA analysis data
import churnAnalysis from './churn_analysis.json';

export class DashboardDataService {
  constructor() {
    this.data = churnAnalysis;
  }

  // KPI Metrics for dashboard cards
  getKPIMetrics() {
    const kpis = this.data.summary_kpis.kpi_metrics;
    const riskSegments = this.data.summary_kpis.risk_segments;
    
    return {
      totalCustomers: kpis.total_customers,
      churnedCustomers: kpis.churned_customers,
      churnRate: (kpis.overall_churn_rate * 100).toFixed(1),
      retentionRate: (kpis.retention_rate * 100).toFixed(1),
      avgCustomerAge: Math.round(kpis.avg_customer_age),
      avgTenure: Math.round(kpis.avg_tenure_months),
      avgCreditLimit: Math.round(kpis.avg_credit_limit),
      avgTransactionAmount: Math.round(kpis.avg_transaction_amount),
      highRiskCustomers: riskSegments.high_risk_customers,
      mediumRiskCustomers: riskSegments.medium_risk_customers,
      lowRiskCustomers: riskSegments.low_risk_customers
    };
  }

  // Churn overview data for charts
  getChurnOverview() {
    return this.data.churn_overview;
  }

  // Demographics data for charts
  getDemographics() {
    return this.data.demographics;
  }

  // Customer activity patterns
  getCustomerActivity() {
    return this.data.customer_activity;
  }

  // Financial behavior patterns
  getFinancialBehavior() {
    return this.data.financial_behavior;
  }

  // Customer value analysis
  getCustomerValue() {
    return this.data.customer_value;
  }

  // Product engagement data
  getProductEngagement() {
    return this.data.product_engagement;
  }

  // Key insights and churn drivers
  getKeyInsights() {
    return this.data.churn_drivers.key_insights;
  }

  // Top numerical drivers
  getTopDrivers() {
    return this.data.churn_drivers.top_numerical_drivers;
  }

  // Format data for chart libraries (Chart.js, Recharts, etc.)
  formatChartData(dataObject, labelKey = 'label', valueKey = 'value') {
    if (!dataObject) return { labels: [], datasets: [] };
    
    const entries = Object.entries(dataObject);
    const labels = entries.map(([key]) => key);
    const values = entries.map(([, value]) => 
      typeof value === 'object' ? value.Churn_Rate || value.Total_Customers || 0 : value
    );

    return {
      labels,
      data: values,
      datasets: [{
        label: 'Churn Rate',
        data: values,
        backgroundColor: [
          '#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6',
          '#8b5cf6', '#ec4899', '#6b7280', '#059669', '#dc2626'
        ],
        borderColor: '#fff',
        borderWidth: 2
      }]
    };
  }

  // Format data specifically for age group analysis
  getAgeGroupChartData() {
    const ageData = this.data.churn_overview.churn_by_age;
    const labels = Object.keys(ageData);
    const churnRates = labels.map(age => (ageData[age].Churn_Rate * 100).toFixed(1));
    const customerCounts = labels.map(age => ageData[age].Total_Customers);

    return {
      labels,
      datasets: [
        {
          label: 'Churn Rate (%)',
          data: churnRates,
          backgroundColor: 'rgba(239, 68, 68, 0.8)',
          borderColor: '#ef4444',
          borderWidth: 2,
          yAxisID: 'y'
        },
        {
          label: 'Total Customers',
          data: customerCounts,
          backgroundColor: 'rgba(59, 130, 246, 0.8)',
          borderColor: '#3b82f6',
          borderWidth: 2,
          yAxisID: 'y1'
        }
      ]
    };
  }

  // Format data for income category analysis
  getIncomeChartData() {
    const incomeData = this.data.churn_overview.churn_by_income;
    const labels = Object.keys(incomeData);
    const churnRates = labels.map(income => (incomeData[income].Churn_Rate * 100).toFixed(1));
    const customerCounts = labels.map(income => incomeData[income].Total_Customers);

    return {
      labels,
      datasets: [
        {
          label: 'Churn Rate (%)',
          data: churnRates,
          backgroundColor: 'rgba(239, 68, 68, 0.8)',
          borderColor: '#ef4444',
          borderWidth: 2
        }
      ]
    };
  }

  // Format data for card category analysis
  getCardCategoryData() {
    const cardData = this.data.churn_overview.churn_by_card_type;
    const labels = Object.keys(cardData);
    const churnRates = labels.map(card => (cardData[card].Churn_Rate * 100).toFixed(1));
    const customerCounts = labels.map(card => cardData[card].Total_Customers);

    return {
      labels,
      churnRates,
      customerCounts,
      pieData: {
        labels,
        datasets: [{
          data: customerCounts,
          backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'],
          borderColor: '#fff',
          borderWidth: 2
        }]
      }
    };
  }

  // Format data for customer activity analysis
  getActivityChartData() {
    const inactiveData = this.data.customer_activity.churn_by_months_inactive;
    const contactsData = this.data.customer_activity.churn_by_service_contacts;
    
    return {
      inactivity: {
        labels: Object.keys(inactiveData),
        data: Object.values(inactiveData).map(item => (item.Churn_Rate * 100).toFixed(1))
      },
      serviceContacts: {
        labels: Object.keys(contactsData),
        data: Object.values(contactsData).map(item => (item.Churn_Rate * 100).toFixed(1))
      }
    };
  }

  // Format data for financial behavior analysis
  getFinancialChartData() {
    const utilizationData = this.data.financial_behavior.churn_by_utilization;
    const creditLimitData = this.data.financial_behavior.churn_by_credit_limit;
    
    return {
      utilization: {
        labels: Object.keys(utilizationData),
        data: Object.values(utilizationData).map(item => (item.Churn_Rate * 100).toFixed(1))
      },
      creditLimit: {
        labels: Object.keys(creditLimitData),
        data: Object.values(creditLimitData).map(item => (item.Churn_Rate * 100).toFixed(1))
      }
    };
  }

  // Get customer segments data
  getCustomerSegments() {
    const valueData = this.data.customer_value.churn_by_customer_value;
    const engagementData = this.data.product_engagement.churn_by_product_engagement;
    
    return {
      byValue: {
        labels: Object.keys(valueData),
        churnRates: Object.values(valueData).map(item => (item.Churn_Rate * 100).toFixed(1)),
        customerCounts: Object.values(valueData).map(item => item.Total_Customers)
      },
      byEngagement: {
        labels: Object.keys(engagementData),
        churnRates: Object.values(engagementData).map(item => (item.Churn_Rate * 100).toFixed(1)),
        customerCounts: Object.values(engagementData).map(item => item.Total_Customers)
      }
    };
  }

  // Get risk insights summary
  getRiskInsightsSummary() {
    const insights = this.data.churn_drivers.key_insights;
    const topDrivers = this.data.churn_drivers.top_numerical_drivers;
    
    return {
      insights: insights.map(insight => ({
        category: insight.category,
        description: insight.insight,
        riskLevel: insight.risk_level,
        color: insight.risk_level === 'High' ? 'red' : 'yellow'
      })),
      topFeatures: Object.entries(topDrivers)
        .slice(0, 5)
        .map(([feature, correlation]) => ({
          feature: feature.replace(/_/g, ' '),
          importance: (Math.abs(correlation) * 100).toFixed(1)
        }))
    };
  }

  // Format data for tenure analysis
  getTenureChartData() {
    const tenureData = this.data.churn_overview.churn_by_tenure;
    
    // Filter out segments with no customers and transform data
    const transformedData = Object.entries(tenureData)
      .filter(([, data]) => data.Total_Customers > 0)
      .map(([tenure, data]) => ({
        tenure: tenure,
        tenureLabel: tenure.replace(/\(.*\)/, '').trim(), // Clean label for display
        totalCustomers: data.Total_Customers,
        churnedCustomers: data.Churned_Count,
        churnRate: (data.Churn_Rate * 100).toFixed(1),
        monthsRange: tenure.match(/\((.*?)\)/)?.[1] || tenure // Extract months range
      }));

    return {
      data: transformedData,
      chartData: transformedData.map(item => ({
        name: item.tenureLabel,
        churnRate: parseFloat(item.churnRate),
        customers: item.totalCustomers,
        churned: item.churnedCustomers
      }))
    };
  }

  // Get data for specific dashboard widgets
  getWidgetData(widgetType) {
    switch (widgetType) {
      case 'kpi':
        return this.getKPIMetrics();
      case 'ageGroup':
        return this.getAgeGroupChartData();
      case 'income':
        return this.getIncomeChartData();
      case 'cardCategory':
        return this.getCardCategoryData();
      case 'activity':
        return this.getActivityChartData();
      case 'financial':
        return this.getFinancialChartData();
      case 'segments':
        return this.getCustomerSegments();
      case 'insights':
        return this.getRiskInsightsSummary();
      case 'tenure':
        return this.getTenureChartData();
      default:
        return null;
    }
  }
}

// Export singleton instance
export const dashboardData = new DashboardDataService();
export default dashboardData;


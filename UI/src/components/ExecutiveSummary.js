import React, { useState, useEffect } from 'react';
import { TrendingUp, AlertTriangle, Shield, Target, Zap, Award } from 'lucide-react';
import { dashboardData } from '../services/dashboardData';

const ExecutiveSummary = () => {
  const [metrics, setMetrics] = useState(null);
  const [insights, setInsights] = useState([]);

  useEffect(() => {
    const kpiData = dashboardData.getKPIMetrics();
    const insightsData = dashboardData.getRiskInsightsSummary();
    setMetrics(kpiData);
    setInsights(insightsData.insights);
  }, []);

  if (!metrics) {
    return (
      <div className="animate-pulse bg-white/60 rounded-2xl p-8">
        <div className="h-40 bg-gray-200 rounded"></div>
      </div>
    );
  }

  const criticalInsights = [
    {
      title: "High-Risk Segments",
      value: `${((metrics.highRiskCustomers / metrics.totalCustomers) * 100).toFixed(1)}%`,
      description: "Customers requiring immediate attention",
      icon: AlertTriangle,
      color: "text-red-600",
      bgColor: "bg-red-50",
      trend: "urgent"
    },
    {
      title: "Churn Prevention Opportunity", 
      value: `${metrics.retentionRate}%`,
      description: "Current retention rate with improvement potential",
      icon: Shield,
      color: "text-green-600",
      bgColor: "bg-green-50",
      trend: "positive"
    },
    {
      title: "Business Impact",
      value: `${metrics.churnRate}%`,
      description: "Overall churn rate affecting revenue",
      icon: TrendingUp,
      color: "text-orange-600",
      bgColor: "bg-orange-50",
      trend: "monitor"
    }
  ];

  return (
    <div className="bg-gradient-to-r from-white via-blue-50 to-indigo-50 rounded-2xl shadow-2xl border border-blue-100 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 px-8 py-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <Award className="w-6 h-6" />
              <h2 className="text-2xl font-bold">Executive Summary</h2>
            </div>
            <p className="text-blue-100">Strategic insights from comprehensive EDA analysis</p>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold">{metrics.totalCustomers.toLocaleString()}</div>
            <div className="text-blue-200 text-sm">Total Customers</div>
          </div>
        </div>
      </div>

      {/* Critical Metrics */}
      <div className="p-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {criticalInsights.map((insight, index) => (
            <div key={index} className={`${insight.bgColor} rounded-xl p-6 border-l-4 ${insight.color.replace('text-', 'border-')}`}>
              <div className="flex items-center justify-between mb-3">
                <insight.icon className={`w-8 h-8 ${insight.color}`} />
                <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                  insight.trend === 'urgent' ? 'bg-red-100 text-red-800' :
                  insight.trend === 'positive' ? 'bg-green-100 text-green-800' :
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {insight.trend.toUpperCase()}
                </div>
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-2">{insight.value}</div>
              <div className="text-sm font-medium text-gray-700 mb-1">{insight.title}</div>
              <div className="text-xs text-gray-600">{insight.description}</div>
            </div>
          ))}
        </div>

        {/* Key Business Insights */}
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center space-x-2 mb-4">
            <Target className="w-5 h-5 text-indigo-600" />
            <h3 className="text-lg font-bold text-gray-900">Strategic Action Items</h3>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {insights.slice(0, 4).map((insight, index) => (
              <div key={index} className="flex items-start space-x-3 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white ${
                  insight.riskLevel === 'High' ? 'bg-red-500' : 'bg-yellow-500'
                }`}>
                  {index + 1}
                </div>
                <div className="flex-1">
                  <div className="text-sm font-semibold text-gray-900 mb-1">{insight.category}</div>
                  <div className="text-xs text-gray-600">{insight.description}</div>
                </div>
                <div className={`px-2 py-1 rounded text-xs font-medium ${
                  insight.riskLevel === 'High' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'
                }`}>
                  {insight.riskLevel}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Bottom Stats */}
        <div className="mt-6 bg-gradient-to-r from-indigo-500 to-blue-600 rounded-xl p-6 text-white">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Zap className="w-6 h-6" />
              <div>
                <div className="text-sm font-medium">EDA Analysis Status</div>
                <div className="text-xs text-indigo-200">Last updated: {new Date().toLocaleDateString()}</div>
              </div>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold">{metrics.churnedCustomers.toLocaleString()}</div>
              <div className="text-indigo-200 text-sm">Customers at Risk</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExecutiveSummary;


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
      <div className="animate-pulse bg-slate-900/60 rounded-2xl p-8 border border-slate-800">
        <div className="h-40 bg-slate-800 rounded"></div>
      </div>
    );
  }

  const criticalInsights = [
    {
      title: "High-Risk Segments",
      value: `${((metrics.highRiskCustomers / metrics.totalCustomers) * 100).toFixed(1)}%`,
      description: "Customers requiring immediate attention",
      icon: AlertTriangle,
      color: "text-red-300",
      bgColor: "bg-red-900/20",
      trend: "urgent"
    },
    {
      title: "Churn Prevention Opportunity", 
      value: `${metrics.retentionRate}%`,
      description: "Current retention rate with improvement potential",
      icon: Shield,
      color: "text-green-300",
      bgColor: "bg-green-900/20",
      trend: "positive"
    },
    {
      title: "Business Impact",
      value: `${metrics.churnRate}%`,
      description: "Overall churn rate affecting revenue",
      icon: TrendingUp,
      color: "text-orange-300",
      bgColor: "bg-orange-900/20",
      trend: "monitor"
    }
  ];

  return (
    <div className="bg-gradient-to-r from-slate-900/70 via-slate-900/40 to-indigo-900/30 rounded-2xl shadow-2xl border border-slate-800 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-700 to-indigo-800 px-8 py-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <Award className="w-6 h-6" />
              <h2 className="text-2xl font-bold">Executive Summary</h2>
            </div>
            <p className="text-blue-200">Strategic insights from comprehensive EDA analysis</p>
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
            <div key={index} className={`${insight.bgColor} rounded-xl p-6 border border-slate-800`}>
              <div className="flex items-center justify-between mb-3">
                <insight.icon className={`w-8 h-8 ${insight.color}`} />
                <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                  insight.trend === 'urgent' ? 'bg-red-900/30 text-red-200' :
                  insight.trend === 'positive' ? 'bg-green-900/30 text-green-200' :
                  'bg-yellow-900/30 text-yellow-200'
                }`}>
                  {insight.trend.toUpperCase()}
                </div>
              </div>
              <div className="text-3xl font-bold text-slate-100 mb-2">{insight.value}</div>
              <div className="text-sm font-medium text-slate-300 mb-1">{insight.title}</div>
              <div className="text-xs text-slate-400">{insight.description}</div>
            </div>
          ))}
        </div>

        {/* Key Business Insights */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 shadow-lg">
          <div className="flex items-center space-x-2 mb-4">
            <Target className="w-5 h-5 text-indigo-300" />
            <h3 className="text-lg font-bold text-slate-100">Strategic Action Items</h3>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {insights.slice(0, 4).map((insight, index) => (
              <div key={index} className="flex items-start space-x-3 p-4 bg-slate-900/50 rounded-lg border border-slate-800 hover:bg-slate-900 transition-colors">
                <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white ${
                  insight.riskLevel === 'High' ? 'bg-red-600' : 'bg-yellow-600'
                }`}>
                  {index + 1}
                </div>
                <div className="flex-1">
                  <div className="text-sm font-semibold text-slate-100 mb-1">{insight.category}</div>
                  <div className="text-xs text-slate-400">{insight.description}</div>
                </div>
                <div className={`px-2 py-1 rounded text-xs font-medium ${
                  insight.riskLevel === 'High' ? 'bg-red-900/30 text-red-200' : 'bg-yellow-900/30 text-yellow-200'
                }`}>
                  {insight.riskLevel}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Bottom Stats */}
        <div className="mt-6 bg-gradient-to-r from-indigo-700 to-blue-700 rounded-xl p-6 text-white">
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


import React, { useState, useEffect } from 'react';
import { AlertTriangle, TrendingDown, Users, Activity } from 'lucide-react';
import { dashboardData } from '../services/dashboardData';

const InsightCard = ({ icon: Icon, title, description, riskLevel, percentage, color }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start space-x-3">
        <div className={`p-2 rounded-lg ${color}`}>
          <Icon className="w-5 h-5 text-white" />
        </div>
        <div className="flex-1">
          <div className="flex items-center justify-between mb-2">
            <h4 className="text-sm font-semibold text-gray-900">{title}</h4>
            {percentage && (
              <span className={`text-xs px-2 py-1 rounded-full ${
                riskLevel === 'High' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
              }`}>
                {percentage}
              </span>
            )}
          </div>
          <p className="text-xs text-gray-600 leading-relaxed">{description}</p>
        </div>
      </div>
    </div>
  );
};

const TopDriverCard = ({ feature, importance, rank }) => {
  const getBarColor = (rank) => {
    switch (rank) {
      case 1: return 'bg-red-500';
      case 2: return 'bg-orange-500';
      case 3: return 'bg-yellow-500';
      case 4: return 'bg-blue-500';
      default: return 'bg-gray-500';
    }
  };

  const getReadableFeature = (feature) => {
    const featureMap = {
      'total trans ct': 'Low Transaction Activity',
      'total trans amt': 'Low Transaction Amount',
      'total revolving bal': 'High Revolving Balance',
      'months inactive 12 mon': 'Customer Inactivity Period',
      'contacts count 12 mon': 'Frequent Service Contacts',
      'total relationship count': 'Few Bank Relationships',
      'customer age': 'Customer Age Factor',
      'avg utilization ratio': 'Credit Utilization Rate',
      'credit limit': 'Credit Limit Level',
      'dependent count': 'Number of Dependents'
    };
    
    return featureMap[feature.toLowerCase()] || feature.replace(/\b\w/g, l => l.toUpperCase());
  };

  const getDescription = (feature) => {
    const descriptions = {
      'total trans ct': 'Customers with fewer transactions are more likely to churn',
      'total trans amt': 'Lower spending customers show higher churn rates',
      'total revolving bal': 'High credit card balances indicate financial stress',
      'months inactive 12 mon': 'Inactive customers are at highest churn risk',
      'contacts count 12 mon': 'Multiple service contacts signal dissatisfaction',
      'total relationship count': 'Single-product customers churn more frequently',
      'customer age': 'Certain age groups show higher churn tendency',
      'avg utilization ratio': 'High credit utilization indicates financial strain',
      'credit limit': 'Credit limit changes affect customer satisfaction',
      'dependent count': 'Family size impacts banking stability'
    };
    
    return descriptions[feature.toLowerCase()] || 'Significant factor in customer churn prediction';
  };

  return (
    <div className="flex items-start space-x-3 p-4 bg-white rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
      <div className={`flex-shrink-0 w-10 h-10 rounded-full ${getBarColor(rank)} flex items-center justify-center`}>
        <span className="text-sm font-bold text-white">#{rank}</span>
      </div>
      <div className="flex-1">
        <div className="flex items-center justify-between mb-2">
          <h5 className="text-sm font-bold text-gray-900">{getReadableFeature(feature)}</h5>
          <span className="text-xs font-medium text-gray-700 bg-gray-100 px-2 py-1 rounded">{importance}%</span>
        </div>
        <p className="text-xs text-gray-600 mb-2">{getDescription(feature)}</p>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className={`h-2 rounded-full ${getBarColor(rank)}`}
            style={{ width: `${Math.min(importance, 100)}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

const ChurnInsights = () => {
  const [insights, setInsights] = useState([]);
  const [topDrivers, setTopDrivers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const insightsData = dashboardData.getRiskInsightsSummary();
    setInsights(insightsData.insights);
    setTopDrivers(insightsData.topFeatures);
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="animate-pulse space-y-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Churn Risk Insights</h3>
        {[1, 2, 3].map(i => (
          <div key={i} className="h-20 bg-gray-200 rounded"></div>
        ))}
      </div>
    );
  }

  const getInsightIcon = (category) => {
    switch (category) {
      case 'Inactivity Risk': return Activity;
      case 'Service Issues': return AlertTriangle;
      case 'Financial Stress': return TrendingDown;
      case 'Engagement Decline': return Users;
      default: return AlertTriangle;
    }
  };

  const getInsightColor = (riskLevel) => {
    return riskLevel === 'High' ? 'bg-red-500' : 'bg-yellow-500';
  };

  return (
    <div>
      <div className="flex items-center space-x-3 mb-6">
        <div className="p-3 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl">
          <AlertTriangle className="w-6 h-6 text-white" />
        </div>
        <div>
          <h3 className="text-xl font-bold text-gray-900">🎯 Risk Insights</h3>
          <p className="text-sm text-gray-600">Key churn drivers</p>
        </div>
      </div>
      
      {/* Top Feature Drivers Only */}
      <div className="space-y-4">
        {topDrivers.slice(0, 3).map((driver, index) => (
          <TopDriverCard
            key={index}
            feature={driver.feature}
            importance={driver.importance}
            rank={index + 1}
          />
        ))}
      </div>

      <div className="mt-6 p-4 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg border border-indigo-200">
        <p className="text-sm text-indigo-800">
          🎯 <strong>Action Plan:</strong> Focus on these top 3 drivers to maximize customer retention ROI. 
          Each factor offers concrete intervention opportunities.
        </p>
      </div>
    </div>
  );
};

export default ChurnInsights;


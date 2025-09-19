import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Users, DollarSign, AlertTriangle, Shield } from 'lucide-react';
import { dashboardData } from '../services/dashboardData';

const KPICard = ({ title, value, subtitle, icon: Icon, trend, trendValue, color, gradient }) => {
  return (
    <div className={`relative overflow-hidden rounded-2xl shadow-xl border border-slate-800 p-8 hover:shadow-2xl transition-all duration-500 hover:scale-105 ${gradient || 'bg-slate-900/70 backdrop-blur-sm'}`}>
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent"></div>
      
      <div className="relative">
        <div className="flex items-center justify-between mb-6">
          <div className={`p-4 rounded-2xl shadow-lg ${color} transform transition-transform hover:scale-110`}>
            <Icon className="w-8 h-8 text-white" />
          </div>
          {trend && (
            <div className={`flex items-center px-3 py-2 rounded-full text-sm font-medium ${
              trend === 'up' ? 'text-red-300 bg-red-900/30' : 'text-green-300 bg-green-900/30'
            }`}>
              {trend === 'up' ? <TrendingUp className="w-4 h-4 mr-1" /> : <TrendingDown className="w-4 h-4 mr-1" />}
              {trendValue}
            </div>
          )}
        </div>
        
        <div>
          <div className="text-4xl font-bold text-slate-100 mb-2 tracking-tight">{value}</div>
          <div className="text-lg font-semibold text-slate-300 mb-1">{title}</div>
          {subtitle && <div className="text-sm text-slate-400 font-medium">{subtitle}</div>}
        </div>
      </div>
    </div>
  );
};

const KPICards = () => {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    const kpiData = dashboardData.getKPIMetrics();
    setMetrics(kpiData);
  }, []);

  if (!metrics) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="bg-slate-900/60 rounded-lg shadow-sm border border-slate-800 p-6 animate-pulse">
            <div className="w-full h-20 bg-slate-800 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
      <KPICard
        title="Total Customers"
        value={metrics.totalCustomers.toLocaleString()}
        subtitle={`Avg Age: ${metrics.avgCustomerAge} years`}
        icon={Users}
        color="bg-gradient-to-r from-blue-500 to-blue-600"
        gradient="bg-gradient-to-br from-slate-900/70 to-indigo-900/30"
      />
      <KPICard
        title="Churned Customers"
        value={metrics.churnedCustomers.toLocaleString()}
        subtitle="Lost customers"
        icon={AlertTriangle}
        color="bg-gradient-to-r from-red-500 to-red-600"
        gradient="bg-gradient-to-br from-slate-900/70 to-rose-900/30"
        trend="up"
        trendValue={`${metrics.churnRate}%`}
      />
      <KPICard
        title="Churn Rate"
        value={`${metrics.churnRate}%`}
        subtitle={`${metrics.retentionRate}% retained`}
        icon={TrendingDown}
        color="bg-gradient-to-r from-orange-500 to-red-500"
        gradient="bg-gradient-to-br from-slate-900/70 to-amber-900/30"
        trend="up"
        trendValue="Above target"
      />
      <KPICard
        title="High-Risk Customers"
        value={metrics.highRiskCustomers.toLocaleString()}
        subtitle="Requiring attention"
        icon={Shield}
        color="bg-gradient-to-r from-yellow-500 to-orange-500"
        gradient="bg-gradient-to-br from-slate-900/70 to-orange-900/30"
        trend="up"
        trendValue="Priority"
      />
    </div>
  );
};

export default KPICards;

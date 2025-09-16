import React from 'react';
import { TrendingUp, TrendingDown, Users, DollarSign } from 'lucide-react';

const KPICard = ({ title, value, subtitle, icon: Icon, trend, trendValue, color }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className={`p-2 rounded-lg ${color}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        {trend && (
          <div className={`flex items-center text-sm ${trend === 'up' ? 'text-red-500' : 'text-green-500'}`}>
            {trend === 'up' ? <TrendingUp className="w-4 h-4 mr-1" /> : <TrendingDown className="w-4 h-4 mr-1" />}
            {trendValue}
          </div>
        )}
      </div>
      <div>
        <div className="text-3xl font-bold text-gray-900 mb-1">{value}</div>
        <div className="text-sm text-gray-600">{title}</div>
        {subtitle && <div className="text-xs text-gray-500 mt-1">{subtitle}</div>}
      </div>
    </div>
  );
};

const KPICards = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <KPICard
        title="Risky Customers"
        value="23423"
        icon={Users}
        color="bg-red-500"
        trend="up"
        trendValue="12.5%"
      />
      <KPICard
        title="Impacted Revenue From Risky Cohorts"
        value="$53.2M"
        icon={DollarSign}
        color="bg-orange-500"
        trend="up"
        trendValue="8.3%"
      />
      <KPICard
        title="Average Churn Rate"
        value="14.2%"
        icon={TrendingDown}
        color="bg-blue-500"
        trend="down"
        trendValue="2.1%"
      />
      <KPICard
        title="Impacted Revenue From Low Churn Risk Customers"
        value="$12.2M"
        icon={DollarSign}
        color="bg-green-500"
        trend="down"
        trendValue="5.7%"
      />
    </div>
  );
};

export default KPICards;

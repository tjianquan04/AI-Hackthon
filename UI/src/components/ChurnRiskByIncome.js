import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip } from 'recharts';
import { dashboardData } from '../services/dashboardData';

const ChurnRiskByIncome = () => {
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const incomeData = dashboardData.getIncomeChartData();
    
    // Transform the data for the chart
    const transformedData = incomeData.labels.map((label, index) => ({
      income: label.replace('$', '').replace(' +', '+'), // Clean up labels
      churnRate: parseFloat(incomeData.datasets[0].data[index]),
      customers: Object.values(dashboardData.getChurnOverview().churn_by_income)[index]?.Total_Customers || 0
    }));
    
    setChartData(transformedData);
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="animate-pulse">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Churn Risk By Income</h3>
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">📊 Churn Analysis by Income</h3>
          <p className="text-gray-600">Customer retention rates across income segments • EDA Insights</p>
        </div>
        <div className="text-right">
          <div className="text-sm text-gray-500">Total Customers</div>
          <div className="text-2xl font-bold text-blue-600">
            {chartData.reduce((sum, item) => sum + item.customers, 0).toLocaleString()}
          </div>
        </div>
      </div>
      <div className="h-80 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-4">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis 
              dataKey="income" 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 11, fill: '#475569', fontWeight: 500 }}
              angle={-45}
              textAnchor="end"
              height={60}
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#475569', fontWeight: 500 }}
              tickFormatter={(value) => `${value}%`}
            />
            <Tooltip 
              formatter={(value, name) => [
                name === 'churnRate' ? `${value}%` : value.toLocaleString(),
                name === 'churnRate' ? 'Churn Rate' : 'Total Customers'
              ]}
              labelFormatter={(label) => `Income Category: ${label}`}
              contentStyle={{
                backgroundColor: '#fff',
                border: 'none',
                borderRadius: '12px',
                boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
                fontSize: '14px',
                fontWeight: '500'
              }}
            />
            <Bar 
              dataKey="churnRate" 
              fill="url(#colorGradient)"
              radius={[6, 6, 0, 0]}
              opacity={0.9}
            />
            <defs>
              <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#3B82F6" />
                <stop offset="100%" stopColor="#1D4ED8" />
              </linearGradient>
            </defs>
          </BarChart>
        </ResponsiveContainer>
      </div>
      
      {/* Summary Stats */}
      <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
        {chartData.map((item, index) => (
          <div key={index} className="text-center p-3 bg-white/60 rounded-lg border border-gray-200">
            <div className="text-xs font-medium text-gray-600 mb-1">{item.income}</div>
            <div className="text-lg font-bold text-gray-900">{item.churnRate}%</div>
            <div className="text-xs text-gray-500">{item.customers.toLocaleString()} customers</div>
          </div>
        ))}
      </div>
      
    </div>
  );
};

export default ChurnRiskByIncome;

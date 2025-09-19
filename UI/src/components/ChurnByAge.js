import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip, BarChart, Bar, Legend } from 'recharts';
import { dashboardData } from '../services/dashboardData';

const ChurnByAge = () => {
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const ageData = dashboardData.getAgeGroupChartData();
    
    // Transform the data for the chart
    const transformedData = ageData.labels.map((label, index) => ({
      ageGroup: label,
      churnRate: parseFloat(ageData.datasets[0].data[index]),
      totalCustomers: ageData.datasets[1].data[index],
      churnedCustomers: Math.round((parseFloat(ageData.datasets[0].data[index]) / 100) * ageData.datasets[1].data[index])
    }));
    
    setChartData(transformedData);
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="animate-pulse">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Churn Analysis by Age Group</h3>
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">👥 Age Demographics Analysis</h3>
          <p className="text-gray-600">Customer behavior patterns by age cohorts • EDA Deep Dive</p>
        </div>
        <div className="text-right">
          <div className="text-sm text-gray-500">Highest Risk Age</div>
          <div className="text-2xl font-bold text-orange-600">40-50</div>
        </div>
      </div>
      
      <div className="h-80 bg-gradient-to-br from-orange-50 to-red-50 rounded-xl p-4">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis 
              dataKey="ageGroup" 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#475569', fontWeight: 500 }}
            />
            <YAxis 
              yAxisId="left"
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 11, fill: '#475569' }}
              tickFormatter={(value) => value.toLocaleString()}
            />
            <YAxis 
              yAxisId="right"
              orientation="right"
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 11, fill: '#475569' }}
              tickFormatter={(value) => `${value}%`}
            />
            <Tooltip 
              formatter={(value, name) => [
                name === 'churnRate' ? `${value}%` : value.toLocaleString(),
                name === 'churnRate' ? 'Churn Rate' : 
                name === 'totalCustomers' ? 'Total Customers' : 'Churned Customers'
              ]}
              labelFormatter={(label) => `Age Group: ${label}`}
              contentStyle={{
                backgroundColor: '#fff',
                border: 'none',
                borderRadius: '12px',
                boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
                fontSize: '14px'
              }}
            />
            <Legend 
              wrapperStyle={{ 
                paddingTop: '20px',
                fontSize: '14px',
                fontWeight: '500'
              }}
            />
            <Bar 
              yAxisId="left"
              dataKey="totalCustomers" 
              fill="url(#blueGradient)"
              radius={[4, 4, 0, 0]}
              opacity={0.8}
              name="Total Customers"
            />
            <Bar 
              yAxisId="left"
              dataKey="churnedCustomers" 
              fill="url(#redGradient)"
              radius={[4, 4, 0, 0]}
              opacity={0.9}
              name="Churned Customers"
            />
            <defs>
              <linearGradient id="blueGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#60A5FA" />
                <stop offset="100%" stopColor="#3B82F6" />
              </linearGradient>
              <linearGradient id="redGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#F87171" />
                <stop offset="100%" stopColor="#EF4444" />
              </linearGradient>
            </defs>
          </BarChart>
        </ResponsiveContainer>
      </div>
      
      <div className="mt-6 grid grid-cols-2 md:grid-cols-5 gap-4 text-center">
        {chartData.map((item, index) => (
          <div key={index} className={`p-4 rounded-xl border-2 transition-all hover:scale-105 ${
            item.churnRate > 15 ? 'bg-red-50 border-red-200' : 
            item.churnRate > 12 ? 'bg-yellow-50 border-yellow-200' : 
            'bg-green-50 border-green-200'
          }`}>
            <div className="text-sm font-bold text-gray-700 mb-1">{item.ageGroup}</div>
            <div className={`text-2xl font-bold mb-1 ${
              item.churnRate > 15 ? 'text-red-600' : 
              item.churnRate > 12 ? 'text-yellow-600' : 
              'text-green-600'
            }`}>{item.churnRate}%</div>
            <div className="text-xs text-gray-600">{item.totalCustomers.toLocaleString()}</div>
            <div className="text-xs text-gray-500">{item.churnedCustomers} churned</div>
          </div>
        ))}
      </div>
      
    </div>
  );
};

export default ChurnByAge;


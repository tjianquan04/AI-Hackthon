import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer } from 'recharts';

const ChurnRiskByIncome = () => {
  // Sample data based on the dashboard image - histogram showing churn risk distribution by income
  const data = [
    { range: '0%', value: 120 },
    { range: '10%', value: 450 },
    { range: '20%', value: 890 },
    { range: '30%', value: 1240 },
    { range: '40%', value: 1680 },
    { range: '50%', value: 1520 },
    { range: '60%', value: 1200 },
    { range: '70%', value: 850 },
    { range: '80%', value: 420 },
    { range: '90%', value: 180 },
    { range: '100%', value: 60 }
  ];

  return (
    <div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">Churn Risk By Income</h3>
      <p className="text-sm text-gray-600 mb-4">(Total Spendings vs Churn Risk)</p>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="range" 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#6b7280' }}
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#6b7280' }}
              tickFormatter={(value) => `$${value}`}
            />
            <Bar 
              dataKey="value" 
              fill="#3b82f6" 
              radius={[2, 2, 0, 0]}
              opacity={0.8}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4 text-center">
        <div className="text-xs text-gray-500">
          Distribution shows customer spending patterns across different churn risk percentiles
        </div>
      </div>
    </div>
  );
};

export default ChurnRiskByIncome;

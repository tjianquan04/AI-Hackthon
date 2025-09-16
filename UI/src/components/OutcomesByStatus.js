import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Legend } from 'recharts';

const OutcomesByStatus = () => {
  // Sample data based on the dashboard image
  const data = [
    { month: 'Jan', Active: 45, New: 8, Inactive: 12, Lost: 5 },
    { month: 'Feb', Active: 52, New: 12, Inactive: 8, Lost: 3 },
    { month: 'Mar', Active: 38, New: 15, Inactive: 18, Lost: 7 },
    { month: 'Apr', Active: 61, New: 9, Inactive: 6, Lost: 4 },
    { month: 'May', Active: 55, New: 18, Inactive: 14, Lost: 8 },
    { month: 'Jun', Active: 67, New: 6, Inactive: 9, Lost: 6 },
    { month: 'Jul', Active: 43, New: 11, Inactive: 16, Lost: 9 },
    { month: 'Aug', Active: 58, New: 14, Inactive: 11, Lost: 5 },
    { month: 'Sep', Active: 49, New: 7, Inactive: 13, Lost: 8 },
    { month: 'Oct', Active: 44, New: 16, Inactive: 15, Lost: 6 },
    { month: 'Nov', Active: 52, New: 5, Inactive: 12, Lost: 4 },
    { month: 'Dec', Active: 35, New: 9, Inactive: 19, Lost: 12 }
  ];

  return (
    <div>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Outcomes By Status</h3>
      <div className="flex items-center text-sm text-gray-600 mb-4">
        <span className="flex items-center mr-4">
          <span className="w-3 h-3 bg-blue-500 rounded mr-2"></span>
          Active
        </span>
        <span className="flex items-center mr-4">
          <span className="w-3 h-3 bg-green-500 rounded mr-2"></span>
          New
        </span>
        <span className="flex items-center mr-4">
          <span className="w-3 h-3 bg-yellow-500 rounded mr-2"></span>
          Inactive
        </span>
        <span className="flex items-center">
          <span className="w-3 h-3 bg-red-500 rounded mr-2"></span>
          Lost
        </span>
      </div>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="month" 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#6b7280' }}
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#6b7280' }}
            />
            <Bar dataKey="Active" stackId="a" fill="#3b82f6" radius={[0, 0, 0, 0]} />
            <Bar dataKey="New" stackId="a" fill="#10b981" radius={[0, 0, 0, 0]} />
            <Bar dataKey="Inactive" stackId="a" fill="#f59e0b" radius={[0, 0, 0, 0]} />
            <Bar dataKey="Lost" stackId="a" fill="#ef4444" radius={[2, 2, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default OutcomesByStatus;

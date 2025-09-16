import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Cell } from 'recharts';

const SegmentsAnalysis = () => {
  // Sample data for bubble chart showing different customer segments
  const data = [
    { x: 25, y: 15, size: 800, segment: 'High Spenders', color: '#ef4444' },
    { x: 35, y: 25, size: 1200, segment: 'Avg Spenders', color: '#f59e0b' },
    { x: 45, y: 35, size: 600, segment: 'Low Spenders', color: '#3b82f6' },
    { x: 55, y: 45, size: 400, segment: 'Premium', color: '#8b5cf6' },
    { x: 65, y: 55, size: 300, segment: 'VIP', color: '#10b981' },
    { x: 20, y: 60, size: 500, segment: 'At Risk', color: '#dc2626' }
  ];

  return (
    <div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">Which Segments Are Likely To Leave?</h3>
      <p className="text-sm text-gray-600 mb-4">Avg. Churn Risk vs Spending | ● = 1.2k Avg. Customers Per Segment</p>
      
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              type="number" 
              dataKey="x" 
              name="spending" 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#6b7280' }}
              domain={[0, 80]}
            />
            <YAxis 
              type="number" 
              dataKey="y" 
              name="churn_risk" 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#6b7280' }}
              domain={[0, 70]}
            />
            <Scatter dataKey="size" data={data}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
      </div>

      {/* Legend */}
      <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
        {data.map((item, index) => (
          <div key={index} className="flex items-center">
            <div 
              className="w-3 h-3 rounded-full mr-2" 
              style={{ backgroundColor: item.color }}
            ></div>
            <span className="text-gray-600">{item.segment}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SegmentsAnalysis;

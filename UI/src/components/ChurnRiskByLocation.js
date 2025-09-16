import React from 'react';

const ChurnRiskByLocation = () => {
  // Sample customer data for the table
  const customerData = [
    { id: 'C001', name: 'James', gender: 'Male', churnRisk: '4%', spending: '$1,234' },
    { id: 'C002', name: 'Patricia', gender: 'Female', churnRisk: '8%', spending: '$987' },
    { id: 'C003', name: 'John', gender: 'Male', churnRisk: '12%', spending: '$2,145' },
    { id: 'C004', name: 'Jennifer', gender: 'Female', churnRisk: '6%', spending: '$1,876' },
    { id: 'C005', name: 'Michael', gender: 'Male', churnRisk: '15%', spending: '$654' },
    { id: 'C006', name: 'Linda', gender: 'Female', churnRisk: '3%', spending: '$3,210' },
    { id: 'C007', name: 'David', gender: 'Male', churnRisk: '9%', spending: '$1,543' },
    { id: 'C008', name: 'Barbara', gender: 'Female', churnRisk: '11%', spending: '$798' },
    { id: 'C009', name: 'Richard', gender: 'Male', churnRisk: '7%', spending: '$2,987' },
    { id: 'C010', name: 'Susan', gender: 'Female', churnRisk: '5%', spending: '$1,432' }
  ];

  const getChurnRiskColor = (risk) => {
    const riskValue = parseInt(risk);
    if (riskValue <= 5) return 'text-green-600 bg-green-100';
    if (riskValue <= 10) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  return (
    <div>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Churn Risk By Location</h3>
      
      {/* Simple US Map Representation */}
      <div className="mb-6 p-4 bg-blue-50 rounded-lg">
        <div className="flex items-center justify-center h-32 bg-blue-100 rounded-lg mb-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-700 mb-2">🗺️ US Map</div>
            <div className="text-sm text-blue-600">Interactive map visualization would go here</div>
            <div className="text-xs text-blue-500 mt-1">Showing churn risk by state/region</div>
          </div>
        </div>
        
        {/* Map Legend */}
        <div className="flex justify-center space-x-6 text-xs">
          <div className="flex items-center">
            <div className="w-4 h-4 bg-green-400 rounded mr-2"></div>
            <span>Low Risk (0-5%)</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-yellow-400 rounded mr-2"></div>
            <span>Medium Risk (6-10%)</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-red-400 rounded mr-2"></div>
            <span>High Risk (11%+)</span>
          </div>
        </div>
      </div>

      {/* Customer Data Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-2 px-3 text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th className="text-left py-2 px-3 text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
              <th className="text-left py-2 px-3 text-xs font-medium text-gray-500 uppercase tracking-wider">Gender</th>
              <th className="text-left py-2 px-3 text-xs font-medium text-gray-500 uppercase tracking-wider">Churn Risk</th>
              <th className="text-left py-2 px-3 text-xs font-medium text-gray-500 uppercase tracking-wider">Spending</th>
            </tr>
          </thead>
          <tbody>
            {customerData.map((customer, index) => (
              <tr key={customer.id} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                <td className="py-2 px-3 text-sm text-gray-900">{customer.id}</td>
                <td className="py-2 px-3 text-sm text-gray-900">{customer.name}</td>
                <td className="py-2 px-3 text-sm text-gray-900">{customer.gender}</td>
                <td className="py-2 px-3">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getChurnRiskColor(customer.churnRisk)}`}>
                    {customer.churnRisk}
                  </span>
                </td>
                <td className="py-2 px-3 text-sm text-gray-900 font-medium">{customer.spending}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ChurnRiskByLocation;

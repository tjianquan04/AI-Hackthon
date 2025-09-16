import React from 'react';

const CustomerTable = () => {
  // Extended customer data matching the dashboard image format
  const customers = [
    { id: 'C001', name: 'James', gender: 'Male', churnRisk: '4%', spending: '$1,234' },
    { id: 'C002', name: 'Patricia', gender: 'Female', churnRisk: '8%', spending: '$987' },
    { id: 'C003', name: 'John', gender: 'Male', churnRisk: '12%', spending: '$2,145' },
    { id: 'C004', name: 'Jennifer', gender: 'Female', churnRisk: '6%', spending: '$1,876' },
    { id: 'C005', name: 'Michael', gender: 'Male', churnRisk: '15%', spending: '$654' },
    { id: 'C006', name: 'Linda', gender: 'Female', churnRisk: '3%', spending: '$3,210' },
    { id: 'C007', name: 'David', gender: 'Male', churnRisk: '9%', spending: '$1,543' },
    { id: 'C008', name: 'Barbara', gender: 'Female', churnRisk: '11%', spending: '$798' },
    { id: 'C009', name: 'Richard', gender: 'Male', churnRisk: '7%', spending: '$2,987' },
    { id: 'C010', name: 'Susan', gender: 'Female', churnRisk: '5%', spending: '$1,432' },
    { id: 'C011', name: 'William', gender: 'Male', churnRisk: '13%', spending: '$892' },
    { id: 'C012', name: 'Karen', gender: 'Female', churnRisk: '2%', spending: '$4,567' },
    { id: 'C013', name: 'Thomas', gender: 'Male', churnRisk: '16%', spending: '$543' },
    { id: 'C014', name: 'Nancy', gender: 'Female', churnRisk: '10%', spending: '$1,765' },
    { id: 'C015', name: 'Christopher', gender: 'Male', churnRisk: '6%', spending: '$2,234' }
  ];

  const getChurnRiskColor = (risk) => {
    const riskValue = parseInt(risk);
    if (riskValue <= 5) return 'text-green-600 bg-green-100';
    if (riskValue <= 10) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getGenderIcon = (gender) => {
    return gender === 'Male' ? '👨' : '👩';
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-lg font-semibold text-gray-900">Customer Details</h3>
        <div className="text-sm text-gray-500">
          Showing {customers.length} customers
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                ID
              </th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                Name
              </th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                Gender
              </th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                Churn Risk
              </th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                Spending
              </th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {customers.map((customer) => (
              <tr key={customer.id} className="hover:bg-gray-50">
                <td className="py-4 px-4 text-sm text-gray-900 font-medium">
                  {customer.id}
                </td>
                <td className="py-4 px-4 text-sm text-gray-900">
                  <div className="flex items-center">
                    <span className="mr-2">{getGenderIcon(customer.gender)}</span>
                    {customer.name}
                  </div>
                </td>
                <td className="py-4 px-4 text-sm text-gray-900">
                  {customer.gender}
                </td>
                <td className="py-4 px-4">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getChurnRiskColor(customer.churnRisk)}`}>
                    {customer.churnRisk}
                  </span>
                </td>
                <td className="py-4 px-4 text-sm text-gray-900 font-semibold">
                  {customer.spending}
                </td>
                <td className="py-4 px-4 text-sm">
                  <div className="flex space-x-2">
                    <button className="text-blue-600 hover:text-blue-800 text-xs bg-blue-100 px-2 py-1 rounded">
                      View
                    </button>
                    <button className="text-green-600 hover:text-green-800 text-xs bg-green-100 px-2 py-1 rounded">
                      Retain
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="flex items-center justify-between mt-6">
        <div className="text-sm text-gray-500">
          Showing 1 to {customers.length} of {customers.length} results
        </div>
        <div className="flex space-x-2">
          <button className="px-3 py-1 text-sm bg-gray-100 text-gray-600 rounded hover:bg-gray-200">
            Previous
          </button>
          <button className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600">
            1
          </button>
          <button className="px-3 py-1 text-sm bg-gray-100 text-gray-600 rounded hover:bg-gray-200">
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default CustomerTable;

import React, { useState, useMemo } from 'react';
import { Search, Filter, Download, Eye, AlertTriangle, User } from 'lucide-react';
import { generateCustomerData, calculateChurnRisk, getRiskLevel, formatCurrency } from '../services/customerData';

const CustomerListView = () => {
  const [customers] = useState(() => generateCustomerData());
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRisk, setFilterRisk] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(20);

  // Process customers with risk calculation
  const processedCustomers = useMemo(() => {
    return customers.map(customer => ({
      ...customer,
      churnRisk: calculateChurnRisk(customer),
      riskLevel: getRiskLevel(calculateChurnRisk(customer))
    }));
  }, [customers]);

  // Filter and search customers
  const filteredCustomers = useMemo(() => {
    return processedCustomers.filter(customer => {
      const matchesSearch = customer.CLIENTNUM.toString().includes(searchTerm) ||
                          customer.Income_Category.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          customer.Education_Level.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesRiskFilter = filterRisk === 'all' || 
                               (filterRisk === 'low' && customer.churnRisk <= 20) ||
                               (filterRisk === 'medium' && customer.churnRisk > 20 && customer.churnRisk <= 50) ||
                               (filterRisk === 'high' && customer.churnRisk > 50);
      
      const matchesStatusFilter = filterStatus === 'all' || 
                                 customer.Attrition_Flag.toLowerCase().includes(filterStatus.toLowerCase());
      
      return matchesSearch && matchesRiskFilter && matchesStatusFilter;
    });
  }, [processedCustomers, searchTerm, filterRisk, filterStatus]);

  // Pagination
  const totalPages = Math.ceil(filteredCustomers.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentCustomers = filteredCustomers.slice(startIndex, endIndex);

  // Statistics
  const stats = useMemo(() => {
    const total = filteredCustomers.length;
    const attrited = filteredCustomers.filter(c => c.Attrition_Flag === 'Attrited Customer').length;
    const highRisk = filteredCustomers.filter(c => c.churnRisk > 50).length;
    const avgCreditLimit = filteredCustomers.reduce((sum, c) => sum + c.Credit_Limit, 0) / total;
    
    return {
      total,
      attrited,
      highRisk,
      avgCreditLimit: formatCurrency(avgCreditLimit || 0),
      churnRate: ((attrited / total) * 100).toFixed(1)
    };
  }, [filteredCustomers]);

  return (
    <div className="p-6 pt-20">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Customer Database</h1>
        <p className="text-gray-600">Complete customer information with risk assessment</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <User className="w-8 h-8 text-blue-500 mr-3" />
            <div>
              <div className="text-2xl font-bold text-gray-900">{stats.total}</div>
              <div className="text-sm text-gray-600">Total Customers</div>
            </div>
          </div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <AlertTriangle className="w-8 h-8 text-red-500 mr-3" />
            <div>
              <div className="text-2xl font-bold text-gray-900">{stats.highRisk}</div>
              <div className="text-sm text-gray-600">High Risk</div>
            </div>
          </div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center mr-3">
              <span className="text-white font-bold text-sm">%</span>
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{stats.churnRate}%</div>
              <div className="text-sm text-gray-600">Churn Rate</div>
            </div>
          </div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center mr-3">
              <span className="text-white font-bold text-sm">$</span>
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{stats.avgCreditLimit}</div>
              <div className="text-sm text-gray-600">Avg Credit Limit</div>
            </div>
          </div>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 mb-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
          <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4">
            {/* Search */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search by ID, income, education..."
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>

            {/* Risk Filter */}
            <select
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={filterRisk}
              onChange={(e) => setFilterRisk(e.target.value)}
            >
              <option value="all">All Risk Levels</option>
              <option value="low">Low Risk</option>
              <option value="medium">Medium Risk</option>
              <option value="high">High Risk</option>
            </select>

            {/* Status Filter */}
            <select
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
            >
              <option value="all">All Status</option>
              <option value="existing">Existing Customer</option>
              <option value="attrited">Attrited Customer</option>
            </select>
          </div>

          <button className="flex items-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
            <Download className="w-4 h-4 mr-2" />
            Export CSV
          </button>
        </div>
      </div>

      {/* Customer Table */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Customer ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Demographics
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Financial Info
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Activity
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Churn Risk
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {currentCustomers.map((customer) => (
                <tr key={customer.CLIENTNUM} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {customer.CLIENTNUM}
                    </div>
                    <div className="text-sm text-gray-500">
                      {customer.Card_Category}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {customer.Gender === 'M' ? '👨' : '👩'} Age {customer.Customer_Age}
                    </div>
                    <div className="text-sm text-gray-500">
                      {customer.Education_Level}
                    </div>
                    <div className="text-sm text-gray-500">
                      {customer.Marital_Status} • {customer.Dependent_count} deps
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {formatCurrency(customer.Credit_Limit)} limit
                    </div>
                    <div className="text-sm text-gray-500">
                      {customer.Income_Category}
                    </div>
                    <div className="text-sm text-gray-500">
                      {formatCurrency(customer.Total_Trans_Amt)} spent
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {customer.Total_Trans_Ct} transactions
                    </div>
                    <div className="text-sm text-gray-500">
                      {customer.Months_Inactive_12_mon} months inactive
                    </div>
                    <div className="text-sm text-gray-500">
                      {customer.Contacts_Count_12_mon} contacts
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${customer.riskLevel.color}`}>
                      {customer.churnRisk}% {customer.riskLevel.level}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      customer.Attrition_Flag === 'Existing Customer' 
                        ? 'text-green-600 bg-green-100' 
                        : 'text-red-600 bg-red-100'
                    }`}>
                      {customer.Attrition_Flag === 'Existing Customer' ? 'Active' : 'Churned'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button className="text-blue-600 hover:text-blue-900 mr-2">
                      <Eye className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="px-6 py-3 bg-gray-50 border-t border-gray-200 flex items-center justify-between">
          <div className="text-sm text-gray-700">
            Showing {startIndex + 1} to {Math.min(endIndex, filteredCustomers.length)} of {filteredCustomers.length} results
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
              disabled={currentPage === 1}
              className="px-3 py-1 text-sm bg-white border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <span className="px-3 py-1 text-sm bg-blue-500 text-white rounded">
              {currentPage} of {totalPages}
            </span>
            <button
              onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
              disabled={currentPage === totalPages}
              className="px-3 py-1 text-sm bg-white border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CustomerListView;

import React from 'react';
import KPICards from './KPICards';
import OutcomesByStatus from './OutcomesByStatus';
import ChurnRiskByIncome from './ChurnRiskByIncome';
import SegmentsAnalysis from './SegmentsAnalysis';
import ChurnRiskByLocation from './ChurnRiskByLocation';
import CustomerTable from './CustomerTable';

const Dashboard = () => {
  return (
    <div className="p-6 pt-20">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Customer Churn Dashboard</h1>
          <p className="text-gray-600">Monitor customer retention and identify at-risk segments</p>
        </div>

        {/* KPI Cards */}
        <div className="mb-8">
          <KPICards />
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Outcomes By Status */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <OutcomesByStatus />
          </div>

          {/* Churn Risk By Income */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <ChurnRiskByIncome />
          </div>

          {/* Segments Analysis */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <SegmentsAnalysis />
          </div>

          {/* Churn Risk By Location */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <ChurnRiskByLocation />
          </div>
        </div>

        {/* Customer Table */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <CustomerTable />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

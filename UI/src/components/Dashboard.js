import React from 'react';
import KPICards from './KPICards';
import ChurnRiskByIncome from './ChurnRiskByIncome';
import SegmentsAnalysis from './SegmentsAnalysis';
import ChurnInsights from './ChurnInsights';
import ChurnByAge from './ChurnByAge';
import TenureAnalysis from './TenureAnalysis';

const Dashboard = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="p-6 pt-20">
        <div className="max-w-7xl mx-auto">
          {/* Premium Header */}
          <div className="mb-8 text-center">
            <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-sm font-medium rounded-full mb-4">
              <span className="w-2 h-2 bg-white rounded-full mr-2 animate-pulse"></span>
              Live Analytics Dashboard
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-indigo-900 bg-clip-text text-transparent mb-3">
              Customer Churn Analytics
            </h1>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              Advanced EDA insights from 10,127+ customers • Real-time business intelligence for data-driven retention strategies
            </p>
          </div>

          {/* Premium KPI Cards */}
          <div className="mb-10">
            <KPICards />
          </div>

          {/* Main Analytics Grid - Streamlined */}
          <div className="grid grid-cols-1 xl:grid-cols-4 gap-8 mb-10">
            {/* Primary Analytics - Income Analysis */}
            <div className="xl:col-span-2 bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-8 hover:shadow-2xl transition-all duration-300">
              <ChurnRiskByIncome />
            </div>

            {/* Age Demographics Analysis */}
            <div className="xl:col-span-2 bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-8 hover:shadow-2xl transition-all duration-300">
              <ChurnByAge />
            </div>

            {/* Tenure Analysis - New Component */}
            <div className="xl:col-span-4 bg-gradient-to-br from-purple-50 to-indigo-50 rounded-2xl shadow-xl border border-purple-100 p-8 hover:shadow-2xl transition-all duration-300">
              <TenureAnalysis />
            </div>

            {/* Risk Insights */}
            <div className="xl:col-span-2 bg-gradient-to-br from-indigo-50 to-blue-50 rounded-2xl shadow-xl border border-indigo-100 p-8 hover:shadow-2xl transition-all duration-300">
              <ChurnInsights />
            </div>

            {/* Customer Segments - Full Width for Better Readability */}
            <div className="xl:col-span-2 bg-gradient-to-br from-green-50 to-blue-50 rounded-2xl shadow-xl border border-green-100 p-8 hover:shadow-2xl transition-all duration-300">
              <SegmentsAnalysis />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

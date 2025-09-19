import React from 'react';
import KPICards from './KPICards';
import ChurnRiskByIncome from './ChurnRiskByIncome';
import SegmentsAnalysis from './SegmentsAnalysis';
import ChurnInsights from './ChurnInsights';
import ChurnByAge from './ChurnByAge';
import TenureAnalysis from './TenureAnalysis';

const Dashboard = () => {
  return (
    <div className="min-h-screen">
      <div className="p-6 pt-20">
        <div className="max-w-7xl mx-auto">
          {/* Premium Header */}
          <div className="mb-8 text-center">
            <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-sm font-medium rounded-full mb-4 shadow-lg shadow-blue-900/30">
              <span className="w-2 h-2 bg-white rounded-full mr-2 animate-pulse"></span>
              Live Analytics Dashboard
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-slate-100 via-blue-200 to-indigo-200 bg-clip-text text-transparent mb-3">
              Customer Churn Analytics
            </h1>
            <p className="text-lg text-slate-300 max-w-3xl mx-auto">
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
            <div className="xl:col-span-2 bg-slate-900/70 backdrop-blur-sm rounded-2xl shadow-xl border border-slate-800 p-8 hover:shadow-2xl hover:shadow-blue-900/20 transition-all duration-300">
              <ChurnRiskByIncome />
            </div>

            {/* Age Demographics Analysis */}
            <div className="xl:col-span-2 bg-slate-900/70 backdrop-blur-sm rounded-2xl shadow-xl border border-slate-800 p-8 hover:shadow-2xl hover:shadow-indigo-900/20 transition-all duration-300">
              <ChurnByAge />
            </div>

            {/* Tenure Analysis - New Component */}
            <div className="xl:col-span-4 bg-gradient-to-br from-indigo-900/40 via-purple-900/30 to-blue-900/30 rounded-2xl shadow-xl border border-indigo-900/30 p-8 hover:shadow-2xl hover:shadow-purple-900/20 transition-all duration-300">
              <TenureAnalysis />
            </div>

            {/* Risk Insights */}
            <div className="xl:col-span-2 bg-gradient-to-br from-slate-900/70 to-blue-900/40 rounded-2xl shadow-xl border border-slate-800 p-8 hover:shadow-2xl transition-all duration-300">
              <ChurnInsights />
            </div>

            {/* Customer Segments - Full Width for Better Readability */}
            <div className="xl:col-span-2 bg-gradient-to-br from-slate-900/70 to-emerald-900/30 rounded-2xl shadow-xl border border-slate-800 p-8 hover:shadow-2xl transition-all duration-300">
              <SegmentsAnalysis />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

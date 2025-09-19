import React from 'react';
import { BarChart3, Users, Menu, X } from 'lucide-react';

const Sidebar = ({ activeView, setActiveView, isOpen, setIsOpen }) => {
  const menuItems = [
    {
      id: 'dashboard',
      name: 'Dashboard',
      icon: BarChart3,
      description: 'Analytics Overview'
    },
    {
      id: 'customers',
      name: 'Customer List',
      icon: Users,
      description: 'All Customers'
    },
    {
      id: 'predict',
      name: 'Predict New Churn',
      icon: BarChart3,
      description: 'Model Predictions with SHAP'
    }
  ];

  return (
    <>
      {/* Menu Toggle Button - Always visible */}
      <div className="fixed top-4 left-4 z-50">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="p-3 rounded-lg bg-slate-800/80 backdrop-blur border border-slate-700 hover:bg-slate-800 hover:shadow-xl transition-all duration-200 transform hover:scale-105"
        >
          {isOpen ? (
            <X className="w-5 h-5 text-slate-200 transition-transform duration-200" />
          ) : (
            <Menu className="w-5 h-5 text-slate-200 transition-transform duration-200" />
          )}
        </button>
      </div>

      {/* Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/60 z-40"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed top-0 left-0 h-full bg-slate-900/95 backdrop-blur shadow-2xl border-r border-slate-800 z-40
        transform transition-transform duration-300 ease-in-out
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        w-64
      `}>
        <div className="p-6">
          {/* Logo/Title */}
          <div className="mb-8">
            <h2 className="text-xl font-bold text-slate-100">Churn Analytics</h2>
            <p className="text-sm text-slate-400">Customer Intelligence</p>
          </div>

          {/* Navigation Menu */}
          <nav className="space-y-2">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeView === item.id;
              
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveView(item.id);
                    setIsOpen(false); // Close mobile menu after selection
                  }}
                  className={`
                    w-full flex items-center px-4 py-3 rounded-lg text-left
                    transition-colors duration-200
                    ${isActive 
                      ? 'bg-blue-500/15 text-blue-300 border border-blue-500/30' 
                      : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                    }
                  `}
                >
                  <Icon className={`w-5 h-5 mr-3 ${isActive ? 'text-blue-400' : 'text-slate-400'}`} />
                  <div>
                    <div className="font-medium text-slate-100">{item.name}</div>
                    <div className="text-xs text-slate-400">{item.description}</div>
                  </div>
                </button>
              );
            })}
          </nav>

          {/* Stats Summary */}
          <div className="mt-8 p-4 bg-slate-800/70 border border-slate-700 rounded-lg">
            <h3 className="text-sm font-medium text-slate-100 mb-2">Quick Stats</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-slate-400">Total Customers</span>
                <span className="font-medium text-slate-100">10,127</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">At Risk</span>
                <span className="font-medium text-red-400">1,627</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Retention Rate</span>
                <span className="font-medium text-green-400">83.9%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;

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
    }
  ];

  return (
    <>
      {/* Menu Toggle Button - Always visible */}
      <div className="fixed top-4 left-4 z-50">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="p-3 rounded-lg bg-white shadow-lg border border-gray-200 hover:bg-gray-50 hover:shadow-xl transition-all duration-200 transform hover:scale-105"
        >
          {isOpen ? (
            <X className="w-5 h-5 text-gray-700 transition-transform duration-200" />
          ) : (
            <Menu className="w-5 h-5 text-gray-700 transition-transform duration-200" />
          )}
        </button>
      </div>

      {/* Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed top-0 left-0 h-full bg-white shadow-xl border-r border-gray-200 z-40
        transform transition-transform duration-300 ease-in-out
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        w-64
      `}>
        <div className="p-6">
          {/* Logo/Title */}
          <div className="mb-8">
            <h2 className="text-xl font-bold text-gray-900">Churn Analytics</h2>
            <p className="text-sm text-gray-600">Customer Intelligence</p>
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
                      ? 'bg-blue-50 text-blue-700 border border-blue-200' 
                      : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                    }
                  `}
                >
                  <Icon className={`w-5 h-5 mr-3 ${isActive ? 'text-blue-600' : 'text-gray-500'}`} />
                  <div>
                    <div className="font-medium">{item.name}</div>
                    <div className="text-xs text-gray-500">{item.description}</div>
                  </div>
                </button>
              );
            })}
          </nav>

          {/* Stats Summary */}
          <div className="mt-8 p-4 bg-gray-50 rounded-lg">
            <h3 className="text-sm font-medium text-gray-900 mb-2">Quick Stats</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Total Customers</span>
                <span className="font-medium">10,127</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">At Risk</span>
                <span className="font-medium text-red-600">1,627</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Retention Rate</span>
                <span className="font-medium text-green-600">83.9%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;

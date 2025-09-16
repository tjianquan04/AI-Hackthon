import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import CustomerListView from './components/CustomerListView';

function App() {
  const [activeView, setActiveView] = useState('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const renderCurrentView = () => {
    switch (activeView) {
      case 'dashboard':
        return <Dashboard />;
      case 'customers':
        return <CustomerListView />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar 
        activeView={activeView}
        setActiveView={setActiveView}
        isOpen={sidebarOpen}
        setIsOpen={setSidebarOpen}
      />
      
      {/* Main Content */}
      <div className="w-full">
        {renderCurrentView()}
      </div>
    </div>
  );
}

export default App;

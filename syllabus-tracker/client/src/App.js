import React, { useState } from 'react';
import SyllabusDisplay from './components/SyllabusDisplay';
import ProgressDashboard from './components/ProgressDashboard';

function App() {
  const [activeTab, setActiveTab] = useState('syllabus');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-blue-600 text-white shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-center">
            📚 Competitive Exam Syllabus Tracker
          </h1>
          <p className="text-center mt-2 opacity-90">
            SSC CGL | IBPS PO | Patwari | VDO | MHA IB - Complete Coverage
          </p>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab('syllabus')}
              className={`py-4 px-2 border-b-2 font-medium text-sm ${
                activeTab === 'syllabus'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              📖 Syllabus
            </button>
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`py-4 px-2 border-b-2 font-medium text-sm ${
                activeTab === 'dashboard'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              📊 Progress Dashboard
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {activeTab === 'syllabus' && <SyllabusDisplay />}
        {activeTab === 'dashboard' && <ProgressDashboard />}
      </main>
    </div>
  );
}

export default App;

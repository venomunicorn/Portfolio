import React, { useEffect, useState } from 'react';
import { useApp } from '../context/AppContext';

function ProgressDashboard() {
  const { progress, loadProgress } = useApp();
  const [stats, setStats] = useState({
    totalSubtopics: 0,
    completedSubtopics: 0,
    totalTimeSpent: 0,
    topicStats: {}
  });

  useEffect(() => {
    loadProgress();
  }, []);

  useEffect(() => {
    calculateStats();
  }, [progress]);

  const calculateStats = () => {
    let totalSubtopics = 0;
    let completedSubtopics = 0;
    let totalTimeSpent = 0;
    const topicStats = {};

    Object.entries(progress).forEach(([subtopicId, data]) => {
      totalSubtopics++;
      if (data.finish_time) {
        completedSubtopics++;
        totalTimeSpent += data.time_taken || 0;
      }

      // Extract topic from subtopic ID
      const topicId = subtopicId.split('_').slice(0, -1).join('_');
      if (!topicStats[topicId]) {
        topicStats[topicId] = {
          total: 0,
          completed: 0,
          timeSpent: 0
        };
      }
      topicStats[topicId].total++;
      if (data.finish_time) {
        topicStats[topicId].completed++;
        topicStats[topicId].timeSpent += data.time_taken || 0;
      }
    });

    setStats({
      totalSubtopics,
      completedSubtopics,
      totalTimeSpent,
      topicStats
    });
  };

  const formatTime = (seconds) => {
    if (!seconds) return '00:00:00';
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getProgressPercentage = (completed, total) => {
    return total > 0 ? Math.round((completed / total) * 100) : 0;
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">
          📊 Progress Dashboard
        </h2>
        
        {/* Overall Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-md border">
            <div className="text-3xl font-bold text-blue-600">
              {stats.completedSubtopics}
            </div>
            <div className="text-gray-600">Completed Topics</div>
            <div className="text-sm text-gray-500">
              out of {stats.totalSubtopics}
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md border">
            <div className="text-3xl font-bold text-green-600">
              {getProgressPercentage(stats.completedSubtopics, stats.totalSubtopics)}%
            </div>
            <div className="text-gray-600">Overall Progress</div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md border">
            <div className="text-3xl font-bold text-purple-600">
              {formatTime(stats.totalTimeSpent)}
            </div>
            <div className="text-gray-600">Total Time Spent</div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md border">
            <div className="text-3xl font-bold text-orange-600">
              {Object.keys(stats.topicStats).length}
            </div>
            <div className="text-gray-600">Topics Started</div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="bg-white p-6 rounded-lg shadow-md border mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Overall Progress</span>
            <span className="text-sm font-medium text-gray-700">
              {getProgressPercentage(stats.completedSubtopics, stats.totalSubtopics)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div 
              className="bg-blue-600 h-4 rounded-full transition-all duration-300"
              style={{ 
                width: `${getProgressPercentage(stats.completedSubtopics, stats.totalSubtopics)}%` 
              }}
            ></div>
          </div>
        </div>

        {/* Topic-wise Progress */}
        <div className="bg-white rounded-lg shadow-md border">
          <div className="p-6 border-b">
            <h3 className="text-xl font-semibold text-gray-800">Topic-wise Progress</h3>
          </div>
          <div className="p-6">
            {Object.entries(stats.topicStats).map(([topicId, data]) => {
              const percentage = getProgressPercentage(data.completed, data.total);
              const topicName = topicId.replace(/_/g, ' ').toUpperCase();
              
              return (
                <div key={topicId} className="mb-6 last:mb-0">
                  <div className="flex justify-between items-center mb-2">
                    <h4 className="font-medium text-gray-800">{topicName}</h4>
                    <div className="text-sm text-gray-600">
                      {data.completed}/{data.total} • {formatTime(data.timeSpent)}
                    </div>
                  </div>
                  <div className="flex justify-between mb-1">
                    <span className="text-sm text-gray-600">Progress</span>
                    <span className="text-sm text-gray-600">{percentage}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div 
                      className="bg-green-500 h-3 rounded-full transition-all duration-300"
                      style={{ width: `${percentage}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="mt-8 bg-white rounded-lg shadow-md border">
          <div className="p-6 border-b">
            <h3 className="text-xl font-semibold text-gray-800">Recent Activity</h3>
          </div>
          <div className="p-6">
            {Object.entries(progress)
              .filter(([_, data]) => data.finish_time)
              .sort((a, b) => new Date(b[1].finish_time) - new Date(a[1].finish_time))
              .slice(0, 10)
              .map(([subtopicId, data]) => (
                <div key={subtopicId} className="flex items-center justify-between py-3 border-b last:border-b-0">
                  <div>
                    <div className="font-medium text-gray-800">
                      {subtopicId.replace(/_/g, ' ')}
                    </div>
                    <div className="text-sm text-gray-600">
                      Completed {new Date(data.finish_time).toLocaleDateString()}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-green-600 font-medium">✅ Complete</div>
                    <div className="text-sm text-gray-600">
                      {formatTime(data.time_taken)}
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProgressDashboard;

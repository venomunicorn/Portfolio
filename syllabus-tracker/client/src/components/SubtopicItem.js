import React, { useState } from 'react';
import { startSubtopic, finishSubtopic } from '../services/api';
import { useApp } from '../context/AppContext';

function SubtopicItem({ subtopic, topicId }) {
  const { progress, updateSubtopicProgress } = useApp();
  const [loading, setLoading] = useState(false);
  
  const subtopicId = `${topicId}_${subtopic.replace(/\s+/g, '_').toLowerCase()}`;
  const subtopicProgress = progress[subtopicId] || {};
  
  const hasStarted = subtopicProgress.start_time;
  const hasFinished = subtopicProgress.finish_time;
  const timeTaken = subtopicProgress.time_taken || 0;

  const handleStart = async () => {
    if (hasStarted && !hasFinished) return; // Already started
    
    try {
      setLoading(true);
      const result = await startSubtopic(subtopicId);
      updateSubtopicProgress(subtopicId, result);
    } catch (error) {
      console.error('Error starting subtopic:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFinish = async () => {
    if (!hasStarted || hasFinished) return;
    
    try {
      setLoading(true);
      const result = await finishSubtopic(subtopicId);
      updateSubtopicProgress(subtopicId, result);
    } catch (error) {
      console.error('Error finishing subtopic:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    if (!seconds) return '00:00:00';
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getStatusColor = () => {
    if (hasFinished) return 'text-green-600 bg-green-50';
    if (hasStarted) return 'text-yellow-600 bg-yellow-50';
    return 'text-gray-600 bg-gray-50';
  };

  const getStatusIcon = () => {
    if (hasFinished) return '✅';
    if (hasStarted) return '⏳';
    return '⭕';
  };

  return (
    <div className={`p-4 rounded-lg border ${getStatusColor()} mb-2`}>
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <span className="text-lg mr-2">{getStatusIcon()}</span>
          <span className="font-medium">{subtopic}</span>
        </div>
        
        <div className="flex items-center space-x-3">
          {hasFinished && (
            <span className="text-sm font-mono bg-white px-2 py-1 rounded">
              ⏱️ {formatTime(timeTaken)}
            </span>
          )}
          
          <div className="flex space-x-2">
            <button
              onClick={handleStart}
              disabled={loading || (hasStarted && !hasFinished)}
              className={`px-4 py-2 rounded font-medium ${
                hasStarted && !hasFinished
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-green-500 hover:bg-green-600 text-white'
              }`}
            >
              {hasStarted && !hasFinished ? 'Started' : 'Start'}
            </button>
            
            <button
              onClick={handleFinish}
              disabled={loading || !hasStarted || hasFinished}
              className={`px-4 py-2 rounded font-medium ${
                !hasStarted || hasFinished
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-500 hover:bg-blue-600 text-white'
              }`}
            >
              {hasFinished ? 'Finished' : 'Finish'}
            </button>
          </div>
        </div>
      </div>
      
      {(hasStarted || hasFinished) && (
        <div className="mt-2 text-sm text-gray-600 bg-white p-2 rounded">
          {hasStarted && (
            <div>📅 Started: {new Date(subtopicProgress.start_time).toLocaleString()}</div>
          )}
          {hasFinished && (
            <div>🏁 Finished: {new Date(subtopicProgress.finish_time).toLocaleString()}</div>
          )}
        </div>
      )}
    </div>
  );
}

export default SubtopicItem;

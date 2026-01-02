import React, { useState } from 'react';
import SubtopicItem from './SubtopicItem';

function TopicSection({ topic, subtopics, topicId }) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="mb-6 border rounded-lg overflow-hidden shadow-sm">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-4 bg-blue-500 text-white text-left font-semibold text-lg hover:bg-blue-600 flex items-center justify-between"
      >
        <span>{topic}</span>
        <span className="text-xl">{isExpanded ? '▼' : '▶'}</span>
      </button>
      
      {isExpanded && (
        <div className="p-4 bg-white">
          {subtopics.map((subtopic, index) => (
            <SubtopicItem
              key={index}
              subtopic={subtopic}
              topicId={topicId}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default TopicSection;

import axios from 'axios';

const API_BASE = '/api';

export const startSubtopic = async (subtopicId) => {
  const response = await axios.post(`${API_BASE}/start`, {
    subtopicId,
    timestamp: new Date().toISOString()
  });
  return response.data;
};

export const finishSubtopic = async (subtopicId) => {
  const response = await axios.post(`${API_BASE}/finish`, {
    subtopicId,
    timestamp: new Date().toISOString()
  });
  return response.data;
};

export const fetchProgress = async () => {
  const response = await axios.get(`${API_BASE}/progress`);
  return response.data;
};

export const fetchSyllabus = async () => {
  const response = await axios.get(`${API_BASE}/syllabus`);
  return response.data;
};

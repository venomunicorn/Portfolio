import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { fetchProgress } from '../services/api';

const AppContext = createContext();

const initialState = {
  progress: {},
  loading: false,
  error: null
};

function appReducer(state, action) {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_PROGRESS':
      return { ...state, progress: action.payload, loading: false };
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    case 'UPDATE_SUBTOPIC':
      return {
        ...state,
        progress: {
          ...state.progress,
          [action.payload.subtopicId]: action.payload.data
        }
      };
    default:
      return state;
  }
}

export function AppProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const data = await fetchProgress();
      dispatch({ type: 'SET_PROGRESS', payload: data });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
    }
  };

  const updateSubtopicProgress = (subtopicId, data) => {
    dispatch({ type: 'UPDATE_SUBTOPIC', payload: { subtopicId, data } });
  };

  return (
    <AppContext.Provider value={{
      ...state,
      loadProgress,
      updateSubtopicProgress
    }}>
      {children}
    </AppContext.Provider>
  );
}

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};

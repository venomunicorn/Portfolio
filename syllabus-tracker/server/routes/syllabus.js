const express = require('express');
const router = express.Router();
const db = require('../database/db');

// Get syllabus data
router.get('/syllabus', (req, res) => {
  try {
    const topics = db.prepare('SELECT * FROM topics ORDER BY id').all();
    res.json(topics);
  } catch (error) {
    console.error('Error fetching syllabus:', error);
    res.status(500).json({ error: 'Failed to fetch syllabus' });
  }
});

// Start a subtopic
router.post('/start', (req, res) => {
  try {
    const { subtopicId, timestamp } = req.body;
    
    if (!subtopicId || !timestamp) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    const startTime = new Date(timestamp).toISOString();
    
    // Insert or update study session
    const stmt = db.prepare(`
      INSERT INTO study_sessions (subtopic_id, start_time, updated_at)
      VALUES (?, ?, CURRENT_TIMESTAMP)
      ON CONFLICT(subtopic_id) DO UPDATE SET
        start_time = excluded.start_time,
        finish_time = NULL,
        time_taken = 0,
        updated_at = CURRENT_TIMESTAMP
    `);
    
    stmt.run(subtopicId, startTime);
    
    // Return updated data
    const session = db.prepare('SELECT * FROM study_sessions WHERE subtopic_id = ?').get(subtopicId);
    
    res.json({
      subtopicId,
      start_time: session.start_time,
      finish_time: session.finish_time,
      time_taken: session.time_taken
    });
  } catch (error) {
    console.error('Error starting subtopic:', error);
    res.status(500).json({ error: 'Failed to start subtopic' });
  }
});

// Finish a subtopic
router.post('/finish', (req, res) => {
  try {
    const { subtopicId, timestamp } = req.body;
    
    if (!subtopicId || !timestamp) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    const finishTime = new Date(timestamp).toISOString();
    
    // Get current session
    const session = db.prepare('SELECT * FROM study_sessions WHERE subtopic_id = ?').get(subtopicId);
    
    if (!session || !session.start_time) {
      return res.status(400).json({ error: 'No active session found. Please start first.' });
    }

    // Calculate time taken in seconds
    const startTime = new Date(session.start_time);
    const endTime = new Date(finishTime);
    const timeTaken = Math.floor((endTime - startTime) / 1000);
    
    // Update session with finish time
    const stmt = db.prepare(`
      UPDATE study_sessions 
      SET finish_time = ?, time_taken = ?, updated_at = CURRENT_TIMESTAMP
      WHERE subtopic_id = ?
    `);
    
    stmt.run(finishTime, timeTaken, subtopicId);
    
    res.json({
      subtopicId,
      start_time: session.start_time,
      finish_time: finishTime,
      time_taken: timeTaken
    });
  } catch (error) {
    console.error('Error finishing subtopic:', error);
    res.status(500).json({ error: 'Failed to finish subtopic' });
  }
});

// Get progress data
router.get('/progress', (req, res) => {
  try {
    const sessions = db.prepare('SELECT * FROM study_sessions').all();
    
    const progress = {};
    sessions.forEach(session => {
      progress[session.subtopic_id] = {
        start_time: session.start_time,
        finish_time: session.finish_time,
        time_taken: session.time_taken
      };
    });
    
    res.json(progress);
  } catch (error) {
    console.error('Error fetching progress:', error);
    res.status(500).json({ error: 'Failed to fetch progress' });
  }
});

// Reset progress (optional)
router.post('/reset', (req, res) => {
  try {
    db.prepare('DELETE FROM study_sessions').run();
    res.json({ message: 'Progress reset successfully' });
  } catch (error) {
    console.error('Error resetting progress:', error);
    res.status(500).json({ error: 'Failed to reset progress' });
  }
});

module.exports = router;

-- Create topics table
CREATE TABLE IF NOT EXISTS topics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create subtopics table  
CREATE TABLE IF NOT EXISTS subtopics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  topic_id INTEGER,
  name TEXT NOT NULL,
  subtopic_id TEXT UNIQUE NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (topic_id) REFERENCES topics (id)
);

-- Create study sessions table
CREATE TABLE IF NOT EXISTS study_sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subtopic_id TEXT NOT NULL,
  start_time DATETIME,
  finish_time DATETIME,
  time_taken INTEGER DEFAULT 0, -- in seconds
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(subtopic_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_subtopic_id ON study_sessions(subtopic_id);
CREATE INDEX IF NOT EXISTS idx_topic_id ON subtopics(topic_id);

-- Insert sample data if tables are empty
INSERT OR IGNORE INTO topics (name) VALUES 
  ('QUANTITATIVE APTITUDE (Pre + Mains)'),
  ('REASONING ABILITY (Pre + Mains)'),
  ('ENGLISH LANGUAGE (Pre + Mains)'),
  ('GENERAL AWARENESS / GENERAL KNOWLEDGE'),
  ('DESCRIPTIVE SECTION (Tier 3 / Mains)'),
  ('INTERVIEW (IBPS PO / MHA IB)'),
  ('STATE SPECIFIC (Patwari/VDO)');

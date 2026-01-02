#pragma once

#include <string>
#include <vector>
#include <fstream>

struct HighScoreEntry {
    std::string name;
    int score;
    int waveReached;
};

struct GameSettings {
    float masterVolume = 100.0f;
    float musicVolume = 70.0f;
    float sfxVolume = 100.0f;
    bool fullscreen = false;
    bool vsync = true;
    int screenShakeIntensity = 100;  // 0-100
};

class SaveManager {
public:
    static SaveManager& getInstance();
    
    // High scores
    void loadHighScores();
    void saveHighScores();
    bool isHighScore(int score) const;
    void addHighScore(const std::string& name, int score, int waveReached);
    const std::vector<HighScoreEntry>& getHighScores() const { return m_highScores; }
    
    // Settings
    void loadSettings();
    void saveSettings();
    GameSettings& getSettings() { return m_settings; }
    const GameSettings& getSettings() const { return m_settings; }
    
private:
    SaveManager();
    ~SaveManager() = default;
    SaveManager(const SaveManager&) = delete;
    SaveManager& operator=(const SaveManager&) = delete;
    
    std::string getSavePath() const;
    
    std::vector<HighScoreEntry> m_highScores;
    GameSettings m_settings;
    
    static constexpr int MAX_HIGH_SCORES = 10;
};

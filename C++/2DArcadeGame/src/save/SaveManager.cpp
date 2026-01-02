#include "SaveManager.h"
#include <algorithm>
#include <sstream>
#include <iostream>

#ifdef _WIN32
#include <Windows.h>
#include <ShlObj.h>
#endif

SaveManager& SaveManager::getInstance() {
    static SaveManager instance;
    return instance;
}

SaveManager::SaveManager() {
    loadHighScores();
    loadSettings();
}

std::string SaveManager::getSavePath() const {
#ifdef _WIN32
    char path[MAX_PATH];
    if (SUCCEEDED(SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, 0, path))) {
        return std::string(path) + "\\2DArcadeGame\\";
    }
#endif
    return "./";
}

void SaveManager::loadHighScores() {
    m_highScores.clear();
    
    std::ifstream file(getSavePath() + "highscores.dat");
    if (!file.is_open()) {
        // Create default empty high scores
        return;
    }
    
    std::string line;
    while (std::getline(file, line) && m_highScores.size() < MAX_HIGH_SCORES) {
        std::istringstream iss(line);
        HighScoreEntry entry;
        if (iss >> entry.name >> entry.score >> entry.waveReached) {
            m_highScores.push_back(entry);
        }
    }
    
    // Sort by score descending
    std::sort(m_highScores.begin(), m_highScores.end(),
              [](const HighScoreEntry& a, const HighScoreEntry& b) {
                  return a.score > b.score;
              });
}

void SaveManager::saveHighScores() {
    // Create directory if needed
    std::string savePath = getSavePath();
#ifdef _WIN32
    CreateDirectoryA(savePath.c_str(), NULL);
#endif
    
    std::ofstream file(savePath + "highscores.dat");
    if (!file.is_open()) {
        std::cerr << "Warning: Could not save high scores" << std::endl;
        return;
    }
    
    for (const auto& entry : m_highScores) {
        file << entry.name << " " << entry.score << " " << entry.waveReached << "\n";
    }
}

bool SaveManager::isHighScore(int score) const {
    if (m_highScores.size() < MAX_HIGH_SCORES) {
        return score > 0;
    }
    return score > m_highScores.back().score;
}

void SaveManager::addHighScore(const std::string& name, int score, int waveReached) {
    HighScoreEntry entry{name, score, waveReached};
    m_highScores.push_back(entry);
    
    // Sort by score descending
    std::sort(m_highScores.begin(), m_highScores.end(),
              [](const HighScoreEntry& a, const HighScoreEntry& b) {
                  return a.score > b.score;
              });
    
    // Keep only top N
    if (m_highScores.size() > MAX_HIGH_SCORES) {
        m_highScores.resize(MAX_HIGH_SCORES);
    }
    
    saveHighScores();
}

void SaveManager::loadSettings() {
    std::ifstream file(getSavePath() + "settings.dat");
    if (!file.is_open()) {
        // Use defaults
        return;
    }
    
    file >> m_settings.masterVolume
         >> m_settings.musicVolume
         >> m_settings.sfxVolume
         >> m_settings.fullscreen
         >> m_settings.vsync
         >> m_settings.screenShakeIntensity;
}

void SaveManager::saveSettings() {
    std::string savePath = getSavePath();
#ifdef _WIN32
    CreateDirectoryA(savePath.c_str(), NULL);
#endif
    
    std::ofstream file(savePath + "settings.dat");
    if (!file.is_open()) {
        std::cerr << "Warning: Could not save settings" << std::endl;
        return;
    }
    
    file << m_settings.masterVolume << "\n"
         << m_settings.musicVolume << "\n"
         << m_settings.sfxVolume << "\n"
         << m_settings.fullscreen << "\n"
         << m_settings.vsync << "\n"
         << m_settings.screenShakeIntensity << "\n";
}

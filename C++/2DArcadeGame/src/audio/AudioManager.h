#pragma once

#include <SFML/Audio.hpp>
#include <unordered_map>
#include <string>
#include <memory>

class AudioManager {
public:
    static AudioManager& getInstance();
    
    // Initialization
    void init();
    
    // Sound effects
    void loadSound(const std::string& name, const std::string& filepath);
    void playSound(const std::string& name, float volume = 100.0f, float pitch = 1.0f);
    
    // Music
    void playMusic(const std::string& filepath, bool loop = true);
    void stopMusic();
    void pauseMusic();
    void resumeMusic();
    
    // Volume controls
    void setMasterVolume(float volume);
    void setMusicVolume(float volume);
    void setSFXVolume(float volume);
    
    float getMasterVolume() const { return m_masterVolume; }
    float getMusicVolume() const { return m_musicVolume; }
    float getSFXVolume() const { return m_sfxVolume; }
    
    // Mute when unfocused
    void setMuted(bool muted);
    bool isMuted() const { return m_muted; }
    
private:
    AudioManager();
    ~AudioManager() = default;
    AudioManager(const AudioManager&) = delete;
    AudioManager& operator=(const AudioManager&) = delete;
    
    std::unordered_map<std::string, sf::SoundBuffer> m_soundBuffers;
    std::vector<sf::Sound> m_activeSounds;
    sf::Music m_music;
    
    float m_masterVolume;
    float m_musicVolume;
    float m_sfxVolume;
    bool m_muted;
    
    static constexpr int MAX_SOUNDS = 32;
};

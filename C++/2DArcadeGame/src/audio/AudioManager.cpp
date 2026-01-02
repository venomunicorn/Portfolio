#include "AudioManager.h"
#include <iostream>

AudioManager& AudioManager::getInstance() {
    static AudioManager instance;
    return instance;
}

AudioManager::AudioManager()
    : m_masterVolume(100.0f)
    , m_musicVolume(70.0f)
    , m_sfxVolume(100.0f)
    , m_muted(false)
{
    m_activeSounds.resize(MAX_SOUNDS);
}

void AudioManager::init() {
    // Load default sounds
    loadSound("shoot", "assets/audio/shoot.wav");
    loadSound("hit", "assets/audio/hit.wav");
    loadSound("explosion", "assets/audio/explosion.wav");
    loadSound("pickup", "assets/audio/pickup.wav");
    loadSound("powerup", "assets/audio/powerup.wav");
    loadSound("damage", "assets/audio/damage.wav");
    loadSound("death", "assets/audio/death.wav");
    loadSound("select", "assets/audio/select.wav");
    loadSound("pause", "assets/audio/pause.wav");
}

void AudioManager::loadSound(const std::string& name, const std::string& filepath) {
    sf::SoundBuffer buffer;
    if (buffer.loadFromFile(filepath)) {
        m_soundBuffers[name] = std::move(buffer);
    } else {
        // Silent fail - audio is optional
        std::cerr << "Warning: Could not load sound: " << filepath << std::endl;
    }
}

void AudioManager::playSound(const std::string& name, float volume, float pitch) {
    if (m_muted) return;
    
    auto it = m_soundBuffers.find(name);
    if (it == m_soundBuffers.end()) return;
    
    // Find an available sound slot
    for (auto& sound : m_activeSounds) {
        if (sound.getStatus() != sf::Sound::Playing) {
            sound.setBuffer(it->second);
            sound.setVolume(volume * (m_sfxVolume / 100.0f) * (m_masterVolume / 100.0f));
            sound.setPitch(pitch);
            sound.play();
            return;
        }
    }
    
    // All slots busy, replace the first one
    m_activeSounds[0].setBuffer(it->second);
    m_activeSounds[0].setVolume(volume * (m_sfxVolume / 100.0f) * (m_masterVolume / 100.0f));
    m_activeSounds[0].setPitch(pitch);
    m_activeSounds[0].play();
}

void AudioManager::playMusic(const std::string& filepath, bool loop) {
    if (m_music.openFromFile(filepath)) {
        m_music.setLoop(loop);
        m_music.setVolume(m_musicVolume * (m_masterVolume / 100.0f));
        if (!m_muted) {
            m_music.play();
        }
    }
}

void AudioManager::stopMusic() {
    m_music.stop();
}

void AudioManager::pauseMusic() {
    m_music.pause();
}

void AudioManager::resumeMusic() {
    if (!m_muted) {
        m_music.play();
    }
}

void AudioManager::setMasterVolume(float volume) {
    m_masterVolume = std::max(0.0f, std::min(100.0f, volume));
    m_music.setVolume(m_musicVolume * (m_masterVolume / 100.0f));
}

void AudioManager::setMusicVolume(float volume) {
    m_musicVolume = std::max(0.0f, std::min(100.0f, volume));
    m_music.setVolume(m_musicVolume * (m_masterVolume / 100.0f));
}

void AudioManager::setSFXVolume(float volume) {
    m_sfxVolume = std::max(0.0f, std::min(100.0f, volume));
}

void AudioManager::setMuted(bool muted) {
    m_muted = muted;
    if (muted) {
        m_music.pause();
    } else if (m_music.getStatus() == sf::Music::Paused) {
        m_music.play();
    }
}

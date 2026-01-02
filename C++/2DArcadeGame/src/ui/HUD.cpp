#include "HUD.h"
#include "entities/Player.h"
#include "systems/SpawnSystem.h"
#include "core/Config.h"
#include <sstream>
#include <iomanip>

HUD::HUD()
    : m_maxHealthBarWidth(200.0f)
    , m_hasSpeedBoost(false)
    , m_hasRapidFire(false)
    , m_hasShield(false)
{
}

void HUD::init() {
    // Load font
    if (!m_font.loadFromFile("assets/fonts/arcade.ttf")) {
        m_font.loadFromFile("C:/Windows/Fonts/arial.ttf");
    }
    
    // Score text (top right)
    m_scoreText.setFont(m_font);
    m_scoreText.setCharacterSize(28);
    m_scoreText.setFillColor(sf::Color::White);
    m_scoreText.setPosition(Config::WINDOW_WIDTH - 250.0f, 20.0f);
    
    // Multiplier text (below score)
    m_multiplierText.setFont(m_font);
    m_multiplierText.setCharacterSize(20);
    m_multiplierText.setFillColor(sf::Color::Yellow);
    m_multiplierText.setPosition(Config::WINDOW_WIDTH - 250.0f, 55.0f);
    
    // Wave text (top center)
    m_waveText.setFont(m_font);
    m_waveText.setCharacterSize(24);
    m_waveText.setFillColor(sf::Color(180, 180, 180));
    m_waveText.setPosition(Config::WINDOW_WIDTH / 2.0f - 50.0f, 20.0f);
    
    // Health bar background
    m_healthBarBg.setSize(sf::Vector2f(m_maxHealthBarWidth, 20.0f));
    m_healthBarBg.setPosition(20.0f, 20.0f);
    m_healthBarBg.setFillColor(sf::Color(66, 66, 66));
    
    // Health bar
    m_healthBar.setSize(sf::Vector2f(m_maxHealthBarWidth, 20.0f));
    m_healthBar.setPosition(20.0f, 20.0f);
    m_healthBar.setFillColor(sf::Color(102, 187, 106));
    
    // Power-up indicators (below health bar)
    float indicatorY = 50.0f;
    float indicatorSize = 15.0f;
    float indicatorSpacing = 20.0f;
    
    m_speedBoostIndicator.setSize(sf::Vector2f(indicatorSize, indicatorSize));
    m_speedBoostIndicator.setPosition(20.0f, indicatorY);
    m_speedBoostIndicator.setFillColor(sf::Color(33, 150, 243));  // Blue
    
    m_rapidFireIndicator.setSize(sf::Vector2f(indicatorSize, indicatorSize));
    m_rapidFireIndicator.setPosition(20.0f + indicatorSpacing, indicatorY);
    m_rapidFireIndicator.setFillColor(sf::Color(255, 193, 7));   // Yellow
    
    m_shieldIndicator.setSize(sf::Vector2f(indicatorSize, indicatorSize));
    m_shieldIndicator.setPosition(20.0f + indicatorSpacing * 2, indicatorY);
    m_shieldIndicator.setFillColor(sf::Color(156, 39, 176));     // Purple
    
    // Power-up label
    m_powerUpText.setFont(m_font);
    m_powerUpText.setCharacterSize(12);
    m_powerUpText.setFillColor(sf::Color(150, 150, 150));
    m_powerUpText.setPosition(20.0f + indicatorSpacing * 3 + 5, indicatorY);
}

void HUD::update(const Player& player, const SpawnSystem& spawner) {
    // Update score
    std::stringstream ss;
    ss << "SCORE: " << std::setw(8) << std::setfill('0') << player.getScore();
    m_scoreText.setString(ss.str());
    
    // Update multiplier
    std::stringstream ms;
    ms << std::fixed << std::setprecision(2) << "x" << player.getMultiplier();
    m_multiplierText.setString(ms.str());
    
    // Color multiplier based on value
    float mult = player.getMultiplier();
    if (mult >= 4.0f) {
        m_multiplierText.setFillColor(sf::Color::Red);
    } else if (mult >= 2.5f) {
        m_multiplierText.setFillColor(sf::Color(255, 165, 0)); // Orange
    } else if (mult >= 1.5f) {
        m_multiplierText.setFillColor(sf::Color::Yellow);
    } else {
        m_multiplierText.setFillColor(sf::Color::White);
    }
    
    // Update wave
    std::stringstream ws;
    ws << "WAVE " << spawner.getWaveNumber();
    m_waveText.setString(ws.str());
    
    // Update health bar
    float healthPercent = static_cast<float>(player.getHealth()) / 
                          static_cast<float>(Config::PLAYER_MAX_HEALTH);
    healthPercent = Math::clamp(healthPercent, 0.0f, 1.0f);
    m_healthBar.setSize(sf::Vector2f(m_maxHealthBarWidth * healthPercent, 20.0f));
    
    // Color health bar based on health
    if (healthPercent > 0.6f) {
        m_healthBar.setFillColor(sf::Color(102, 187, 106)); // Green
    } else if (healthPercent > 0.3f) {
        m_healthBar.setFillColor(sf::Color(255, 193, 7));   // Yellow
    } else {
        m_healthBar.setFillColor(sf::Color(244, 67, 54));   // Red
    }
    
    // Update power-up indicators
    m_hasSpeedBoost = player.hasSpeedBoost();
    m_hasRapidFire = player.hasRapidFire();
    m_hasShield = player.hasShield();
    
    // Build power-up text
    std::string powerUpStr;
    if (m_hasSpeedBoost || m_hasRapidFire || m_hasShield) {
        powerUpStr = "ACTIVE: ";
        if (m_hasSpeedBoost) powerUpStr += "SPEED ";
        if (m_hasRapidFire) powerUpStr += "RAPID ";
        if (m_hasShield) powerUpStr += "SHIELD";
    }
    m_powerUpText.setString(powerUpStr);
}

void HUD::render(sf::RenderWindow& window) {
    window.draw(m_healthBarBg);
    window.draw(m_healthBar);
    window.draw(m_scoreText);
    window.draw(m_multiplierText);
    window.draw(m_waveText);
    
    // Draw active power-up indicators
    if (m_hasSpeedBoost) {
        window.draw(m_speedBoostIndicator);
    }
    if (m_hasRapidFire) {
        window.draw(m_rapidFireIndicator);
    }
    if (m_hasShield) {
        window.draw(m_shieldIndicator);
    }
    
    window.draw(m_powerUpText);
}

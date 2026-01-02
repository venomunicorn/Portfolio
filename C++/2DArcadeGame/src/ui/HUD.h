#pragma once

#include <SFML/Graphics.hpp>

class Player;
class SpawnSystem;

class HUD {
public:
    HUD();
    
    void init();
    void update(const Player& player, const SpawnSystem& spawner);
    void render(sf::RenderWindow& window);
    
private:
    sf::Font m_font;
    sf::Text m_scoreText;
    sf::Text m_multiplierText;
    sf::Text m_waveText;
    
    // Health bar
    sf::RectangleShape m_healthBarBg;
    sf::RectangleShape m_healthBar;
    
    // Power-up indicators
    sf::RectangleShape m_speedBoostIndicator;
    sf::RectangleShape m_rapidFireIndicator;
    sf::RectangleShape m_shieldIndicator;
    sf::Text m_powerUpText;
    
    float m_maxHealthBarWidth;
    bool m_hasSpeedBoost;
    bool m_hasRapidFire;
    bool m_hasShield;
};

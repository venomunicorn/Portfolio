#include "PowerUp.h"
#include "core/Config.h"
#include <cmath>

PowerUp::PowerUp()
    : m_type(PowerUpType::Health)
    , m_value(0)
    , m_duration(0.0f)
    , m_lifetime(0.0f)
    , m_maxLifetime(10.0f)
    , m_pulseTimer(0.0f)
{
    m_size = sf::Vector2f(24.0f, 24.0f);
    m_active = false;
    
    m_shape.setRadius(12.0f);
    m_shape.setOrigin(12.0f, 12.0f);
    m_shape.setOutlineThickness(2.0f);
    
    m_innerShape.setRadius(6.0f);
    m_innerShape.setOrigin(6.0f, 6.0f);
}

void PowerUp::spawn(const sf::Vector2f& position, PowerUpType type) {
    m_position = position;
    m_type = type;
    m_active = true;
    m_lifetime = m_maxLifetime;
    m_pulseTimer = 0.0f;
    
    switch (type) {
        case PowerUpType::Health:
            m_value = 30;  // Restore 30 HP
            m_duration = 0.0f;
            m_shape.setFillColor(sf::Color(76, 175, 80, 200));      // Green
            m_shape.setOutlineColor(sf::Color(129, 199, 132));
            m_innerShape.setFillColor(sf::Color(200, 230, 201));
            break;
            
        case PowerUpType::SpeedBoost:
            m_value = 0;
            m_duration = 5.0f;  // 5 seconds
            m_shape.setFillColor(sf::Color(33, 150, 243, 200));     // Blue
            m_shape.setOutlineColor(sf::Color(100, 181, 246));
            m_innerShape.setFillColor(sf::Color(187, 222, 251));
            break;
            
        case PowerUpType::RapidFire:
            m_value = 0;
            m_duration = 5.0f;  // 5 seconds
            m_shape.setFillColor(sf::Color(255, 193, 7, 200));      // Yellow/Amber
            m_shape.setOutlineColor(sf::Color(255, 213, 79));
            m_innerShape.setFillColor(sf::Color(255, 236, 179));
            break;
            
        case PowerUpType::Shield:
            m_value = 0;
            m_duration = 4.0f;  // 4 seconds
            m_shape.setFillColor(sf::Color(156, 39, 176, 200));     // Purple
            m_shape.setOutlineColor(sf::Color(186, 104, 200));
            m_innerShape.setFillColor(sf::Color(225, 190, 231));
            break;
            
        case PowerUpType::ScoreBonus:
            m_value = 500;  // 500 bonus points
            m_duration = 0.0f;
            m_shape.setFillColor(sf::Color(255, 215, 0, 200));      // Gold
            m_shape.setOutlineColor(sf::Color(255, 235, 59));
            m_innerShape.setFillColor(sf::Color(255, 255, 224));
            break;
    }
}

void PowerUp::update(float deltaTime) {
    if (!m_active) return;
    
    m_lifetime -= deltaTime;
    m_pulseTimer += deltaTime;
    
    // Deactivate if lifetime expired
    if (m_lifetime <= 0.0f) {
        m_active = false;
        return;
    }
    
    // Pulse effect
    float pulse = std::sin(m_pulseTimer * 4.0f) * 0.2f + 1.0f;
    m_shape.setScale(pulse, pulse);
    
    // Blink when about to expire
    if (m_lifetime < 3.0f) {
        float blink = std::sin(m_lifetime * 10.0f);
        sf::Color color = m_shape.getFillColor();
        color.a = static_cast<sf::Uint8>(blink > 0 ? 200 : 50);
        m_shape.setFillColor(color);
    }
    
    // Gentle floating motion
    m_position.y += std::sin(m_pulseTimer * 2.0f) * 0.5f;
    
    m_shape.setPosition(m_position);
    m_innerShape.setPosition(m_position);
}

void PowerUp::render(sf::RenderWindow& window) {
    if (!m_active) return;
    window.draw(m_shape);
    window.draw(m_innerShape);
}

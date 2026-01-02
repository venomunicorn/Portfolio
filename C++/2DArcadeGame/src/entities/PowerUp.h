#pragma once

#include "Entity.h"

enum class PowerUpType {
    Health,      // Restore health
    SpeedBoost,  // Temporary speed increase
    RapidFire,   // Faster fire rate
    Shield,      // Temporary invulnerability
    ScoreBonus   // Bonus points
};

class PowerUp : public Entity {
public:
    PowerUp();
    
    void update(float deltaTime) override;
    void render(sf::RenderWindow& window) override;
    
    void spawn(const sf::Vector2f& position, PowerUpType type);
    
    PowerUpType getType() const { return m_type; }
    int getValue() const { return m_value; }
    float getDuration() const { return m_duration; }
    
private:
    sf::CircleShape m_shape;
    sf::CircleShape m_innerShape;
    PowerUpType m_type;
    int m_value;
    float m_duration;
    float m_lifetime;
    float m_maxLifetime;
    float m_pulseTimer;
};

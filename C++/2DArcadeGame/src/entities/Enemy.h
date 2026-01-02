#pragma once

#include "Entity.h"

enum class EnemyType {
    Chaser,     // Basic: follows player directly
    Shooter,    // Stops at range and shoots
    Bomber,     // Rushes player, explodes on contact or death
    Tank        // Slow but high HP, high damage
};

class Projectile;
class Player;

class Enemy : public Entity {
public:
    Enemy();
    
    void update(float deltaTime) override;
    void render(sf::RenderWindow& window) override;
    
    void spawn(const sf::Vector2f& position, EnemyType type = EnemyType::Chaser);
    void setTarget(const sf::Vector2f& targetPosition) { m_targetPosition = targetPosition; }
    
    int getContactDamage() const { return m_contactDamage; }
    int getScoreValue() const { return m_scoreValue; }
    EnemyType getType() const { return m_type; }
    
    // For shooter enemies
    bool canShoot() const { return m_shootTimer <= 0.0f && m_type == EnemyType::Shooter; }
    void resetShootTimer();
    sf::Vector2f getShootDirection() const;
    
    // For bomber enemies
    bool isExploding() const { return m_exploding; }
    float getExplosionRadius() const { return m_explosionRadius; }
    void triggerExplosion();
    
private:
    void updateChaser(float deltaTime);
    void updateShooter(float deltaTime);
    void updateBomber(float deltaTime);
    void updateTank(float deltaTime);
    
    sf::RectangleShape m_shape;
    sf::CircleShape m_explosionShape;  // For bomber
    sf::Vector2f m_targetPosition;
    
    EnemyType m_type;
    int m_contactDamage;
    int m_scoreValue;
    
    // Shooter specific
    float m_shootTimer;
    float m_preferredRange;
    
    // Bomber specific
    bool m_exploding;
    float m_explosionTimer;
    float m_explosionRadius;
    float m_chargeSpeed;
};

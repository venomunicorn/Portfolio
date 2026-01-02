#pragma once

#include "Entity.h"
#include "Projectile.h"
#include "PowerUp.h"
#include <vector>
#include <memory>

class Player : public Entity {
public:
    Player();
    
    void update(float deltaTime) override;
    void render(sf::RenderWindow& window) override;
    
    void handleInput();
    void shoot(std::vector<std::unique_ptr<Projectile>>& projectiles);
    
    // Invulnerability
    bool isInvulnerable() const { return m_invulnerabilityTimer > 0.0f || m_shieldTimer > 0.0f; }
    void makeInvulnerable(float duration);
    
    // Scoring
    int getScore() const { return m_score; }
    void addScore(int points);
    float getMultiplier() const { return m_comboMultiplier; }
    void resetCombo();
    
    // Power-ups
    void applyPowerUp(const PowerUp& powerUp);
    bool hasSpeedBoost() const { return m_speedBoostTimer > 0.0f; }
    bool hasRapidFire() const { return m_rapidFireTimer > 0.0f; }
    bool hasShield() const { return m_shieldTimer > 0.0f; }
    
private:
    void applyMovement(float deltaTime);
    void clampToScreen();
    void updatePowerUpTimers(float deltaTime);
    
    sf::RectangleShape m_shape;
    sf::CircleShape m_shieldShape;  // Visual for shield
    sf::Vector2f m_inputDirection;
    
    // Combat
    float m_fireTimer;
    float m_invulnerabilityTimer;
    
    // Scoring
    int m_score;
    float m_comboTimer;
    float m_comboMultiplier;
    
    // Power-up timers
    float m_speedBoostTimer;
    float m_rapidFireTimer;
    float m_shieldTimer;
    float m_speedMultiplier;
    float m_fireRateMultiplier;
};

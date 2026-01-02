#pragma once

#include "Entity.h"
#include <vector>
#include <functional>

enum class BossPhase {
    Intro,      // Moving into position
    Phase1,     // Basic attack patterns
    Phase2,     // More aggressive attacks
    Phase3,     // Enraged mode
    Death       // Death animation
};

enum class BossAttack {
    CircleShot,     // Bullets in a circle
    AimedShot,      // Aimed at player
    SweepShot,      // Rotating beam of bullets
    SpawnMinions,   // Spawn helper enemies
    Charge          // Dash towards player
};

class Projectile;

class Boss : public Entity {
public:
    Boss();
    
    void update(float deltaTime) override;
    void render(sf::RenderWindow& window) override;
    
    void spawn(const sf::Vector2f& position);
    void setTarget(const sf::Vector2f& target) { m_targetPosition = target; }
    
    // Attack interface
    bool hasProjectilesToSpawn() const { return !m_pendingProjectiles.empty(); }
    std::pair<sf::Vector2f, sf::Vector2f> popProjectile();
    
    bool wantsToSpawnMinion() const { return m_spawnMinionFlag; }
    sf::Vector2f getMinionSpawnPosition();
    
    BossPhase getPhase() const { return m_phase; }
    int getScoreValue() const { return m_scoreValue; }
    bool isIntroComplete() const { return m_phase != BossPhase::Intro; }
    
private:
    void updatePhase();
    void executeAttack(float deltaTime);
    void performCircleShot(int bulletCount);
    void performAimedShot(int bulletCount);
    void performSweepShot(float deltaTime);
    void performCharge(float deltaTime);
    
    sf::RectangleShape m_shape;
    sf::RectangleShape m_healthBarBg;
    sf::RectangleShape m_healthBar;
    
    sf::Vector2f m_targetPosition;
    sf::Vector2f m_homePosition;
    
    BossPhase m_phase;
    BossAttack m_currentAttack;
    
    float m_attackTimer;
    float m_attackCooldown;
    float m_patternTimer;
    float m_sweepAngle;
    int m_attackIndex;
    bool m_charging;
    sf::Vector2f m_chargeTarget;
    
    int m_scoreValue;
    bool m_spawnMinionFlag;
    
    std::vector<std::pair<sf::Vector2f, sf::Vector2f>> m_pendingProjectiles;
};

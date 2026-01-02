#include "Boss.h"
#include "core/Config.h"
#include <cmath>

Boss::Boss()
    : m_phase(BossPhase::Intro)
    , m_currentAttack(BossAttack::CircleShot)
    , m_attackTimer(0.0f)
    , m_attackCooldown(2.0f)
    , m_patternTimer(0.0f)
    , m_sweepAngle(0.0f)
    , m_attackIndex(0)
    , m_charging(false)
    , m_scoreValue(5000)
    , m_spawnMinionFlag(false)
{
    m_size = sf::Vector2f(80.0f, 80.0f);
    m_health = 500;
    m_maxHealth = 500;
    m_active = false;
    
    m_shape.setSize(m_size);
    m_shape.setOrigin(m_size.x / 2.0f, m_size.y / 2.0f);
    m_shape.setFillColor(sf::Color(180, 0, 180));
    m_shape.setOutlineThickness(3.0f);
    m_shape.setOutlineColor(sf::Color(255, 100, 255));
    
    // Health bar
    m_healthBarBg.setSize(sf::Vector2f(Config::WINDOW_WIDTH - 200.0f, 15.0f));
    m_healthBarBg.setPosition(100.0f, 60.0f);
    m_healthBarBg.setFillColor(sf::Color(60, 60, 60));
    
    m_healthBar.setSize(sf::Vector2f(Config::WINDOW_WIDTH - 200.0f, 15.0f));
    m_healthBar.setPosition(100.0f, 60.0f);
    m_healthBar.setFillColor(sf::Color(200, 0, 200));
    
    m_homePosition = sf::Vector2f(Config::WINDOW_WIDTH / 2.0f, 120.0f);
}

void Boss::spawn(const sf::Vector2f& position) {
    m_position = position;
    m_health = m_maxHealth;
    m_phase = BossPhase::Intro;
    m_active = true;
    m_attackTimer = 3.0f;  // Delay before first attack
    m_patternTimer = 0.0f;
}

void Boss::update(float deltaTime) {
    if (!m_active) return;
    
    m_spawnMinionFlag = false;
    updatePhase();
    
    // Intro: move to home position
    if (m_phase == BossPhase::Intro) {
        sf::Vector2f toHome = m_homePosition - m_position;
        float dist = Math::magnitude(toHome);
        if (dist > 5.0f) {
            m_velocity = Math::normalize(toHome) * 100.0f;
        } else {
            m_position = m_homePosition;
            m_velocity = sf::Vector2f(0, 0);
            m_phase = BossPhase::Phase1;
        }
    }
    // Death animation
    else if (m_phase == BossPhase::Death) {
        m_patternTimer += deltaTime;
        float scale = 1.0f + m_patternTimer * 0.5f;
        m_shape.setScale(scale, scale);
        sf::Color color = m_shape.getFillColor();
        color.a = static_cast<sf::Uint8>(255 * (1.0f - m_patternTimer / 2.0f));
        m_shape.setFillColor(color);
        
        if (m_patternTimer >= 2.0f) {
            m_active = false;
        }
    }
    // Combat phases
    else {
        if (!m_charging) {
            // Gentle hovering motion
            m_position.y = m_homePosition.y + std::sin(m_patternTimer * 2.0f) * 20.0f;
            m_position.x = m_homePosition.x + std::sin(m_patternTimer * 1.5f) * 50.0f;
        }
        
        m_patternTimer += deltaTime;
        executeAttack(deltaTime);
    }
    
    m_position += m_velocity * deltaTime;
    m_shape.setPosition(m_position);
    
    // Update health bar
    float healthPercent = static_cast<float>(m_health) / static_cast<float>(m_maxHealth);
    m_healthBar.setSize(sf::Vector2f((Config::WINDOW_WIDTH - 200.0f) * healthPercent, 15.0f));
    
    // Check death
    if (m_health <= 0 && m_phase != BossPhase::Death) {
        m_phase = BossPhase::Death;
        m_patternTimer = 0.0f;
        m_velocity = sf::Vector2f(0, 0);
    }
}

void Boss::updatePhase() {
    float healthPercent = static_cast<float>(m_health) / static_cast<float>(m_maxHealth);
    
    if (m_phase != BossPhase::Death && m_phase != BossPhase::Intro) {
        if (healthPercent <= 0.3f) {
            m_phase = BossPhase::Phase3;
            m_attackCooldown = 0.8f;
        } else if (healthPercent <= 0.6f) {
            m_phase = BossPhase::Phase2;
            m_attackCooldown = 1.2f;
        } else {
            m_phase = BossPhase::Phase1;
            m_attackCooldown = 2.0f;
        }
    }
}

void Boss::executeAttack(float deltaTime) {
    m_attackTimer -= deltaTime;
    
    if (m_charging) {
        performCharge(deltaTime);
        return;
    }
    
    if (m_attackTimer <= 0.0f) {
        // Choose attack based on phase
        int maxAttack = 2;
        if (m_phase == BossPhase::Phase2) maxAttack = 3;
        if (m_phase == BossPhase::Phase3) maxAttack = 5;
        
        m_attackIndex = (m_attackIndex + 1) % maxAttack;
        
        switch (m_attackIndex) {
            case 0:
                performCircleShot(m_phase == BossPhase::Phase3 ? 24 : 12);
                break;
            case 1:
                performAimedShot(m_phase == BossPhase::Phase3 ? 5 : 3);
                break;
            case 2:
                m_sweepAngle = 0.0f;
                m_currentAttack = BossAttack::SweepShot;
                break;
            case 3:
                m_spawnMinionFlag = true;
                break;
            case 4:
                m_charging = true;
                m_chargeTarget = m_targetPosition;
                break;
        }
        
        m_attackTimer = m_attackCooldown;
    }
    
    // Continuous sweep attack
    if (m_currentAttack == BossAttack::SweepShot) {
        performSweepShot(deltaTime);
    }
}

void Boss::performCircleShot(int bulletCount) {
    for (int i = 0; i < bulletCount; ++i) {
        float angle = (360.0f / bulletCount) * i * 3.14159f / 180.0f;
        sf::Vector2f direction(std::cos(angle), std::sin(angle));
        m_pendingProjectiles.push_back({m_position, direction});
    }
}

void Boss::performAimedShot(int bulletCount) {
    sf::Vector2f baseDir = Math::normalize(m_targetPosition - m_position);
    
    for (int i = 0; i < bulletCount; ++i) {
        float spread = (i - bulletCount / 2) * 15.0f * 3.14159f / 180.0f;
        float angle = std::atan2(baseDir.y, baseDir.x) + spread;
        sf::Vector2f direction(std::cos(angle), std::sin(angle));
        m_pendingProjectiles.push_back({m_position, direction});
    }
}

void Boss::performSweepShot(float deltaTime) {
    m_sweepAngle += deltaTime * 180.0f;  // 180 degrees per second
    
    if (m_sweepAngle >= 360.0f) {
        m_currentAttack = BossAttack::CircleShot;
        return;
    }
    
    // Fire bullet at current sweep angle
    static float lastShotAngle = 0.0f;
    if (m_sweepAngle - lastShotAngle >= 15.0f) {
        float angle = m_sweepAngle * 3.14159f / 180.0f;
        sf::Vector2f direction(std::cos(angle), std::sin(angle));
        m_pendingProjectiles.push_back({m_position, direction});
        lastShotAngle = m_sweepAngle;
    }
}

void Boss::performCharge(float deltaTime) {
    sf::Vector2f toTarget = m_chargeTarget - m_position;
    float dist = Math::magnitude(toTarget);
    
    if (dist > 20.0f) {
        m_velocity = Math::normalize(toTarget) * 400.0f;
    } else {
        m_charging = false;
        m_velocity = sf::Vector2f(0, 0);
    }
}

std::pair<sf::Vector2f, sf::Vector2f> Boss::popProjectile() {
    if (m_pendingProjectiles.empty()) {
        return {{0,0}, {0,0}};
    }
    auto proj = m_pendingProjectiles.back();
    m_pendingProjectiles.pop_back();
    return proj;
}

sf::Vector2f Boss::getMinionSpawnPosition() {
    m_spawnMinionFlag = false;
    float angle = Math::randomFloat(0.0f, 360.0f) * 3.14159f / 180.0f;
    return m_position + sf::Vector2f(std::cos(angle), std::sin(angle)) * 60.0f;
}

void Boss::render(sf::RenderWindow& window) {
    if (!m_active) return;
    
    // Draw health bar (only after intro)
    if (m_phase != BossPhase::Intro) {
        window.draw(m_healthBarBg);
        window.draw(m_healthBar);
    }
    
    window.draw(m_shape);
}

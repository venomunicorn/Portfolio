#include "Enemy.h"
#include "core/Config.h"

Enemy::Enemy()
    : m_type(EnemyType::Chaser)
    , m_contactDamage(Config::ENEMY_DAMAGE)
    , m_scoreValue(Config::ENEMY_SCORE_VALUE)
    , m_shootTimer(0.0f)
    , m_preferredRange(250.0f)
    , m_exploding(false)
    , m_explosionTimer(0.0f)
    , m_explosionRadius(80.0f)
    , m_chargeSpeed(200.0f)
{
    m_size = sf::Vector2f(Config::ENEMY_SIZE, Config::ENEMY_SIZE);
    m_health = Config::ENEMY_HEALTH;
    m_maxHealth = Config::ENEMY_HEALTH;
    m_active = false;
    
    m_shape.setSize(m_size);
    m_shape.setOrigin(m_size.x / 2.0f, m_size.y / 2.0f);
    m_shape.setFillColor(sf::Color(239, 83, 80));  // Red
    
    m_explosionShape.setRadius(m_explosionRadius);
    m_explosionShape.setOrigin(m_explosionRadius, m_explosionRadius);
    m_explosionShape.setFillColor(sf::Color(255, 100, 0, 150));
}

void Enemy::spawn(const sf::Vector2f& position, EnemyType type) {
    m_position = position;
    m_type = type;
    m_active = true;
    m_exploding = false;
    m_explosionTimer = 0.0f;
    m_shootTimer = 1.5f;  // Initial delay before first shot
    
    // Configure based on type
    switch (type) {
        case EnemyType::Chaser:
            m_health = 30;
            m_contactDamage = 15;
            m_scoreValue = 100;
            m_size = sf::Vector2f(28.0f, 28.0f);
            m_shape.setFillColor(sf::Color(239, 83, 80));  // Red
            break;
            
        case EnemyType::Shooter:
            m_health = 25;
            m_contactDamage = 10;
            m_scoreValue = 150;
            m_size = sf::Vector2f(24.0f, 24.0f);
            m_shape.setFillColor(sf::Color(156, 39, 176));  // Purple
            break;
            
        case EnemyType::Bomber:
            m_health = 20;
            m_contactDamage = 40;
            m_scoreValue = 200;
            m_size = sf::Vector2f(32.0f, 32.0f);
            m_chargeSpeed = 250.0f;
            m_shape.setFillColor(sf::Color(255, 152, 0));  // Orange
            break;
            
        case EnemyType::Tank:
            m_health = 100;
            m_contactDamage = 25;
            m_scoreValue = 300;
            m_size = sf::Vector2f(40.0f, 40.0f);
            m_shape.setFillColor(sf::Color(96, 125, 139));  // Blue-gray
            break;
    }
    
    m_maxHealth = m_health;
    m_shape.setSize(m_size);
    m_shape.setOrigin(m_size.x / 2.0f, m_size.y / 2.0f);
}

void Enemy::update(float deltaTime) {
    if (!m_active) return;
    
    // Handle explosion state for bombers
    if (m_exploding) {
        m_explosionTimer += deltaTime;
        if (m_explosionTimer >= 0.3f) {
            m_active = false;
        }
        m_explosionShape.setPosition(m_position);
        float alpha = 150.0f * (1.0f - m_explosionTimer / 0.3f);
        m_explosionShape.setFillColor(sf::Color(255, 100, 0, static_cast<sf::Uint8>(alpha)));
        return;
    }
    
    // Update based on type
    switch (m_type) {
        case EnemyType::Chaser:
            updateChaser(deltaTime);
            break;
        case EnemyType::Shooter:
            updateShooter(deltaTime);
            break;
        case EnemyType::Bomber:
            updateBomber(deltaTime);
            break;
        case EnemyType::Tank:
            updateTank(deltaTime);
            break;
    }
    
    m_position += m_velocity * deltaTime;
    
    // Check if dead
    if (m_health <= 0) {
        if (m_type == EnemyType::Bomber && !m_exploding) {
            triggerExplosion();
        } else {
            m_active = false;
        }
    }
    
    m_shape.setPosition(m_position);
    
    // Visual feedback when damaged
    float healthPercent = static_cast<float>(m_health) / static_cast<float>(m_maxHealth);
    sf::Color baseColor = m_shape.getFillColor();
    baseColor.a = static_cast<sf::Uint8>(128 + 127 * healthPercent);
    m_shape.setFillColor(baseColor);
}

void Enemy::updateChaser(float deltaTime) {
    sf::Vector2f direction = m_targetPosition - m_position;
    float dist = Math::magnitude(direction);
    
    if (dist > 1.0f) {
        direction = Math::normalize(direction);
        m_velocity = direction * Config::ENEMY_SPEED;
    }
}

void Enemy::updateShooter(float deltaTime) {
    sf::Vector2f direction = m_targetPosition - m_position;
    float dist = Math::magnitude(direction);
    
    // Move to preferred range
    if (dist > m_preferredRange + 30.0f) {
        direction = Math::normalize(direction);
        m_velocity = direction * (Config::ENEMY_SPEED * 0.8f);
    } else if (dist < m_preferredRange - 30.0f) {
        direction = Math::normalize(direction);
        m_velocity = -direction * (Config::ENEMY_SPEED * 0.5f);
    } else {
        // Strafe slowly when at range
        sf::Vector2f perpendicular(-direction.y, direction.x);
        perpendicular = Math::normalize(perpendicular);
        m_velocity = perpendicular * (Config::ENEMY_SPEED * 0.3f);
    }
    
    // Update shoot timer
    if (m_shootTimer > 0.0f) {
        m_shootTimer -= deltaTime;
    }
}

void Enemy::updateBomber(float deltaTime) {
    sf::Vector2f direction = m_targetPosition - m_position;
    float dist = Math::magnitude(direction);
    
    if (dist > 1.0f) {
        direction = Math::normalize(direction);
        m_velocity = direction * m_chargeSpeed;
    }
    
    // Pulse effect - bomber gets brighter as it approaches
    float intensity = Math::clamp(1.0f - dist / 300.0f, 0.0f, 1.0f);
    sf::Uint8 r = static_cast<sf::Uint8>(255);
    sf::Uint8 g = static_cast<sf::Uint8>(152 - 100 * intensity);
    sf::Uint8 b = static_cast<sf::Uint8>(0);
    m_shape.setFillColor(sf::Color(r, g, b));
}

void Enemy::updateTank(float deltaTime) {
    sf::Vector2f direction = m_targetPosition - m_position;
    float dist = Math::magnitude(direction);
    
    if (dist > 1.0f) {
        direction = Math::normalize(direction);
        m_velocity = direction * (Config::ENEMY_SPEED * 0.5f);  // Slow
    }
}

void Enemy::render(sf::RenderWindow& window) {
    if (!m_active) return;
    
    if (m_exploding) {
        window.draw(m_explosionShape);
    }
    
    window.draw(m_shape);
}

void Enemy::resetShootTimer() {
    m_shootTimer = 2.0f;  // 2 seconds between shots
}

sf::Vector2f Enemy::getShootDirection() const {
    return Math::normalize(m_targetPosition - m_position);
}

void Enemy::triggerExplosion() {
    m_exploding = true;
    m_explosionTimer = 0.0f;
    m_velocity = sf::Vector2f(0.0f, 0.0f);
}

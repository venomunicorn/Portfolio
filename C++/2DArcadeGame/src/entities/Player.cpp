#include "Player.h"
#include "core/Config.h"
#include <SFML/Window/Keyboard.hpp>
#include <cmath>

Player::Player()
    : m_inputDirection(0.0f, 0.0f)
    , m_fireTimer(0.0f)
    , m_invulnerabilityTimer(0.0f)
    , m_score(0)
    , m_comboTimer(0.0f)
    , m_comboMultiplier(1.0f)
    , m_speedBoostTimer(0.0f)
    , m_rapidFireTimer(0.0f)
    , m_shieldTimer(0.0f)
    , m_speedMultiplier(1.0f)
    , m_fireRateMultiplier(1.0f)
{
    m_size = sf::Vector2f(Config::PLAYER_SIZE, Config::PLAYER_SIZE);
    m_position = sf::Vector2f(Config::WINDOW_WIDTH / 2.0f, Config::WINDOW_HEIGHT / 2.0f);
    m_health = Config::PLAYER_MAX_HEALTH;
    m_maxHealth = Config::PLAYER_MAX_HEALTH;
    
    // Setup player visual
    m_shape.setSize(m_size);
    m_shape.setOrigin(m_size.x / 2.0f, m_size.y / 2.0f);
    m_shape.setFillColor(sf::Color(79, 195, 247));  // Light blue
    
    // Setup shield visual
    m_shieldShape.setRadius(Config::PLAYER_SIZE * 0.8f);
    m_shieldShape.setOrigin(Config::PLAYER_SIZE * 0.8f, Config::PLAYER_SIZE * 0.8f);
    m_shieldShape.setFillColor(sf::Color(156, 39, 176, 80));
    m_shieldShape.setOutlineThickness(3.0f);
    m_shieldShape.setOutlineColor(sf::Color(186, 104, 200, 180));
}

void Player::handleInput() {
    m_inputDirection = sf::Vector2f(0.0f, 0.0f);
    
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::W) || sf::Keyboard::isKeyPressed(sf::Keyboard::Up)) {
        m_inputDirection.y -= 1.0f;
    }
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::S) || sf::Keyboard::isKeyPressed(sf::Keyboard::Down)) {
        m_inputDirection.y += 1.0f;
    }
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::A) || sf::Keyboard::isKeyPressed(sf::Keyboard::Left)) {
        m_inputDirection.x -= 1.0f;
    }
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::D) || sf::Keyboard::isKeyPressed(sf::Keyboard::Right)) {
        m_inputDirection.x += 1.0f;
    }
    
    // Normalize diagonal movement
    float mag = Math::magnitude(m_inputDirection);
    if (mag > 1.0f) {
        m_inputDirection = Math::normalize(m_inputDirection);
    }
}

void Player::update(float deltaTime) {
    handleInput();
    applyMovement(deltaTime);
    clampToScreen();
    updatePowerUpTimers(deltaTime);
    
    // Update fire timer
    if (m_fireTimer > 0.0f) {
        m_fireTimer -= deltaTime;
    }
    
    // Update invulnerability
    if (m_invulnerabilityTimer > 0.0f) {
        m_invulnerabilityTimer -= deltaTime;
    }
    
    // Combo decay
    if (m_comboTimer > 0.0f) {
        m_comboTimer -= deltaTime;
        if (m_comboTimer <= 0.0f) {
            resetCombo();
        }
    }
    
    // Update visuals
    m_shape.setPosition(m_position);
    m_shieldShape.setPosition(m_position);
    
    // Visual effects based on state
    sf::Color playerColor(79, 195, 247);
    
    // Flash when invulnerable (from damage)
    if (m_invulnerabilityTimer > 0.0f) {
        int flashPhase = static_cast<int>(m_invulnerabilityTimer * 10) % 2;
        playerColor = flashPhase == 0 ? sf::Color::White : sf::Color(79, 195, 247);
    }
    
    // Speed boost effect - more blue
    if (hasSpeedBoost()) {
        playerColor.b = 255;
        playerColor.r = static_cast<sf::Uint8>(79 + 50 * std::sin(m_speedBoostTimer * 8));
    }
    
    // Rapid fire effect - more yellow
    if (hasRapidFire()) {
        playerColor.r = 255;
        playerColor.g = 235;
        playerColor.b = static_cast<sf::Uint8>(59 + 50 * std::sin(m_rapidFireTimer * 8));
    }
    
    m_shape.setFillColor(playerColor);
    
    // Shield pulse
    if (hasShield()) {
        float pulse = std::sin(m_shieldTimer * 6) * 0.15f + 1.0f;
        m_shieldShape.setScale(pulse, pulse);
    }
}

void Player::updatePowerUpTimers(float deltaTime) {
    // Speed boost
    if (m_speedBoostTimer > 0.0f) {
        m_speedBoostTimer -= deltaTime;
        m_speedMultiplier = 1.5f;
    } else {
        m_speedMultiplier = 1.0f;
    }
    
    // Rapid fire
    if (m_rapidFireTimer > 0.0f) {
        m_rapidFireTimer -= deltaTime;
        m_fireRateMultiplier = 3.0f;
    } else {
        m_fireRateMultiplier = 1.0f;
    }
    
    // Shield
    if (m_shieldTimer > 0.0f) {
        m_shieldTimer -= deltaTime;
    }
}

void Player::applyMovement(float deltaTime) {
    float currentSpeed = Config::PLAYER_SPEED * m_speedMultiplier;
    float currentAccel = Config::PLAYER_ACCELERATION * m_speedMultiplier;
    
    if (Math::magnitude(m_inputDirection) > 0.1f) {
        sf::Vector2f targetVelocity = m_inputDirection * currentSpeed;
        m_velocity.x = Math::moveTowards(m_velocity.x, targetVelocity.x, currentAccel * deltaTime);
        m_velocity.y = Math::moveTowards(m_velocity.y, targetVelocity.y, currentAccel * deltaTime);
    } else {
        m_velocity.x = Math::moveTowards(m_velocity.x, 0.0f, Config::PLAYER_FRICTION * deltaTime);
        m_velocity.y = Math::moveTowards(m_velocity.y, 0.0f, Config::PLAYER_FRICTION * deltaTime);
    }
    
    m_position += m_velocity * deltaTime;
}

void Player::clampToScreen() {
    float halfWidth = m_size.x / 2.0f;
    float halfHeight = m_size.y / 2.0f;
    
    m_position.x = Math::clamp(m_position.x, halfWidth, Config::WINDOW_WIDTH - halfWidth);
    m_position.y = Math::clamp(m_position.y, halfHeight, Config::WINDOW_HEIGHT - halfHeight);
}

void Player::shoot(std::vector<std::unique_ptr<Projectile>>& projectiles) {
    if (m_fireTimer > 0.0f) return;
    if (!sf::Keyboard::isKeyPressed(sf::Keyboard::Space)) return;
    
    m_fireTimer = Config::PLAYER_FIRE_RATE / m_fireRateMultiplier;
    
    // Find inactive projectile or create new one
    Projectile* bullet = nullptr;
    for (auto& proj : projectiles) {
        if (!proj->isActive()) {
            bullet = proj.get();
            break;
        }
    }
    
    if (!bullet && projectiles.size() < Config::MAX_PROJECTILES) {
        projectiles.push_back(std::make_unique<Projectile>());
        bullet = projectiles.back().get();
    }
    
    if (bullet) {
        sf::Vector2f direction(0.0f, -1.0f);  // Default: shoot up
        
        if (Math::magnitude(m_inputDirection) > 0.1f) {
            direction = Math::normalize(m_inputDirection);
        }
        
        bullet->fire(m_position, direction);
    }
}

void Player::render(sf::RenderWindow& window) {
    // Draw shield behind player
    if (hasShield()) {
        window.draw(m_shieldShape);
    }
    
    window.draw(m_shape);
}

void Player::makeInvulnerable(float duration) {
    m_invulnerabilityTimer = duration;
}

void Player::addScore(int points) {
    int actualPoints = static_cast<int>(points * m_comboMultiplier);
    m_score += actualPoints;
    
    m_comboTimer = Config::COMBO_TIMEOUT;
    m_comboMultiplier = std::min(m_comboMultiplier + Config::COMBO_MULTIPLIER_INCREMENT, 
                                 Config::MAX_COMBO_MULTIPLIER);
}

void Player::resetCombo() {
    m_comboTimer = 0.0f;
    m_comboMultiplier = 1.0f;
}

void Player::applyPowerUp(const PowerUp& powerUp) {
    switch (powerUp.getType()) {
        case PowerUpType::Health:
            m_health = std::min(m_health + powerUp.getValue(), m_maxHealth);
            break;
            
        case PowerUpType::SpeedBoost:
            m_speedBoostTimer = powerUp.getDuration();
            break;
            
        case PowerUpType::RapidFire:
            m_rapidFireTimer = powerUp.getDuration();
            break;
            
        case PowerUpType::Shield:
            m_shieldTimer = powerUp.getDuration();
            break;
            
        case PowerUpType::ScoreBonus:
            m_score += powerUp.getValue();
            break;
    }
}

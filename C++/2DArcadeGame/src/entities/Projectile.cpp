#include "Projectile.h"
#include "core/Config.h"

Projectile::Projectile()
    : m_lifetime(0.0f)
    , m_maxLifetime(Config::PROJECTILE_LIFETIME)
    , m_damage(10)
{
    m_size = sf::Vector2f(Config::PROJECTILE_SIZE, Config::PROJECTILE_SIZE);
    m_active = false;
    
    m_shape.setSize(m_size);
    m_shape.setOrigin(m_size.x / 2.0f, m_size.y / 2.0f);
    
    sf::Color projColor(
        (Config::Colors::PROJECTILE >> 24) & 0xFF,
        (Config::Colors::PROJECTILE >> 16) & 0xFF,
        (Config::Colors::PROJECTILE >> 8) & 0xFF,
        Config::Colors::PROJECTILE & 0xFF
    );
    m_shape.setFillColor(projColor);
}

void Projectile::fire(const sf::Vector2f& position, const sf::Vector2f& direction) {
    m_position = position;
    m_velocity = Math::normalize(direction) * Config::PROJECTILE_SPEED;
    m_lifetime = m_maxLifetime;
    m_active = true;
}

void Projectile::update(float deltaTime) {
    if (!m_active) return;
    
    m_position += m_velocity * deltaTime;
    m_lifetime -= deltaTime;
    
    // Deactivate if lifetime expired or off-screen
    if (m_lifetime <= 0.0f ||
        m_position.x < -50 || m_position.x > Config::WINDOW_WIDTH + 50 ||
        m_position.y < -50 || m_position.y > Config::WINDOW_HEIGHT + 50) {
        m_active = false;
    }
    
    m_shape.setPosition(m_position);
}

void Projectile::render(sf::RenderWindow& window) {
    if (!m_active) return;
    window.draw(m_shape);
}

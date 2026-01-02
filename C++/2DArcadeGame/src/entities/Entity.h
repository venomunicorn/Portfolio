#pragma once

#include <SFML/Graphics.hpp>
#include "utils/Math.h"

// Base class for all game entities
class Entity {
public:
    Entity();
    virtual ~Entity() = default;
    
    virtual void update(float deltaTime) = 0;
    virtual void render(sf::RenderWindow& window) = 0;
    
    // Position and movement
    sf::Vector2f getPosition() const { return m_position; }
    void setPosition(const sf::Vector2f& pos) { m_position = pos; }
    void setPosition(float x, float y) { m_position = sf::Vector2f(x, y); }
    
    sf::Vector2f getVelocity() const { return m_velocity; }
    void setVelocity(const sf::Vector2f& vel) { m_velocity = vel; }
    
    // Size and collision
    sf::Vector2f getSize() const { return m_size; }
    void setSize(const sf::Vector2f& size) { m_size = size; }
    void setSize(float w, float h) { m_size = sf::Vector2f(w, h); }
    
    Math::AABB getBounds() const;
    
    // State
    bool isActive() const { return m_active; }
    void setActive(bool active) { m_active = active; }
    
    // Health
    int getHealth() const { return m_health; }
    void setHealth(int health) { m_health = health; }
    void takeDamage(int damage);
    bool isDead() const { return m_health <= 0; }
    
protected:
    sf::Vector2f m_position;
    sf::Vector2f m_velocity;
    sf::Vector2f m_size;
    bool m_active;
    int m_health;
    int m_maxHealth;
};

#pragma once

#include "Entity.h"

class Projectile : public Entity {
public:
    Projectile();
    
    void update(float deltaTime) override;
    void render(sf::RenderWindow& window) override;
    
    void fire(const sf::Vector2f& position, const sf::Vector2f& direction);
    
    int getDamage() const { return m_damage; }
    
private:
    sf::RectangleShape m_shape;
    float m_lifetime;
    float m_maxLifetime;
    int m_damage;
};

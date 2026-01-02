#pragma once

#include <SFML/Graphics.hpp>
#include <vector>

struct Particle {
    sf::Vector2f position;
    sf::Vector2f velocity;
    sf::Color color;
    float lifetime;
    float maxLifetime;
    float size;
    float rotation;
    float rotationSpeed;
    bool active;
};

class ParticleSystem {
public:
    ParticleSystem(size_t maxParticles = 500);
    
    void update(float deltaTime);
    void render(sf::RenderWindow& window);
    
    // Emit particle effects
    void emitExplosion(const sf::Vector2f& position, const sf::Color& color, int count = 20);
    void emitHit(const sf::Vector2f& position, const sf::Color& color, int count = 8);
    void emitPickup(const sf::Vector2f& position, const sf::Color& color, int count = 12);
    void emitDeath(const sf::Vector2f& position, int count = 30);
    void emitTrail(const sf::Vector2f& position, const sf::Color& color);
    
    void clear();
    int getActiveCount() const;
    
private:
    Particle* getInactiveParticle();
    void emitParticle(const sf::Vector2f& position, const sf::Vector2f& velocity,
                      const sf::Color& color, float lifetime, float size, float rotationSpeed = 0.0f);
    
    std::vector<Particle> m_particles;
    sf::RectangleShape m_shape;
};

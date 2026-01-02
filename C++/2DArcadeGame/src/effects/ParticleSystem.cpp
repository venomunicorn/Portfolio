#include "ParticleSystem.h"
#include "utils/Math.h"
#include <cmath>

ParticleSystem::ParticleSystem(size_t maxParticles)
    : m_particles(maxParticles)
{
    for (auto& p : m_particles) {
        p.active = false;
    }
    
    m_shape.setSize(sf::Vector2f(4.0f, 4.0f));
    m_shape.setOrigin(2.0f, 2.0f);
}

void ParticleSystem::update(float deltaTime) {
    for (auto& p : m_particles) {
        if (!p.active) continue;
        
        p.lifetime -= deltaTime;
        if (p.lifetime <= 0.0f) {
            p.active = false;
            continue;
        }
        
        // Physics
        p.position += p.velocity * deltaTime;
        p.velocity *= 0.98f;  // Drag
        p.velocity.y += 50.0f * deltaTime;  // Slight gravity
        p.rotation += p.rotationSpeed * deltaTime;
        
        // Fade out
        float t = p.lifetime / p.maxLifetime;
        p.color.a = static_cast<sf::Uint8>(255 * t);
    }
}

void ParticleSystem::render(sf::RenderWindow& window) {
    for (auto& p : m_particles) {
        if (!p.active) continue;
        
        m_shape.setPosition(p.position);
        m_shape.setSize(sf::Vector2f(p.size, p.size));
        m_shape.setOrigin(p.size / 2.0f, p.size / 2.0f);
        m_shape.setRotation(p.rotation);
        m_shape.setFillColor(p.color);
        window.draw(m_shape);
    }
}

Particle* ParticleSystem::getInactiveParticle() {
    for (auto& p : m_particles) {
        if (!p.active) return &p;
    }
    return nullptr;
}

void ParticleSystem::emitParticle(const sf::Vector2f& position, const sf::Vector2f& velocity,
                                   const sf::Color& color, float lifetime, float size, float rotationSpeed) {
    Particle* p = getInactiveParticle();
    if (!p) return;
    
    p->position = position;
    p->velocity = velocity;
    p->color = color;
    p->lifetime = lifetime;
    p->maxLifetime = lifetime;
    p->size = size;
    p->rotation = Math::randomFloat(0.0f, 360.0f);
    p->rotationSpeed = rotationSpeed;
    p->active = true;
}

void ParticleSystem::emitExplosion(const sf::Vector2f& position, const sf::Color& color, int count) {
    for (int i = 0; i < count; ++i) {
        float angle = Math::randomFloat(0.0f, 360.0f) * 3.14159f / 180.0f;
        float speed = Math::randomFloat(100.0f, 300.0f);
        sf::Vector2f velocity(std::cos(angle) * speed, std::sin(angle) * speed);
        
        sf::Color particleColor = color;
        particleColor.r = static_cast<sf::Uint8>(Math::clamp(color.r + Math::randomInt(-30, 30), 0, 255));
        particleColor.g = static_cast<sf::Uint8>(Math::clamp(color.g + Math::randomInt(-30, 30), 0, 255));
        particleColor.b = static_cast<sf::Uint8>(Math::clamp(color.b + Math::randomInt(-30, 30), 0, 255));
        
        float size = Math::randomFloat(3.0f, 8.0f);
        float lifetime = Math::randomFloat(0.3f, 0.6f);
        float rotation = Math::randomFloat(-300.0f, 300.0f);
        
        emitParticle(position, velocity, particleColor, lifetime, size, rotation);
    }
}

void ParticleSystem::emitHit(const sf::Vector2f& position, const sf::Color& color, int count) {
    for (int i = 0; i < count; ++i) {
        float angle = Math::randomFloat(0.0f, 360.0f) * 3.14159f / 180.0f;
        float speed = Math::randomFloat(80.0f, 180.0f);
        sf::Vector2f velocity(std::cos(angle) * speed, std::sin(angle) * speed);
        
        float size = Math::randomFloat(2.0f, 5.0f);
        float lifetime = Math::randomFloat(0.15f, 0.3f);
        
        emitParticle(position, velocity, color, lifetime, size, Math::randomFloat(-200.0f, 200.0f));
    }
}

void ParticleSystem::emitPickup(const sf::Vector2f& position, const sf::Color& color, int count) {
    for (int i = 0; i < count; ++i) {
        float angle = (360.0f / count) * i * 3.14159f / 180.0f;
        float speed = Math::randomFloat(50.0f, 120.0f);
        sf::Vector2f velocity(std::cos(angle) * speed, std::sin(angle) * speed - 80.0f);  // Upward bias
        
        float size = Math::randomFloat(3.0f, 6.0f);
        float lifetime = Math::randomFloat(0.4f, 0.7f);
        
        emitParticle(position, velocity, color, lifetime, size, 0.0f);
    }
}

void ParticleSystem::emitDeath(const sf::Vector2f& position, int count) {
    // Multi-color death explosion
    std::vector<sf::Color> colors = {
        sf::Color(255, 100, 100),
        sf::Color(255, 200, 100),
        sf::Color(255, 255, 100)
    };
    
    for (int i = 0; i < count; ++i) {
        float angle = Math::randomFloat(0.0f, 360.0f) * 3.14159f / 180.0f;
        float speed = Math::randomFloat(150.0f, 400.0f);
        sf::Vector2f velocity(std::cos(angle) * speed, std::sin(angle) * speed);
        
        sf::Color color = colors[Math::randomInt(0, colors.size() - 1)];
        float size = Math::randomFloat(4.0f, 10.0f);
        float lifetime = Math::randomFloat(0.4f, 0.8f);
        
        emitParticle(position, velocity, color, lifetime, size, Math::randomFloat(-400.0f, 400.0f));
    }
}

void ParticleSystem::emitTrail(const sf::Vector2f& position, const sf::Color& color) {
    sf::Vector2f velocity(Math::randomFloat(-20.0f, 20.0f), Math::randomFloat(-20.0f, 20.0f));
    float size = Math::randomFloat(2.0f, 4.0f);
    float lifetime = Math::randomFloat(0.1f, 0.2f);
    
    emitParticle(position, velocity, color, lifetime, size, 0.0f);
}

void ParticleSystem::clear() {
    for (auto& p : m_particles) {
        p.active = false;
    }
}

int ParticleSystem::getActiveCount() const {
    int count = 0;
    for (const auto& p : m_particles) {
        if (p.active) count++;
    }
    return count;
}

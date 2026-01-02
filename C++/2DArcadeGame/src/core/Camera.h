#pragma once

#include <SFML/Graphics.hpp>

class Camera {
public:
    Camera();
    
    void update(float deltaTime);
    void apply(sf::RenderWindow& window);
    void reset(sf::RenderWindow& window);
    
    // Screen shake
    void shake(float intensity, float duration);
    
    // Camera follow (for future use)
    void setTarget(const sf::Vector2f& target) { m_target = target; }
    void setPosition(const sf::Vector2f& position) { m_position = position; }
    
    sf::Vector2f getPosition() const { return m_position; }
    bool isShaking() const { return m_shakeTimer > 0.0f; }
    
private:
    sf::View m_view;
    sf::Vector2f m_position;
    sf::Vector2f m_target;
    sf::Vector2f m_shakeOffset;
    
    float m_shakeIntensity;
    float m_shakeDuration;
    float m_shakeTimer;
};

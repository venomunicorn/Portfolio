#include "Camera.h"
#include "Config.h"
#include "utils/Math.h"
#include <cmath>

Camera::Camera()
    : m_position(Config::WINDOW_WIDTH / 2.0f, Config::WINDOW_HEIGHT / 2.0f)
    , m_target(m_position)
    , m_shakeOffset(0.0f, 0.0f)
    , m_shakeIntensity(0.0f)
    , m_shakeDuration(0.0f)
    , m_shakeTimer(0.0f)
{
    m_view.setSize(static_cast<float>(Config::WINDOW_WIDTH), 
                   static_cast<float>(Config::WINDOW_HEIGHT));
    m_view.setCenter(m_position);
}

void Camera::update(float deltaTime) {
    // Update screen shake
    if (m_shakeTimer > 0.0f) {
        m_shakeTimer -= deltaTime;
        
        // Decrease intensity over time
        float t = m_shakeTimer / m_shakeDuration;
        float currentIntensity = m_shakeIntensity * t;
        
        // Random shake offset
        m_shakeOffset.x = Math::randomFloat(-currentIntensity, currentIntensity);
        m_shakeOffset.y = Math::randomFloat(-currentIntensity, currentIntensity);
        
        if (m_shakeTimer <= 0.0f) {
            m_shakeOffset = sf::Vector2f(0.0f, 0.0f);
        }
    }
    
    // Apply position + shake
    sf::Vector2f finalPosition = m_position + m_shakeOffset;
    m_view.setCenter(finalPosition);
}

void Camera::apply(sf::RenderWindow& window) {
    window.setView(m_view);
}

void Camera::reset(sf::RenderWindow& window) {
    sf::View defaultView(sf::FloatRect(0, 0, 
        static_cast<float>(Config::WINDOW_WIDTH), 
        static_cast<float>(Config::WINDOW_HEIGHT)));
    window.setView(defaultView);
}

void Camera::shake(float intensity, float duration) {
    // Stack shakes if called multiple times
    if (intensity > m_shakeIntensity * (m_shakeTimer / m_shakeDuration)) {
        m_shakeIntensity = intensity;
        m_shakeDuration = duration;
        m_shakeTimer = duration;
    }
}

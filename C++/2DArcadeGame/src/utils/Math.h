#pragma once

// ============================================
// Math Utilities
// ============================================

#include <SFML/System/Vector2.hpp>
#include <cmath>

namespace Math {

// Vector magnitude
inline float magnitude(const sf::Vector2f& v) {
    return std::sqrt(v.x * v.x + v.y * v.y);
}

// Normalize vector
inline sf::Vector2f normalize(const sf::Vector2f& v) {
    float mag = magnitude(v);
    if (mag > 0.0001f) {
        return sf::Vector2f(v.x / mag, v.y / mag);
    }
    return sf::Vector2f(0.0f, 0.0f);
}

// Distance between two points
inline float distance(const sf::Vector2f& a, const sf::Vector2f& b) {
    return magnitude(b - a);
}

// Dot product
inline float dot(const sf::Vector2f& a, const sf::Vector2f& b) {
    return a.x * b.x + a.y * b.y;
}

// Lerp
inline float lerp(float a, float b, float t) {
    return a + (b - a) * t;
}

inline sf::Vector2f lerp(const sf::Vector2f& a, const sf::Vector2f& b, float t) {
    return sf::Vector2f(lerp(a.x, b.x, t), lerp(a.y, b.y, t));
}

// Clamp
inline float clamp(float value, float min, float max) {
    if (value < min) return min;
    if (value > max) return max;
    return value;
}

// Move towards with max delta
inline float moveTowards(float current, float target, float maxDelta) {
    if (std::abs(target - current) <= maxDelta) {
        return target;
    }
    return current + (target > current ? maxDelta : -maxDelta);
}

// AABB collision check
struct AABB {
    float x, y, width, height;
    
    bool intersects(const AABB& other) const {
        return x < other.x + other.width &&
               x + width > other.x &&
               y < other.y + other.height &&
               y + height > other.y;
    }
    
    sf::Vector2f center() const {
        return sf::Vector2f(x + width / 2.0f, y + height / 2.0f);
    }
};

// Circle collision check
struct Circle {
    float x, y, radius;
    
    bool intersects(const Circle& other) const {
        float dx = other.x - x;
        float dy = other.y - y;
        float distSquared = dx * dx + dy * dy;
        float radiusSum = radius + other.radius;
        return distSquared < radiusSum * radiusSum;
    }
    
    sf::Vector2f center() const {
        return sf::Vector2f(x, y);
    }
};

// Random float in range
inline float randomFloat(float min, float max) {
    return min + static_cast<float>(rand()) / (static_cast<float>(RAND_MAX / (max - min)));
}

// Random int in range
inline int randomInt(int min, int max) {
    return min + rand() % (max - min + 1);
}

} // namespace Math

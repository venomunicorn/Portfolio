#include "Entity.h"

Entity::Entity()
    : m_position(0.0f, 0.0f)
    , m_velocity(0.0f, 0.0f)
    , m_size(32.0f, 32.0f)
    , m_active(true)
    , m_health(100)
    , m_maxHealth(100)
{
}

Math::AABB Entity::getBounds() const {
    return Math::AABB{
        m_position.x - m_size.x / 2.0f,
        m_position.y - m_size.y / 2.0f,
        m_size.x,
        m_size.y
    };
}

void Entity::takeDamage(int damage) {
    m_health -= damage;
    if (m_health < 0) {
        m_health = 0;
    }
}

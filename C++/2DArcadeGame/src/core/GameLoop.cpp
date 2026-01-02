#include "GameLoop.h"
#include <algorithm>

GameLoop::GameLoop(float fixedTimeStep)
    : m_fixedTimeStep(fixedTimeStep)
    , m_accumulator(0.0f)
    , m_deltaTime(0.0f)
{
}

void GameLoop::start() {
    m_clock.restart();
    m_accumulator = 0.0f;
}

int GameLoop::accumulateAndGetUpdateCount(float maxUpdates) {
    m_deltaTime = m_clock.restart().asSeconds();
    
    // Clamp delta to prevent spiral of death
    m_deltaTime = std::min(m_deltaTime, m_fixedTimeStep * maxUpdates);
    
    m_accumulator += m_deltaTime;
    
    int updateCount = 0;
    while (m_accumulator >= m_fixedTimeStep) {
        m_accumulator -= m_fixedTimeStep;
        updateCount++;
        
        // Safety cap
        if (updateCount >= static_cast<int>(maxUpdates)) {
            m_accumulator = 0.0f;
            break;
        }
    }
    
    return updateCount;
}

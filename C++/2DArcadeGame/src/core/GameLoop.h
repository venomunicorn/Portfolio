#pragma once

#include <SFML/System/Clock.hpp>

// Fixed timestep game loop helper
class GameLoop {
public:
    GameLoop(float fixedTimeStep = 1.0f / 60.0f);
    
    void start();
    
    // Returns how many fixed updates should occur
    int accumulateAndGetUpdateCount(float maxUpdates = 5);
    
    float getFixedTimeStep() const { return m_fixedTimeStep; }
    float getInterpolation() const { return m_accumulator / m_fixedTimeStep; }
    float getDeltaTime() const { return m_deltaTime; }
    float getFPS() const { return 1.0f / m_deltaTime; }
    
private:
    sf::Clock m_clock;
    float m_fixedTimeStep;
    float m_accumulator;
    float m_deltaTime;
};

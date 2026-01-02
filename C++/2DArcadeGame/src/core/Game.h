#pragma once

#include <SFML/Graphics.hpp>
#include <memory>
#include <stack>
#include "states/GameState.h"

class Game {
public:
    Game();
    ~Game();
    
    void run();
    
    // State management
    void pushState(std::unique_ptr<GameState> state);
    void popState();
    void changeState(std::unique_ptr<GameState> state);
    
    // Accessors
    sf::RenderWindow& getWindow() { return m_window; }
    bool isRunning() const { return m_running; }
    
private:
    void processEvents();
    void update(float deltaTime);
    void render();
    
    sf::RenderWindow m_window;
    std::stack<std::unique_ptr<GameState>> m_states;
    sf::Clock m_clock;
    bool m_running;
    
    // Fixed timestep accumulator
    float m_accumulator;
};

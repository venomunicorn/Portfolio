#pragma once

#include <SFML/Graphics.hpp>

class Game;

// Abstract base class for game states
class GameState {
public:
    explicit GameState(Game& game) : m_game(game) {}
    virtual ~GameState() = default;
    
    virtual void init() = 0;
    virtual void handleEvent(const sf::Event& event) = 0;
    virtual void update(float deltaTime) = 0;
    virtual void render(sf::RenderWindow& window) = 0;
    
    virtual void pause() {}
    virtual void resume() {}
    
protected:
    Game& m_game;
};

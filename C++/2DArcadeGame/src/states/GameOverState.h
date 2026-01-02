#pragma once

#include "GameState.h"
#include <SFML/Graphics.hpp>

class GameOverState : public GameState {
public:
    GameOverState(Game& game, int finalScore, int waveReached);
    
    void init() override;
    void handleEvent(const sf::Event& event) override;
    void update(float deltaTime) override;
    void render(sf::RenderWindow& window) override;
    
private:
    sf::Font m_font;
    sf::Text m_gameOverText;
    sf::Text m_scoreText;
    sf::Text m_waveText;
    sf::Text m_restartText;
    sf::Text m_menuText;
    
    int m_finalScore;
    int m_waveReached;
    
    float m_blinkTimer;
    bool m_showRestartText;
};

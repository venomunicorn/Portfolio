#pragma once

#include "GameState.h"
#include <SFML/Graphics.hpp>

class TitleState : public GameState {
public:
    explicit TitleState(Game& game);
    
    void init() override;
    void handleEvent(const sf::Event& event) override;
    void update(float deltaTime) override;
    void render(sf::RenderWindow& window) override;
    
private:
    sf::Font m_font;
    sf::Text m_titleText;
    sf::Text m_startText;
    sf::Text m_controlsText;
    
    float m_blinkTimer;
    bool m_showStartText;
};

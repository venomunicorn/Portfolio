#pragma once

#include "GameState.h"
#include "save/SaveManager.h"
#include <SFML/Graphics.hpp>

class HighScoreState : public GameState {
public:
    HighScoreState(Game& game, int playerScore = -1, int waveReached = 0);
    
    void init() override;
    void handleEvent(const sf::Event& event) override;
    void update(float deltaTime) override;
    void render(sf::RenderWindow& window) override;
    
private:
    sf::Font m_font;
    sf::Text m_titleText;
    sf::Text m_backText;
    std::vector<sf::Text> m_scoreTexts;
    
    // Name entry for new high score
    bool m_enteringName;
    std::string m_playerName;
    sf::Text m_namePromptText;
    sf::Text m_nameInputText;
    sf::RectangleShape m_cursor;
    float m_cursorBlinkTimer;
    
    int m_playerScore;
    int m_waveReached;
};

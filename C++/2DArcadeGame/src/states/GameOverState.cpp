#include "GameOverState.h"
#include "TitleState.h"
#include "PlayingState.h"
#include "HighScoreState.h"
#include "core/Game.h"
#include "core/Config.h"
#include "audio/AudioManager.h"
#include "save/SaveManager.h"
#include <sstream>
#include <iomanip>

GameOverState::GameOverState(Game& game, int finalScore, int waveReached)
    : GameState(game)
    , m_finalScore(finalScore)
    , m_waveReached(waveReached)
    , m_blinkTimer(0.0f)
    , m_showRestartText(true)
{
}

void GameOverState::init() {
    // Play death sound
    AudioManager::getInstance().playSound("death");
    
    // Load font
    if (!m_font.loadFromFile("assets/fonts/arcade.ttf")) {
        m_font.loadFromFile("C:/Windows/Fonts/arial.ttf");
    }
    
    // Game Over text
    m_gameOverText.setFont(m_font);
    m_gameOverText.setString("GAME OVER");
    m_gameOverText.setCharacterSize(72);
    m_gameOverText.setFillColor(sf::Color::Red);
    m_gameOverText.setStyle(sf::Text::Bold);
    
    sf::FloatRect goBounds = m_gameOverText.getLocalBounds();
    m_gameOverText.setOrigin(goBounds.width / 2.0f, goBounds.height / 2.0f);
    m_gameOverText.setPosition(Config::WINDOW_WIDTH / 2.0f, Config::WINDOW_HEIGHT * 0.2f);
    
    // Score text
    std::stringstream ss;
    ss << "FINAL SCORE: " << std::setw(8) << std::setfill('0') << m_finalScore;
    m_scoreText.setFont(m_font);
    m_scoreText.setString(ss.str());
    m_scoreText.setCharacterSize(36);
    m_scoreText.setFillColor(sf::Color::White);
    
    sf::FloatRect scoreBounds = m_scoreText.getLocalBounds();
    m_scoreText.setOrigin(scoreBounds.width / 2.0f, scoreBounds.height / 2.0f);
    m_scoreText.setPosition(Config::WINDOW_WIDTH / 2.0f, Config::WINDOW_HEIGHT * 0.35f);
    
    // Wave text
    std::stringstream ws;
    ws << "WAVE REACHED: " << m_waveReached;
    m_waveText.setFont(m_font);
    m_waveText.setString(ws.str());
    m_waveText.setCharacterSize(28);
    m_waveText.setFillColor(sf::Color(180, 180, 180));
    
    sf::FloatRect waveBounds = m_waveText.getLocalBounds();
    m_waveText.setOrigin(waveBounds.width / 2.0f, waveBounds.height / 2.0f);
    m_waveText.setPosition(Config::WINDOW_WIDTH / 2.0f, Config::WINDOW_HEIGHT * 0.45f);
    
    // High score indicator
    if (SaveManager::getInstance().isHighScore(m_finalScore)) {
        m_scoreText.setFillColor(sf::Color::Yellow);
        m_scoreText.setString(ss.str() + " - NEW HIGH SCORE!");
        sf::FloatRect newBounds = m_scoreText.getLocalBounds();
        m_scoreText.setOrigin(newBounds.width / 2.0f, newBounds.height / 2.0f);
    }
    
    // Restart text
    m_restartText.setFont(m_font);
    m_restartText.setString("PRESS R TO RESTART");
    m_restartText.setCharacterSize(32);
    m_restartText.setFillColor(sf::Color::Yellow);
    
    sf::FloatRect restartBounds = m_restartText.getLocalBounds();
    m_restartText.setOrigin(restartBounds.width / 2.0f, restartBounds.height / 2.0f);
    m_restartText.setPosition(Config::WINDOW_WIDTH / 2.0f, Config::WINDOW_HEIGHT * 0.6f);
    
    // Menu text
    m_menuText.setFont(m_font);
    m_menuText.setString("ESC - MENU    H - HIGH SCORES");
    m_menuText.setCharacterSize(20);
    m_menuText.setFillColor(sf::Color(150, 150, 150));
    
    sf::FloatRect menuBounds = m_menuText.getLocalBounds();
    m_menuText.setOrigin(menuBounds.width / 2.0f, menuBounds.height / 2.0f);
    m_menuText.setPosition(Config::WINDOW_WIDTH / 2.0f, Config::WINDOW_HEIGHT * 0.75f);
}

void GameOverState::handleEvent(const sf::Event& event) {
    if (event.type == sf::Event::KeyPressed) {
        if (event.key.code == sf::Keyboard::R) {
            AudioManager::getInstance().playSound("select");
            m_game.changeState(std::make_unique<PlayingState>(m_game));
        }
        if (event.key.code == sf::Keyboard::Escape) {
            AudioManager::getInstance().playSound("select");
            m_game.changeState(std::make_unique<TitleState>(m_game));
        }
        if (event.key.code == sf::Keyboard::H) {
            AudioManager::getInstance().playSound("select");
            m_game.changeState(std::make_unique<HighScoreState>(m_game, m_finalScore, m_waveReached));
        }
    }
}

void GameOverState::update(float deltaTime) {
    // Blink restart text
    m_blinkTimer += deltaTime;
    if (m_blinkTimer >= 0.5f) {
        m_blinkTimer = 0.0f;
        m_showRestartText = !m_showRestartText;
    }
}

void GameOverState::render(sf::RenderWindow& window) {
    window.draw(m_gameOverText);
    window.draw(m_scoreText);
    window.draw(m_waveText);
    
    if (m_showRestartText) {
        window.draw(m_restartText);
    }
    
    window.draw(m_menuText);
}

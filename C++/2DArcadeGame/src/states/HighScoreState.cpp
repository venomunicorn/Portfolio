#include "HighScoreState.h"
#include "TitleState.h"
#include "core/Game.h"
#include "core/Config.h"
#include "audio/AudioManager.h"
#include <sstream>
#include <iomanip>

HighScoreState::HighScoreState(Game& game, int playerScore, int waveReached)
    : GameState(game)
    , m_enteringName(false)
    , m_playerName("")
    , m_cursorBlinkTimer(0.0f)
    , m_playerScore(playerScore)
    , m_waveReached(waveReached)
{
}

void HighScoreState::init() {
    if (!m_font.loadFromFile("assets/fonts/arcade.ttf")) {
        m_font.loadFromFile("C:/Windows/Fonts/arial.ttf");
    }
    
    // Check if player achieved a high score
    if (m_playerScore > 0 && SaveManager::getInstance().isHighScore(m_playerScore)) {
        m_enteringName = true;
    }
    
    // Title
    m_titleText.setFont(m_font);
    m_titleText.setString("HIGH SCORES");
    m_titleText.setCharacterSize(48);
    m_titleText.setFillColor(sf::Color::Yellow);
    
    sf::FloatRect titleBounds = m_titleText.getLocalBounds();
    m_titleText.setOrigin(titleBounds.width / 2.0f, titleBounds.height / 2.0f);
    m_titleText.setPosition(Config::WINDOW_WIDTH / 2.0f, 60.0f);
    
    // Name entry prompt
    m_namePromptText.setFont(m_font);
    m_namePromptText.setString("NEW HIGH SCORE! ENTER YOUR NAME:");
    m_namePromptText.setCharacterSize(24);
    m_namePromptText.setFillColor(sf::Color::White);
    
    sf::FloatRect promptBounds = m_namePromptText.getLocalBounds();
    m_namePromptText.setOrigin(promptBounds.width / 2.0f, promptBounds.height / 2.0f);
    m_namePromptText.setPosition(Config::WINDOW_WIDTH / 2.0f, 120.0f);
    
    // Name input
    m_nameInputText.setFont(m_font);
    m_nameInputText.setCharacterSize(36);
    m_nameInputText.setFillColor(sf::Color::Cyan);
    m_nameInputText.setPosition(Config::WINDOW_WIDTH / 2.0f - 100.0f, 160.0f);
    
    // Cursor
    m_cursor.setSize(sf::Vector2f(20.0f, 36.0f));
    m_cursor.setFillColor(sf::Color::White);
    
    // Back text
    m_backText.setFont(m_font);
    m_backText.setString("PRESS ESC TO RETURN");
    m_backText.setCharacterSize(20);
    m_backText.setFillColor(sf::Color(150, 150, 150));
    
    sf::FloatRect backBounds = m_backText.getLocalBounds();
    m_backText.setOrigin(backBounds.width / 2.0f, backBounds.height / 2.0f);
    m_backText.setPosition(Config::WINDOW_WIDTH / 2.0f, Config::WINDOW_HEIGHT - 50.0f);
    
    // Load and display high scores
    const auto& scores = SaveManager::getInstance().getHighScores();
    float yPos = m_enteringName ? 220.0f : 140.0f;
    
    for (size_t i = 0; i < 10; ++i) {
        sf::Text scoreText;
        scoreText.setFont(m_font);
        scoreText.setCharacterSize(24);
        
        std::stringstream ss;
        ss << std::setw(2) << (i + 1) << ". ";
        
        if (i < scores.size()) {
            ss << std::setw(10) << std::left << scores[i].name << " "
               << std::setw(8) << std::right << std::setfill('0') << scores[i].score
               << "  WAVE " << scores[i].waveReached;
            scoreText.setFillColor(sf::Color::White);
        } else {
            ss << "----------   --------";
            scoreText.setFillColor(sf::Color(100, 100, 100));
        }
        
        scoreText.setString(ss.str());
        scoreText.setPosition(Config::WINDOW_WIDTH / 2.0f - 200.0f, yPos + i * 40.0f);
        m_scoreTexts.push_back(scoreText);
    }
}

void HighScoreState::handleEvent(const sf::Event& event) {
    if (event.type == sf::Event::KeyPressed) {
        if (event.key.code == sf::Keyboard::Escape) {
            if (m_enteringName && !m_playerName.empty()) {
                // Save the score first
                SaveManager::getInstance().addHighScore(m_playerName, m_playerScore, m_waveReached);
            }
            AudioManager::getInstance().playSound("select");
            m_game.changeState(std::make_unique<TitleState>(m_game));
        }
        
        if (m_enteringName) {
            if (event.key.code == sf::Keyboard::Return && !m_playerName.empty()) {
                SaveManager::getInstance().addHighScore(m_playerName, m_playerScore, m_waveReached);
                AudioManager::getInstance().playSound("powerup");
                m_enteringName = false;
                
                // Refresh score display
                m_scoreTexts.clear();
                const auto& scores = SaveManager::getInstance().getHighScores();
                float yPos = 140.0f;
                
                for (size_t i = 0; i < 10; ++i) {
                    sf::Text scoreText;
                    scoreText.setFont(m_font);
                    scoreText.setCharacterSize(24);
                    
                    std::stringstream ss;
                    ss << std::setw(2) << (i + 1) << ". ";
                    
                    if (i < scores.size()) {
                        ss << std::setw(10) << std::left << scores[i].name << " "
                           << std::setw(8) << std::right << std::setfill('0') << scores[i].score
                           << "  WAVE " << scores[i].waveReached;
                        // Highlight the new score
                        if (scores[i].name == m_playerName && scores[i].score == m_playerScore) {
                            scoreText.setFillColor(sf::Color::Yellow);
                        } else {
                            scoreText.setFillColor(sf::Color::White);
                        }
                    } else {
                        ss << "----------   --------";
                        scoreText.setFillColor(sf::Color(100, 100, 100));
                    }
                    
                    scoreText.setString(ss.str());
                    scoreText.setPosition(Config::WINDOW_WIDTH / 2.0f - 200.0f, yPos + i * 40.0f);
                    m_scoreTexts.push_back(scoreText);
                }
            }
            else if (event.key.code == sf::Keyboard::BackSpace && !m_playerName.empty()) {
                m_playerName.pop_back();
                AudioManager::getInstance().playSound("select", 50.0f);
            }
        }
    }
    
    // Text input for name entry
    if (m_enteringName && event.type == sf::Event::TextEntered) {
        if (event.text.unicode >= 32 && event.text.unicode < 127 && m_playerName.size() < 10) {
            char c = static_cast<char>(event.text.unicode);
            if ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9')) {
                m_playerName += static_cast<char>(std::toupper(c));
                AudioManager::getInstance().playSound("select", 50.0f);
            }
        }
    }
}

void HighScoreState::update(float deltaTime) {
    m_cursorBlinkTimer += deltaTime;
    if (m_cursorBlinkTimer >= 1.0f) {
        m_cursorBlinkTimer = 0.0f;
    }
    
    m_nameInputText.setString(m_playerName);
    
    // Update cursor position
    sf::FloatRect inputBounds = m_nameInputText.getGlobalBounds();
    m_cursor.setPosition(inputBounds.left + inputBounds.width + 5.0f, 160.0f);
}

void HighScoreState::render(sf::RenderWindow& window) {
    window.draw(m_titleText);
    
    if (m_enteringName) {
        window.draw(m_namePromptText);
        window.draw(m_nameInputText);
        
        // Blinking cursor
        if (m_cursorBlinkTimer < 0.5f) {
            window.draw(m_cursor);
        }
    }
    
    for (const auto& text : m_scoreTexts) {
        window.draw(text);
    }
    
    window.draw(m_backText);
}

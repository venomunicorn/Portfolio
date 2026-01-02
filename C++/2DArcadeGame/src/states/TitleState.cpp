#include "TitleState.h"
#include "PlayingState.h"
#include "HighScoreState.h"
#include "SettingsState.h"
#include "core/Game.h"
#include "core/Config.h"
#include "audio/AudioManager.h"

TitleState::TitleState(Game& game)
    : GameState(game)
    , m_blinkTimer(0.0f)
    , m_showStartText(true)
{
}

void TitleState::init() {
    // Initialize audio
    AudioManager::getInstance().init();
    
    // Load font
    if (!m_font.loadFromFile("assets/fonts/arcade.ttf")) {
        m_font.loadFromFile("C:/Windows/Fonts/arial.ttf");
    }
    
    // Title text
    m_titleText.setFont(m_font);
    m_titleText.setString("2D ARCADE GAME");
    m_titleText.setCharacterSize(64);
    m_titleText.setFillColor(sf::Color::White);
    m_titleText.setStyle(sf::Text::Bold);
    
    sf::FloatRect titleBounds = m_titleText.getLocalBounds();
    m_titleText.setOrigin(titleBounds.width / 2, titleBounds.height / 2);
    m_titleText.setPosition(Config::WINDOW_WIDTH / 2.0f, Config::WINDOW_HEIGHT / 3.0f);
    
    // Start text
    m_startText.setFont(m_font);
    m_startText.setString("PRESS ENTER TO START");
    m_startText.setCharacterSize(32);
    m_startText.setFillColor(sf::Color::Yellow);
    
    sf::FloatRect startBounds = m_startText.getLocalBounds();
    m_startText.setOrigin(startBounds.width / 2, startBounds.height / 2);
    m_startText.setPosition(Config::WINDOW_WIDTH / 2.0f, Config::WINDOW_HEIGHT / 2.0f);
    
    // Controls text with settings option
    m_controlsText.setFont(m_font);
    m_controlsText.setString("H - High Scores    S - Settings    ESC - Quit");
    m_controlsText.setCharacterSize(18);
    m_controlsText.setFillColor(sf::Color(180, 180, 180));
    
    sf::FloatRect controlsBounds = m_controlsText.getLocalBounds();
    m_controlsText.setOrigin(controlsBounds.width / 2, controlsBounds.height / 2);
    m_controlsText.setPosition(Config::WINDOW_WIDTH / 2.0f, Config::WINDOW_HEIGHT * 0.75f);
    
    // Try to play menu music
    AudioManager::getInstance().playMusic("assets/audio/menu_music.ogg", true);
}

void TitleState::handleEvent(const sf::Event& event) {
    if (event.type == sf::Event::KeyPressed) {
        if (event.key.code == sf::Keyboard::Return || event.key.code == sf::Keyboard::Space) {
            AudioManager::getInstance().playSound("select");
            AudioManager::getInstance().stopMusic();
            m_game.changeState(std::make_unique<PlayingState>(m_game));
        }
        if (event.key.code == sf::Keyboard::H) {
            AudioManager::getInstance().playSound("select");
            m_game.changeState(std::make_unique<HighScoreState>(m_game));
        }
        if (event.key.code == sf::Keyboard::S) {
            AudioManager::getInstance().playSound("select");
            m_game.changeState(std::make_unique<SettingsState>(m_game));
        }
        if (event.key.code == sf::Keyboard::Escape) {
            m_game.getWindow().close();
        }
    }
}

void TitleState::update(float deltaTime) {
    m_blinkTimer += deltaTime;
    if (m_blinkTimer >= 0.5f) {
        m_blinkTimer = 0.0f;
        m_showStartText = !m_showStartText;
    }
}

void TitleState::render(sf::RenderWindow& window) {
    window.draw(m_titleText);
    
    if (m_showStartText) {
        window.draw(m_startText);
    }
    
    window.draw(m_controlsText);
}

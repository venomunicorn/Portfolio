#include "SettingsState.h"
#include "TitleState.h"
#include "core/Game.h"
#include "core/Config.h"

SettingsState::SettingsState(Game& game)
    : GameState(game)
    , m_selectedIndex(0)
{
}

void SettingsState::init() {
    if (!m_font.loadFromFile("assets/fonts/arcade.ttf")) {
        m_font.loadFromFile("C:/Windows/Fonts/arial.ttf");
    }
    
    // Load current settings
    m_tempSettings = SaveManager::getInstance().getSettings();
    
    // Title
    m_titleText.setFont(m_font);
    m_titleText.setString("SETTINGS");
    m_titleText.setCharacterSize(48);
    m_titleText.setFillColor(sf::Color::Yellow);
    
    sf::FloatRect titleBounds = m_titleText.getLocalBounds();
    m_titleText.setOrigin(titleBounds.width / 2.0f, titleBounds.height / 2.0f);
    m_titleText.setPosition(Config::WINDOW_WIDTH / 2.0f, 60.0f);
    
    // Menu items
    std::vector<std::string> labels = {
        "MASTER VOLUME",
        "MUSIC VOLUME",
        "SFX VOLUME",
        "SCREEN SHAKE",
        "VSYNC",
        "BACK"
    };
    
    float startY = 150.0f;
    float spacing = 60.0f;
    
    for (size_t i = 0; i < labels.size(); ++i) {
        sf::Text text;
        text.setFont(m_font);
        text.setString(labels[i]);
        text.setCharacterSize(24);
        text.setFillColor(sf::Color::White);
        text.setPosition(200.0f, startY + i * spacing);
        m_menuItems.push_back(text);
        
        // Create sliders for volume options
        if (i < 4) {
            sf::RectangleShape sliderBg;
            sliderBg.setSize(sf::Vector2f(200.0f, 20.0f));
            sliderBg.setPosition(500.0f, startY + i * spacing + 5.0f);
            sliderBg.setFillColor(sf::Color(60, 60, 60));
            m_sliderBgs.push_back(sliderBg);
            
            sf::RectangleShape slider;
            slider.setSize(sf::Vector2f(100.0f, 20.0f));
            slider.setPosition(500.0f, startY + i * spacing + 5.0f);
            slider.setFillColor(sf::Color(100, 200, 100));
            m_sliders.push_back(slider);
        }
    }
}

void SettingsState::handleEvent(const sf::Event& event) {
    if (event.type == sf::Event::KeyPressed) {
        if (event.key.code == sf::Keyboard::Up) {
            m_selectedIndex = (m_selectedIndex - 1 + static_cast<int>(MenuItem::COUNT)) % static_cast<int>(MenuItem::COUNT);
            AudioManager::getInstance().playSound("select", 50.0f);
        }
        else if (event.key.code == sf::Keyboard::Down) {
            m_selectedIndex = (m_selectedIndex + 1) % static_cast<int>(MenuItem::COUNT);
            AudioManager::getInstance().playSound("select", 50.0f);
        }
        else if (event.key.code == sf::Keyboard::Left) {
            updateMenuItem(-1);
        }
        else if (event.key.code == sf::Keyboard::Right) {
            updateMenuItem(1);
        }
        else if (event.key.code == sf::Keyboard::Return) {
            selectMenuItem();
        }
        else if (event.key.code == sf::Keyboard::Escape) {
            // Save and exit
            SaveManager::getInstance().getSettings() = m_tempSettings;
            SaveManager::getInstance().saveSettings();
            AudioManager::getInstance().playSound("select");
            m_game.changeState(std::make_unique<TitleState>(m_game));
        }
    }
}

void SettingsState::updateMenuItem(int direction) {
    float delta = direction * 10.0f;
    
    switch (static_cast<MenuItem>(m_selectedIndex)) {
        case MenuItem::MasterVolume:
            m_tempSettings.masterVolume = std::max(0.0f, std::min(100.0f, m_tempSettings.masterVolume + delta));
            AudioManager::getInstance().setMasterVolume(m_tempSettings.masterVolume);
            AudioManager::getInstance().playSound("hit", 80.0f);
            break;
            
        case MenuItem::MusicVolume:
            m_tempSettings.musicVolume = std::max(0.0f, std::min(100.0f, m_tempSettings.musicVolume + delta));
            AudioManager::getInstance().setMusicVolume(m_tempSettings.musicVolume);
            break;
            
        case MenuItem::SFXVolume:
            m_tempSettings.sfxVolume = std::max(0.0f, std::min(100.0f, m_tempSettings.sfxVolume + delta));
            AudioManager::getInstance().setSFXVolume(m_tempSettings.sfxVolume);
            AudioManager::getInstance().playSound("hit", 80.0f);
            break;
            
        case MenuItem::ScreenShake:
            m_tempSettings.screenShakeIntensity = std::max(0, std::min(100, m_tempSettings.screenShakeIntensity + static_cast<int>(delta)));
            break;
            
        case MenuItem::VSync:
            m_tempSettings.vsync = !m_tempSettings.vsync;
            m_game.getWindow().setVerticalSyncEnabled(m_tempSettings.vsync);
            AudioManager::getInstance().playSound("select");
            break;
            
        default:
            break;
    }
}

void SettingsState::selectMenuItem() {
    if (static_cast<MenuItem>(m_selectedIndex) == MenuItem::Back) {
        SaveManager::getInstance().getSettings() = m_tempSettings;
        SaveManager::getInstance().saveSettings();
        AudioManager::getInstance().playSound("select");
        m_game.changeState(std::make_unique<TitleState>(m_game));
    }
    else if (static_cast<MenuItem>(m_selectedIndex) == MenuItem::VSync) {
        updateMenuItem(1);  // Toggle
    }
}

void SettingsState::update(float deltaTime) {
    // Update slider widths
    if (m_sliders.size() >= 4) {
        m_sliders[0].setSize(sf::Vector2f(m_tempSettings.masterVolume * 2.0f, 20.0f));
        m_sliders[1].setSize(sf::Vector2f(m_tempSettings.musicVolume * 2.0f, 20.0f));
        m_sliders[2].setSize(sf::Vector2f(m_tempSettings.sfxVolume * 2.0f, 20.0f));
        m_sliders[3].setSize(sf::Vector2f(m_tempSettings.screenShakeIntensity * 2.0f, 20.0f));
    }
    
    // Update menu item colors
    for (size_t i = 0; i < m_menuItems.size(); ++i) {
        if (static_cast<int>(i) == m_selectedIndex) {
            m_menuItems[i].setFillColor(sf::Color::Yellow);
        } else {
            m_menuItems[i].setFillColor(sf::Color::White);
        }
    }
}

void SettingsState::render(sf::RenderWindow& window) {
    window.draw(m_titleText);
    
    // Draw menu items with values
    for (size_t i = 0; i < m_menuItems.size(); ++i) {
        window.draw(m_menuItems[i]);
    }
    
    // Draw sliders
    for (size_t i = 0; i < m_sliderBgs.size(); ++i) {
        window.draw(m_sliderBgs[i]);
        window.draw(m_sliders[i]);
    }
    
    // Draw VSync status
    sf::Text vsyncText;
    vsyncText.setFont(m_font);
    vsyncText.setString(m_tempSettings.vsync ? "ON" : "OFF");
    vsyncText.setCharacterSize(24);
    vsyncText.setFillColor(m_tempSettings.vsync ? sf::Color::Green : sf::Color::Red);
    vsyncText.setPosition(500.0f, 150.0f + 4 * 60.0f);
    window.draw(vsyncText);
    
    // Draw hint
    sf::Text hintText;
    hintText.setFont(m_font);
    hintText.setString("UP/DOWN - Select    LEFT/RIGHT - Adjust    ESC - Save & Exit");
    hintText.setCharacterSize(16);
    hintText.setFillColor(sf::Color(150, 150, 150));
    hintText.setPosition(200.0f, Config::WINDOW_HEIGHT - 50.0f);
    window.draw(hintText);
}

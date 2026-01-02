#pragma once

#include "GameState.h"
#include "save/SaveManager.h"
#include "audio/AudioManager.h"
#include <SFML/Graphics.hpp>

class SettingsState : public GameState {
public:
    explicit SettingsState(Game& game);
    
    void init() override;
    void handleEvent(const sf::Event& event) override;
    void update(float deltaTime) override;
    void render(sf::RenderWindow& window) override;
    
private:
    enum class MenuItem {
        MasterVolume,
        MusicVolume,
        SFXVolume,
        ScreenShake,
        VSync,
        Back,
        COUNT
    };
    
    void updateMenuItem(int direction);
    void selectMenuItem();
    
    sf::Font m_font;
    sf::Text m_titleText;
    std::vector<sf::Text> m_menuItems;
    std::vector<sf::RectangleShape> m_sliders;
    std::vector<sf::RectangleShape> m_sliderBgs;
    
    int m_selectedIndex;
    GameSettings m_tempSettings;
};

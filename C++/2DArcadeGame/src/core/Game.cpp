#include "Game.h"
#include "Config.h"
#include "states/TitleState.h"
#include <algorithm>

Game::Game()
    : m_window(sf::VideoMode(Config::WINDOW_WIDTH, Config::WINDOW_HEIGHT), 
               Config::WINDOW_TITLE,
               sf::Style::Close | sf::Style::Titlebar)
    , m_running(true)
    , m_accumulator(0.0f)
{
    m_window.setVerticalSyncEnabled(Config::VSYNC_ENABLED);
    
    // Start with title state
    pushState(std::make_unique<TitleState>(*this));
}

Game::~Game() {
    while (!m_states.empty()) {
        m_states.pop();
    }
}

void Game::run() {
    m_clock.restart();
    
    while (m_running && m_window.isOpen()) {
        float frameTime = m_clock.restart().asSeconds();
        
        // Clamp frame time to prevent spiral of death
        frameTime = std::min(frameTime, Config::FIXED_TIMESTEP * Config::MAX_UPDATES_PER_FRAME);
        
        m_accumulator += frameTime;
        
        processEvents();
        
        // Fixed timestep updates
        while (m_accumulator >= Config::FIXED_TIMESTEP) {
            update(Config::FIXED_TIMESTEP);
            m_accumulator -= Config::FIXED_TIMESTEP;
        }
        
        render();
    }
}

void Game::processEvents() {
    sf::Event event;
    while (m_window.pollEvent(event)) {
        if (event.type == sf::Event::Closed) {
            m_running = false;
        }
        
        // Pass events to current state
        if (!m_states.empty()) {
            m_states.top()->handleEvent(event);
        }
    }
}

void Game::update(float deltaTime) {
    if (!m_states.empty()) {
        m_states.top()->update(deltaTime);
    }
}

void Game::render() {
    // Clear with background color
    sf::Color bgColor(
        (Config::Colors::BACKGROUND >> 24) & 0xFF,
        (Config::Colors::BACKGROUND >> 16) & 0xFF,
        (Config::Colors::BACKGROUND >> 8) & 0xFF,
        Config::Colors::BACKGROUND & 0xFF
    );
    m_window.clear(bgColor);
    
    // Render current state
    if (!m_states.empty()) {
        m_states.top()->render(m_window);
    }
    
    m_window.display();
}

void Game::pushState(std::unique_ptr<GameState> state) {
    if (!m_states.empty()) {
        m_states.top()->pause();
    }
    m_states.push(std::move(state));
    m_states.top()->init();
}

void Game::popState() {
    if (!m_states.empty()) {
        m_states.pop();
    }
    if (!m_states.empty()) {
        m_states.top()->resume();
    }
}

void Game::changeState(std::unique_ptr<GameState> state) {
    if (!m_states.empty()) {
        m_states.pop();
    }
    m_states.push(std::move(state));
    m_states.top()->init();
}

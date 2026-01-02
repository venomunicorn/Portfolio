#include "InputSystem.h"
#include <SFML/Window/Keyboard.hpp>

bool InputSystem::isActionPressed(Action action) {
    switch (action) {
        case Action::MoveUp:
            return sf::Keyboard::isKeyPressed(sf::Keyboard::W) ||
                   sf::Keyboard::isKeyPressed(sf::Keyboard::Up);
        case Action::MoveDown:
            return sf::Keyboard::isKeyPressed(sf::Keyboard::S) ||
                   sf::Keyboard::isKeyPressed(sf::Keyboard::Down);
        case Action::MoveLeft:
            return sf::Keyboard::isKeyPressed(sf::Keyboard::A) ||
                   sf::Keyboard::isKeyPressed(sf::Keyboard::Left);
        case Action::MoveRight:
            return sf::Keyboard::isKeyPressed(sf::Keyboard::D) ||
                   sf::Keyboard::isKeyPressed(sf::Keyboard::Right);
        case Action::Fire:
            return sf::Keyboard::isKeyPressed(sf::Keyboard::Space);
        case Action::Pause:
            return sf::Keyboard::isKeyPressed(sf::Keyboard::Escape);
        case Action::Confirm:
            return sf::Keyboard::isKeyPressed(sf::Keyboard::Return) ||
                   sf::Keyboard::isKeyPressed(sf::Keyboard::Space);
        case Action::Back:
            return sf::Keyboard::isKeyPressed(sf::Keyboard::Escape);
        default:
            return false;
    }
}

bool InputSystem::isActionJustPressed(Action action, const sf::Event& event) {
    if (event.type != sf::Event::KeyPressed) return false;
    
    switch (action) {
        case Action::MoveUp:
            return event.key.code == sf::Keyboard::W || event.key.code == sf::Keyboard::Up;
        case Action::MoveDown:
            return event.key.code == sf::Keyboard::S || event.key.code == sf::Keyboard::Down;
        case Action::MoveLeft:
            return event.key.code == sf::Keyboard::A || event.key.code == sf::Keyboard::Left;
        case Action::MoveRight:
            return event.key.code == sf::Keyboard::D || event.key.code == sf::Keyboard::Right;
        case Action::Fire:
            return event.key.code == sf::Keyboard::Space;
        case Action::Pause:
            return event.key.code == sf::Keyboard::Escape;
        case Action::Confirm:
            return event.key.code == sf::Keyboard::Return || event.key.code == sf::Keyboard::Space;
        case Action::Back:
            return event.key.code == sf::Keyboard::Escape;
        default:
            return false;
    }
}

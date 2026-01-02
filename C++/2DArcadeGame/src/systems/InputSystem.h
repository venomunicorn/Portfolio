#pragma once

#include <SFML/Window/Event.hpp>

// Input action mapping for cleaner input handling
class InputSystem {
public:
    enum class Action {
        MoveUp,
        MoveDown,
        MoveLeft,
        MoveRight,
        Fire,
        Pause,
        Confirm,
        Back
    };
    
    static bool isActionPressed(Action action);
    static bool isActionJustPressed(Action action, const sf::Event& event);
};

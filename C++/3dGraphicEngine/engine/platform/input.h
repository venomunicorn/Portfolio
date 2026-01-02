#pragma once

#include "core/types.h"

#include <SDL_scancode.h>

namespace engine {

// Wrapper for SDL scancodes
using KeyCode = SDL_Scancode;

// Mouse button indices
enum class MouseButton : u8 {
    Left = 1,
    Middle = 2,
    Right = 3,
    X1 = 4,
    X2 = 5
};

// Static input system - tracks keyboard and mouse state
class Input {
public:
    // Called at start of frame to update previous state
    static void BeginFrame();

    // Event handlers (called by Window)
    static void OnKeyEvent(KeyCode key, bool pressed);
    static void OnMouseMove(i32 x, i32 y, i32 relX, i32 relY);
    static void OnMouseButton(u8 button, bool pressed);
    static void OnMouseScroll(f32 x, f32 y);

    // Keyboard queries
    [[nodiscard]] static bool IsKeyDown(KeyCode key);
    [[nodiscard]] static bool IsKeyPressed(KeyCode key);   // Just pressed this frame
    [[nodiscard]] static bool IsKeyReleased(KeyCode key);  // Just released this frame

    // Mouse queries
    [[nodiscard]] static Vec2i GetMousePosition();
    [[nodiscard]] static Vec2i GetMouseDelta();
    [[nodiscard]] static Vec2 GetMouseScroll();
    [[nodiscard]] static bool IsMouseButtonDown(MouseButton button);
    [[nodiscard]] static bool IsMouseButtonPressed(MouseButton button);
    [[nodiscard]] static bool IsMouseButtonReleased(MouseButton button);

private:
    static constexpr size_t KEY_COUNT = SDL_NUM_SCANCODES;
    static constexpr size_t MOUSE_BUTTON_COUNT = 6;

    static bool s_keysDown[KEY_COUNT];
    static bool s_keysPrev[KEY_COUNT];

    static bool s_mouseDown[MOUSE_BUTTON_COUNT];
    static bool s_mousePrev[MOUSE_BUTTON_COUNT];

    static Vec2i s_mousePos;
    static Vec2i s_mouseDelta;
    static Vec2 s_mouseScroll;
};

}  // namespace engine

#include "input.h"

#include <cstring>

namespace engine {

// Static member definitions
bool Input::s_keysDown[KEY_COUNT] = {};
bool Input::s_keysPrev[KEY_COUNT] = {};
bool Input::s_mouseDown[MOUSE_BUTTON_COUNT] = {};
bool Input::s_mousePrev[MOUSE_BUTTON_COUNT] = {};
Vec2i Input::s_mousePos = {0, 0};
Vec2i Input::s_mouseDelta = {0, 0};
Vec2 Input::s_mouseScroll = {0.0f, 0.0f};

void Input::BeginFrame() {
    // Copy current state to previous
    std::memcpy(s_keysPrev, s_keysDown, sizeof(s_keysDown));
    std::memcpy(s_mousePrev, s_mouseDown, sizeof(s_mouseDown));

    // Reset per-frame values
    s_mouseDelta = {0, 0};
    s_mouseScroll = {0.0f, 0.0f};
}

void Input::OnKeyEvent(KeyCode key, bool pressed) {
    if (key >= 0 && key < static_cast<i32>(KEY_COUNT)) {
        s_keysDown[key] = pressed;
    }
}

void Input::OnMouseMove(i32 x, i32 y, i32 relX, i32 relY) {
    s_mousePos = {x, y};
    s_mouseDelta = {relX, relY};
}

void Input::OnMouseButton(u8 button, bool pressed) {
    if (button < MOUSE_BUTTON_COUNT) {
        s_mouseDown[button] = pressed;
    }
}

void Input::OnMouseScroll(f32 x, f32 y) {
    s_mouseScroll = {x, y};
}

bool Input::IsKeyDown(KeyCode key) {
    if (key >= 0 && key < static_cast<i32>(KEY_COUNT)) {
        return s_keysDown[key];
    }
    return false;
}

bool Input::IsKeyPressed(KeyCode key) {
    if (key >= 0 && key < static_cast<i32>(KEY_COUNT)) {
        return s_keysDown[key] && !s_keysPrev[key];
    }
    return false;
}

bool Input::IsKeyReleased(KeyCode key) {
    if (key >= 0 && key < static_cast<i32>(KEY_COUNT)) {
        return !s_keysDown[key] && s_keysPrev[key];
    }
    return false;
}

Vec2i Input::GetMousePosition() {
    return s_mousePos;
}

Vec2i Input::GetMouseDelta() {
    return s_mouseDelta;
}

Vec2 Input::GetMouseScroll() {
    return s_mouseScroll;
}

bool Input::IsMouseButtonDown(MouseButton button) {
    auto idx = static_cast<u8>(button);
    if (idx < MOUSE_BUTTON_COUNT) {
        return s_mouseDown[idx];
    }
    return false;
}

bool Input::IsMouseButtonPressed(MouseButton button) {
    auto idx = static_cast<u8>(button);
    if (idx < MOUSE_BUTTON_COUNT) {
        return s_mouseDown[idx] && !s_mousePrev[idx];
    }
    return false;
}

bool Input::IsMouseButtonReleased(MouseButton button) {
    auto idx = static_cast<u8>(button);
    if (idx < MOUSE_BUTTON_COUNT) {
        return !s_mouseDown[idx] && s_mousePrev[idx];
    }
    return false;
}

}  // namespace engine

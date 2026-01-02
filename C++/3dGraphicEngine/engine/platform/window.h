#pragma once

#include "core/types.h"

#include <SDL.h>

#include <string>
#include <string_view>

namespace engine {

struct WindowConfig {
    std::string title = "MathVis Engine";
    u32 width = 1280;
    u32 height = 720;
    bool fullscreen = false;
    bool resizable = true;
    bool vsync = true;
};

class Window {
public:
    Window() = default;
    ~Window();

    // Non-copyable, movable
    Window(const Window&) = delete;
    Window& operator=(const Window&) = delete;
    Window(Window&& other) noexcept;
    Window& operator=(Window&& other) noexcept;

    // Initialize the window
    bool Init(const WindowConfig& config = {});

    // Shutdown and cleanup
    void Shutdown();

    // Process events, returns false if should quit
    bool PollEvents();

    // Getters
    [[nodiscard]] SDL_Window* GetHandle() const { return m_window; }
    [[nodiscard]] u32 GetWidth() const { return m_width; }
    [[nodiscard]] u32 GetHeight() const { return m_height; }
    [[nodiscard]] bool IsMinimized() const { return m_minimized; }
    [[nodiscard]] bool WasResized() const { return m_resized; }
    [[nodiscard]] bool IsValid() const { return m_window != nullptr; }

    // Reset the resized flag (call after handling resize)
    void ClearResizedFlag() { m_resized = false; }

    // Get required Vulkan extensions for this window
    std::vector<const char*> GetVulkanExtensions() const;

private:
    SDL_Window* m_window = nullptr;
    u32 m_width = 0;
    u32 m_height = 0;
    bool m_minimized = false;
    bool m_resized = false;
};

}  // namespace engine

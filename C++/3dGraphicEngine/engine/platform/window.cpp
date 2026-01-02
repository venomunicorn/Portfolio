#include "window.h"

#include "core/assert.h"
#include "core/log.h"
#include "input.h"

#include <SDL_vulkan.h>

namespace engine {

Window::~Window() {
    Shutdown();
}

Window::Window(Window&& other) noexcept
    : m_window(other.m_window)
    , m_width(other.m_width)
    , m_height(other.m_height)
    , m_minimized(other.m_minimized)
    , m_resized(other.m_resized) {
    other.m_window = nullptr;
}

Window& Window::operator=(Window&& other) noexcept {
    if (this != &other) {
        Shutdown();
        m_window = other.m_window;
        m_width = other.m_width;
        m_height = other.m_height;
        m_minimized = other.m_minimized;
        m_resized = other.m_resized;
        other.m_window = nullptr;
    }
    return *this;
}

bool Window::Init(const WindowConfig& config) {
    if (m_window) {
        LOG_WARN("Window already initialized");
        return true;
    }

    // Initialize SDL video subsystem
    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_EVENTS) != 0) {
        LOG_ERROR("Failed to initialize SDL: {}", SDL_GetError());
        return false;
    }

    // Create window flags
    Uint32 flags = SDL_WINDOW_VULKAN | SDL_WINDOW_SHOWN;
    if (config.resizable) {
        flags |= SDL_WINDOW_RESIZABLE;
    }
    if (config.fullscreen) {
        flags |= SDL_WINDOW_FULLSCREEN_DESKTOP;
    }

    // Create the window
    m_window = SDL_CreateWindow(config.title.c_str(), SDL_WINDOWPOS_CENTERED,
                                SDL_WINDOWPOS_CENTERED, static_cast<int>(config.width),
                                static_cast<int>(config.height), flags);

    if (!m_window) {
        LOG_ERROR("Failed to create SDL window: {}", SDL_GetError());
        SDL_Quit();
        return false;
    }

    m_width = config.width;
    m_height = config.height;

    LOG_INFO("Window created: {}x{} ({})", m_width, m_height, config.title);
    return true;
}

void Window::Shutdown() {
    if (m_window) {
        SDL_DestroyWindow(m_window);
        m_window = nullptr;
        SDL_Quit();
        LOG_INFO("Window destroyed");
    }
}

bool Window::PollEvents() {
    // Reset per-frame input state
    Input::BeginFrame();

    SDL_Event event;
    while (SDL_PollEvent(&event)) {
        switch (event.type) {
        case SDL_QUIT:
            return false;

        case SDL_WINDOWEVENT:
            switch (event.window.event) {
            case SDL_WINDOWEVENT_RESIZED:
            case SDL_WINDOWEVENT_SIZE_CHANGED:
                m_width = static_cast<u32>(event.window.data1);
                m_height = static_cast<u32>(event.window.data2);
                m_resized = true;
                LOG_DEBUG("Window resized: {}x{}", m_width, m_height);
                break;

            case SDL_WINDOWEVENT_MINIMIZED:
                m_minimized = true;
                break;

            case SDL_WINDOWEVENT_RESTORED:
                m_minimized = false;
                break;
            }
            break;

        case SDL_KEYDOWN:
            Input::OnKeyEvent(event.key.keysym.scancode, true);
            break;

        case SDL_KEYUP:
            Input::OnKeyEvent(event.key.keysym.scancode, false);
            break;

        case SDL_MOUSEMOTION:
            Input::OnMouseMove(event.motion.x, event.motion.y, event.motion.xrel,
                               event.motion.yrel);
            break;

        case SDL_MOUSEBUTTONDOWN:
            Input::OnMouseButton(event.button.button, true);
            break;

        case SDL_MOUSEBUTTONUP:
            Input::OnMouseButton(event.button.button, false);
            break;

        case SDL_MOUSEWHEEL:
            Input::OnMouseScroll(static_cast<f32>(event.wheel.x),
                                 static_cast<f32>(event.wheel.y));
            break;
        }
    }

    return true;
}

std::vector<const char*> Window::GetVulkanExtensions() const {
    unsigned int count = 0;
    SDL_Vulkan_GetInstanceExtensions(m_window, &count, nullptr);

    std::vector<const char*> extensions(count);
    SDL_Vulkan_GetInstanceExtensions(m_window, &count, extensions.data());

    return extensions;
}

}  // namespace engine

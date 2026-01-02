#pragma once

#include "core/types.h"
#include "vulkan_context.h"

#include <vulkan/vulkan.h>

#include <vector>

namespace engine {

class Window;

struct SwapchainConfig {
    bool vsync = true;
    u32 preferredImageCount = 3;  // Triple buffering
};

// Swapchain management - handles presentation
class Swapchain {
public:
    static constexpr u32 MAX_FRAMES_IN_FLIGHT = 2;

    Swapchain() = default;
    ~Swapchain();

    // Non-copyable
    Swapchain(const Swapchain&) = delete;
    Swapchain& operator=(const Swapchain&) = delete;

    // Initialize swapchain
    bool Init(VulkanContext& context, Window& window, const SwapchainConfig& config = {});

    // Recreate swapchain (on resize)
    bool Recreate(u32 width, u32 height);

    // Cleanup
    void Shutdown();

    // Frame synchronization
    VkResult AcquireNextImage(u32& imageIndex);
    VkResult Present(u32 imageIndex);

    // Getters
    [[nodiscard]] VkSwapchainKHR GetHandle() const { return m_swapchain; }
    [[nodiscard]] VkFormat GetImageFormat() const { return m_imageFormat; }
    [[nodiscard]] VkExtent2D GetExtent() const { return m_extent; }
    [[nodiscard]] u32 GetImageCount() const { return static_cast<u32>(m_images.size()); }
    [[nodiscard]] VkImageView GetImageView(u32 index) const { return m_imageViews[index]; }
    [[nodiscard]] VkSemaphore GetImageAvailableSemaphore() const {
        return m_imageAvailableSemaphores[m_currentFrame];
    }
    [[nodiscard]] VkSemaphore GetRenderFinishedSemaphore() const {
        return m_renderFinishedSemaphores[m_currentFrame];
    }
    [[nodiscard]] VkFence GetInFlightFence() const { return m_inFlightFences[m_currentFrame]; }
    [[nodiscard]] u32 GetCurrentFrame() const { return m_currentFrame; }
    [[nodiscard]] bool IsValid() const { return m_swapchain != VK_NULL_HANDLE; }

    // Advance to next frame (call after present)
    void NextFrame() { m_currentFrame = (m_currentFrame + 1) % MAX_FRAMES_IN_FLIGHT; }

private:
    bool CreateSwapchain(u32 width, u32 height);
    bool CreateImageViews();
    bool CreateSyncObjects();
    void CleanupSwapchain();

    VkSurfaceFormatKHR ChooseSurfaceFormat(
        const std::vector<VkSurfaceFormatKHR>& availableFormats);
    VkPresentModeKHR ChoosePresentMode(const std::vector<VkPresentModeKHR>& availableModes);
    VkExtent2D ChooseExtent(const VkSurfaceCapabilitiesKHR& capabilities, u32 width, u32 height);

    VulkanContext* m_context = nullptr;
    SwapchainConfig m_config{};

    VkSwapchainKHR m_swapchain = VK_NULL_HANDLE;
    VkFormat m_imageFormat = VK_FORMAT_UNDEFINED;
    VkExtent2D m_extent{};

    std::vector<VkImage> m_images;
    std::vector<VkImageView> m_imageViews;

    // Synchronization objects (per frame in flight)
    std::vector<VkSemaphore> m_imageAvailableSemaphores;
    std::vector<VkSemaphore> m_renderFinishedSemaphores;
    std::vector<VkFence> m_inFlightFences;

    u32 m_currentFrame = 0;
};

}  // namespace engine

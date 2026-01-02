#include "swapchain.h"

#include "core/assert.h"
#include "core/log.h"

#include <algorithm>
#include <limits>

namespace engine {

Swapchain::~Swapchain() {
    Shutdown();
}

bool Swapchain::Init(VulkanContext& context, Window& window, const SwapchainConfig& config) {
    m_context = &context;
    m_config = config;

    if (!CreateSwapchain(window.GetWidth(), window.GetHeight())) {
        return false;
    }

    if (!CreateImageViews()) {
        return false;
    }

    if (!CreateSyncObjects()) {
        return false;
    }

    LOG_INFO("Swapchain created: {}x{}, {} images", m_extent.width, m_extent.height,
             m_images.size());
    return true;
}

bool Swapchain::Recreate(u32 width, u32 height) {
    if (width == 0 || height == 0) {
        return true;  // Window is minimized, skip recreation
    }

    m_context->WaitIdle();
    CleanupSwapchain();

    if (!CreateSwapchain(width, height)) {
        return false;
    }

    if (!CreateImageViews()) {
        return false;
    }

    LOG_INFO("Swapchain recreated: {}x{}", m_extent.width, m_extent.height);
    return true;
}

void Swapchain::Shutdown() {
    if (!m_context) {
        return;
    }

    m_context->WaitIdle();

    VkDevice device = m_context->GetDevice();

    // Destroy sync objects
    for (auto semaphore : m_imageAvailableSemaphores) {
        vkDestroySemaphore(device, semaphore, nullptr);
    }
    for (auto semaphore : m_renderFinishedSemaphores) {
        vkDestroySemaphore(device, semaphore, nullptr);
    }
    for (auto fence : m_inFlightFences) {
        vkDestroyFence(device, fence, nullptr);
    }

    m_imageAvailableSemaphores.clear();
    m_renderFinishedSemaphores.clear();
    m_inFlightFences.clear();

    CleanupSwapchain();
    m_context = nullptr;

    LOG_INFO("Swapchain destroyed");
}

VkResult Swapchain::AcquireNextImage(u32& imageIndex) {
    VkDevice device = m_context->GetDevice();

    // Wait for previous frame using this slot
    vkWaitForFences(device, 1, &m_inFlightFences[m_currentFrame], VK_TRUE,
                    std::numeric_limits<u64>::max());

    VkResult result =
        vkAcquireNextImageKHR(device, m_swapchain, std::numeric_limits<u64>::max(),
                              m_imageAvailableSemaphores[m_currentFrame], VK_NULL_HANDLE, &imageIndex);

    if (result == VK_SUCCESS || result == VK_SUBOPTIMAL_KHR) {
        // Reset fence only if we're going to submit work
        vkResetFences(device, 1, &m_inFlightFences[m_currentFrame]);
    }

    return result;
}

VkResult Swapchain::Present(u32 imageIndex) {
    VkPresentInfoKHR presentInfo{};
    presentInfo.sType = VK_STRUCTURE_TYPE_PRESENT_INFO_KHR;

    VkSemaphore waitSemaphores[] = {m_renderFinishedSemaphores[m_currentFrame]};
    presentInfo.waitSemaphoreCount = 1;
    presentInfo.pWaitSemaphores = waitSemaphores;

    VkSwapchainKHR swapchains[] = {m_swapchain};
    presentInfo.swapchainCount = 1;
    presentInfo.pSwapchains = swapchains;
    presentInfo.pImageIndices = &imageIndex;

    return vkQueuePresentKHR(m_context->GetPresentQueue(), &presentInfo);
}

bool Swapchain::CreateSwapchain(u32 width, u32 height) {
    VkPhysicalDevice physicalDevice = m_context->GetPhysicalDevice();
    VkDevice device = m_context->GetDevice();
    VkSurfaceKHR surface = m_context->GetSurface();

    // Query swapchain support
    VkSurfaceCapabilitiesKHR capabilities;
    vkGetPhysicalDeviceSurfaceCapabilitiesKHR(physicalDevice, surface, &capabilities);

    u32 formatCount;
    vkGetPhysicalDeviceSurfaceFormatsKHR(physicalDevice, surface, &formatCount, nullptr);
    std::vector<VkSurfaceFormatKHR> formats(formatCount);
    vkGetPhysicalDeviceSurfaceFormatsKHR(physicalDevice, surface, &formatCount, formats.data());

    u32 presentModeCount;
    vkGetPhysicalDeviceSurfacePresentModesKHR(physicalDevice, surface, &presentModeCount, nullptr);
    std::vector<VkPresentModeKHR> presentModes(presentModeCount);
    vkGetPhysicalDeviceSurfacePresentModesKHR(physicalDevice, surface, &presentModeCount,
                                              presentModes.data());

    // Choose optimal settings
    VkSurfaceFormatKHR surfaceFormat = ChooseSurfaceFormat(formats);
    VkPresentModeKHR presentMode = ChoosePresentMode(presentModes);
    VkExtent2D extent = ChooseExtent(capabilities, width, height);

    // Determine image count
    u32 imageCount = m_config.preferredImageCount;
    if (imageCount < capabilities.minImageCount) {
        imageCount = capabilities.minImageCount;
    }
    if (capabilities.maxImageCount > 0 && imageCount > capabilities.maxImageCount) {
        imageCount = capabilities.maxImageCount;
    }

    // Create swapchain
    VkSwapchainCreateInfoKHR createInfo{};
    createInfo.sType = VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR;
    createInfo.surface = surface;
    createInfo.minImageCount = imageCount;
    createInfo.imageFormat = surfaceFormat.format;
    createInfo.imageColorSpace = surfaceFormat.colorSpace;
    createInfo.imageExtent = extent;
    createInfo.imageArrayLayers = 1;
    createInfo.imageUsage = VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT;

    u32 queueFamilyIndices[] = {m_context->GetGraphicsQueueFamily(),
                                m_context->GetPresentQueueFamily()};

    if (queueFamilyIndices[0] != queueFamilyIndices[1]) {
        createInfo.imageSharingMode = VK_SHARING_MODE_CONCURRENT;
        createInfo.queueFamilyIndexCount = 2;
        createInfo.pQueueFamilyIndices = queueFamilyIndices;
    } else {
        createInfo.imageSharingMode = VK_SHARING_MODE_EXCLUSIVE;
    }

    createInfo.preTransform = capabilities.currentTransform;
    createInfo.compositeAlpha = VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR;
    createInfo.presentMode = presentMode;
    createInfo.clipped = VK_TRUE;
    createInfo.oldSwapchain = VK_NULL_HANDLE;

    VkResult result = vkCreateSwapchainKHR(device, &createInfo, nullptr, &m_swapchain);
    if (result != VK_SUCCESS) {
        LOG_ERROR("Failed to create swapchain: {}", static_cast<i32>(result));
        return false;
    }

    // Get swapchain images
    vkGetSwapchainImagesKHR(device, m_swapchain, &imageCount, nullptr);
    m_images.resize(imageCount);
    vkGetSwapchainImagesKHR(device, m_swapchain, &imageCount, m_images.data());

    m_imageFormat = surfaceFormat.format;
    m_extent = extent;

    return true;
}

bool Swapchain::CreateImageViews() {
    VkDevice device = m_context->GetDevice();
    m_imageViews.resize(m_images.size());

    for (size_t i = 0; i < m_images.size(); i++) {
        VkImageViewCreateInfo createInfo{};
        createInfo.sType = VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO;
        createInfo.image = m_images[i];
        createInfo.viewType = VK_IMAGE_VIEW_TYPE_2D;
        createInfo.format = m_imageFormat;
        createInfo.components.r = VK_COMPONENT_SWIZZLE_IDENTITY;
        createInfo.components.g = VK_COMPONENT_SWIZZLE_IDENTITY;
        createInfo.components.b = VK_COMPONENT_SWIZZLE_IDENTITY;
        createInfo.components.a = VK_COMPONENT_SWIZZLE_IDENTITY;
        createInfo.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
        createInfo.subresourceRange.baseMipLevel = 0;
        createInfo.subresourceRange.levelCount = 1;
        createInfo.subresourceRange.baseArrayLayer = 0;
        createInfo.subresourceRange.layerCount = 1;

        VkResult result = vkCreateImageView(device, &createInfo, nullptr, &m_imageViews[i]);
        if (result != VK_SUCCESS) {
            LOG_ERROR("Failed to create image view {}: {}", i, static_cast<i32>(result));
            return false;
        }
    }

    return true;
}

bool Swapchain::CreateSyncObjects() {
    VkDevice device = m_context->GetDevice();

    m_imageAvailableSemaphores.resize(MAX_FRAMES_IN_FLIGHT);
    m_renderFinishedSemaphores.resize(MAX_FRAMES_IN_FLIGHT);
    m_inFlightFences.resize(MAX_FRAMES_IN_FLIGHT);

    VkSemaphoreCreateInfo semaphoreInfo{};
    semaphoreInfo.sType = VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO;

    VkFenceCreateInfo fenceInfo{};
    fenceInfo.sType = VK_STRUCTURE_TYPE_FENCE_CREATE_INFO;
    fenceInfo.flags = VK_FENCE_CREATE_SIGNALED_BIT;  // Start signaled

    for (u32 i = 0; i < MAX_FRAMES_IN_FLIGHT; i++) {
        if (vkCreateSemaphore(device, &semaphoreInfo, nullptr, &m_imageAvailableSemaphores[i]) !=
                VK_SUCCESS ||
            vkCreateSemaphore(device, &semaphoreInfo, nullptr, &m_renderFinishedSemaphores[i]) !=
                VK_SUCCESS ||
            vkCreateFence(device, &fenceInfo, nullptr, &m_inFlightFences[i]) != VK_SUCCESS) {
            LOG_ERROR("Failed to create synchronization objects for frame {}", i);
            return false;
        }
    }

    return true;
}

void Swapchain::CleanupSwapchain() {
    if (!m_context) {
        return;
    }

    VkDevice device = m_context->GetDevice();

    for (auto imageView : m_imageViews) {
        vkDestroyImageView(device, imageView, nullptr);
    }
    m_imageViews.clear();
    m_images.clear();

    if (m_swapchain) {
        vkDestroySwapchainKHR(device, m_swapchain, nullptr);
        m_swapchain = VK_NULL_HANDLE;
    }
}

VkSurfaceFormatKHR Swapchain::ChooseSurfaceFormat(
    const std::vector<VkSurfaceFormatKHR>& availableFormats) {
    // Prefer sRGB for correct color
    for (const auto& format : availableFormats) {
        if (format.format == VK_FORMAT_B8G8R8A8_SRGB &&
            format.colorSpace == VK_COLOR_SPACE_SRGB_NONLINEAR_KHR) {
            return format;
        }
    }

    // Fall back to first available
    return availableFormats[0];
}

VkPresentModeKHR Swapchain::ChoosePresentMode(
    const std::vector<VkPresentModeKHR>& availableModes) {
    if (!m_config.vsync) {
        // Prefer immediate for lowest latency
        for (const auto& mode : availableModes) {
            if (mode == VK_PRESENT_MODE_IMMEDIATE_KHR) {
                return mode;
            }
        }
    }

    // Prefer mailbox for vsync without latency
    for (const auto& mode : availableModes) {
        if (mode == VK_PRESENT_MODE_MAILBOX_KHR) {
            return mode;
        }
    }

    // FIFO is always available
    return VK_PRESENT_MODE_FIFO_KHR;
}

VkExtent2D Swapchain::ChooseExtent(const VkSurfaceCapabilitiesKHR& capabilities, u32 width,
                                   u32 height) {
    if (capabilities.currentExtent.width != std::numeric_limits<u32>::max()) {
        return capabilities.currentExtent;
    }

    VkExtent2D extent = {width, height};
    extent.width =
        std::clamp(extent.width, capabilities.minImageExtent.width, capabilities.maxImageExtent.width);
    extent.height = std::clamp(extent.height, capabilities.minImageExtent.height,
                               capabilities.maxImageExtent.height);
    return extent;
}

}  // namespace engine

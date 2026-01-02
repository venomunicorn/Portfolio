#pragma once

#include "core/types.h"

#include <vulkan/vulkan.h>
#include <vk_mem_alloc.h>

#include <vector>

namespace engine {

class Window;

struct VulkanContextConfig {
    bool enableValidation = true;  // Enable validation layers in debug
    bool preferDiscreteGPU = true;
};

// Core Vulkan context - instance, device, queues, allocator
class VulkanContext {
public:
    VulkanContext() = default;
    ~VulkanContext();

    // Non-copyable
    VulkanContext(const VulkanContext&) = delete;
    VulkanContext& operator=(const VulkanContext&) = delete;

    // Initialize Vulkan context
    bool Init(Window& window, const VulkanContextConfig& config = {});

    // Cleanup
    void Shutdown();

    // Wait for device to be idle
    void WaitIdle();

    // Getters
    [[nodiscard]] VkInstance GetInstance() const { return m_instance; }
    [[nodiscard]] VkPhysicalDevice GetPhysicalDevice() const { return m_physicalDevice; }
    [[nodiscard]] VkDevice GetDevice() const { return m_device; }
    [[nodiscard]] VkQueue GetGraphicsQueue() const { return m_graphicsQueue; }
    [[nodiscard]] VkQueue GetPresentQueue() const { return m_presentQueue; }
    [[nodiscard]] u32 GetGraphicsQueueFamily() const { return m_graphicsQueueFamily; }
    [[nodiscard]] u32 GetPresentQueueFamily() const { return m_presentQueueFamily; }
    [[nodiscard]] VkSurfaceKHR GetSurface() const { return m_surface; }
    [[nodiscard]] VmaAllocator GetAllocator() const { return m_allocator; }
    [[nodiscard]] const VkPhysicalDeviceProperties& GetDeviceProperties() const {
        return m_deviceProperties;
    }
    [[nodiscard]] bool IsValid() const { return m_device != VK_NULL_HANDLE; }

private:
    bool CreateInstance(const Window& window, bool enableValidation);
    bool SelectPhysicalDevice();
    bool CreateLogicalDevice();
    bool CreateSurface(Window& window);
    bool CreateAllocator();

    VkInstance m_instance = VK_NULL_HANDLE;
    VkDebugUtilsMessengerEXT m_debugMessenger = VK_NULL_HANDLE;
    VkSurfaceKHR m_surface = VK_NULL_HANDLE;
    VkPhysicalDevice m_physicalDevice = VK_NULL_HANDLE;
    VkDevice m_device = VK_NULL_HANDLE;
    VmaAllocator m_allocator = VK_NULL_HANDLE;

    VkQueue m_graphicsQueue = VK_NULL_HANDLE;
    VkQueue m_presentQueue = VK_NULL_HANDLE;
    u32 m_graphicsQueueFamily = 0;
    u32 m_presentQueueFamily = 0;

    VkPhysicalDeviceProperties m_deviceProperties{};

    bool m_validationEnabled = false;
};

}  // namespace engine

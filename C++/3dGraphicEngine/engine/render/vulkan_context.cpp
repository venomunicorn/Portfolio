#include "vulkan_context.h"

#include "core/assert.h"
#include "core/log.h"
#include "platform/window.h"

#include <SDL_vulkan.h>

#include <algorithm>
#include <cstring>
#include <set>

#define VMA_IMPLEMENTATION
#include <vk_mem_alloc.h>

namespace engine {

// Validation layer callback
static VKAPI_ATTR VkBool32 VKAPI_CALL DebugCallback(
    VkDebugUtilsMessageSeverityFlagBitsEXT messageSeverity,
    VkDebugUtilsMessageTypeFlagsEXT /*messageType*/,
    const VkDebugUtilsMessengerCallbackDataEXT* pCallbackData, void* /*pUserData*/) {
    if (messageSeverity >= VK_DEBUG_UTILS_MESSAGE_SEVERITY_ERROR_BIT_EXT) {
        LOG_ERROR("[Vulkan] {}", pCallbackData->pMessage);
    } else if (messageSeverity >= VK_DEBUG_UTILS_MESSAGE_SEVERITY_WARNING_BIT_EXT) {
        LOG_WARN("[Vulkan] {}", pCallbackData->pMessage);
    } else if (messageSeverity >= VK_DEBUG_UTILS_MESSAGE_SEVERITY_INFO_BIT_EXT) {
        LOG_DEBUG("[Vulkan] {}", pCallbackData->pMessage);
    }
    return VK_FALSE;
}

VulkanContext::~VulkanContext() {
    Shutdown();
}

bool VulkanContext::Init(Window& window, const VulkanContextConfig& config) {
#ifdef NDEBUG
    bool enableValidation = false;
#else
    bool enableValidation = config.enableValidation;
#endif

    if (!CreateInstance(window, enableValidation)) {
        return false;
    }

    if (!CreateSurface(window)) {
        return false;
    }

    if (!SelectPhysicalDevice()) {
        return false;
    }

    if (!CreateLogicalDevice()) {
        return false;
    }

    if (!CreateAllocator()) {
        return false;
    }

    LOG_INFO("Vulkan context initialized successfully");
    return true;
}

void VulkanContext::Shutdown() {
    if (m_allocator) {
        vmaDestroyAllocator(m_allocator);
        m_allocator = VK_NULL_HANDLE;
    }

    if (m_device) {
        vkDestroyDevice(m_device, nullptr);
        m_device = VK_NULL_HANDLE;
    }

    if (m_surface) {
        vkDestroySurfaceKHR(m_instance, m_surface, nullptr);
        m_surface = VK_NULL_HANDLE;
    }

    if (m_debugMessenger) {
        auto func = reinterpret_cast<PFN_vkDestroyDebugUtilsMessengerEXT>(
            vkGetInstanceProcAddr(m_instance, "vkDestroyDebugUtilsMessengerEXT"));
        if (func) {
            func(m_instance, m_debugMessenger, nullptr);
        }
        m_debugMessenger = VK_NULL_HANDLE;
    }

    if (m_instance) {
        vkDestroyInstance(m_instance, nullptr);
        m_instance = VK_NULL_HANDLE;
        LOG_INFO("Vulkan context destroyed");
    }
}

void VulkanContext::WaitIdle() {
    if (m_device) {
        vkDeviceWaitIdle(m_device);
    }
}

bool VulkanContext::CreateInstance(const Window& window, bool enableValidation) {
    // Application info
    VkApplicationInfo appInfo{};
    appInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
    appInfo.pApplicationName = "MathVis Engine";
    appInfo.applicationVersion = VK_MAKE_VERSION(0, 1, 0);
    appInfo.pEngineName = "MathVis";
    appInfo.engineVersion = VK_MAKE_VERSION(0, 1, 0);
    appInfo.apiVersion = VK_API_VERSION_1_3;

    // Get required extensions from SDL
    auto extensions = window.GetVulkanExtensions();

    // Add debug utils if validation is enabled
    if (enableValidation) {
        extensions.push_back(VK_EXT_DEBUG_UTILS_EXTENSION_NAME);
    }

    LOG_DEBUG("Vulkan extensions requested:");
    for (const auto* ext : extensions) {
        LOG_DEBUG("  - {}", ext);
    }

    // Validation layers
    const std::vector<const char*> validationLayers = {"VK_LAYER_KHRONOS_validation"};

    VkInstanceCreateInfo createInfo{};
    createInfo.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
    createInfo.pApplicationInfo = &appInfo;
    createInfo.enabledExtensionCount = static_cast<u32>(extensions.size());
    createInfo.ppEnabledExtensionNames = extensions.data();

    VkDebugUtilsMessengerCreateInfoEXT debugCreateInfo{};
    if (enableValidation) {
        // Check if validation layers are available
        u32 layerCount = 0;
        vkEnumerateInstanceLayerProperties(&layerCount, nullptr);
        std::vector<VkLayerProperties> availableLayers(layerCount);
        vkEnumerateInstanceLayerProperties(&layerCount, availableLayers.data());

        bool found = false;
        for (const auto& layer : availableLayers) {
            if (strcmp(layer.layerName, validationLayers[0]) == 0) {
                found = true;
                break;
            }
        }

        if (found) {
            createInfo.enabledLayerCount = static_cast<u32>(validationLayers.size());
            createInfo.ppEnabledLayerNames = validationLayers.data();

            debugCreateInfo.sType = VK_STRUCTURE_TYPE_DEBUG_UTILS_MESSENGER_CREATE_INFO_EXT;
            debugCreateInfo.messageSeverity = VK_DEBUG_UTILS_MESSAGE_SEVERITY_WARNING_BIT_EXT |
                                              VK_DEBUG_UTILS_MESSAGE_SEVERITY_ERROR_BIT_EXT;
            debugCreateInfo.messageType = VK_DEBUG_UTILS_MESSAGE_TYPE_GENERAL_BIT_EXT |
                                          VK_DEBUG_UTILS_MESSAGE_TYPE_VALIDATION_BIT_EXT |
                                          VK_DEBUG_UTILS_MESSAGE_TYPE_PERFORMANCE_BIT_EXT;
            debugCreateInfo.pfnUserCallback = DebugCallback;
            createInfo.pNext = &debugCreateInfo;

            m_validationEnabled = true;
            LOG_INFO("Vulkan validation layers enabled");
        } else {
            LOG_WARN("Validation layers requested but not available");
        }
    }

    VkResult result = vkCreateInstance(&createInfo, nullptr, &m_instance);
    if (result != VK_SUCCESS) {
        LOG_ERROR("Failed to create Vulkan instance: {}", static_cast<i32>(result));
        return false;
    }

    // Create debug messenger
    if (m_validationEnabled) {
        auto func = reinterpret_cast<PFN_vkCreateDebugUtilsMessengerEXT>(
            vkGetInstanceProcAddr(m_instance, "vkCreateDebugUtilsMessengerEXT"));
        if (func) {
            func(m_instance, &debugCreateInfo, nullptr, &m_debugMessenger);
        }
    }

    LOG_INFO("Vulkan instance created (API 1.3)");
    return true;
}

bool VulkanContext::CreateSurface(Window& window) {
    if (!SDL_Vulkan_CreateSurface(window.GetHandle(), m_instance, &m_surface)) {
        LOG_ERROR("Failed to create Vulkan surface: {}", SDL_GetError());
        return false;
    }
    return true;
}

bool VulkanContext::SelectPhysicalDevice() {
    u32 deviceCount = 0;
    vkEnumeratePhysicalDevices(m_instance, &deviceCount, nullptr);

    if (deviceCount == 0) {
        LOG_ERROR("No Vulkan-capable GPU found");
        return false;
    }

    std::vector<VkPhysicalDevice> devices(deviceCount);
    vkEnumeratePhysicalDevices(m_instance, &deviceCount, devices.data());

    LOG_INFO("Found {} Vulkan device(s):", deviceCount);

    // Score devices and pick the best one
    i32 bestScore = -1;
    for (const auto& device : devices) {
        VkPhysicalDeviceProperties props;
        vkGetPhysicalDeviceProperties(device, &props);

        LOG_INFO("  - {} ({})", props.deviceName,
                 props.deviceType == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU     ? "Discrete"
                 : props.deviceType == VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU ? "Integrated"
                                                                              : "Other");

        // Check for required queue families
        u32 queueFamilyCount = 0;
        vkGetPhysicalDeviceQueueFamilyProperties(device, &queueFamilyCount, nullptr);
        std::vector<VkQueueFamilyProperties> queueFamilies(queueFamilyCount);
        vkGetPhysicalDeviceQueueFamilyProperties(device, &queueFamilyCount, queueFamilies.data());

        bool hasGraphics = false;
        bool hasPresent = false;
        u32 graphicsFamily = 0;
        u32 presentFamily = 0;

        for (u32 i = 0; i < queueFamilyCount; i++) {
            if (queueFamilies[i].queueFlags & VK_QUEUE_GRAPHICS_BIT) {
                hasGraphics = true;
                graphicsFamily = i;
            }

            VkBool32 presentSupport = false;
            vkGetPhysicalDeviceSurfaceSupportKHR(device, i, m_surface, &presentSupport);
            if (presentSupport) {
                hasPresent = true;
                presentFamily = i;
            }
        }

        if (!hasGraphics || !hasPresent) {
            continue;  // Skip this device
        }

        // Score the device
        i32 score = 0;
        if (props.deviceType == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU) {
            score += 1000;
        }
        score += static_cast<i32>(props.limits.maxImageDimension2D / 1000);

        if (score > bestScore) {
            bestScore = score;
            m_physicalDevice = device;
            m_graphicsQueueFamily = graphicsFamily;
            m_presentQueueFamily = presentFamily;
            m_deviceProperties = props;
        }
    }

    if (m_physicalDevice == VK_NULL_HANDLE) {
        LOG_ERROR("Failed to find suitable GPU");
        return false;
    }

    LOG_INFO("Selected GPU: {}", m_deviceProperties.deviceName);
    return true;
}

bool VulkanContext::CreateLogicalDevice() {
    // Create unique queue families
    std::set<u32> uniqueQueueFamilies = {m_graphicsQueueFamily, m_presentQueueFamily};

    std::vector<VkDeviceQueueCreateInfo> queueCreateInfos;
    float queuePriority = 1.0f;

    for (u32 queueFamily : uniqueQueueFamilies) {
        VkDeviceQueueCreateInfo queueCreateInfo{};
        queueCreateInfo.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
        queueCreateInfo.queueFamilyIndex = queueFamily;
        queueCreateInfo.queueCount = 1;
        queueCreateInfo.pQueuePriorities = &queuePriority;
        queueCreateInfos.push_back(queueCreateInfo);
    }

    // Required device extensions
    std::vector<const char*> deviceExtensions = {VK_KHR_SWAPCHAIN_EXTENSION_NAME};

    // Device features
    VkPhysicalDeviceFeatures deviceFeatures{};
    deviceFeatures.fillModeNonSolid = VK_TRUE;  // For wireframe
    deviceFeatures.wideLines = VK_TRUE;         // For thick lines
    deviceFeatures.samplerAnisotropy = VK_TRUE;

    VkDeviceCreateInfo createInfo{};
    createInfo.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
    createInfo.queueCreateInfoCount = static_cast<u32>(queueCreateInfos.size());
    createInfo.pQueueCreateInfos = queueCreateInfos.data();
    createInfo.pEnabledFeatures = &deviceFeatures;
    createInfo.enabledExtensionCount = static_cast<u32>(deviceExtensions.size());
    createInfo.ppEnabledExtensionNames = deviceExtensions.data();

    VkResult result = vkCreateDevice(m_physicalDevice, &createInfo, nullptr, &m_device);
    if (result != VK_SUCCESS) {
        LOG_ERROR("Failed to create logical device: {}", static_cast<i32>(result));
        return false;
    }

    // Get queue handles
    vkGetDeviceQueue(m_device, m_graphicsQueueFamily, 0, &m_graphicsQueue);
    vkGetDeviceQueue(m_device, m_presentQueueFamily, 0, &m_presentQueue);

    LOG_INFO("Vulkan logical device created");
    return true;
}

bool VulkanContext::CreateAllocator() {
    VmaAllocatorCreateInfo allocatorInfo{};
    allocatorInfo.physicalDevice = m_physicalDevice;
    allocatorInfo.device = m_device;
    allocatorInfo.instance = m_instance;
    allocatorInfo.vulkanApiVersion = VK_API_VERSION_1_3;

    VkResult result = vmaCreateAllocator(&allocatorInfo, &m_allocator);
    if (result != VK_SUCCESS) {
        LOG_ERROR("Failed to create VMA allocator: {}", static_cast<i32>(result));
        return false;
    }

    LOG_INFO("VMA allocator created");
    return true;
}

}  // namespace engine

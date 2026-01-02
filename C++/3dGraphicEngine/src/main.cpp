#include "core/log.h"
#include "core/types.h"
#include "platform/input.h"
#include "platform/timer.h"
#include "platform/window.h"
#include "render/swapchain.h"
#include "render/vulkan_context.h"

#include <vulkan/vulkan.h>

using namespace engine;

// Simple render loop that clears to a color
class Application {
public:
    bool Init() {
        // Initialize logging
        InitLogging("MathVis");
        LOG_INFO("Starting MathVis Engine v0.1.0");

        // Create window
        WindowConfig windowConfig;
        windowConfig.title = "MathVis Engine";
        windowConfig.width = 1280;
        windowConfig.height = 720;

        if (!m_window.Init(windowConfig)) {
            LOG_ERROR("Failed to create window");
            return false;
        }

        // Initialize Vulkan context
        VulkanContextConfig vkConfig;
        vkConfig.enableValidation = true;
        vkConfig.preferDiscreteGPU = true;

        if (!m_vulkanContext.Init(m_window, vkConfig)) {
            LOG_ERROR("Failed to initialize Vulkan");
            return false;
        }

        // Create swapchain
        SwapchainConfig swapchainConfig;
        swapchainConfig.vsync = true;

        if (!m_swapchain.Init(m_vulkanContext, m_window, swapchainConfig)) {
            LOG_ERROR("Failed to create swapchain");
            return false;
        }

        // Create command pool and buffers
        if (!CreateCommandBuffers()) {
            LOG_ERROR("Failed to create command buffers");
            return false;
        }

        LOG_INFO("Engine initialized successfully");
        return true;
    }

    void Run() {
        m_timer.Reset();

        while (m_window.PollEvents()) {
            m_timer.Tick();

            // Handle input
            if (Input::IsKeyPressed(SDL_SCANCODE_ESCAPE)) {
                break;
            }

            // Handle resize
            if (m_window.WasResized()) {
                m_window.ClearResizedFlag();
                HandleResize();
            }

            // Skip rendering if minimized
            if (m_window.IsMinimized()) {
                continue;
            }

            // Render frame
            RenderFrame();
        }
    }

    void Shutdown() {
        m_vulkanContext.WaitIdle();

        // Destroy command pool
        if (m_commandPool != VK_NULL_HANDLE) {
            vkDestroyCommandPool(m_vulkanContext.GetDevice(), m_commandPool, nullptr);
        }

        m_swapchain.Shutdown();
        m_vulkanContext.Shutdown();
        m_window.Shutdown();

        LOG_INFO("Engine shutdown complete");
    }

private:
    bool CreateCommandBuffers() {
        VkDevice device = m_vulkanContext.GetDevice();

        // Create command pool
        VkCommandPoolCreateInfo poolInfo{};
        poolInfo.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO;
        poolInfo.flags = VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT;
        poolInfo.queueFamilyIndex = m_vulkanContext.GetGraphicsQueueFamily();

        if (vkCreateCommandPool(device, &poolInfo, nullptr, &m_commandPool) != VK_SUCCESS) {
            return false;
        }

        // Allocate command buffers (one per frame in flight)
        m_commandBuffers.resize(Swapchain::MAX_FRAMES_IN_FLIGHT);

        VkCommandBufferAllocateInfo allocInfo{};
        allocInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO;
        allocInfo.commandPool = m_commandPool;
        allocInfo.level = VK_COMMAND_BUFFER_LEVEL_PRIMARY;
        allocInfo.commandBufferCount = static_cast<u32>(m_commandBuffers.size());

        if (vkAllocateCommandBuffers(device, &allocInfo, m_commandBuffers.data()) != VK_SUCCESS) {
            return false;
        }

        return true;
    }

    void HandleResize() {
        m_vulkanContext.WaitIdle();
        m_swapchain.Recreate(m_window.GetWidth(), m_window.GetHeight());
    }

    void RenderFrame() {
        // Acquire next image
        u32 imageIndex;
        VkResult result = m_swapchain.AcquireNextImage(imageIndex);

        if (result == VK_ERROR_OUT_OF_DATE_KHR) {
            HandleResize();
            return;
        } else if (result != VK_SUCCESS && result != VK_SUBOPTIMAL_KHR) {
            LOG_ERROR("Failed to acquire swapchain image");
            return;
        }

        // Record command buffer
        VkCommandBuffer cmd = m_commandBuffers[m_swapchain.GetCurrentFrame()];
        vkResetCommandBuffer(cmd, 0);

        VkCommandBufferBeginInfo beginInfo{};
        beginInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;
        vkBeginCommandBuffer(cmd, &beginInfo);

        // Transition image to color attachment
        VkImageMemoryBarrier barrier{};
        barrier.sType = VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER;
        barrier.srcAccessMask = 0;
        barrier.dstAccessMask = VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT;
        barrier.oldLayout = VK_IMAGE_LAYOUT_UNDEFINED;
        barrier.newLayout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;
        barrier.srcQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
        barrier.dstQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
        barrier.image = GetSwapchainImage(imageIndex);
        barrier.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
        barrier.subresourceRange.baseMipLevel = 0;
        barrier.subresourceRange.levelCount = 1;
        barrier.subresourceRange.baseArrayLayer = 0;
        barrier.subresourceRange.layerCount = 1;

        vkCmdPipelineBarrier(cmd, VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT,
                             VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT, 0, 0, nullptr, 0,
                             nullptr, 1, &barrier);

        // Begin dynamic rendering (Vulkan 1.3)
        VkRenderingAttachmentInfo colorAttachment{};
        colorAttachment.sType = VK_STRUCTURE_TYPE_RENDERING_ATTACHMENT_INFO;
        colorAttachment.imageView = m_swapchain.GetImageView(imageIndex);
        colorAttachment.imageLayout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;
        colorAttachment.loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR;
        colorAttachment.storeOp = VK_ATTACHMENT_STORE_OP_STORE;

        // Animate clear color
        f32 t = m_timer.GetElapsedTimeF();
        colorAttachment.clearValue.color = {
            {0.1f, 0.1f + 0.05f * sinf(t), 0.2f + 0.1f * sinf(t * 0.7f), 1.0f}};

        VkRenderingInfo renderInfo{};
        renderInfo.sType = VK_STRUCTURE_TYPE_RENDERING_INFO;
        renderInfo.renderArea.offset = {0, 0};
        renderInfo.renderArea.extent = m_swapchain.GetExtent();
        renderInfo.layerCount = 1;
        renderInfo.colorAttachmentCount = 1;
        renderInfo.pColorAttachments = &colorAttachment;

        vkCmdBeginRendering(cmd, &renderInfo);

        // Set viewport and scissor
        VkViewport viewport{};
        viewport.x = 0.0f;
        viewport.y = 0.0f;
        viewport.width = static_cast<f32>(m_swapchain.GetExtent().width);
        viewport.height = static_cast<f32>(m_swapchain.GetExtent().height);
        viewport.minDepth = 0.0f;
        viewport.maxDepth = 1.0f;
        vkCmdSetViewport(cmd, 0, 1, &viewport);

        VkRect2D scissor{};
        scissor.offset = {0, 0};
        scissor.extent = m_swapchain.GetExtent();
        vkCmdSetScissor(cmd, 0, 1, &scissor);

        // End rendering
        vkCmdEndRendering(cmd);

        // Transition image to present
        barrier.srcAccessMask = VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT;
        barrier.dstAccessMask = 0;
        barrier.oldLayout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;
        barrier.newLayout = VK_IMAGE_LAYOUT_PRESENT_SRC_KHR;

        vkCmdPipelineBarrier(cmd, VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT,
                             VK_PIPELINE_STAGE_BOTTOM_OF_PIPE_BIT, 0, 0, nullptr, 0, nullptr, 1,
                             &barrier);

        vkEndCommandBuffer(cmd);

        // Submit command buffer
        VkSubmitInfo submitInfo{};
        submitInfo.sType = VK_STRUCTURE_TYPE_SUBMIT_INFO;

        VkSemaphore waitSemaphores[] = {m_swapchain.GetImageAvailableSemaphore()};
        VkPipelineStageFlags waitStages[] = {VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT};
        submitInfo.waitSemaphoreCount = 1;
        submitInfo.pWaitSemaphores = waitSemaphores;
        submitInfo.pWaitDstStageMask = waitStages;
        submitInfo.commandBufferCount = 1;
        submitInfo.pCommandBuffers = &cmd;

        VkSemaphore signalSemaphores[] = {m_swapchain.GetRenderFinishedSemaphore()};
        submitInfo.signalSemaphoreCount = 1;
        submitInfo.pSignalSemaphores = signalSemaphores;

        vkQueueSubmit(m_vulkanContext.GetGraphicsQueue(), 1, &submitInfo,
                      m_swapchain.GetInFlightFence());

        // Present
        result = m_swapchain.Present(imageIndex);

        if (result == VK_ERROR_OUT_OF_DATE_KHR || result == VK_SUBOPTIMAL_KHR) {
            HandleResize();
        }

        m_swapchain.NextFrame();

        // Log FPS periodically
        static f64 lastFpsLog = 0.0;
        if (m_timer.GetElapsedTime() - lastFpsLog > 2.0) {
            LOG_DEBUG("FPS: {:.1f}", m_timer.GetFPS());
            lastFpsLog = m_timer.GetElapsedTime();
        }
    }

    VkImage GetSwapchainImage(u32 imageIndex) {
        // Access swapchain images directly (we need to expose this later)
        VkImage images[8];
        u32 count = 8;
        vkGetSwapchainImagesKHR(m_vulkanContext.GetDevice(), m_swapchain.GetHandle(), &count,
                                images);
        return images[imageIndex];
    }

    Window m_window;
    VulkanContext m_vulkanContext;
    Swapchain m_swapchain;
    Timer m_timer;

    VkCommandPool m_commandPool = VK_NULL_HANDLE;
    std::vector<VkCommandBuffer> m_commandBuffers;
};

int main(int /*argc*/, char* /*argv*/[]) {
    Application app;

    if (!app.Init()) {
        return 1;
    }

    app.Run();
    app.Shutdown();

    return 0;
}

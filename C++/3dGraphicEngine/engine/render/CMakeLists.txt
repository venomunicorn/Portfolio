add_library(engine_render STATIC
    vulkan_context.cpp
    swapchain.cpp
)

target_include_directories(engine_render PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_SOURCE_DIR}/engine
)

target_link_libraries(engine_render PUBLIC
    engine_core
    engine_platform
    Vulkan::Vulkan
    GPUOpen::VulkanMemoryAllocator
)

# stb for image loading
target_include_directories(engine_render PRIVATE
    ${stb_SOURCE_DIR}
)

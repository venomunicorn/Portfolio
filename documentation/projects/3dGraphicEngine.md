# 3D Math Visualization Engine Documentation

**Category**: C++ Systems
**Path**: `C++/3dGraphicEngine`
**Version**: 0.1.0

## Overview
The **3D Math Visualization Engine** (internally "MathVis") is a high-performance **Vulkan-based** rendering engine designed for educational math videos. It leverages **C++20** and modern Vulkan 1.3 features (Dynamic Rendering) to provide a robust platform for real-time 3D graphics.

## Key Features

### 1. Rendering Architecture
- **Vulkan Backend**: Direct hardware abstraction using the Vulkan API.
- **Dynamic Rendering**: Utilizes Vulkan 1.3 dynamic rendering to simplify render pass management (no traditional `VkRenderPass` objects).
- **Swapchain Management**: Handles window resizing, present modes (VSync), and double/triple buffering.
- **Shader Pipeline**: Automated SPIR-V compilation using `glslangValidator`.

### 2. Core Systems
- **Windowing**: Integrated with **SDL2** for cross-platform window creation and event handling.
- **Math Library**: Uses **GLM** for vector and matrix mathematics.
- **Logging System**: Custom `spdlog`-based logging for debugging and runtime info.
- **Memory Management**: Integration with **VulkanMemoryAllocator (VMA)**.

### 3. Web Demo
- **Canvas 3D**: A lightweight HTML5/Canvas demo (`demo.html`) is provided to visualize 3D projection concepts (rotation matrices, perspective projection) directly in the browser without compiling the engine.
- **Interactive Controls**: Sliders for rotation (X, Y) and zoom, plus shape switching (Cube, Pyramid, Octahedron).

## Architecture

### Directory Structure
```
3dGraphicEngine/
├── engine/
│   ├── core/       # Logger, Types, Assertions
│   ├── platform/   # Window (SDL2), Input, Timer
│   └── render/     # VulkanContext, Swapchain, Shader Management
├── shaders/        # GLSL Shader source code and compiled SPIR-V
├── src/
│   └── main.cpp    # Application entry point & Render Loop
├── CMakeLists.txt  # Build configuration
└── demo.html       # Web-based projection demo
```

### Dependencies
- **Vulkan SDK**: 1.3+
- **SDL2**: Windowing & Input
- **GLM**: Mathematics
- **spdlog**: Fast logging
- **VulkanMemoryAllocator**: GPU memory management
- **stb**: Image loading (via FetchContent)

## Setup & Compilation

### Prerequisites
- Visual Studio 2022 (C++20 support required)
- CMake 3.25+
- Vulkan SDK installed
- Vcpkg for dependencies

### Build Instructions
1.  **Install dependencies**:
    ```powershell
    vcpkg install sdl2 glm spdlog vulkan-memory-allocator
    ```
2.  **Configure**:
    ```powershell
    mkdir build && cd build
    cmake .. -DCMAKE_TOOLCHAIN_FILE="<vcpkg_root>/scripts/buildsystems/vcpkg.cmake"
    ```
3.  **Build**:
    ```powershell
    cmake --build . --config Release
    ```
4.  **Run**:
    The executable `MathVisEngine.exe` will be in `build/bin/Release`.

## Web Demo Usage
Since the C++ engine requires a GPU environment, a JavaScript version is available for quick visualization of the underlying math concepts.
- Open `demo.html` in any modern web browser.
- Use the **Shape** dropdown to switch geometries.
- Use sliders to rotate and zoom the 3D wireframes.

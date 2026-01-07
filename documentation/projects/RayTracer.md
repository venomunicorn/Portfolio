# Ray Tracer Documentation

**Category**: C++ Systems
**Path**: `C++/RayTracer`
**Version**: 1.0

## Overview
The **Ray Tracer** is a computer graphics project that renders a 3D image by simulating the physical path of light rays. The C++ application generates a static image file (`output.ppm`) showing a red sphere floating in a sky-like gradient, demonstrating fundamental 3D math and file output techniques.

## Key Features

### 1. Rendering Engine (C++)
- **Ray-Sphere Intersection**: Uses the quadratic formula to calculate if and where a light ray hits a sphere geometry.
- **PPM Image Output**: Writes a raw Portable Pixel Map (`.ppm`) file, a simple ASCII image format that requires no external libraries to generate.
- **Vector Mathematics**: Implements a custom `Vec3` struct to handle 3D coordinates, dot products, and vector normalization.
- **Gradient Background**: Generates a linear gradient (blue to white) for rays that miss all objects, simulating a sky.

### 2. Live Web Demo
The web demo is a significantly more advanced implementation of the same math, running in real-time in the browser:
- **Reflections**: Recursive ray tracing allows spheres to reflect each other and the environment.
- **Shadows**: Simple shadow casting logic creates depth and realism.
- **Animation**: The "Animate" button moves the spheres in a sinusoidal pattern to prove the renderer's speed.
- **Interactive Controls**:
  - **Color Pickers**: Change the material color of the two spheres dynamically.
  - **Lighting Control**: Move the light source along the X-axis to see how shadows shift.
  - **Reflectivity Slider**: Adjust how shiny (mirror-like) surfaces are.

## Architecture

### Directory Structure
```
RayTracer/
├── main.cpp    # C++ Static Renderer
└── demo.html   # Real-time Web Ray Tracer
```

### Core Math (`main.cpp`)
The ray-sphere intersection is solved using the discriminant of the quadratic equation:
$$b^2 - 4ac$$
- If `discriminant > 0`: The ray hits the sphere (2 intersection points).
- If `discriminant < 0`: The ray misses.
- `ir, ig, ib` (Integer Red/Green/Blue) values are calculated for each pixel and written to the output stream.

## Setup & Compilation

### Prerequisites
- Standard C++ Compiler
- An image viewer that supports `.ppm` files (e.g., IrfanView, GIMP) or an online converter.

### Build Instructions
1.  **Navigate directly**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\C++\RayTracer"
    ```
2.  **Compile**:
    ```powershell
    g++ main.cpp -o raytracer
    ```
3.  **Run**:
    ```powershell
    .\raytracer
    ```

### Viewing Results
- After running, a file named `output.ppm` will be created in the same directory.
- Open this file to see the rendered sphere.

## Web Demo Usage
- Open `demo.html` in a modern web browser (Canvas API required).
- **Modify Scene**: Use the color inputs to change the sphere colors.
- **Lighting**: Drag the "Light X Position" slider to change the lighting angle.
- **Animate**: Click "Animate" to see the ray tracer updating at 60 FPS (performance depends on device).

#pragma once

#include <cstdint>
#include <glm/glm.hpp>
#include <glm/gtc/quaternion.hpp>

namespace engine {

// Common type aliases
using u8 = uint8_t;
using u16 = uint16_t;
using u32 = uint32_t;
using u64 = uint64_t;

using i8 = int8_t;
using i16 = int16_t;
using i32 = int32_t;
using i64 = int64_t;

using f32 = float;
using f64 = double;

// GLM vector aliases
using Vec2 = glm::vec2;
using Vec3 = glm::vec3;
using Vec4 = glm::vec4;

using Vec2i = glm::ivec2;
using Vec3i = glm::ivec3;
using Vec4i = glm::ivec4;

using Vec2u = glm::uvec2;
using Vec3u = glm::uvec3;
using Vec4u = glm::uvec4;

// Matrix aliases
using Mat3 = glm::mat3;
using Mat4 = glm::mat4;

// Quaternion
using Quat = glm::quat;

// Color (RGBA float)
struct Color {
    f32 r = 1.0f;
    f32 g = 1.0f;
    f32 b = 1.0f;
    f32 a = 1.0f;

    constexpr Color() = default;
    constexpr Color(f32 r, f32 g, f32 b, f32 a = 1.0f) : r(r), g(g), b(b), a(a) {}

    static constexpr Color White() { return {1.0f, 1.0f, 1.0f, 1.0f}; }
    static constexpr Color Black() { return {0.0f, 0.0f, 0.0f, 1.0f}; }
    static constexpr Color Red() { return {1.0f, 0.0f, 0.0f, 1.0f}; }
    static constexpr Color Green() { return {0.0f, 1.0f, 0.0f, 1.0f}; }
    static constexpr Color Blue() { return {0.0f, 0.0f, 1.0f, 1.0f}; }
    static constexpr Color Yellow() { return {1.0f, 1.0f, 0.0f, 1.0f}; }
    static constexpr Color Cyan() { return {0.0f, 1.0f, 1.0f, 1.0f}; }
    static constexpr Color Magenta() { return {1.0f, 0.0f, 1.0f, 1.0f}; }
    static constexpr Color Clear() { return {0.0f, 0.0f, 0.0f, 0.0f}; }

    Vec4 ToVec4() const { return {r, g, b, a}; }
};

}  // namespace engine

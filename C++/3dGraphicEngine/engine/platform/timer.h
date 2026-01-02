#pragma once

#include "core/types.h"

#include <chrono>

namespace engine {

// High-resolution timer for frame timing and profiling
class Timer {
public:
    using Clock = std::chrono::high_resolution_clock;
    using TimePoint = Clock::time_point;
    using Duration = std::chrono::duration<f64>;

    Timer();

    // Update the timer (call once per frame)
    void Tick();

    // Reset the timer
    void Reset();

    // Getters
    [[nodiscard]] f64 GetDeltaTime() const { return m_deltaTime; }
    [[nodiscard]] f64 GetElapsedTime() const { return m_elapsedTime; }
    [[nodiscard]] f32 GetDeltaTimeF() const { return static_cast<f32>(m_deltaTime); }
    [[nodiscard]] f32 GetElapsedTimeF() const { return static_cast<f32>(m_elapsedTime); }
    [[nodiscard]] u64 GetFrameCount() const { return m_frameCount; }

    // Average FPS over recent frames
    [[nodiscard]] f64 GetFPS() const { return m_fps; }

private:
    TimePoint m_startTime;
    TimePoint m_lastTick;
    f64 m_deltaTime = 0.0;
    f64 m_elapsedTime = 0.0;
    u64 m_frameCount = 0;

    // FPS calculation
    static constexpr f64 FPS_UPDATE_INTERVAL = 0.5;  // Update FPS every 0.5 seconds
    f64 m_fpsAccumulator = 0.0;
    u32 m_fpsFrameCount = 0;
    f64 m_fps = 0.0;
};

// Fixed timestep timer for offline/deterministic rendering
class FixedTimer {
public:
    explicit FixedTimer(f64 fixedDeltaTime = 1.0 / 60.0);

    // Advance to next frame
    void Step();

    // Reset to frame 0
    void Reset();

    // Set fixed delta time (e.g., 1/60 for 60fps)
    void SetFixedDeltaTime(f64 dt) { m_fixedDeltaTime = dt; }

    // Getters
    [[nodiscard]] f64 GetTime() const { return m_time; }
    [[nodiscard]] f64 GetDeltaTime() const { return m_fixedDeltaTime; }
    [[nodiscard]] u64 GetFrame() const { return m_frame; }

    // Helper to get time for a specific frame
    [[nodiscard]] f64 GetTimeForFrame(u64 frame) const { return frame * m_fixedDeltaTime; }

private:
    f64 m_fixedDeltaTime;
    f64 m_time = 0.0;
    u64 m_frame = 0;
};

}  // namespace engine

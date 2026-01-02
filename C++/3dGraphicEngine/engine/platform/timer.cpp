#include "timer.h"

namespace engine {

Timer::Timer() {
    Reset();
}

void Timer::Tick() {
    TimePoint now = Clock::now();
    Duration elapsed = now - m_lastTick;
    m_lastTick = now;

    m_deltaTime = elapsed.count();
    m_elapsedTime = Duration(now - m_startTime).count();
    m_frameCount++;

    // Update FPS counter
    m_fpsAccumulator += m_deltaTime;
    m_fpsFrameCount++;

    if (m_fpsAccumulator >= FPS_UPDATE_INTERVAL) {
        m_fps = m_fpsFrameCount / m_fpsAccumulator;
        m_fpsAccumulator = 0.0;
        m_fpsFrameCount = 0;
    }
}

void Timer::Reset() {
    m_startTime = Clock::now();
    m_lastTick = m_startTime;
    m_deltaTime = 0.0;
    m_elapsedTime = 0.0;
    m_frameCount = 0;
    m_fpsAccumulator = 0.0;
    m_fpsFrameCount = 0;
    m_fps = 0.0;
}

// FixedTimer implementation

FixedTimer::FixedTimer(f64 fixedDeltaTime)
    : m_fixedDeltaTime(fixedDeltaTime) {}

void FixedTimer::Step() {
    m_frame++;
    m_time = m_frame * m_fixedDeltaTime;
}

void FixedTimer::Reset() {
    m_frame = 0;
    m_time = 0.0;
}

}  // namespace engine

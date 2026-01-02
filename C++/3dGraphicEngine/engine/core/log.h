#pragma once

#include <spdlog/spdlog.h>

#include <string_view>

namespace engine {

// Log levels matching spdlog
enum class LogLevel { Trace, Debug, Info, Warn, Error, Critical };

// Initialize the logging system
void InitLogging(const char* appName = "MathVis");

// Get the logger instance
spdlog::logger* GetLogger();

}  // namespace engine

// Logging macros for convenience
#define LOG_TRACE(...) SPDLOG_LOGGER_TRACE(::engine::GetLogger(), __VA_ARGS__)
#define LOG_DEBUG(...) SPDLOG_LOGGER_DEBUG(::engine::GetLogger(), __VA_ARGS__)
#define LOG_INFO(...) SPDLOG_LOGGER_INFO(::engine::GetLogger(), __VA_ARGS__)
#define LOG_WARN(...) SPDLOG_LOGGER_WARN(::engine::GetLogger(), __VA_ARGS__)
#define LOG_ERROR(...) SPDLOG_LOGGER_ERROR(::engine::GetLogger(), __VA_ARGS__)
#define LOG_CRITICAL(...) SPDLOG_LOGGER_CRITICAL(::engine::GetLogger(), __VA_ARGS__)

#include "log.h"

#include <spdlog/sinks/stdout_color_sinks.h>

#include <memory>

namespace engine {

static std::shared_ptr<spdlog::logger> s_logger;

void InitLogging(const char* appName) {
    // Create console sink with colors
    auto consoleSink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
    consoleSink->set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%^%l%$] [%s:%#] %v");

    // Create logger with console sink
    s_logger = std::make_shared<spdlog::logger>(appName, consoleSink);

#ifdef NDEBUG
    s_logger->set_level(spdlog::level::info);
#else
    s_logger->set_level(spdlog::level::trace);
#endif

    // Register as default logger
    spdlog::set_default_logger(s_logger);

    LOG_INFO("Logging initialized: {}", appName);
}

spdlog::logger* GetLogger() {
    return s_logger.get();
}

}  // namespace engine

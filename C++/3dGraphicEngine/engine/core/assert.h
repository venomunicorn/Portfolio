#pragma once

#include "log.h"

#include <cstdlib>

namespace engine {

// Debug break - platform specific
#if defined(_MSC_VER)
#define DEBUG_BREAK() __debugbreak()
#elif defined(__clang__) || defined(__GNUC__)
#define DEBUG_BREAK() __builtin_trap()
#else
#define DEBUG_BREAK() std::abort()
#endif

}  // namespace engine

// Assert that always runs (even in release)
#define ASSERT_ALWAYS(condition, ...)                                     \
    do {                                                                  \
        if (!(condition)) {                                               \
            LOG_CRITICAL("Assertion failed: {} at {}:{}", #condition,     \
                         __FILE__, __LINE__);                             \
            LOG_CRITICAL(__VA_ARGS__);                                    \
            DEBUG_BREAK();                                                \
        }                                                                 \
    } while (false)

// Assert that only runs in debug builds
#ifdef NDEBUG
#define ASSERT(condition, ...) ((void)0)
#else
#define ASSERT(condition, ...) ASSERT_ALWAYS(condition, __VA_ARGS__)
#endif

// Verify - like assert but expression is always evaluated
#define VERIFY(condition, ...)                                            \
    do {                                                                  \
        if (!(condition)) {                                               \
            LOG_ERROR("Verification failed: {} at {}:{}", #condition,     \
                      __FILE__, __LINE__);                                \
        }                                                                 \
    } while (false)

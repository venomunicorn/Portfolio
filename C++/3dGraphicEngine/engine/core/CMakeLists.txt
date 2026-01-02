add_library(engine_core STATIC
    log.cpp
    types.h
    assert.h
)

target_include_directories(engine_core PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_SOURCE_DIR}/engine
)

target_link_libraries(engine_core PUBLIC
    spdlog::spdlog
)

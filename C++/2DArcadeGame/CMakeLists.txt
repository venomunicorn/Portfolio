cmake_minimum_required(VERSION 3.16)
project(2DArcadeGame VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find SFML
find_package(SFML 2.5 COMPONENTS system window graphics audio REQUIRED)

# Source files
set(SOURCES
    src/main.cpp
    src/core/Game.cpp
    src/core/GameLoop.cpp
    src/core/Camera.cpp
    src/states/TitleState.cpp
    src/states/PlayingState.cpp
    src/states/GameOverState.cpp
    src/states/HighScoreState.cpp
    src/states/SettingsState.cpp
    src/entities/Entity.cpp
    src/entities/Player.cpp
    src/entities/Enemy.cpp
    src/entities/Projectile.cpp
    src/entities/PowerUp.cpp
    src/entities/Boss.cpp
    src/systems/CollisionSystem.cpp
    src/systems/InputSystem.cpp
    src/systems/SpawnSystem.cpp
    src/effects/ParticleSystem.cpp
    src/audio/AudioManager.cpp
    src/save/SaveManager.cpp
    src/ui/HUD.cpp
)

# Header files
set(HEADERS
    src/core/Game.h
    src/core/GameLoop.h
    src/core/Camera.h
    src/core/Config.h
    src/states/GameState.h
    src/states/TitleState.h
    src/states/PlayingState.h
    src/states/GameOverState.h
    src/states/HighScoreState.h
    src/states/SettingsState.h
    src/entities/Entity.h
    src/entities/Player.h
    src/entities/Enemy.h
    src/entities/Projectile.h
    src/entities/PowerUp.h
    src/entities/Boss.h
    src/systems/CollisionSystem.h
    src/systems/InputSystem.h
    src/systems/SpawnSystem.h
    src/effects/ParticleSystem.h
    src/audio/AudioManager.h
    src/save/SaveManager.h
    src/ui/HUD.h
    src/utils/Math.h
)

# Create executable
add_executable(${PROJECT_NAME} ${SOURCES} ${HEADERS})

# Include directories
target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_SOURCE_DIR}/src)

# Link SFML
target_link_libraries(${PROJECT_NAME} PRIVATE 
    sfml-system 
    sfml-window 
    sfml-graphics 
    sfml-audio
)

# Copy assets to build directory
file(COPY ${CMAKE_SOURCE_DIR}/assets DESTINATION ${CMAKE_BINARY_DIR})
file(COPY ${CMAKE_SOURCE_DIR}/config DESTINATION ${CMAKE_BINARY_DIR})

# Compiler warnings
if(MSVC)
    target_compile_options(${PROJECT_NAME} PRIVATE /W4)
else()
    target_compile_options(${PROJECT_NAME} PRIVATE -Wall -Wextra -Wpedantic)
endif()

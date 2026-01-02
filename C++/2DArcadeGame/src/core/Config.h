#pragma once

// ============================================
// Game Configuration Constants
// ============================================

namespace Config {

// Window settings
constexpr int WINDOW_WIDTH = 1280;
constexpr int WINDOW_HEIGHT = 720;
constexpr const char* WINDOW_TITLE = "2D Arcade Game";
constexpr bool VSYNC_ENABLED = true;

// Game loop settings
constexpr float FIXED_TIMESTEP = 1.0f / 60.0f;  // 60 updates per second
constexpr int MAX_UPDATES_PER_FRAME = 5;         // Prevent spiral of death

// Player settings
constexpr float PLAYER_SPEED = 300.0f;
constexpr float PLAYER_ACCELERATION = 1500.0f;
constexpr float PLAYER_FRICTION = 800.0f;
constexpr float PLAYER_SIZE = 32.0f;
constexpr int PLAYER_MAX_HEALTH = 100;
constexpr float PLAYER_INVULNERABILITY_TIME = 1.5f;
constexpr float PLAYER_FIRE_RATE = 0.15f;  // Seconds between shots

// Projectile settings
constexpr float PROJECTILE_SPEED = 600.0f;
constexpr float PROJECTILE_SIZE = 8.0f;
constexpr float PROJECTILE_LIFETIME = 2.0f;
constexpr int MAX_PROJECTILES = 100;

// Enemy settings
constexpr float ENEMY_SPEED = 120.0f;
constexpr float ENEMY_SIZE = 28.0f;
constexpr int ENEMY_HEALTH = 30;
constexpr int ENEMY_DAMAGE = 15;
constexpr int ENEMY_SCORE_VALUE = 100;
constexpr int MAX_ENEMIES = 50;

// Spawner settings
constexpr float INITIAL_SPAWN_DELAY = 2.0f;
constexpr float MIN_SPAWN_DELAY = 0.3f;
constexpr float SPAWN_DELAY_DECREASE_RATE = 0.02f;  // Per second

// Scoring
constexpr int SCORE_PER_KILL = 100;
constexpr float COMBO_TIMEOUT = 2.0f;
constexpr float COMBO_MULTIPLIER_INCREMENT = 0.25f;
constexpr float MAX_COMBO_MULTIPLIER = 5.0f;

// Colors (RGBA)
namespace Colors {
    constexpr unsigned int PLAYER = 0x4FC3F7FF;      // Light blue
    constexpr unsigned int ENEMY = 0xEF5350FF;        // Red
    constexpr unsigned int PROJECTILE = 0xFFEB3BFF;   // Yellow
    constexpr unsigned int BACKGROUND = 0x1A1A2EFF;   // Dark blue
    constexpr unsigned int HUD_TEXT = 0xFFFFFFFF;     // White
    constexpr unsigned int HEALTH_BAR = 0x66BB6AFF;   // Green
    constexpr unsigned int HEALTH_BAR_BG = 0x424242FF;// Dark gray
}

} // namespace Config

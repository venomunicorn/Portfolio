#include "SpawnSystem.h"
#include "core/Config.h"
#include "utils/Math.h"

SpawnSystem::SpawnSystem()
    : m_spawnTimer(0.0f)
    , m_spawnDelay(Config::INITIAL_SPAWN_DELAY)
    , m_elapsedTime(0.0f)
    , m_waveNumber(1)
    , m_enemiesSpawned(0)
    , m_enemiesKilledSinceLastPowerUp(0)
{
}

void SpawnSystem::reset() {
    m_spawnTimer = 0.0f;
    m_spawnDelay = Config::INITIAL_SPAWN_DELAY;
    m_elapsedTime = 0.0f;
    m_waveNumber = 1;
    m_enemiesSpawned = 0;
    m_enemiesKilledSinceLastPowerUp = 0;
}

void SpawnSystem::update(float deltaTime, const sf::Vector2f& playerPosition,
                         std::vector<std::unique_ptr<Enemy>>& enemies) {
    m_elapsedTime += deltaTime;
    m_spawnTimer += deltaTime;
    
    // Increase difficulty over time
    m_spawnDelay = std::max(Config::MIN_SPAWN_DELAY,
                            Config::INITIAL_SPAWN_DELAY - m_elapsedTime * Config::SPAWN_DELAY_DECREASE_RATE);
    
    // Update wave number based on time
    m_waveNumber = 1 + static_cast<int>(m_elapsedTime / 30.0f);  // New wave every 30 seconds
    
    // Spawn enemies
    if (m_spawnTimer >= m_spawnDelay) {
        m_spawnTimer = 0.0f;
        
        // Count active enemies
        int activeEnemies = 0;
        for (const auto& enemy : enemies) {
            if (enemy->isActive()) activeEnemies++;
        }
        
        // Only spawn if under limit
        if (activeEnemies < Config::MAX_ENEMIES) {
            spawnEnemy(playerPosition, enemies);
            
            // Sometimes spawn multiple in later waves
            if (m_waveNumber >= 3 && Math::randomFloat(0, 1) < 0.3f) {
                spawnEnemy(playerPosition, enemies);
            }
        }
    }
}

EnemyType SpawnSystem::getRandomEnemyType() {
    // Early game: mostly chasers
    if (m_waveNumber <= 2) {
        return EnemyType::Chaser;
    }
    
    // Mid game: introduce shooters
    if (m_waveNumber <= 4) {
        float roll = Math::randomFloat(0, 1);
        if (roll < 0.7f) return EnemyType::Chaser;
        return EnemyType::Shooter;
    }
    
    // Later: all types
    float roll = Math::randomFloat(0, 1);
    if (roll < 0.4f) return EnemyType::Chaser;
    if (roll < 0.6f) return EnemyType::Shooter;
    if (roll < 0.8f) return EnemyType::Bomber;
    return EnemyType::Tank;
}

PowerUpType SpawnSystem::getRandomPowerUpType() {
    float roll = Math::randomFloat(0, 1);
    if (roll < 0.35f) return PowerUpType::Health;
    if (roll < 0.55f) return PowerUpType::SpeedBoost;
    if (roll < 0.75f) return PowerUpType::RapidFire;
    if (roll < 0.90f) return PowerUpType::Shield;
    return PowerUpType::ScoreBonus;
}

sf::Vector2f SpawnSystem::getSpawnPosition() {
    // Spawn from screen edges
    int edge = Math::randomInt(0, 3);
    float x, y;
    
    switch (edge) {
        case 0: // Top
            x = Math::randomFloat(0, Config::WINDOW_WIDTH);
            y = -30.0f;
            break;
        case 1: // Right
            x = Config::WINDOW_WIDTH + 30.0f;
            y = Math::randomFloat(0, Config::WINDOW_HEIGHT);
            break;
        case 2: // Bottom
            x = Math::randomFloat(0, Config::WINDOW_WIDTH);
            y = Config::WINDOW_HEIGHT + 30.0f;
            break;
        default: // Left
            x = -30.0f;
            y = Math::randomFloat(0, Config::WINDOW_HEIGHT);
            break;
    }
    
    return sf::Vector2f(x, y);
}

void SpawnSystem::spawnEnemy(const sf::Vector2f& playerPosition,
                              std::vector<std::unique_ptr<Enemy>>& enemies) {
    // Find inactive enemy or create new one
    Enemy* enemy = nullptr;
    for (auto& e : enemies) {
        if (!e->isActive()) {
            enemy = e.get();
            break;
        }
    }
    
    if (!enemy && enemies.size() < Config::MAX_ENEMIES) {
        enemies.push_back(std::make_unique<Enemy>());
        enemy = enemies.back().get();
    }
    
    if (enemy) {
        EnemyType type = getRandomEnemyType();
        enemy->spawn(getSpawnPosition(), type);
        enemy->setTarget(playerPosition);
        m_enemiesSpawned++;
    }
}

void SpawnSystem::spawnPowerUp(const sf::Vector2f& position,
                                std::vector<std::unique_ptr<PowerUp>>& powerUps) {
    m_enemiesKilledSinceLastPowerUp++;
    
    // Spawn power-up every 5-8 kills
    if (m_enemiesKilledSinceLastPowerUp >= Math::randomInt(5, 8)) {
        m_enemiesKilledSinceLastPowerUp = 0;
        
        // Find inactive power-up or create new one
        PowerUp* powerUp = nullptr;
        for (auto& p : powerUps) {
            if (!p->isActive()) {
                powerUp = p.get();
                break;
            }
        }
        
        if (!powerUp && powerUps.size() < 10) {
            powerUps.push_back(std::make_unique<PowerUp>());
            powerUp = powerUps.back().get();
        }
        
        if (powerUp) {
            powerUp->spawn(position, getRandomPowerUpType());
        }
    }
}

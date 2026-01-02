#pragma once

#include "entities/Enemy.h"
#include "entities/PowerUp.h"
#include <vector>
#include <memory>

class SpawnSystem {
public:
    SpawnSystem();
    
    void update(float deltaTime, const sf::Vector2f& playerPosition,
                std::vector<std::unique_ptr<Enemy>>& enemies);
    
    void spawnPowerUp(const sf::Vector2f& position,
                      std::vector<std::unique_ptr<PowerUp>>& powerUps);
    
    void reset();
    
    int getWaveNumber() const { return m_waveNumber; }
    float getElapsedTime() const { return m_elapsedTime; }
    
private:
    sf::Vector2f getSpawnPosition();
    EnemyType getRandomEnemyType();
    PowerUpType getRandomPowerUpType();
    void spawnEnemy(const sf::Vector2f& playerPosition,
                    std::vector<std::unique_ptr<Enemy>>& enemies);
    
    float m_spawnTimer;
    float m_spawnDelay;
    float m_elapsedTime;
    int m_waveNumber;
    int m_enemiesSpawned;
    int m_enemiesKilledSinceLastPowerUp;
};

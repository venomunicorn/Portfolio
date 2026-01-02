#pragma once

#include "entities/Player.h"
#include "entities/Enemy.h"
#include "entities/Projectile.h"
#include "entities/PowerUp.h"
#include <vector>
#include <memory>

class CollisionSystem {
public:
    struct CollisionResult {
        bool playerHit = false;
        bool playerDamagedByExplosion = false;
        int enemiesKilled = 0;
        int scoreGained = 0;
        std::vector<sf::Vector2f> enemyDeathPositions;  // For power-up spawning
        bool powerUpCollected = false;
    };
    
    static CollisionResult update(
        Player& player,
        std::vector<std::unique_ptr<Enemy>>& enemies,
        std::vector<std::unique_ptr<Projectile>>& projectiles,
        std::vector<std::unique_ptr<PowerUp>>& powerUps
    );
    
private:
    static void handlePlayerEnemyCollision(Player& player, Enemy& enemy, CollisionResult& result);
    static void handleProjectileEnemyCollision(Projectile& proj, Enemy& enemy, CollisionResult& result);
    static void handlePlayerPowerUpCollision(Player& player, PowerUp& powerUp, CollisionResult& result);
    static void handleBomberExplosion(Player& player, Enemy& bomber, CollisionResult& result);
};

#include "CollisionSystem.h"
#include "core/Config.h"

CollisionSystem::CollisionResult CollisionSystem::update(
    Player& player,
    std::vector<std::unique_ptr<Enemy>>& enemies,
    std::vector<std::unique_ptr<Projectile>>& projectiles,
    std::vector<std::unique_ptr<PowerUp>>& powerUps
) {
    CollisionResult result;
    
    // Player vs PowerUps
    for (auto& powerUp : powerUps) {
        if (!powerUp->isActive()) continue;
        handlePlayerPowerUpCollision(player, *powerUp, result);
    }
    
    for (auto& enemy : enemies) {
        if (!enemy->isActive()) continue;
        
        // Check bomber explosions
        if (enemy->isExploding()) {
            handleBomberExplosion(player, *enemy, result);
            continue;
        }
        
        // Player vs Enemy
        if (!player.isInvulnerable()) {
            handlePlayerEnemyCollision(player, *enemy, result);
        }
        
        // Projectiles vs Enemy
        for (auto& proj : projectiles) {
            if (!proj->isActive()) continue;
            handleProjectileEnemyCollision(*proj, *enemy, result);
        }
    }
    
    return result;
}

void CollisionSystem::handlePlayerEnemyCollision(Player& player, Enemy& enemy, CollisionResult& result) {
    Math::AABB playerBounds = player.getBounds();
    Math::AABB enemyBounds = enemy.getBounds();
    
    if (playerBounds.intersects(enemyBounds)) {
        // Bombers explode on contact
        if (enemy.getType() == EnemyType::Bomber) {
            enemy.triggerExplosion();
        }
        
        player.takeDamage(enemy.getContactDamage());
        player.makeInvulnerable(Config::PLAYER_INVULNERABILITY_TIME);
        player.resetCombo();
        
        // Knockback player away from enemy
        sf::Vector2f knockback = player.getPosition() - enemy.getPosition();
        knockback = Math::normalize(knockback) * 150.0f;
        player.setVelocity(knockback);
        
        result.playerHit = true;
    }
}

void CollisionSystem::handleProjectileEnemyCollision(Projectile& proj, Enemy& enemy, CollisionResult& result) {
    Math::AABB projBounds = proj.getBounds();
    Math::AABB enemyBounds = enemy.getBounds();
    
    if (projBounds.intersects(enemyBounds)) {
        enemy.takeDamage(proj.getDamage());
        proj.setActive(false);
        
        if (enemy.isDead()) {
            result.enemiesKilled++;
            result.scoreGained += enemy.getScoreValue();
            result.enemyDeathPositions.push_back(enemy.getPosition());
            
            // Bomber doesn't deactivate immediately - it explodes
            if (enemy.getType() != EnemyType::Bomber) {
                enemy.setActive(false);
            }
        }
    }
}

void CollisionSystem::handlePlayerPowerUpCollision(Player& player, PowerUp& powerUp, CollisionResult& result) {
    Math::AABB playerBounds = player.getBounds();
    Math::AABB powerUpBounds = {
        powerUp.getPosition().x - 12.0f,
        powerUp.getPosition().y - 12.0f,
        24.0f, 24.0f
    };
    
    if (playerBounds.intersects(powerUpBounds)) {
        player.applyPowerUp(powerUp);
        powerUp.setActive(false);
        result.powerUpCollected = true;
    }
}

void CollisionSystem::handleBomberExplosion(Player& player, Enemy& bomber, CollisionResult& result) {
    if (!player.isInvulnerable()) {
        float dist = Math::distance(player.getPosition(), bomber.getPosition());
        if (dist < bomber.getExplosionRadius()) {
            player.takeDamage(bomber.getContactDamage());
            player.makeInvulnerable(Config::PLAYER_INVULNERABILITY_TIME);
            player.resetCombo();
            
            // Strong knockback from explosion
            sf::Vector2f knockback = player.getPosition() - bomber.getPosition();
            knockback = Math::normalize(knockback) * 250.0f;
            player.setVelocity(knockback);
            
            result.playerDamagedByExplosion = true;
        }
    }
}

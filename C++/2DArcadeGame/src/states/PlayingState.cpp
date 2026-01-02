#include "PlayingState.h"
#include "GameOverState.h"
#include "core/Game.h"
#include "core/Config.h"
#include "audio/AudioManager.h"
#include <cstdlib>
#include <ctime>

PlayingState::PlayingState(Game& game)
    : GameState(game)
    , m_particles(500)
    , m_paused(false)
    , m_hitStopTimer(0.0f)
    , m_lastWaveForBoss(0)
    , m_bossActive(false)
    , m_bossWarningTimer(0.0f)
{
}

void PlayingState::init() {
    std::srand(static_cast<unsigned>(std::time(nullptr)));
    
    m_hud.init();
    
    AudioManager::getInstance().playMusic("assets/audio/game_music.ogg", true);
    
    if (!m_font.loadFromFile("assets/fonts/arcade.ttf")) {
        m_font.loadFromFile("C:/Windows/Fonts/arial.ttf");
    }
    
    m_pauseText.setFont(m_font);
    m_pauseText.setString("PAUSED\nPress ESC to Resume");
    m_pauseText.setCharacterSize(48);
    m_pauseText.setFillColor(sf::Color::White);
    
    sf::FloatRect bounds = m_pauseText.getLocalBounds();
    m_pauseText.setOrigin(bounds.width / 2.0f, bounds.height / 2.0f);
    m_pauseText.setPosition(Config::WINDOW_WIDTH / 2.0f, Config::WINDOW_HEIGHT / 2.0f);
    
    // Boss warning text
    m_bossWarningText.setFont(m_font);
    m_bossWarningText.setString("WARNING: BOSS APPROACHING!");
    m_bossWarningText.setCharacterSize(40);
    m_bossWarningText.setFillColor(sf::Color::Red);
    sf::FloatRect warnBounds = m_bossWarningText.getLocalBounds();
    m_bossWarningText.setOrigin(warnBounds.width / 2.0f, warnBounds.height / 2.0f);
    m_bossWarningText.setPosition(Config::WINDOW_WIDTH / 2.0f, Config::WINDOW_HEIGHT / 2.0f);
    
    m_enemies.reserve(Config::MAX_ENEMIES);
    m_projectiles.reserve(Config::MAX_PROJECTILES);
    m_enemyProjectiles.reserve(100);
    m_powerUps.reserve(10);
}

void PlayingState::handleEvent(const sf::Event& event) {
    if (event.type == sf::Event::KeyPressed) {
        if (event.key.code == sf::Keyboard::Escape) {
            m_paused = !m_paused;
            AudioManager::getInstance().playSound("pause");
            if (m_paused) {
                AudioManager::getInstance().pauseMusic();
            } else {
                AudioManager::getInstance().resumeMusic();
            }
        }
    }
}

void PlayingState::spawnBoss() {
    if (!m_boss) {
        m_boss = std::make_unique<Boss>();
    }
    m_boss->spawn(sf::Vector2f(Config::WINDOW_WIDTH / 2.0f, -100.0f));
    m_bossActive = true;
    m_bossWarningTimer = 3.0f;
    
    // Clear regular enemies for boss fight
    for (auto& enemy : m_enemies) {
        enemy->setActive(false);
    }
    
    AudioManager::getInstance().stopMusic();
    AudioManager::getInstance().playMusic("assets/audio/boss_music.ogg", true);
}

void PlayingState::updateBoss(float deltaTime) {
    if (!m_boss || !m_boss->isActive()) return;
    
    m_boss->setTarget(m_player.getPosition());
    m_boss->update(deltaTime);
    
    // Spawn boss projectiles
    while (m_boss->hasProjectilesToSpawn()) {
        auto [pos, dir] = m_boss->popProjectile();
        
        Projectile* bullet = nullptr;
        for (auto& proj : m_enemyProjectiles) {
            if (!proj->isActive()) {
                bullet = proj.get();
                break;
            }
        }
        
        if (!bullet && m_enemyProjectiles.size() < 100) {
            m_enemyProjectiles.push_back(std::make_unique<Projectile>());
            bullet = m_enemyProjectiles.back().get();
        }
        
        if (bullet) {
            bullet->fire(pos, dir);
            bullet->setVelocity(dir * 250.0f);
        }
    }
    
    // Spawn minions
    if (m_boss->wantsToSpawnMinion()) {
        sf::Vector2f spawnPos = m_boss->getMinionSpawnPosition();
        
        Enemy* enemy = nullptr;
        for (auto& e : m_enemies) {
            if (!e->isActive()) {
                enemy = e.get();
                break;
            }
        }
        
        if (!enemy && m_enemies.size() < Config::MAX_ENEMIES) {
            m_enemies.push_back(std::make_unique<Enemy>());
            enemy = m_enemies.back().get();
        }
        
        if (enemy) {
            enemy->spawn(spawnPos, EnemyType::Chaser);
            enemy->setTarget(m_player.getPosition());
            m_particles.emitExplosion(spawnPos, sf::Color::Magenta, 10);
        }
    }
    
    // Boss collision with player
    if (!m_player.isInvulnerable() && m_boss->isIntroComplete()) {
        Math::AABB playerBounds = m_player.getBounds();
        Math::AABB bossBounds = m_boss->getBounds();
        
        if (playerBounds.intersects(bossBounds)) {
            m_player.takeDamage(30);
            m_player.makeInvulnerable(Config::PLAYER_INVULNERABILITY_TIME);
            m_player.resetCombo();
            
            sf::Vector2f knockback = m_player.getPosition() - m_boss->getPosition();
            m_player.setVelocity(Math::normalize(knockback) * 200.0f);
            
            m_camera.shake(12.0f, 0.2f);
            m_particles.emitHit(m_player.getPosition(), sf::Color::White, 15);
            AudioManager::getInstance().playSound("damage");
        }
    }
    
    // Player projectiles hitting boss
    for (auto& proj : m_projectiles) {
        if (!proj->isActive()) continue;
        
        Math::AABB projBounds = proj->getBounds();
        Math::AABB bossBounds = m_boss->getBounds();
        
        if (projBounds.intersects(bossBounds)) {
            m_boss->takeDamage(proj->getDamage());
            proj->setActive(false);
            m_particles.emitHit(proj->getPosition(), sf::Color(255, 100, 255), 5);
            AudioManager::getInstance().playSound("hit", 60.0f);
            
            if (m_boss->isDead()) {
                m_player.addScore(m_boss->getScoreValue());
                m_camera.shake(20.0f, 0.5f);
                m_particles.emitDeath(m_boss->getPosition(), 50);
                AudioManager::getInstance().playSound("explosion");
            }
        }
    }
    
    // Check if boss died
    if (!m_boss->isActive() && m_bossActive) {
        m_bossActive = false;
        AudioManager::getInstance().stopMusic();
        AudioManager::getInstance().playMusic("assets/audio/game_music.ogg", true);
    }
}

void PlayingState::update(float deltaTime) {
    if (m_paused) return;
    
    // Boss warning countdown
    if (m_bossWarningTimer > 0.0f) {
        m_bossWarningTimer -= deltaTime;
    }
    
    if (m_hitStopTimer > 0.0f) {
        m_hitStopTimer -= deltaTime;
        m_particles.update(deltaTime);
        return;
    }
    
    m_camera.update(deltaTime);
    m_particles.update(deltaTime);
    
    m_player.update(deltaTime);
    
    // Handle shooting with sound
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::Space)) {
        size_t prevCount = m_projectiles.size();
        int prevActive = 0;
        for (const auto& p : m_projectiles) {
            if (p->isActive()) prevActive++;
        }
        
        m_player.shoot(m_projectiles);
        
        int nowActive = 0;
        for (const auto& p : m_projectiles) {
            if (p->isActive()) nowActive++;
        }
        
        if (nowActive > prevActive || m_projectiles.size() > prevCount) {
            AudioManager::getInstance().playSound("shoot", 60.0f, 0.9f + static_cast<float>(rand() % 20) / 100.0f);
        }
    }
    
    // Spawn boss every 5 waves if not already fighting one
    int currentWave = m_spawner.getWaveNumber();
    if (!m_bossActive && currentWave > 0 && currentWave % 5 == 0 && currentWave != m_lastWaveForBoss) {
        m_lastWaveForBoss = currentWave;
        spawnBoss();
    }
    
    // Update boss
    if (m_bossActive) {
        updateBoss(deltaTime);
    }
    
    // Update enemies if not in boss fight
    if (!m_bossActive) {
        for (auto& enemy : m_enemies) {
            if (enemy->isActive()) {
                enemy->setTarget(m_player.getPosition());
                enemy->update(deltaTime);
            }
        }
        
        handleEnemyShooting();
        m_spawner.update(deltaTime, m_player.getPosition(), m_enemies);
    } else {
        // Still update active enemies during boss (minions)
        for (auto& enemy : m_enemies) {
            if (enemy->isActive()) {
                enemy->setTarget(m_player.getPosition());
                enemy->update(deltaTime);
            }
        }
    }
    
    for (auto& proj : m_projectiles) {
        proj->update(deltaTime);
    }
    
    for (auto& proj : m_enemyProjectiles) {
        proj->update(deltaTime);
    }
    
    for (auto& powerUp : m_powerUps) {
        powerUp->update(deltaTime);
    }
    
    auto result = CollisionSystem::update(m_player, m_enemies, m_projectiles, m_powerUps);
    
    if (result.scoreGained > 0) {
        m_player.addScore(result.scoreGained);
    }
    
    if (result.playerHit) {
        m_camera.shake(8.0f, 0.15f);
        m_hitStopTimer = 0.05f;
        m_particles.emitHit(m_player.getPosition(), sf::Color::White, 10);
        AudioManager::getInstance().playSound("damage");
    }
    
    if (result.playerDamagedByExplosion) {
        m_camera.shake(15.0f, 0.25f);
        m_hitStopTimer = 0.08f;
        m_particles.emitExplosion(m_player.getPosition(), sf::Color(255, 150, 50), 25);
        AudioManager::getInstance().playSound("explosion");
    }
    
    if (result.enemiesKilled > 0) {
        m_camera.shake(3.0f, 0.08f);
    }
    
    for (const auto& pos : result.enemyDeathPositions) {
        m_spawner.spawnPowerUp(pos, m_powerUps);
        m_particles.emitDeath(pos, 20);
        AudioManager::getInstance().playSound("hit", 80.0f, 0.8f + static_cast<float>(rand() % 40) / 100.0f);
    }
    
    if (result.powerUpCollected) {
        m_particles.emitPickup(m_player.getPosition(), sf::Color(100, 255, 100), 15);
        AudioManager::getInstance().playSound("powerup");
    }
    
    // Enemy projectiles hitting player
    if (!m_player.isInvulnerable()) {
        for (auto& proj : m_enemyProjectiles) {
            if (!proj->isActive()) continue;
            
            Math::AABB playerBounds = m_player.getBounds();
            Math::AABB projBounds = proj->getBounds();
            
            if (playerBounds.intersects(projBounds)) {
                m_player.takeDamage(10);
                m_player.makeInvulnerable(Config::PLAYER_INVULNERABILITY_TIME);
                m_player.resetCombo();
                proj->setActive(false);
                m_camera.shake(6.0f, 0.12f);
                m_particles.emitHit(m_player.getPosition(), sf::Color(255, 100, 100), 8);
                AudioManager::getInstance().playSound("damage");
            }
        }
    }
    
    m_hud.update(m_player, m_spawner);
    checkGameOver();
}

void PlayingState::handleEnemyShooting() {
    for (auto& enemy : m_enemies) {
        if (!enemy->isActive()) continue;
        if (!enemy->canShoot()) continue;
        
        enemy->resetShootTimer();
        
        Projectile* bullet = nullptr;
        for (auto& proj : m_enemyProjectiles) {
            if (!proj->isActive()) {
                bullet = proj.get();
                break;
            }
        }
        
        if (!bullet && m_enemyProjectiles.size() < 100) {
            m_enemyProjectiles.push_back(std::make_unique<Projectile>());
            bullet = m_enemyProjectiles.back().get();
        }
        
        if (bullet) {
            bullet->fire(enemy->getPosition(), enemy->getShootDirection());
            bullet->setVelocity(bullet->getVelocity() * 0.6f);
            m_particles.emitHit(enemy->getPosition(), sf::Color(255, 200, 100), 4);
            AudioManager::getInstance().playSound("shoot", 40.0f, 0.7f);
        }
    }
}

void PlayingState::checkGameOver() {
    if (m_player.isDead()) {
        m_particles.emitDeath(m_player.getPosition(), 40);
        AudioManager::getInstance().stopMusic();
        m_game.changeState(std::make_unique<GameOverState>(m_game, m_player.getScore(), m_spawner.getWaveNumber()));
    }
}

void PlayingState::render(sf::RenderWindow& window) {
    m_camera.apply(window);
    
    for (auto& powerUp : m_powerUps) {
        powerUp->render(window);
    }
    
    for (auto& proj : m_projectiles) {
        proj->render(window);
    }
    
    for (auto& proj : m_enemyProjectiles) {
        if (proj->isActive()) {
            sf::RectangleShape enemyBullet;
            enemyBullet.setSize(sf::Vector2f(10, 10));
            enemyBullet.setOrigin(5, 5);
            enemyBullet.setPosition(proj->getPosition());
            enemyBullet.setFillColor(sf::Color(255, 100, 100));
            window.draw(enemyBullet);
        }
    }
    
    for (auto& enemy : m_enemies) {
        enemy->render(window);
    }
    
    if (m_boss && m_boss->isActive()) {
        m_boss->render(window);
    }
    
    m_player.render(window);
    m_particles.render(window);
    
    m_camera.reset(window);
    
    m_hud.render(window);
    
    // Boss warning
    if (m_bossWarningTimer > 0.0f) {
        float alpha = std::sin(m_bossWarningTimer * 10.0f) * 127.0f + 128.0f;
        m_bossWarningText.setFillColor(sf::Color(255, 0, 0, static_cast<sf::Uint8>(alpha)));
        window.draw(m_bossWarningText);
    }
    
    if (m_paused) {
        sf::RectangleShape overlay(sf::Vector2f(Config::WINDOW_WIDTH, Config::WINDOW_HEIGHT));
        overlay.setFillColor(sf::Color(0, 0, 0, 150));
        window.draw(overlay);
        window.draw(m_pauseText);
    }
}

void PlayingState::pause() {
    m_paused = true;
    AudioManager::getInstance().pauseMusic();
}

void PlayingState::resume() {
    m_paused = false;
    AudioManager::getInstance().resumeMusic();
}

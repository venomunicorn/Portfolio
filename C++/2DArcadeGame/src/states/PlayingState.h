#pragma once

#include "GameState.h"
#include "entities/Player.h"
#include "entities/Enemy.h"
#include "entities/Projectile.h"
#include "entities/PowerUp.h"
#include "entities/Boss.h"
#include "systems/CollisionSystem.h"
#include "systems/SpawnSystem.h"
#include "core/Camera.h"
#include "effects/ParticleSystem.h"
#include "ui/HUD.h"
#include <vector>
#include <memory>

class PlayingState : public GameState {
public:
    explicit PlayingState(Game& game);
    
    void init() override;
    void handleEvent(const sf::Event& event) override;
    void update(float deltaTime) override;
    void render(sf::RenderWindow& window) override;
    
    void pause() override;
    void resume() override;
    
private:
    void checkGameOver();
    void handleEnemyShooting();
    void updateBoss(float deltaTime);
    void spawnBoss();
    
    Player m_player;
    std::vector<std::unique_ptr<Enemy>> m_enemies;
    std::vector<std::unique_ptr<Projectile>> m_projectiles;
    std::vector<std::unique_ptr<Projectile>> m_enemyProjectiles;
    std::vector<std::unique_ptr<PowerUp>> m_powerUps;
    std::unique_ptr<Boss> m_boss;
    
    SpawnSystem m_spawner;
    Camera m_camera;
    ParticleSystem m_particles;
    HUD m_hud;
    
    bool m_paused;
    float m_hitStopTimer;
    int m_lastWaveForBoss;
    bool m_bossActive;
    
    sf::Text m_pauseText;
    sf::Text m_bossWarningText;
    sf::Font m_font;
    float m_bossWarningTimer;
};

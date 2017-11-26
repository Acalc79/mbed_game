import pygame, sys
import random as rand
import json
from graphics import Graphics, GraphicsObjT, GraphicsParam
from objects import GameObjT, Player, Shield, Enemy, Collectible, PlayerBullet, EnemyBullet, Background
from time import sleep

PLAYER_W = 30
PLAYER_H = 30
SHIELD_W = 85
SHIELD_H = 85
SHIELD_HP = 2
ENEMY_W = 40
ENEMY_H = 28
ENEMY_HP = 3
BULLET_W = 6
BULLET_H = 10
ENEMY_SPAWN_FREQ = 0.015
ENEMY_SHOOT_FREQ = 0.015
GAME_PACE = 1.5
SCROLL_SPEED = 1
INPUT_PERIOD = 5
SHIELD_HUMIDITY = 40

## difficulty levels:
## 1 - easy
## 2 - normal
## 3 - hard
class Game:
    def __init__(self, check_for_input, difficulty):
        self.check_for_input = check_for_input
        self.input = None
        self.width = 2*320
        self.height = 2*240
        self.score = 0
        self.active = False
        self.difficulty = difficulty
        self.delta_t = GAME_PACE * self.difficulty
        self.score = 0
        self.elems = []
        self.to_remove = []
        self.player = Player(self.width/2, self.height - 2*PLAYER_H,
                             PLAYER_W, PLAYER_H, self.game_lost)
        self.shield = None
        self.background = Background(0, SCROLL_SPEED, 0, 0, self.width, self.height)
        self.elems.append(self.player)
        self.elems.append(self.background)
        
    def check_inputs(self):
        self.check_for_input()
        if self.input is not None:
            i = self.input
            if 'x' in i and 'y' in i:
                self.player.speed((i['x'], i['y']))
            if 'btn' in i and i['btn'] is 1:
                self.shoot_player_bullet()
            if 'hum' in i and i['hum'] > SHIELD_HUMIDITY:
                self.create_shield()
            self.input = None
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.active = False
                self.close()

    def create_shield(self):
        if self.shield is not None:
            if self.shield in self.to_remove:
                self.to_remove.remove(self.shield)
            if self.shield in self.elems:
                self.elems.remove(self.shield)
                self.graphics.remove(self.shield)
        x = self.player.x() + self.player.w()/2 - SHIELD_W/2
        y = self.player.y() + self.player.h()/2 - SHIELD_H/2
        self.shield = Shield(x, y, SHIELD_W, SHIELD_H, SHIELD_HP)
        def destroy_shield():
            self.to_remove.append(self.shield)
        self.shield.destruct = destroy_shield
        self.elems.insert(1, self.shield)
        self.graphics.add_element_at(1, GraphicsObjT.SPHERE, self.shield)

    def shoot_player_bullet(self):
        x = self.player.x() + self.player.w()/2
        y = self.player.y()
        bullet = PlayerBullet(0, -1, x, y, BULLET_W, BULLET_H)
        def destroy_bullet():
            self.to_remove.append(bullet)
        bullet.destruct = destroy_bullet
        self.elems.append(bullet)
        self.graphics.add_element(GraphicsObjT.BULLET, bullet)

    def shoot_enemy_bullet(self, enemy):
        x = enemy.x() + enemy.w()/2
        y = enemy.y() + enemy.h()
        bullet = EnemyBullet(0, 1.6, x, y, BULLET_W, BULLET_H)
        def destroy_bullet():
            self.to_remove.append(bullet)
        bullet.destruct = destroy_bullet
        self.elems.append(bullet)
        self.graphics.add_element(GraphicsObjT.DOWN_BULLET, bullet)
    
    def close(self):
        self.graphics.close()
        sys.exit()

    def game_lost(self):
        self.close()
    
    def initialize_game(self):
        self.graphics = Graphics(self.score, self.width, self.height)
        self.graphics.add_element(GraphicsObjT.BACKGROUND, self.background)
        self.graphics.add_element(GraphicsObjT.SPACESHIP, self.player)

    def handle_borders(self, elem):
        if elem.type() is GameObjT.PLAYER:
            if elem.x() < 0:
                elem.x(0)
            elif elem.x()+elem.w() > self.width:
                elem.x(self.width - elem.w())
            if elem.y() < 0:
                elem.y(0)
            elif elem.y()+elem.h() > self.height:
                elem.y(self.height - elem.h())
        else:
            if elem.x() < 0 or elem.x()+elem.w() > self.width:
                elem.bounce_x()
            elif elem.y() > self.height or elem.y() + elem.h() < 0:
                self.to_remove.append(elem)
    
    def update_state(self):
        
        if rand.random() < ENEMY_SPAWN_FREQ * self.difficulty:
            self.attempt_to_create_enemy()
        
        for elem in self.elems:
            elem.update(self.delta_t)
            self.handle_borders(elem)
        
        if self.shield is not None:
            x = self.player.x() + self.player.w()/2 - SHIELD_W/2
            y = self.player.y() + self.player.h()/2 - SHIELD_H/2
            self.shield.pos((x, y))
        
        for i in range(len(self.elems)):
            for j in range(i+1, len(self.elems)):
                self.elems[i].do_collision_check(self.elems[j])
        self.remove_unnecessary()

    def attempt_to_create_enemy(self):
        vx = rand.choice([-1, 0, 1])
        vy = SCROLL_SPEED
        def enemy_tries_to_fire(enemy):
            if rand.random() < ENEMY_SHOOT_FREQ * self.difficulty:
                self.shoot_enemy_bullet(enemy)
        enemy = Enemy(enemy_tries_to_fire, ENEMY_HP, vx, vy, self.width, ENEMY_W, ENEMY_H)
        def destroy_enemy():
            enemy.hp -= 1
            if enemy.hp <= 0:
                self.score += 1
                self.to_remove.append(enemy)
                enemy.dead = True
        enemy.destruct = destroy_enemy
        for elem in self.elems:
            if enemy.collides_with(elem):
                break
        else:
            self.shoot_enemy_bullet(enemy)
            self.elems.append(enemy)
            self.graphics.add_element(GraphicsObjT.ALIEN, enemy)

    def remove_unnecessary(self):
        for elem in self.to_remove:
            self.to_remove.remove(elem)
            if elem in self.elems:
                self.elems.remove(elem)
                self.graphics.remove(elem)
            if elem is self.shield:
                self.shield = None
    
    def mainloop(self):
        i = 0
        while self.active:
            if i % INPUT_PERIOD is 0:
                self.check_inputs()
            self.update_state()
            self.graphics.draw(self.score)
            i += 1

    def start_game(self):
        self.initialize_game()
        self.active = True
        self.mainloop()

if __name__ == '__main__':
    Game().start_game(lambda: None)

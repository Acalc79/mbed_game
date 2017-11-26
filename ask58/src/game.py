import pygame, sys
import random as rand
import json
from graphics import Graphics, GraphicsObjT, GraphicsParam
from objects import Player, Enemy, Collectible, PlayerBullet, Background

PLAYER_W = 30
PLAYER_H = 30
ENEMY_W = 40
ENEMY_H = 28
BULLET_W = 6
BULLET_H = 10
ENEMY_SPAWN_FREQ = 0.004
GAME_PACE = 1
SCROLL_SPEED = 1
INPUT_PERIOD = 5

## difficulty levels:
## 1 - easy
## 2 - normal
## 3 - hard
class Game:
    def __init__(self, check_for_input):
        self.check_for_input = check_for_input
        self.input = None
        self.width = 2*320
        self.height = 2*240
        self.score = 0
        self.active = False
        self.difficulty = 2
        self.delta_t = GAME_PACE * self.difficulty
        self.elems = []
        self.player = Player(self.width/2, self.height - 2*PLAYER_H,
                             PLAYER_W, PLAYER_H, self.game_lost)
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
                x_bullet = self.player.x() + self.player.w()/2
                y_bullet = self.player.y()
                self.add_bullet(0, -1, x_bullet, y_bullet)
            self.input = None
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.active = False
                self.close()

    def add_bullet(self, vx, vy, x, y):
        bullet = PlayerBullet(vx, vy, lambda: 0, x, y, BULLET_W, BULLET_H)
        self.elems.append(bullet)
        self.graphics.add_element(GraphicsObjT.BULLET, bullet)
        
    def close(self):
        self.graphics.close()
        sys.exit()

    def game_lost(self):
        self.close()
    
    def initialize_game(self):
        self.graphics = Graphics(self.width, self.height)
        self.graphics.add_element(GraphicsObjT.BACKGROUND, self.background)
        self.graphics.add_element(GraphicsObjT.SPACESHIP, self.player)

    def handle_borders(self, elem):
        if elem.x() < 0 or elem.x()+elem.w() > self.width:
            elem.bounce_x()
        elif elem.y() > self.height or elem.y() + elem.h() < 0:
            self.elems.remove(elem)
            self.graphics.remove(elem)
    
    def update_state(self):
        if rand.random() < ENEMY_SPAWN_FREQ * self.difficulty:
            self.attempt_to_create_enemy()
        
        for elem in self.elems:
            elem.update(self.delta_t)
            self.handle_borders(elem)
        
        for i in range(len(self.elems)):
            for j in range(i+1, len(self.elems)):
                self.elems[i].do_collision_check(self.elems[j])

    def attempt_to_create_enemy(self):
        vx = rand.choice([-1, 0, 1])
        vy = SCROLL_SPEED
        enemy = Enemy(vx, vy, lambda: 0, self.width, ENEMY_W, ENEMY_H)
        for elem in self.elems:
            if enemy.collides_with(elem):
                break
        else:
            self.elems.append(enemy)
            self.graphics.add_element(GraphicsObjT.ALIEN, enemy)
        
    def mainloop(self):
        i = 0
        while self.active:
            if i % INPUT_PERIOD is 0:
                self.check_inputs()
            self.update_state()
            self.graphics.draw()
            i += 1

    def start_game(self):
        self.initialize_game()
        self.active = True
        self.mainloop()

if __name__ == '__main__':
    Game().start_game()

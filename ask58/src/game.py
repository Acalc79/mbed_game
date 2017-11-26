import pygame, sys
import random as rand
from graphics import Graphics, GraphicsObjT, GraphicsParam
from objects import Player, Enemy, Collectible, Bullet, Background

PLAYER_W = 30
PLAYER_H = 30
ENEMY_W = 40
ENEMY_H = 28
ENEMY_SPAWN_FREQ = 0.004
GAME_PACE = 0.3
SCROLL_SPEED = 1

## difficulty levels:
## 1 - easy
## 2 - normal
## 3 - hard
class Game:
    def __init__(self):
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.active = False
                self.close()

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
        elif elem.y() > self.height:
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
        enemy.debug = True
        for elem in self.elems:
            if enemy.collides_with(elem):
                break
        else:
            self.elems.append(enemy)
            self.graphics.add_element(GraphicsObjT.ALIEN, enemy)
        
    def mainloop(self):
        while self.active:
            self.check_inputs()
            self.update_state()
            self.graphics.draw()

    def start_game(self):
        self.initialize_game()
        self.active = True
        self.mainloop()

if __name__ == '__main__':
    Game().start_game()

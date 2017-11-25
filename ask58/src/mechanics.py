import pygame, sys
from graphics import Graphics
pygame.init()

speed = [2, 2]
size = width, height = 3*320, 3*240

graphics = Graphics(width, height)
# ball = None

class Elem:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

def check_inputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            graphics.close()
            sys.exit()
    
def init():
    global ball
    ball = Elem(0, 0, 10, 10)
    graphics.add_element("ball", ball)

def update_state():
    global ball
    ball.x += speed[0]
    ball.y += speed[1]
    if ball.x < 0 or ball.x > width:
        speed[0] = -speed[0]
    if ball.y < 0 or ball.y > height:
        speed[1] = -speed[1]
    
def mainloop():
    while True:
        check_inputs()
        update_state()
        graphics.draw({'speed': 1})

def main():
    init()
    mainloop()

main()

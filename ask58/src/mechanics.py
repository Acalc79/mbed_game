import pygame, sys
from graphics import Graphics
pygame.init()

speed = [2, 2]
size = width, height = 3*320, 3*240

graphics = Graphics(width, height)
# ball = None

class Wrapper:
    def __init__(self, getx, gety):
        self.getx = getx
        self.gety = gety

def check_inputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            graphics.close()
            sys.exit()
    
def init():
    global ball
    ball = {'x': 0, 'y':0}
    element = Wrapper(lambda: ball['x'], lambda: ball['y'])
    graphics.add_element("ball", element)

def update_state():
    global ball
    ball['x'] += speed[0]
    ball['y'] += speed[1]
    if ball['x'] < 0 or ball['x'] > width:
        speed[0] = -speed[0]
    if ball['y'] < 0 or ball['y'] > height:
        speed[1] = -speed[1]
    
def mainloop():
    while True:
        check_inputs()
        update_state()
        graphics.draw({'speed': 1})

init()
mainloop()

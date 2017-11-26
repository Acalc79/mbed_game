import sys, pygame
from enum import Enum, unique, auto

@unique
class GraphicsParam(Enum):
    SCROLL_SPEED = auto()

@unique
class GraphicsObjT(Enum):
    SPACESHIP = auto()
    ALIEN = auto()
    BALL = auto()
    BULLET = auto()
    COIN = auto()
    SPHERE = auto()
    BACKGROUND = auto()
        
IMAGES = {GraphicsObjT.BALL: "../res/ball.bmp",
          GraphicsObjT.ALIEN: "../res/alien.png",
          GraphicsObjT.SPACESHIP: "../res/spaceship.jpg",
          GraphicsObjT.BACKGROUND: "../res/background.jpg"}
BLACK = 0, 0, 0

# interface with the world
class Graphics:
    
    # initialize graphics          
    def __init__(self, width, height):
        pygame.init()
        self.size = width, height
        self.screen = pygame.display.set_mode(self.size)
        self.elements = []
        self.elem_map = {}
        
    # add element
    # the element must have a get_type() method
    # and also x(), y(), w() and h() methods
    # get_type() deterimnes what kind of image is used, i.e. 'spaceship'
    def add_element(self, elem_type, element):
        filename = IMAGES[elem_type]
        if(elem_type is GraphicsObjT.BACKGROUND):
            drawable_elem = Background(filename, element, self.size)
        elif(elem_type is not None):
            drawable_elem = Drawable(filename, element)
        self.elem_map[element] = drawable_elem
        self.elements.append(drawable_elem)

    def remove(self, elem):
        self.elements.remove(self.elem_map[elem])
    
    # draws all graphics objects
    # params are a dictionary of constants not associated with objects
    # i.e. speed of background scrolling
    # exact format TBD
    def draw(self):
        self.screen.fill(BLACK)
        for elem in self.elements:
            elem.draw(self.screen)
        pygame.display.flip()
        
    # closes graphics window, should only be called by game window
    def close(self):
        pygame.display.quit()
        

class Drawable:
    
    def __init__(self, filename, elem):
        self.surf = pygame.image.load(filename)
        self.e = elem
        
    def draw(self, screen):
        img = pygame.transform.scale(self.surf, (self.e.w(), self.e.h()))
        screen.blit(img, (self.e.x(), self.e.y()))

class Background(Drawable):

    def __init__(self, filename, elem, size):
        original_size = pygame.image.load(filename)
        self.w, self.h = size
        self.e = elem
        self.img = pygame.transform.scale(original_size, (self.w, self.h))

    def draw(self, screen):
        x = self.e.x() % self.w
        y = self.e.y() % self.h
        screen.blit(self.img, dest=(x,y))
        screen.blit(self.img, dest=(x,y - self.h))
        screen.blit(self.img, dest=(x - self.w,y))
        screen.blit(self.img, dest=(x - self.w,y - self.h))

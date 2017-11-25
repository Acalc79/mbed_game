import sys, pygame
        
BACKGROUND = "../res/background.jpg"
IMAGES = {"ball": "../res/ball.bmp",
          "enemy": "../res/alien.png"}
BLACK = 0, 0, 0

# interface with the world
class Graphics:
    # initialize graphics          
    def __init__(self, width, height):
        self.size = width, height
        self.screen = pygame.display.set_mode(self.size)
        self.background = Background(BACKGROUND, self.size)
        self.elements = []
    # add element
    # the element needs to have either
    # .x, .y, .w and .h fields (like pygame.Rect)
    # or .getx(), .gety(), .getw() and .geth() methods
    # elem_type deterimnes what kind of image is used, i.e. 'spaceship'
    def add_element(self, elem_type, element):
        filename = IMAGES[elem_type]
        wrapped = Wrapper(element)
        getx = wrapped.getfunc('x')
        gety = wrapped.getfunc('y')
        getw = wrapped.getfunc('w')
        geth = wrapped.getfunc('h')
        if(elem_type is not None):
            drawable_elem = Drawable(filename, getx, gety, getw, geth)
            self.elements.append(drawable_elem)
    # draws all graphics objects
    # params are a dictionary of constants not associated with objects
    # i.e. speed of background scrolling
    # exact format TBD
    def draw(self, params):
        self.screen.fill(BLACK)
        self.background.draw(self.screen)
        self.background.scroll_down(params['speed'])
        for elem in self.elements:
            elem.draw(self.screen)
        pygame.display.flip()
    # closes graphics window, should only be called by game window
    def close(self):
        pygame.display.quit()

class Drawable:
    
    def __init__(self, filename, getx, gety, getw, geth):
        self.surf = pygame.image.load(filename)
        self.getx = getx
        self.gety = gety
        self.getw = getw
        self.geth = geth
        
    def draw(self, screen):
        img = pygame.transform.scale(self.surf, (self.getw(), self.geth()))
        screen.blit(img, (self.getx(), self.gety()))

class Wrapper:
    def __init__(self, elem):
        self.elem = elem
    def getfunc(self, name):
        if hasattr(self.elem, 'get'+name):
            return getattr(self.elem, 'get'+name)
        else:
            return lambda: getattr(self.elem, name)
        

class Background:

    def __init__(self, filename, size):
        original_size = pygame.image.load(filename)
        self.img = pygame.transform.scale(original_size, size)
        self.h = size[1]
        self.y = 0
    
    def scroll_down(self, amount):
        self.y = (self.y + amount) % self.h

    def draw(self, screen):
        screen.blit(self.img, dest=(0,self.y))
        screen.blit(self.img, dest=(0,self.y - self.h))

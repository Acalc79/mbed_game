import sys, pygame
        
BACKGROUND = "../res/background.jpg"
IMAGES = {"ball": "../res/ball.bmp"}
BLACK = 0, 0, 0

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
    def __init__(self, getx, gety, getw, geth):
        self.getx = getx
        self.gety = gety
        self.getw = getw
        self.geth = geth

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
        if not (hasattr(element, 'getx') and hasattr(element, 'gety')):
            arg_elem = element
            element = Wrapper(lambda: arg_elem.x,
                              lambda: arg_elem.y,
                              lambda: arg_elem.w,
                              lambda: arg_elem.h)
        if(elem_type == "ball"):
            drawable_elem = Drawable(filename,
                                     element.getx, element.gety,
                                     element.getw, element.geth)
            self.elements.append(drawable_elem)
    # draws all graphics objects
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

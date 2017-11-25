import sys, pygame
        
BACKGROUND = "../res/background.jpg"
IMAGES = {"ball": "../res/ball.bmp"}
BLACK = 0, 0, 0

class Drawable:
    
    def __init__(self, filename, getx, gety):
        self.surf = pygame.image.load(filename)
        self.getx = getx
        self.gety = gety
        
    def draw(self, screen):
        screen.blit(self.surf, (self.getx(), self.gety()))

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
        
class Graphics:
                         
    def __init__(self, width, height):
        self.size = width, height
        self.screen = pygame.display.set_mode(self.size)
        self.background = Background(BACKGROUND, self.size)
        self.elements = []

    def add_element(self, elem_type, element):
        filename = IMAGES[elem_type]
        if(elem_type == "ball"):
            drawable_elem = Drawable(filename, element.getx, element.gety)
            self.elements.append(drawable_elem)

    def draw(self, params):
        self.screen.fill(BLACK)
        self.background.draw(self.screen)
        self.background.scroll_down(params['speed'])
        for elem in self.elements:
            elem.draw(self.screen)
        pygame.display.flip()

    def close(self):
        pygame.display.quit()

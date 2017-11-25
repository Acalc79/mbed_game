class Player(GameObject):
    """ This class represents the player """
    
    def __init__(self):
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 60
        height = 30
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
        
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user turns the mbed to the left  """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user turns the mbed to the right """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user holds the mbed in an approximately horizontal position, need to set a range """
        self.change_x = 0
 
    """ # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
 
            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x """        
        

class Enemy(GameObject):
        
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super().__init__()
     
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
     
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
     
        # Instance variables that control the edges of where we bounce
        self.left_boundary = 0
        self.right_boundary = 0
        self.top_boundary = 0
        self.bottom_boundary = 0
     
        # Instance variables for our current speed and direction
        self.change_x = 0
        self.change_y = 0
     
    def update_enemy(self):
        """ Called each frame. """
        self.rect.x += self.change_x
        """ self.rect.y += self.change_y # moving horizontally"""
     
        if self.rect.right >= self.right_boundary or self.rect.left <= self.left_boundary:
            self.change_x *= -1
     
        """ if self.rect.bottom >= self.bottom_boundary or self.rect.top <= self.top_boundary:
            self.change_y *= -1 #moving horizontally"""
            
class GameObject:
    def update(self):
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
            
class Bullet:
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
     
        self.image = pygame.Surface([4, 10])
        self.image.fill(BLACK)
     
        self.rect = self.image.get_rect()
     
    def update(self):
        """ Move the bullet. """
        self.rect.y -= 3    

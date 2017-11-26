# --- Sprite lists
 
# This is a list of every sprite. All enemies and the player block as well.
all_sprites_list = pygame.sprite.Group()
 
# List of each enemy in the game
enemy_list = pygame.sprite.Group()
 
# List of each bullet
bullet_list = pygame.sprite.Group()

# --- Create the sprites
 
for i in range(10):
    # This represents an enemy
    enemy = Enemy(RED, 30, 15)
    # Set a location for the enemy for a fixed interval
    enemy.rect.x = (screen_width/9)*i 
    enemy.rect.y = screen_height - 50 # can be changed depending on enemy size
 
    # Add the enemy to the list of objects
    enemy_list.add(enemy)
    all_sprites_list.add(enemy)

# Create a red player
player = Player()
all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    # get the y-axis reading directly from Mbed 
    if MMA.y < -0.5:
        # Steer player to the right
        player.change_x = 3
    
    #get the y-axis reading directly from Mbed
    elif MMA.y > 0.5:
        # Steer player to the left
        player.change_x = -3
            
    elif mySwitch = 3.3: # get the button input
        # Fire a bullet if the user clicks the SW0/SW1 button
        bullet = Bullet()
        # Set the bullet so it is where the player is
        bullet.rect.x = player.rect.x
        bullet.rect.y = player.rect.y
        # Add the bullet to the lists
        all_sprites_list.add(bullet)
        bullet_list.add(bullet)
 
    # --- Game logic
 
    # Call the update() method on all the sprites
    all_sprites_list.update()
 
    # Calculate mechanics for each bullet
    for bullet in bullet_list:
 
        # See if it hit an enemy
        block_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)
 
        # For each enemy hit, remove the bullet and add to the score (and possibly remove the enemy)
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            enemy_list.remove(enemy)
            all_sprites_list.remove(enemy)
            score += 1
            print(score)
 
        # Remove the bullet if it flies up off the screen
        if bullet.rect.y > screen_height:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
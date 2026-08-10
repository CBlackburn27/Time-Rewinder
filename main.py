import pygame
import sys # import sys module to handle system exit
from collections import deque # import deque to store the player's state history
from enum import Enum


pygame.init()

pygame.mouse.set_visible(False) #sets mouse as invisible to allow crosshair to be seen

screen = pygame.display.set_mode((1280, 729), pygame.RESIZABLE) # create a resizable window
pygame.display.set_caption("Rewind Run") 

clock = pygame.time.Clock() #create a clock object to control the frame rate



#loading background 

level_1_background = pygame.image.load('level_1_background.png')
level_1_background = pygame.transform.scale(level_1_background, (1280, 729))
rewind_bar_frame = pygame.image.load('rewind_bar_frame.png')


#loading ui
button_img = pygame.image.load("button.png")
button_img = pygame.transform.scale(button_img, (250, 80))
cursor_img = pygame.image.load("crosshair_color_b.png")
cursor_img = pygame.transform.scale(cursor_img, (32, 32))

menu_font = pygame.font.Font("Kenney Future.ttf", 20)


# colors
white = (255, 255, 255)
blue = (50, 100, 255)
grey = (119, 123, 126)
red = (255, 80, 80)


# physics
gravity = 1200
movement_speed = 300
jump_force = -500


tile_size = 32


world_data = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,11,11,13,0,0,0,0,0,0,0],
[0,15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[12,11,11,11,11,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,12,11,11,11,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,5,7,0,0,0,0,0,0,6,5,5,5,7,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,2,2,2,3,0,0,0,0,0,0],
[6,5,7,0,0,0,0,0,0,0,0,0,0,0,0,6,5,7,0,0,0,0,0,0,0,0,0,0,0,0,0,8,2,2,2,3,0,0,0,0,0,0,0],
[8,2,3,0,0,0,0,0,0,6,5,7,0,0,0,8,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,8,2,2,2,3,0,0,0,0,0,0,0],
[8,2,3,5,5,7,0,0,0,8,2,3,0,0,0,8,2,3,6,5,7,0,0,0,0,0,0,0,0,0,0,8,2,2,2,3,0,0,0,0,0,0,0],
[8,2,3,2,2,3,0,0,0,8,2,3,0,0,0,0,0,0,8,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[8,2,3,2,2,3,9,9,9,8,2,3,0,0,0,0,0,0,8,2,3,0,0,0,0,0,0,12,11,13,0,0,0,0,0,0,0,0,0,0,0,0],
[8,2,3,2,2,3,10,10,10,8,2,3,0,0,0,0,0,0,8,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[6,5,7,5,7,3,10,10,10,8,2,3,0,0,0,5,5,5,5,5,5,5,5,5,5,5,9,9,9,9,5,5,5,5,5,5,5,5,5,7],
[8,2,3,2,3,3,10,10,10,8,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,10,10,10,0,0,0,0,0,0,0,0],
[8,2,3,2,3,3,10,10,10,8,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5],
[8,2,3,2,3,3,10,10,10,8,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0],
[8,2,3,2,3,3,10,10,10,8,2,3,5,5,5,5,5,5,5,0,0,0,0,0,0],
]

class Tile(Enum): # enum class to represent different types
    empty = 0
    industrial_tile = 1
    dirt = 2
    dirt_right_corner = 3
    industrial_tile_2 = 4
    industrial_tile_3 = 5
    industrial_left_corner = 6
    industrial_right_corner = 7
    dirt_border = 8
    green_liquid = 9
    green_liquid_2 = 10
    orange_platform_flat = 11
    orange_platform_left = 12
    orange_platform_right = 13
    platform_block = 14
    door = 15
    flat_ladder = 16
   


class Button(): 
    def __init__(self, x , y, image, text, font): 
        self.image = image # store the image of the button
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False # store the clicked state

        self.font = font
        self.text = text


    def draw(self):
        action = False # initialize action to false

        pos = pygame.mouse.get_pos() #uses pygame module to get mouse position

        if self.rect.collidepoint(pos): # checks if mouse is over button
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # checks if left mouse button is pressed and button has not been clicked yet
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0: # checks if left mouse button is released
            self.clicked = False


        screen.blit(self.image, self.rect)

        text = self.font.render(self.text, True, (119, 123, 126))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
        return action


    
        

class World:
    def __init__(self, data):
        self.tile_list = []

        #load images

        industrial_tile = pygame.image.load('industrial_tile.png')
        dirt_1 = pygame.image.load('dirt_1.png')
        dirt_right_corner = pygame.image.load('dirt_right_corner.png')
        industrial_tile_2 = pygame.image.load('industrial_tile_2.png')
        industrial_tile_3 = pygame.image.load('industrial_tile_3.png')
        industrial_right_corner_2 = pygame.image.load('industrial_right_corner_2.png')
        industrial_left_corner_2 = pygame.image.load('industrial_left_corner_2.png')
        dirt_border = pygame.image.load('dirt_border.png')
        green_liquid = pygame.image.load('green_liquid.png')
        green_liquid_2 = pygame.image.load('green_liquid_2.png')
        orange_platform_flat = pygame.image.load('orange_platform_flat.png')
        orange_platform_left = pygame.image.load('orange_platform_left.png')
        orange_platform_right = pygame.image.load('orange_platform_right.png')
        platform_block = pygame.image.load('platform_block.png')
        door = pygame.image.load('door.png')
        flat_ladder = pygame.image.load('flat_ladder.png')
        
        
        


        

        row_count = 0 # initialize row count to 0

        for row in data:
            col_count = 0

            for tile in row:

                if tile == Tile.industrial_tile.value: # links to Tile class 
                    img = pygame.transform.scale(industrial_tile, (tile_size, tile_size)) #scales the  image to fit the tile size
                    img_rect = img.get_rect() #gets the rectangle of the image for positioning
                    img_rect.x = col_count * tile_size # sets the x position of the image rectangle based on the column count and tile size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile) #adds the tile to the tile list

                if tile == Tile.dirt.value:
                    img = pygame.transform.scale(dirt_1, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                if tile == Tile.dirt_right_corner.value:
                    img = pygame.transform.scale(dirt_right_corner, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                if tile == Tile.industrial_tile_2.value:
                    img = pygame.transform.scale(industrial_tile_2, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                if tile == Tile.industrial_tile_3.value:
                    img = pygame.transform.scale(industrial_tile_3, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)
                    
                if tile == Tile.industrial_left_corner.value:
                    img = pygame.transform.scale(industrial_left_corner_2, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)
                    
                if tile == Tile.industrial_right_corner.value:
                    img = pygame.transform.scale(industrial_right_corner_2, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                if tile == Tile.dirt_border.value:
                    img = pygame.transform.scale(dirt_border, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                if tile == Tile.green_liquid.value:
                    img = pygame.transform.scale(green_liquid, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                if tile == Tile.green_liquid_2.value:
                    img = pygame.transform.scale(green_liquid_2, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                if tile == Tile.orange_platform_flat.value:
                    img = pygame.transform.scale(orange_platform_flat, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                if tile == Tile.orange_platform_left.value:
                    img = pygame.transform.scale(orange_platform_left, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                if tile == Tile.orange_platform_right.value:
                    img = pygame.transform.scale(orange_platform_right, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                if tile == Tile.platform_block.value:
                    img = pygame.transform.scale(platform_block, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                if tile == Tile.door.value:
                    img = pygame.transform.scale(door, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect, "door") 
                    self.tile_list.append(tile)

                if tile == Tile.flat_ladder.value:
                    img = pygame.transform.scale(flat_ladder, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                                   

                col_count += 1

            row_count += 1

    def draw(self, screen):

        for tile in self.tile_list:
            screen.blit(tile[0], tile[1]) # draws the image of the tile at the position of the rectangle
                
            
    #gameplay


class Puzzle_Object:
    def __init__(self, x , y , image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y)) # get_rect creates a rectangle and places at (x,y)
        self.active = False

    def update(self, player):
        pass

    def draw(self, screen): # draws stored image at rect position
        if not self.active: # is active variable set to True
            screen.blit(self.image, self.rect) # if true then put image on screen


class Key(Puzzle_Object):
    def __init__(self, x , y, image):
        super().__init__(x, y, image) # calls the constructor of the parent class (Puzzle_Object) to initialize the key's position and image

        
    def update(self, player):
        keys = pygame.key.get_pressed()


        
        if self.rect.colliderect(player.rect): #if player touches key, active is set to true
            if keys[pygame.K_e]:
                self.active = True
                return True

        return False


class Lever(Puzzle_Object):
    pass




class Door(Puzzle_Object):
    pass


    
class Pressure_Pad(Puzzle_Object):
    pass


class Ladder:
    def __init__(self, x, y , image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y))


        self.hitbox = pygame.Rect(x, y, self.rect.width, self.rect.height) # creates a hitbox for the ladder

    def draw(self, screen):
        screen.blit(self.image, self.rect)




class Player:
    def __init__(self, x, y):
        #loading player sprite
        self.image = pygame.image.load("sci-fi player_idle.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.__history = deque(maxlen=300) #size of queue 
        self.vel = pygame.Vector2() # create a vector to represent the player's velocity
        self.rect = self.image.get_rect(topleft=(x, y)) #places image as a rectangle in pygame
        self.ground = False
        self.max_rewind_energy = 100 #max rewind energy on the metre
        self.rewind_cost = 20
        self.recharge = 10
        self.current_time_energy = self.max_rewind_energy
        self.climbing = False


    def check_ladder(self, ladder):

        if self.rect.colliderect(ladder.hitbox): # checks if the player is colliding with the ladder's hitbox
            return True
        return False
        
        


    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel.x = 0

        if keys[pygame.K_LEFT]:
            self.vel.x = -movement_speed
            
        if keys[pygame.K_RIGHT]:
            self.vel.x = movement_speed

        if self.climbing:
            self.vel.y = 0

            if keys[pygame.K_w]:
                self.vel.y = -200 

            elif keys[pygame.K_s]:
                self.vel.y = 200


        else:
            if keys[pygame.K_SPACE] and self.ground:
                self.vel.y = jump_force
        
            

    def apply_physics(self, dt, world):
        self.ground = False
        if not self.climbing:
            self.vel.y += gravity * dt  # apply physics to the player (gravity and movement)
   

    # movement
        self.rect.x += int(self.vel.x * dt)
        

    # collision with platform
        for tile in world.tile_list:

            if self.rect.colliderect(tile[1]): # checks if the player is colliding with the tile's rectangle
                if self.vel.x > 0:
                    self.rect.right = tile[1].left 

                elif self.vel.x < 0:
                    self.rect.left = tile[1].right 

        self.rect.y += int(self.vel.y * dt)

        for tile in world.tile_list:

            if self.climbing: 
                continue


            if self.rect.colliderect(tile[1]): 

                if self.vel.y > 0:
                    self.rect.bottom = tile[1].top 
                    self.vel.y = 0
                    self.ground = True

                elif self.vel.y < 0:

                    self.rect.top = tile[1].bottom
                    self.vel.y = 0
                
                
   
#rewinding
    def save_state(self): # save the current state of the player (position and velocity)
        self.__history.append({
            "pos": self.rect.topleft, # save the top-left position of the player
            "vel": (self.vel.x, self.vel.y)  # save the velocity of the player
        })


    def load_state(self):
        if self.__history:
            state = self.__history.pop()
            self.rect.topleft = state["pos"]
            self.vel.x, self.vel.y = state["vel"]


    def draw(self, screen):
        screen.blit(self.image, self.rect)


# ground platform object
world = World(world_data)
#ladder
flat_ladder = pygame.image.load('flat_ladder.png')
flat_ladder = pygame.transform.scale(flat_ladder, (32, 250))
#player object
player = Player(100, 512)
ladder = Ladder(1050, 60, flat_ladder)



key_image = pygame.image.load("key.png")
key_image = pygame.transform.scale(key_image, (32, 32))

key = Key(480, 160, key_image)

game_state = "menu"
has_key = False

rewinding = False

def draw_rewind_bar(screen, player):
    bar_x = 20 #sets position to top left
    bar_y = 20

    bar_width = 84 #width of blue bar
    bar_height = 14 #length of blue bar

    width = int((player.current_time_energy / player.max_rewind_energy) * bar_width) #calcs how full rewind bar should be by dividing current energy with max

    screen.blit(rewind_bar_frame, (bar_x, bar_y))
    energy_bar = pygame.Rect(bar_x + 12, bar_y + 8 , width, bar_height)
    pygame.draw.rect(screen, (0, 255, 255), energy_bar)


def check_door():
    global game_state
    keys = pygame.key.get_pressed()
    for tile in world.tile_list:
        if len(tile) > 2 and tile[2] == "door":
            # Makes a slightly bigger area around the door
            door_area = tile[1].inflate(40, 40)
            if player.rect.colliderect(door_area):
                if has_key and keys[pygame.K_e]:
                    game_state = "complete"
                     

    

def draw():
    screen.blit(level_1_background, (0, 0))
    world.draw(screen)
    ladder.draw(screen)
    player.draw(screen)
    draw_rewind_bar(screen, player)
    key.draw(screen)

    if has_key:
        for tile in world.tile_list:
            if len(tile) > 2 and tile[2] == "door":
                door_area = tile[1].inflate(40, 40)
                if player.rect.colliderect(door_area):
                    font = pygame.font.Font("Kenney Future.ttf", 18)
                    text = font.render(
                        "PRESS E TO UNLOCK", True, white)
                    text_rect = text.get_rect(center=(tile[1].centerx + 60, tile[1].top - 20))
                    screen.blit(text, text_rect)


       
    pygame.display.flip()


def draw_menu():
        screen.fill((15,15,20))

        title = menu_font.render("Rewind Run", True, (255, 255, 255))
        screen.blit(title, (470, 100))

        if start_button.draw():
            return "game"

        settings_button.draw()

        if exit_button.draw():
            pygame.quit()
            sys.exit()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(cursor_img, (mouse_x - 16, mouse_y - 16))

        pygame.display.update()

        return "menu"
        
def draw_level_complete():
    screen.fill((15, 15, 20))

    title_font = pygame.font.Font("Kenney Future.ttf", 50)
    text_font = pygame.font.Font("Kenney Future.ttf", 25)

    title = title_font.render("LEVEL COMPLETE", True, white)
    title_rect = title.get_rect(center=(640, 280))
    screen.blit(title, title_rect)

    message = text_font.render("You escaped with the key!", True, grey)
    message_rect = message.get_rect(center=(640, 350))
    screen.blit(message, message_rect)

    pygame.display.flip()
    
start_button = Button(515, 220, button_img, "BEGIN TIMELINE", menu_font)
settings_button = Button(515, 330, button_img, "SETTINGS", menu_font)
exit_button = Button(515, 440, button_img, "EXIT", menu_font)



# Game loop
while True:
    dt = clock.tick(60) / 1000 # get the time delta in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() #exit the program if the user closes the window

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                (event.w, event.h), pygame.RESIZABLE
            )

    #menu

    if game_state == "menu":

        game_state = draw_menu()

    elif game_state == "game":
        keys = pygame.key.get_pressed()
        rewinding = keys[pygame.K_r] and player.current_time_energy > 10
    

    
        

        if rewinding:
            player.load_state()

            player.current_time_energy -= player.rewind_cost * dt # current energy - rewind cost after each rewind

            player.current_time_energy = max(0, min(player.current_time_energy, player.max_rewind_energy))

        
        
        else:
            player.climbing = player.check_ladder(ladder)
            if player.climbing and player.rect.bottom <= ladder.rect.top + 5: # if player is climbing and the bottom of the player is above the top of the ladder, set the player's bottom to the top of the ladder
                player.climbing = False
            player.handle_input()
            player.apply_physics(dt, world)
            player.save_state()
            if key.update(player):
                has_key = True

            check_door()

        draw()

    elif game_state == "complete":
        draw_level_complete()

        














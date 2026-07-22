import pygame
import sys # import sys module to handle system exit
from collections import deque # import deque to store the player's state history


pygame.init() 

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE) 
pygame.display.set_caption("Rewind Run") 

clock = pygame.time.Clock() #create a clock object to control the frame rate

# Colors
white = (255, 255, 255)
blue = (50, 100, 255)
grey = (119, 123, 126)
red = (255, 80, 80)


# Physics
gravity = 1200
movement_speed = 300
jump_force = -500


tile_size = 32


world_data = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1,1],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[6,5,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[8,2,3,0,0,0,0,0,0,6,5,7,0,0,0,0,0,0,0,0,0,0,0,0,0],
[8,2,3,5,5,7,0,0,0,8,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0],
[8,2,3,2,2,3,0,0,0,8,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0],
[8,2,3,2,2,3,9,9,9,8,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0],
[8,2,3,2,2,3,0,0,0,8,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0],
[8,2,3,2,2,3,0,0,0,8,2,3,2,2,2,2,2,2,2,2,2,2,2,2,2],
]



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
        

        row_count = 0

        for row in data:
            col_count = 0

            for tile in row:

                if tile == 1:
                    img = pygame.transform.scale(industrial_tile, (tile_size, tile_size)) #scales the  image to fit the tile size
                    img_rect = img.get_rect() #gets the rectangle of the image for positioning
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile) #adds the tile to the tile list

                if tile == 2:
                    img = pygame.transform.scale(dirt_1, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                if tile == 3:
                    img = pygame.transform.scale(dirt_right_corner, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                if tile == 4:
                    img = pygame.transform.scale(industrial_tile_2, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                if tile == 5:
                    img = pygame.transform.scale(industrial_tile_3, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)
                    
                if tile == 6:
                    img = pygame.transform.scale(industrial_left_corner_2, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)
                    
                if tile == 7:
                    img = pygame.transform.scale(industrial_right_corner_2, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                if tile == 8:
                    img = pygame.transform.scale(dirt_border, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                if tile == 9:
                    img = pygame.transform.scale(green_liquid, (tile_size, tile_size)) 
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                    

                col_count += 1

            row_count += 1

    def draw(self, screen):

        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
                
            
    











class Player:
    def __init__(self, x, y):
        #loading player sprite
        self.image = pygame.image.load("sci-fi player_idle.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.__history = deque(maxlen=300)
        self.vel = pygame.Vector2() # create a vector to represent the player's velocity
        self.rect = self.image.get_rect(topleft=(x, y)) #places image as a rectangle in pygame
        self.ground = False


    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel.x = 0

        if keys[pygame.K_LEFT]:
            self.vel.x = -movement_speed
            
        if keys[pygame.K_RIGHT]:
            self.vel.x = movement_speed

        if keys[pygame.K_SPACE] and self.ground:
            self.vel.y = jump_force
        
            

    def apply_physics(self, dt, world):
        self.ground = False
        self.vel.y += gravity * dt  # apply physics to the player (gravity and movement)
   

    # movement
        self.rect.x += int(self.vel.x * dt)
        

    # collision with platform
        for tile in world.tile_list:

            if self.rect.colliderect(tile[1]):
                if self.vel.x > 0:
                    self.rect.right = tile[1].left

                elif self.vel.x < 0:
                    self.rect.left = tile[1].right

        self.rect.y += int(self.vel.y * dt)

        for tile in world.tile_list:
            if self.rect.colliderect(tile[1]):

                if self.vel.y > 0:
                    self.rect.bottom = tile[1].top
                    self.vel.y = 0
                    self.ground = True

                elif self.vel.y < 0:

                    self.rect.top = tile[1].bottom
                    self.vel.y = 0
                
                
   

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


#player object
player = Player(100, 512)

rewinding = False



def draw():
    screen.fill(white)
    world.draw(screen)
    player.draw(screen)
    pygame.display.flip()



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

    keys = pygame.key.get_pressed()
    rewinding = keys[pygame.K_r]

    if rewinding:
        player.load_state()
    else:
        player.handle_input()
        player.apply_physics(dt, world)
        player.save_state()

    draw()






































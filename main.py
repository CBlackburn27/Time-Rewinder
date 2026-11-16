import pygame
import sys # import sys module to handle system exit
from collections import deque # import deque to store the player's state history
from enum import Enum
from pygame import mixer 

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
mixer.init()
pygame.joystick.init()

controller = None

if pygame.joystick.get_count() > 0:
    controller = pygame.joystick.Joystick(0)
    controller.init()


pygame.mouse.set_visible(False) #sets mouse as invisible to allow crosshair to be seen

screen = pygame.display.set_mode((1280, 729), pygame.RESIZABLE) # create a resizable window
pygame.display.set_caption("Rewind Run") 

clock = pygame.time.Clock() #create a clock object to control the frame rate
#----------------sounds--------------------------------------------------------------------------------


#jump sound effect
jump_sfx = mixer.Sound("jump.wav")
jump_sfx.set_volume(0.5)



class Music:
    def __init__(self):
        self.__music_vol = 0.5
        self.__sound_vol = 0.5

        self.__muted = False

    def load_music(self, filename): #loads music file 
        mixer.music.load("main_music.wav")

    def set_music_vol(self, volume):
        self.__music_vol = volume
        self.__update_music_vol()

    def __update_music_vol(self):
        if self.__muted:
            mixer.music.set_volume(0)
        else:
            mixer.music.set_volume(self.__music_vol)

    def toggle_music(self):  #toggles music on and off
        self.__muted = not self.__muted
        self.__update_music_vol()

    def get_muted(self):
        return self.__muted #return whether music is muted

    def get_music_vol(self):
        return self.__music_vol #returns current music volume 
    
        

        
#create music object
music = Music()
music.load_music("main_music.wav")
mixer.music.play(-1)
        
#-------------------------------------background--------------------------------------------------------
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




# physics
gravity = 1200
movement_speed = 300
jump_force = -500



tile_size = 32


#---------------------------------World Data--------------------------------------------------------------------
world_data=[
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

level_1_data = world_data

#level 2 map data 
# Level 2 map data
level_2_data = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,5],
[0,0,0,0,0,0,0,0,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[5,5,5,5,5,0,0,0,5,5,5,5,0,0,0,0,5,5,5,5,5,0,0,0,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,15,5,5],
[14,14,14,5,5,5,0,0,0,0,14,14,14,14,14,14,14,14,14,14,14,9,9,9,9,14,14,14,14,14,14,14,14,14,14,9,9,14,14,14,14,14],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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
   
#---------------------------------------Menu Classes-----------------------

class Button(): 
    def __init__(self, x , y, image, text, font): 
        self.image = image # store the image of the button
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False # store the clicked state

        self.font = font
        self.text = text


    def draw(self, settings):
        action = False # initialize action to false

        pos = pygame.mouse.get_pos() #uses pygame module to get mouse position

        if self.rect.collidepoint(pos): # checks if mouse is over button
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # checks if left mouse button is pressed and button has not been clicked yet
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0: # checks if left mouse button is released
            self.clicked = False


        screen.blit(self.image, self.rect)

        text = self.font.render(self.text, True, settings.get_colour("red"))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
        return action


class Slider:
    def __init__(self, x, y, width):
        self.__rect = pygame.Rect(x, y, width, 8) #slider position + size 
        self.__dragging = False

    def draw(self, screen, settings, value):
        if pygame.mouse.get_pressed()[0]:
            if self.__rect.inflate(0, 25).collidepoint(pygame.mouse.get_pos()):
                self.__dragging = True

            else:
                self.__dragging = False

        if self.__dragging:
            mouse_x = pygame.mouse.get_pos()[0]
            value = (mouse_x - self.__rect.x) / self.__rect.width
            value = max(0, min(1, value))

        #draw slider background
            pygame.draw.rect(screen, settings.get_colour("grey"), self.__rect)

        #draw filled section

        filled_width = int(self.__rect.width * value)
        filled_rect = pygame.Rect(self.__rect.x, self.__rect.y, filled_width, self.__rect.height)
        pygame.draw.rect(screen, settings.get_colour("blue"), filled_rect)

        # Draw the slider handle
        handle_x = self.__rect.x + int(self.__rect.width * value)
        pygame.draw.circle(screen, settings.get_colour("white"), (handle_x, self.__rect.centery), 12)

        return value   
    
#---------------------------------World Class------------------------------------        

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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.images_right = []
        self.images_left = []

        for num in range(1, 5):
            img = pygame.image.load("enemy_run_" + str(num) + ".png")
            img = pygame.transform.scale(img, (128, 128))

            self.images_right.append(img)
            self.images_left.append(pygame.transform.flip(img, True, False))

        self.index = 0
        self.counter = 0
        self.facing_right = True
        self.image = self.images_right[self.index]

        self.rect = self.image.get_rect(topleft = (x, y))

        self.__move_direction = 1
        self.__move_speed = 100
        self.__move_counter = 0
        self.__move_distance = 150


    

    def update(self, player):
        self.rect.x += self.__move_speed * self.__move_direction * dt

        self.__move_counter += self.__move_speed * self.__move_direction * dt

        
        if abs(self.__move_counter) >= self.__move_distance:
            self.__move_direction *= -1
            self.__move_counter = 0

       
        if self.__move_direction > 0:
            self.facing_right = True
        else:
            self.facing_right = False

        # animate enemy
        self.counter += 1

        if self.counter > 7:
            self.counter = 0
            self.index += 1

            if self.index >= len(self.images_right):
                self.index = 0

        if self.facing_right:
            self.image = self.images_right[self.index]
        else:
            self.image = self.images_left[self.index]

        # Check collision with player
        if self.rect.colliderect(player.rect):
            return True

        return False


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        

    


    
    
class Pressure_Pad(Puzzle_Object):
    pass


class Ladder:
    def __init__(self, x, y , image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y))


        self.hitbox = pygame.Rect(x, y, self.rect.width, self.rect.height) # creates a hitbox for the ladder

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Spikes:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

        self.__hitbox = self.rect.inflate(-16, -12)


    def update(self, player):
        if self.__hitbox.colliderect(player.rect):
            return True

        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
#-------------------------------------------Player------------------------------------

class Player:
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []

        for num in range(1, 3):
            img_right = pygame.image.load("player_run_" + str(num) + ".png")
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)

            self.images_right.append(img_right)
            self.images_left.append(img_left)


        self.images_jump = []

        for num in range(1, 4):
            img_jump = pygame.image.load("player_jump_" + str(num) + ".png")
            img_jump = pygame.transform.scale(img_jump, (40, 80))

            self.images_jump.append(img_jump)

        

 


        self.index = 0
        self.counter = 0

        self.jump_index = 0
        self.jump_counter = 0
        self.facing_right = True 

        self.image = self.images_right[self.index]



            
        self.__history = deque(maxlen=300) #size of queue 
        self.vel = pygame.Vector2() # create a vector to represent the player's velocity
        self.rect = self.image.get_rect(topleft=(x, y)) #places image as a rectangle in pygame
        self.ground = False
        self.max_rewind_energy = 100 #max rewind energy on the metre
        self.rewind_cost = 20
        self.recharge = 10
        self.current_time_energy = self.max_rewind_energy
        self.climbing = False

    def update_animation(self):
        if not self.ground:
            self.jump_counter += 1


            if self.jump_counter >= 3:
                self.jump_counter = 0
                self.jump_index += 1

                if self.jump_index >= len(self.images_jump):
                    self.jump_index = len(self.images_jump) -1

            self.image = self.images_jump[self.jump_index]

            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

            return


        if self.vel.x != 0:

            self.counter += 1

            if self.counter > 7:
                self.counter = 0
                self.index += 1

                if self.index >= len(self.images_right):
                    self.index = 0

            # Moving right
            if self.vel.x > 0:
                self.image = self.images_right[self.index]

            # Moving left
            else:
                self.image = self.images_left[self.index]

        else:
            self.index = 0
            self.jump_index = 0
            self.jump_counter = 0
            self.image = self.images_right[0]

    def check_ladder(self, ladder):

        if self.rect.colliderect(ladder.hitbox): # checks if the player is colliding with the ladder's hitbox
            return True
        return False
        
    def reset(self, x, y):
        self.rect.topleft = (x, y )
        self.vel = pygame.Vector2()
        self.ground = False
        self.climbing = False
        self.current_time_energy = self.max_rewind_energy
        self.__history.clear()

            
            


    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel.x = 0

        #controller movements
        controller_x = 0

        if controller:
            controller_x = controller.get_axis(0)

            if abs(controller_x) < 0.2:
                controller_x = 0



    

        if keys[pygame.K_LEFT] or controller_x < -0.2:
            self.vel.x = -movement_speed
            self.facing_right = False

            
        elif keys[pygame.K_RIGHT] or controller_x > 0.2:
            self.vel.x = movement_speed
            self.facing_right = True
            

        if self.climbing:
            self.vel.y = 0

            if keys[pygame.K_w]:
                self.vel.y = -200 

            elif keys[pygame.K_s]:
                self.vel.y = 200

            elif controller_x == 0 and controller:
                controller_y = controller.get_axis(1)

                if controller_y < -0.2:
                    self.vel.y = -200

                elif controller_y > 0.2:
                    self.vel.y= 200
                    


        else:


            controller_jump = False

            if controller:
                controller_jump = controller.get_button(0)
                
            if (keys[pygame.K_SPACE] or controller_jump) and self.ground:
                self.vel.y = jump_force
                jump_sfx.play()
        
            

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
            tile_rect = tile[1]

            if self.climbing: 
                continue


            if self.rect.colliderect(tile_rect): 

                if self.vel.y > 0:
                    self.rect.bottom = tile_rect.top 
                    self.vel.y = 0
                    self.ground = True

                elif self.vel.y < 0:
                    self.rect.top = tile_rect.bottom
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

class RewindTrail:
    def __init__(self):
        self.__ghosts = []


    def add_ghost(self, image, rect):
        ghost_image = image.copy() #copies image so it can fade independently
        ghost_image.set_alpha(150) #sets starting transparency

        self.__ghosts.append([ghost_image, rect.copy(), 150]) #stores copied image, position and transparency in a list


    def draw(self, screen):
        for ghost in self.__ghosts[:]:
            image, rect, alpha = ghost

            image.set_alpha(alpha)
            screen.blit(image, rect)

            ghost[2] -= 6 #gradually reduces transparency to create fading effect

            if ghost[2] <= 0:
                self.__ghosts.remove(ghost)


            
# ground platform object
current_level = 1
world = World(level_1_data)
#ladder
flat_ladder = pygame.image.load('flat_ladder.png')
flat_ladder = pygame.transform.scale(flat_ladder, (32, 250))

spikes = pygame.image.load("spikes.png")
spikes = pygame.transform.scale(spikes, (32, 32))



#player object
player = Player(100, 512)
rewind_trail = RewindTrail()
enemy = Enemy(500, 440)
ladder = Ladder(1050, 60, flat_ladder)
spike_1 = Spikes(400, 650, spikes)
spike_2 = Spikes(780, 75, spikes)
spike_3 = Spikes(320, 365, spikes)


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
                     

    

def draw(settings):
    screen.blit(level_1_background, (0, 0))
    world.draw(screen)
    ladder.draw(screen)
    enemy.draw(screen)
    rewind_trail.draw(screen)
    player.draw(screen)
    draw_rewind_bar(screen, player)
    key.draw(screen)
    spike_1.draw(screen)
    spike_2.draw(screen)
    spike_3.draw(screen)


    if has_key:
        for tile in world.tile_list:
            if len(tile) > 2 and tile[2] == "door":
                door_area = tile[1].inflate(40, 40)
                if player.rect.colliderect(door_area):
                    font = pygame.font.Font("Kenney Future.ttf", 18)
                    text = font.render("PRESS E TO UNLOCK", True, settings.get_colour("white"))
                    text_rect = text.get_rect(center=(tile[1].centerx + 60, tile[1].top - 20))
                    screen.blit(text, text_rect)


       
    pygame.display.flip()
    
COLOURS = {
    'normal': {
        'black':(0, 0, 0),
        'white':(255, 255, 255),
        'blue':(50,100,255),
        'grey':(119, 123, 126),
        'red':(255, 80,80)
    },
    'protanopia':{ #red-green colour blindness
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (227, 66, 52), #vermillion
        'blue': (50, 100, 255),
        'grey': (119, 123, 126)
    },

    'tritanopia': { #blue-yellow colour blindness
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'grey': ( 203, 213, 224),
        'red': (227, 66, 52),
        'blue': (128, 0, 128)
    },
}
    

    
class Settings:
    def __init__(self):
        self.current_colour_mode = "normal"

    def set_colour_mode(self, mode):

        if mode in COLOURS:  #if selected mode is in the colours dictionary e.g protanopia then change current colour mode to that selected mode. 
            self.current_colour_mode = mode

    def get_colour_mode(self):
        return self.current_colour_mode

    def get_colour(self, colour):

        return COLOURS[self.current_colour_mode][colour]

settings = Settings()

def draw_general_settings(settings):
    pygame.mouse.set_visible(True)
    screen.fill(settings.get_colour("black"))

    title = menu_font.render("GENERAL SETTINGS", True, settings.get_colour("white"))
    title_rect = title.get_rect(center=(640, 100))
    screen.blit(title, title_rect)

    if controls_button.draw(settings):
        return "controls"

    if audio_settings_button.draw(settings):
        return "audio_settings"


    if accessibility_button.draw(settings):
        return "settings"

    if general_back_button.draw(settings):
        return "menu"

    pygame.display.update()
    return "general_settings"

def draw_controls(settings):
    pygame.mouse.set_visible(True)
    screen.fill(settings.get_colour("black"))

    title = menu_font.render("CONTROLS", True, settings.get_colour("white"))
    screen.blit(title, title.get_rect(center=(640, 100)))

    if back_button.draw(settings):
        return "general_settings"

    pygame.display.update()

    return "controls"

    
def draw_audio_settings(settings):
    pygame.mouse.set_visible(True)
    screen.fill(settings.get_colour("black"))

    title = menu_font.render("AUDIO SETTINGS", True, settings.get_colour("white"))
    screen.blit(title, title.get_rect(center=(640, 100)))

    pygame.draw.rect(screen, (35, 35, 45), (250, 170, 780, 350))
    pygame.draw.rect(screen, settings.get_colour("grey"), (250, 170, 780, 350), 2)

     #music volume labels

    volume_label = menu_font.render("MUSIC VOLUME", True, settings.get_colour("red"))
    screen.blit(volume_label, volume_label.get_rect(center=(640, 150)))

     #updating the volume using the slider

    volume = music_slider.draw(screen, settings, music.get_music_vol())
    music.set_music_vol(volume)

     #displaying current volume

    volume_text = menu_font.render(str(int(volume * 100)) + "%", True, settings.get_colour("red"))
    screen.blit(volume_text, volume_text.get_rect(center=(640, 360)))

     #updating the music text button

    if music.get_muted():
        mute_button.text = "UNMUTE MUSIC"
    else:
        mute_button.text = "MUTE MUSIC"

    #toggle music

    if mute_button.draw(settings):
        music.toggle_music()

    #back button

    if back_button.draw(settings):
        return "general_settings"

    pygame.display.update()
    return "audio_settings"
                                
     

    

def draw_settings(settings):
    pygame.mouse.set_visible(True)
    screen.fill(settings.get_colour("black"))

    title = menu_font.render("ACCESSIBILITY SETTINGS", True, settings.get_colour("white"))
    title_rect = title.get_rect(center=(640, 100))
    screen.blit(title, title_rect)


    
#change colour mode when selected button is clicked 
    if normal_button.draw(settings):
        settings.set_colour_mode("normal")

    if protanopia_button.draw(settings):
        settings.set_colour_mode("protanopia")

    if tritanopia_button.draw(settings):
        settings.set_colour_mode("tritanopia")

    selected_text = menu_font.render("CURRENT MODE: " + settings.get_colour_mode().upper(), True, settings.get_colour("white"))

    selected_rect = selected_text.get_rect(center=(640, 160))
    screen.blit(selected_text, selected_rect)

    if back_button.draw(settings):
        return "general_settings"

    pygame.display.update()

    return "settings"

                                     


def draw_menu(settings):
        screen.fill((15,15,20))

        title = menu_font.render("Rewind Run", True, COLOURS[settings.current_colour_mode]["white"])
        screen.blit(title, (470, 100))

        if start_button.draw(settings):
            mixer.music.stop()
            return "game"

       
        if settings_button.draw(settings):
            return "general_settings"
            

        if exit_button.draw(settings):
            pygame.quit()
            sys.exit()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(cursor_img, (mouse_x - 16, mouse_y - 16))

        pygame.display.update()

        return "menu"


    
        
def draw_level_complete(settings):
    screen.fill(settings.get_colour("grey"))
    

    title_font = pygame.font.Font("Kenney Future.ttf", 50)
    text_font = pygame.font.Font("Kenney Future.ttf", 25)

    title = title_font.render("LEVEL COMPLETE", True, settings.get_colour("white"))
    title_rect = title.get_rect(center=(640, 280))
    screen.blit(title, title_rect)

    message = text_font.render("You escaped with the key!", True, settings.get_colour("grey"))
    message_rect = message.get_rect(center=(640, 350))
    screen.blit(message, message_rect)

    pygame.display.flip()


def draw_game_over(settings):
    pygame.mouse.set_visible(True)

    screen.fill(settings.get_colour("black"))
    

    title_font = pygame.font.Font("Kenney Future.ttf", 50)
    text_font = pygame.font.Font("Kenney Future.ttf", 25)


    title = title_font.render("GAME OVER", True, COLOURS[settings.current_colour_mode]["red"])
    title_rect = title.get_rect(center=(640, 250))
    screen.blit(title, title_rect)

    message = text_font.render("You were killed!", True, COLOURS[settings.current_colour_mode]["grey"])
    message_rect = message.get_rect(center=(640, 320))
    screen.blit(message, message_rect)

    if restart_button.draw(settings):
        reset()

    pygame.display.flip()

def reset():
    global player
    global key
    global has_key
    global game_state

    player.reset(100, 512)

    has_key = False
    game_state = "game"


def load(level):
        global world
        global player
        global ladder
        global enemy
        global spike_1
        global spike_2
        global spike_3
        global key
        global has_key

        has_key = False

        if level == 1:
            world = World(level_1_data)
            player.reset(100, 512)
            enemy = Enemy(500, 440)
            ladder = Ladder(1050, 60, flat_ladder)
            spike_1 = Spikes(400, 650, spikes)
            spike_2 = Spikes(780, 75, spikes)
            spike_3 = Spikes(320, 365, spikes)

            key = Key(900, 200, key_image)

        elif level == 2:
            world = World(level_2_data)
            player.reset(100, 512)
            enemy = Enemy(600, 440)
            ladder = Ladder(1050, 60, flat_ladder)
            spike_1 = Spikes(450, 650, spikes)
            spike_2 = Spikes(800, 300, spikes)
            spike_3 = Spikes(320, 365, spikes)

            key = Key(900, 200, key_image)




#button objects
start_button = Button(515, 220, button_img, "BEGIN TIMELINE", menu_font)
settings_button = Button(515, 330, button_img, "SETTINGS", menu_font)
exit_button = Button(515, 440, button_img, "EXIT", menu_font)
restart_button = Button(515, 400, button_img, "RESTART", menu_font)
normal_button = Button(515, 200, button_img, "NORMAL", menu_font)
protanopia_button = Button(515, 300, button_img, "PROTANOPIA", menu_font)
tritanopia_button = Button(515, 400, button_img, "TRITANOPIA", menu_font)
back_button = Button(515, 520, button_img, "BACK", menu_font)

# General settings buttons
controls_button = Button(515, 180, button_img, "CONTROLS", menu_font)
audio_settings_button = Button(515, 280, button_img, "AUDIO SETTINGS", menu_font)
accessibility_button = Button(515, 380, button_img, "ACCESSIBILITY", menu_font)
general_back_button = Button(515, 480, button_img, "BACK", menu_font)

music_slider = Slider(440, 310, 400)
mute_button = Button(515, 410, button_img, "MUTE MUSIC", menu_font)



# Game loop

# Game loop
while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                (event.w, event.h), pygame.RESIZABLE
            )

    # menu
    if game_state == "menu":
        game_state = draw_menu(settings)

    # general settings
    elif game_state == "general_settings":
        game_state = draw_general_settings(settings)

    # controls
    elif game_state == "controls":
        game_state = draw_controls(settings)

    # audio
    elif game_state == "audio_settings":
        game_state = draw_audio_settings(settings)

    # accessibility
    elif game_state == "settings":
        game_state = draw_settings(settings)

    # gameplay
    elif game_state == "game":

        keys = pygame.key.get_pressed()
        rewinding = keys[pygame.K_r] and player.current_time_energy >= 10

        if rewinding:
            rewind_trail.add_ghost(player.image, player.rect)
            player.load_state()

            player.current_time_energy -= player.rewind_cost * dt
            player.current_time_energy = max(0, min(player.current_time_energy, player.max_rewind_energy))

        else:
            player.climbing = player.check_ladder(ladder)

            if player.climbing and player.rect.bottom <= ladder.rect.top + 5:
                player.climbing = False

            player.handle_input()
            player.apply_physics(dt, world)
            player.save_state()
            player.update_animation()

            if key.update(player):
                has_key = True

            check_door()

            if spike_1.update(player):
                game_state = "gameover"

            if spike_2.update(player):
                game_state = "gameover"

            if spike_3.update(player):
                game_state = "gameover"

            if enemy.update(player):
                game_state = "gameover"

        draw(settings)

    # GAME OVER
    elif game_state == "gameover":
        draw_game_over(settings)

    # LEVEL COMPLETE
    elif game_state == "complete":
        keys = pygame.key.get_pressed()

        if current_level == 1 and keys[pygame.K_RETURN]:
            current_level = 2
            load(2)
            game_state = "game"

        draw_level_complete(settings)

        



















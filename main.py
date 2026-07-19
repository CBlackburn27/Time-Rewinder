import pygame
import sys # import sys module to handle system exit
from collections import deque # import deque to store the player's state history


pygame.init() 

screen = pygame.display.set_mode((800, 600)) 
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

class Player:
    def __init__(self, x, y):
        #loading player sprite
        self.image = pygame.image.load("sci-fi player_idle.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.history = deque(maxlen=300)
        self.vel = pygame.Vector2() # create a vector to represent the player's velocity
        self.rect = self.image.get_rect(topleft=(x, y)) #places image as a rectangle in pygame


    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel.x = 0

        if keys[pygame.K_LEFT]:
            self.vel.x = -movement_speed
            
        if keys[pygame.K_RIGHT]:
            self.vel.x = movement_speed

        if keys[pygame.K_SPACE]:
        # Only jump if on ground
            if self.rect.bottom >= platform.top and self.rect.bottom <= platform.top + 10:
                self.vel.y = jump_force

    def apply_physics(self, dt, platform): # apply physics to the player (gravity and movement)
    # Gravity
        self.vel.y += gravity * dt

    # Move
        self.rect.x += int(self.vel.x * dt)
        self.rect.y += int(self.vel.y * dt)

    # Collision with platform
        if self.rect.colliderect(platform) and self.vel.y > 0:
            self.rect.bottom = platform.top
            self.vel.y = 0

    def save_state(self): # save the current state of the player (position and velocity)
        self.history.append({
            "pos": self.rect.topleft, # save the top-left position of the player
            "vel": (self.vel.x, self.vel.y)  # save the velocity of the player
        })


    def load_state(self):
        if self.history:
            state = self.history.pop()
            self.rect.topleft = state["pos"]
            self.vel.x, self.vel.y = state["vel"]


    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Ground platform object
platform = pygame.Rect(0, 400, 800, 50)


#player object
player = Player(100, 300)

rewinding = False



def draw():
    screen.fill(white)
    pygame.draw.rect(screen, grey, platform)
    player.draw(screen)
    pygame.display.flip()



# Game loop
while True:
    dt = clock.tick(60) / 1000 # get the time delta in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() #exit the program if the user closes the window

    keys = pygame.key.get_pressed()
    rewinding = keys[pygame.K_r]

    if rewinding:
        player.load_state()
    else:
        player.handle_input()
        player.apply_physics(dt, platform)
        player.save_state()

    draw()

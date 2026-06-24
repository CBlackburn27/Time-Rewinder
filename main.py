import pygame
from collections import deque
import sys


pygame.init() #always need to initialise pygame

screen = pygame.display.set_mode((800, 600)) #set the size of the window
pygame.display.set_caption("Time Rewinder") #set the title of the window

clock = pygame.time.Clock() #create a clock object to control the frame rate

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
GREEN = (50, 200, 100)
RED = (255, 80, 80)

# Player
player = pygame.Rect(100, 300, 30, 40) # create a rectangle to represent the player
vel = pygame.Vector2(0, 0) # create a vector to represent the player's velocity

# Physics
GRAVITY = 1200
MOVE_SPEED = 300
JUMP_FORCE = -500

# Ground platform
platform = pygame.Rect(0, 400, 800, 50) # create a rectangle to represent the ground platform

# Time rewind history
MAX_HISTORY = 300  # ~5 seconds at 60 FPS 
history = deque(maxlen=MAX_HISTORY) # create a deque to store the player's state history

rewinding = False # flag to indicate if the player is rewinding time


def save_state(): # save the current state of the player (position and velocity) 
    history.append({
        "pos": player.topleft, # save the top-left position of the player
        "vel": (vel.x, vel.y)  # save the velocity of the player
    })


def load_state():
    global vel
    if history:
        state = history.pop()
        player.topleft = state["pos"]
        vel.x, vel.y = state["vel"]


def handle_input(dt):
    keys = pygame.key.get_pressed()
    vel.x = 0

    if keys[pygame.K_LEFT]:
        vel.x = -MOVE_SPEED
    if keys[pygame.K_RIGHT]:
        vel.x = MOVE_SPEED

    if keys[pygame.K_SPACE]:
        # Only jump if on ground
        if player.bottom >= platform.top and player.bottom <= platform.top + 10:
            vel.y = JUMP_FORCE


def apply_physics(dt):
    # Gravity
    vel.y += GRAVITY * dt

    # Move
    player.x += int(vel.x * dt)
    player.y += int(vel.y * dt)

    # Collision with platform
    if player.colliderect(platform) and vel.y > 0:
        player.bottom = platform.top
        vel.y = 0


def draw():
    screen.fill(WHITE)

    # Platform
    pygame.draw.rect(screen, GREEN, platform)

    # Player (red if rewinding)
    color = RED if rewinding else BLUE
    pygame.draw.rect(screen, color, player)

    pygame.display.flip()


# Game loop
while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    rewinding = keys[pygame.K_r]

    if rewinding:
        load_state()
    else:
        handle_input(dt)
        apply_physics(dt)
        save_state()

    draw()




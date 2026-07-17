import pygame
import sys


pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Rewind Run")

clock = pygame.time.Clock()

#colours

white = (255, 255, 255)
blue = (50, 100, 255)
grey = (119, 123, 126)



#physics
gravity = 1200
movement_speed = 300
jumping_force = -500

class Player():
    def __init__(self, x, y):
        self.image = pygame.image.load("sci-fi player_idle.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.vel = pygame.Vector2(0,0)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        


    def handle_input(self, delta_time):
        keys = pygame.key.get_pressed()

        self.vel.x = 0

        if keys[pygame.K_LEFT]:
            self.vel.x = -movement_speed
        if keys[pygame.K_RIGHT]:
            self.vel.x = movement_speed

        if keys[pygame.K_SPACE]:
            # Only jump if on ground
            if self.rect.bottom >= platform.top and self.rect.bottom <= platform.top + 10:
                self.vel.y = jumping_force



platform = pygame.Rect(0, 550, 800, 50)


player = Player(100, 100) 


def draw():
    screen.fill(white)

    pygame.draw.rect(screen, grey, platform)
    screen.blit(player.image, player.rect)

    pygame.display.flip()







#game loop

while True:
    delta_time = clock.tick(60) / 1000

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                (event.w, event.h), pygame.RESIZABLE
            )

    # Update the player every frame
    player.handle_input(delta_time)

    # Draw everything every frame

    draw()
        

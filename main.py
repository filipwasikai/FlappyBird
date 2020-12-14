import pygame
import sys


def create_pipe():
    new_pipe = pipe_surface.get_rect(midtop=(width / 2, height / 2))
    return new_pipe


pygame.init()

# game variables
width = 600
height = 900
gravity = 0.15
bird_movement = 0

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

floor_height = 50
# creates a surface with the same size as the window
background = pygame.Surface((width, height))
# creates a rectangle on the surface
pygame.draw.rect(background, (0, 0, 0), (0, 0, width, height))

floor_surface = pygame.Surface((width, floor_height))
pygame.draw.rect(floor_surface, (255, 200, 0), (0, 0, width, floor_height))

bird_surface = pygame.image.load('assets/yellowbird-midflap.png').convert()
bird_rect = bird_surface.get_rect(center=(100, int(height / 2)))

pipe_surface = pygame.Surface(width, height)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 7
        if event.type == SPAWNPIPE:
            pipe_list.append(create_pipe)

    # puts the surface onto the canvas
    screen.blit(background, (0, 0))
    screen.blit(floor_surface, (0, height - floor_height))

    bird_movement += gravity
    bird_rect.centery += int(bird_movement)
    screen.blit(bird_surface, bird_rect)

    pygame.display.update()
    clock.tick(120)

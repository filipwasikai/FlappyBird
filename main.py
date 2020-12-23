import pygame
import sys


def create_pipe():
    new_pipe = pipe_surface.get_rect(midtop=(int(width / 2), int(height / 2)))
    return new_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_surface, pipe)


pygame.init()

# game variables
width = 400
height = 600
gravity = 0.15
bird_movement = 0
floor_height = 50

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Background
background = pygame.Surface((width, height))
pygame.draw.rect(background, (0, 0, 0), (0, 0, width, height))

# Floor
floor_surface = pygame.Surface((width, floor_height))
pygame.draw.rect(floor_surface, (255, 200, 0), (0, 0, width, floor_height))

# Bird
# bird_surface = pygame.image.load('assets/yellowbird-midflap.png').convert()
bird_surface = pygame.Surface((34, 24))
bird_surface.fill((255, 0, 0))
bird_rect = bird_surface.get_rect(center=(100, int(height / 2)))

# Pipe
# pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.Surface((50, 100))
pipe_surface.fill((0, 255, 0))
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
            pipe_list.append(create_pipe())

    # puts the surface onto the canvas
    screen.blit(background, (0, 0))
    screen.blit(floor_surface, (0, height - floor_height))

    # Bird
    bird_movement += gravity
    bird_rect.centery += int(bird_movement)
    screen.blit(bird_surface, bird_rect)

    # Pipes
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    pygame.display.update()
    clock.tick(120)

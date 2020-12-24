from collections import deque
import random
import sys
import pygame


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(width + 25, random_pipe_pos + int(pipe_gap / 2)))
    top_pipe = pipe_surface.get_rect(midbottom=(width + 25, random_pipe_pos - int(pipe_gap / 2)))
    return top_pipe, bottom_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_surface, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True

    if bird_rect.top <= 0 or bird_rect.bottom >= height - floor_height:
        return True

    return False


pygame.init()

# game variables
width = 400
height = 800
gravity = 0.2
bird_movement = 0
floor_height = 50
pipe_gap = 150
game_over = False

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Background
background = pygame.Surface((width, height))
pygame.draw.rect(background, (0, 0, 0), (0, 0, width, height))

# Floor
floor_surface = pygame.Surface((width, floor_height))
pygame.draw.rect(floor_surface, (50, 50, 50), (0, 0, width, floor_height))

# Bird
bird_surface = pygame.image.load('assets/yellowbird-midflap.png').convert()
# bird_surface = pygame.Surface((34, 24))
# bird_surface.fill((200, 0, 0))
bird_rect = bird_surface.get_rect(center=(100, int(height / 2)))

# Pipe
# pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.Surface((50, height))
pipe_surface.fill((0, 200, 0))
pipe_list = deque([])
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [int((height / 3) - (floor_height / 2)),
               int((height / 2) - (floor_height / 2)),
               int((height * 2 / 3) - (floor_height / 2))]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 7

            if event.key == pygame.K_SPACE and game_over:
                bird_rect.center = (100, int(height / 2))
                pipe_list.clear()
                game_over = False

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            if len(pipe_list) > 6:
                pipe_list.popleft()
                pipe_list.popleft()

    # Background
    screen.blit(background, (0, 0))

    if not game_over:
        # Bird
        bird_movement += gravity
        bird_rect.centery += int(bird_movement)
        screen.blit(bird_surface, bird_rect)
        game_over = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        screen.blit(floor_surface, (0, height - floor_height))

    # Floor
    screen.blit(floor_surface, (0, height - floor_height))

    pygame.display.update()
    clock.tick(120)

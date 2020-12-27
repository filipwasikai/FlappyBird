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
        if pipe.bottom >= height:
            screen.blit(pipe_surface, pipe)

        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True

    if bird_rect.top <= 0 or bird_rect.bottom >= height - floor_height:
        return True

    return False


def draw_score(game_over):
    if not game_over:
        score_surface_text = score_font.render(str(max(0, score)), True, (255, 255, 255))
        score_rect = score_surface_text.get_rect(center=(int(width / 2), int(height / 4)))
        screen.blit(score_surface_text, score_rect)

    else:
        score_surface_text = score_font.render(f'Score: {str(max(0, score))}', True, (255, 255, 255))
        score_rect = score_surface_text.get_rect(center=(int(width / 2), int(height / 4)))
        screen.blit(score_surface_text, score_rect)

        score_surface_text = score_font.render(f'High Score: {high_score}', True, (255, 255, 255))
        score_rect = score_surface_text.get_rect(center=(int(width / 2), int(height / 2)))
        screen.blit(score_surface_text, score_rect)


def update_high_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def get_high_score():
    # Default high score
    high_score = 0

    # Try to read the high score from a file
    try:
        high_score_file = open("high_score.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
        print("The high score is", high_score)
    except IOError:
        # Error reading file, no high score
        print("There is no high score yet.")
    except ValueError:
        # There's a file there, but we don't understand the number.
        print("I'm confused. Starting with no high score.")

    return high_score


def save_high_score(new_high_score):
    try:
        # Write the file to disk
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()
    except IOError:
        # Hm, can't write it.
        print("Unable to save the high score.")


# game variables
width = 400
height = 800
gravity = 0.2
bird_movement = 0
floor_height = 50
pipe_gap = 150
game_over = False
score = -1
high_score = get_high_score()

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Background
background_surface = pygame.Surface((width, height))
background_surface.fill((0, 0, 0))
background_rect = background_surface.get_rect(topleft=(0, 0))

# Floor
floor_surface = pygame.Surface((width, floor_height))
floor_surface.fill((50, 50, 50))
floor_rect = floor_surface.get_rect(bottomright=(width, height))

# Bird
bird_surface = pygame.image.load('assets/yellowbird-upflap-neg.png').convert()
# bird_surface = pygame.Surface((34, 24))
# bird_surface.fill((200, 0, 0))
bird_rect = bird_surface.get_rect(center=(125, int(height / 2)))

# Pipe
pipe_surface = pygame.image.load('assets/pipe-green-neg.png').convert()
# pipe_surface = pygame.Surface((50, height))
# pipe_surface.fill((0, 200, 0))
pipe_list = deque([], maxlen=6)
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [int((height / 3) - (floor_height / 2)),
               int((height / 2) - (floor_height / 2)),
               int((height * 2 / 3) - (floor_height / 2))]

# Score
pygame.font.init()
score_font = pygame.font.Font('assets/flappy-font.TTF', 30)

# Pygame
pygame.init()
pygame.display.set_caption("Flappy Bird")
bird_icon = pygame.image.load('assets/yellowbird-upflap.png').convert()
pygame.display.set_icon(bird_icon)

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
                score = -1
                game_over = False

        if event.type == SPAWNPIPE and not game_over:
            pipe_list.extend(create_pipe())
            score += 1

    # Background
    screen.blit(background_surface, background_rect)

    if not game_over:
        # Bird
        bird_movement += gravity
        bird_rect.centery += int(bird_movement)
        screen.blit(bird_surface, bird_rect)
        game_over = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)

    draw_pipes(pipe_list)

    # Floor
    screen.blit(floor_surface, floor_rect)

    # Score
    draw_score(game_over)
    high_score = update_high_score(score, high_score)
    save_high_score(high_score)

    pygame.display.update()
    clock.tick(120)

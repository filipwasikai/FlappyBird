import bird
import pipe
import random
import sys
import pygame


# game variables
width = 600
height = 800
floor_height = 50
pipe_gap = 150
game_over = False
score = -1


def draw(surface, rect):
    screen.blit(surface, rect)


def create_2_pipes():
    random_pipe_height = random.randint(int((height / 4) - (floor_height / 2)),
                                        int((height * 3 / 4) - (floor_height / 2)))
    bottom_pipe = pipe.Pipe(screen, "up", width + 25, random_pipe_height + int(pipe_gap / 2), pygame)
    top_pipe = pipe.Pipe(screen, "down", width + 25, random_pipe_height - int(pipe_gap / 2), pygame)

    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        if pipe.x_pos < -50:
            pipe_list.remove(pipe)

    for pipe in pipes:
        pipe.move()

    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        pipe.draw()


def check_collision(pipes):
    for pipe in pipes:
        if bird.rect.colliderect(pipe.rect):
            return True

    if bird.rect.top <= 0 or bird.rect.bottom >= height - floor_height:
        return True

    return False


def draw_score(game_over):
    if not game_over:
        score_surface_text = score_font.render(str(max(0, score)), True, (255, 255, 0))
        score_rect = score_surface_text.get_rect(center=(int(width / 2), int(height / 4)))
        screen.blit(score_surface_text, score_rect)

    else:
        score_surface_text = score_font.render(f'Score: {str(max(0, score))}', True, (255, 255, 0))
        score_rect = score_surface_text.get_rect(center=(int(width / 2), int(height / 4)))
        screen.blit(score_surface_text, score_rect)

        score_surface_text = score_font.render(f'High Score: {high_score}', True, (255, 255, 0))
        score_rect = score_surface_text.get_rect(center=(int(width / 2), int(height / 2)))
        screen.blit(score_surface_text, score_rect)


def update_high_score(score_local, high_score_local):
    if score_local > high_score_local:
        high_score_local = score_local

    return high_score_local


def get_high_score():
    high_score_local = 0

    try:
        high_score_file = open("high_score.txt", "r")
        high_score_local = int(high_score_file.read())
        high_score_file.close()

    except IOError:
        # Error reading file, no high score
        print("There is no high score yet.")

    except ValueError:
        # There's a file there, but we don't understand the number.
        print("Starting with no high score.")

    return high_score_local


def save_high_score(new_high_score):
    try:
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()

    except IOError:
        print("Unable to save the high score.")


high_score = get_high_score()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
bird = bird.Bird(screen, 125, height / 2, pygame)

# Background
background_surface = pygame.Surface((width, height))
background_surface.fill((0, 0, 0))
background_rect = background_surface.get_rect(topleft=(0, 0))

# Floor
floor_surface = pygame.Surface((width, floor_height))
floor_surface.fill((50, 50, 50))
floor_rect = floor_surface.get_rect(bottomright=(width, height))


# Score
pygame.font.init()
score_font = pygame.font.Font('assets/flappy-font.TTF', 30)


# Pygame
pygame.init()
pygame.display.set_caption("Flappy Bird")
bird_icon = pygame.image.load('assets/yellowbird-upflap.png').convert()
pygame.display.set_icon(bird_icon)

# Pipes
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)


def logic():
    global game_over, pipe_list, high_score
    if not game_over:
        # Bird
        game_over = check_collision(pipe_list)
        bird.fall()
        # Pipes
        pipe_list = move_pipes(pipe_list)
    else:
        high_score = update_high_score(score, high_score)
        save_high_score(high_score)


def draw_all():
    draw(background_surface, background_rect)
    if not game_over:
        bird.draw()
        draw_pipes(pipe_list)
    # Floor
    draw(floor_surface, floor_rect)
    # Score
    draw_score(game_over)
    # Window
    pygame.display.update()
    clock.tick(120)


def pygame_stuff():
    global score, game_over
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

            if event.key == pygame.K_SPACE and game_over:
                bird.rect.center = (125, int(height / 2))
                pipe_list.clear()
                score = -1
                game_over = False

        if event.type == SPAWNPIPE and not game_over:
            pipe_list.extend(create_2_pipes())
            score += 1


def start_game():
    while True:
        for i in range(3):
            pygame_stuff()
            logic()
        draw_all()


if __name__ == "__main__":
    start_game()

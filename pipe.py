import pygame


class Pipe:

    def __init__(self, screen, facing, x_pos, y_pos):
        self.screen = screen
        self.facing = facing
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.surface = pygame.image.load('assets/pipe-green-neg.png').convert()

        if self.facing == "up":
            self.rect = self.surface.get_rect(midtop=(self.x_pos, self.y_pos))

        elif self.facing == "down":
            self.rect = self.surface.get_rect(midbottom=(self.x_pos, self.y_pos))
            self.surface = pygame.transform.flip(self.surface, False, True)

    def move(self):
        self.rect.centerx -= 2
        self.x_pos = self.rect.centerx

    def draw(self):
        self.screen.blit(self.surface, self.rect)

import pygame


class Bird:

    def __init__(self, screen, x_pos, y_pos):
        self.screen = screen
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.movement = 0
        self.gravity = 0.2
        self.surface = pygame.image.load('assets/yellowbird-upflap-neg.png').convert()
        self.rect = self.surface.get_rect(center=(self.x_pos, self.y_pos))

    def jump(self):
        self.movement = 0
        self.movement -= 7

    def fall(self):
        self.movement += self.gravity
        self.rect.centery += self.movement
        self.y_pos = self.rect.centery

    def draw(self):
        self.screen.blit(self.surface, self.rect)

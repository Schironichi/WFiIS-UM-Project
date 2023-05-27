import os.path

from utils.imports import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width=50, height=50):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.image.load(os.path.join('data', 'Kratos.png'))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

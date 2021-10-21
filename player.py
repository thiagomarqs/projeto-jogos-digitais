import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = [
            pygame.image.load("player\R1.png"),
            pygame.image.load("player\R2.png"),
            pygame.image.load("player\R3.png"),
            pygame.image.load("player\R4.png"),
            pygame.image.load("player\R5.png"),
            pygame.image.load("player\R6.png"),
            pygame.image.load("player\R7.png"),
            pygame.image.load("player\R8.png"),
            ]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    # speed deve ser um número menor que 1
    def update(self, speed):
        self.current_sprite += speed

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

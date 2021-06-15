"""
	Class: Laser
	Info: logic for the laser sprite
"""

import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, path, pos, speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.speed = speed
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.centery -= self.speed

        # remove offscreen meteors
        if self.rect.centery < -20:
            self.kill()

"""
	Class: PowerUp
	Info: for object that the player can interrupt with (ammo, health, mutators)
"""
import pygame
from src.config.configs import screen_size


class PowerUp(pygame.sprite.Sprite):
	def __init__(self, path, x_pos, y_pos):
		super().__init__()
		self.image = pygame.image.load(path)
		self.clean_image = self.image.copy()
		self.rect = self.image.get_rect(center=(x_pos, y_pos))

	def update(self):
		self.rect.centery += 2

		# remove offscreen meteors
		if self.rect.centery > screen_size[1] + 50:
			self.kill()

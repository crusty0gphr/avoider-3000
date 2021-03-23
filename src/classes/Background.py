"""
	Class: Background
	Info: made for drawing moving non-collide objects on the background (example: moving stars)
"""

import pygame
from configs import screen_size


class Background(pygame.sprite.Sprite):
	def __init__(self, path, x_pos, y_pos, x_speed, y_speed):
		super().__init__()
		self.image = pygame.image.load(path)
		self.clean_image = self.image.copy()

		# movement dimensions
		self.x_speed = x_speed
		self.y_speed = y_speed

		self.rect = self.image.get_rect(center=(x_pos, y_pos))

	# update positions of the background objects frame by frame
	def update(self):
		self.rect.centerx += self.x_speed
		self.rect.centery += self.y_speed

		# remove offscreen sprites
		if self.rect.centery > screen_size[1] + 50:
			self.kill()

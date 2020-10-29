import pygame, glob
from config.configs import meteor_assets_path, natural_sort, screen_size

class Meteor(pygame.sprite.Sprite):
	def __init__(self, path, x_pos, y_pos, x_speed, y_speed, rotation_speed):
		super().__init__()
		self.angle = 0

		self.metheor_collection_path = meteor_assets_path + path
		self.images = natural_sort(glob.glob(self.metheor_collection_path + '*.gif'))

		self.image_index = 0
		self.image = pygame.image.load(self.images[self.image_index])
		self.clean_image = self.image.copy()

		# movement dimentions
		self.x_speed = x_speed
		self.y_speed = y_speed

		self.rect = self.image.get_rect(center = (x_pos, y_pos))
		self.rotation_speed = rotation_speed

	def update(self):
		self.image_index += 1
		self.rect.centerx += self.x_speed
		self.rect.centery += self.y_speed

		self.animate_meteors()

		if 'planetoid' not in self.metheor_collection_path:
			self.rotate_meteors()

		# remove offscreen meteors
		if self.rect.centery > screen_size[1] + 50 or self.rect.centerx < -50 or self.rect.centerx > screen_size[0] + 50:
			self.kill()

	def animate_meteors(self):
		if self.image_index >= len(self.images):
			self.image_index = 0

		self.image = pygame.image.load(self.images[self.image_index])
		self.clean_image = self.image.copy()

	def rotate_meteors(self):
		rotation_tuple = self.rot_center(self.clean_image, self.angle)

		self.image = rotation_tuple[0]
		self.rect =	rotation_tuple[1]
		self.angle += self.rotation_speed

	def rot_center(self, image, angle):
		rotated_image = pygame.transform.rotate(image, angle)
		new_rect = rotated_image.get_rect(center = self.rect.center)

		return rotated_image, new_rect

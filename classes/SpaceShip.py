"""
	Class: Score
	Info: update, reset, show users' score on the screen
"""
import glob
import pygame

from config.configs import spaceship_assets_path, natural_sort, screen_size


class SpaceShip(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos, screen_obj):
		super().__init__()
		self.x = x_pos
		self.y = y_pos

		self.screen = screen_obj
		self.images = natural_sort(glob.glob(spaceship_assets_path + '*.gif'))

		self.image_index = 0
		self.image = pygame.image.load(self.images[self.image_index])
		self.clean_image = self.image.copy()
		self.center = (x_pos, y_pos)

		self.rect = self.image.get_rect(center=self.center)
		self.shield_surface = pygame.image.load('assets/hot-dog-heart.png')

		self.health = 5
		self.ammo = 30

	def update(self):
		self.image_index += 1
		self.rect.center = pygame.mouse.get_pos()

		self.animate_space_ship()
		self.display_health()
		self.display_ammo()
		self.screen_constrain()
		self.rotate()

	def animate_space_ship(self):
		if self.image_index >= len(self.images):
			self.image_index = 0

		self.image = pygame.image.load(self.images[self.image_index])
		self.clean_image = self.image.copy()

	def display_health(self):
		for index, shield in enumerate(range(self.health)):
			index += 1
			self.screen.blit(self.shield_surface, (index * 25, screen_size[1] - 40))

	def display_ammo(self):
		score_font = pygame.font.Font('assets/fonts/retro-gaming.ttf', 18)
		# text_surface_center = (730, 577)
		text_surface_center = (screen_size[0] - 70, screen_size[1] - 23)
		text_surface = score_font.render('AMMO: ' + str(self.ammo), False, (255, 255, 255))
		text_rect = text_surface.get_rect(center=text_surface_center)

		self.screen.blit(text_surface, text_rect)

	# decrease players health when hits an obstacle
	def get_damage(self, damage_amount):
		self.health -= damage_amount

	# decrease ammo when player shoots
	def decrease_ammo(self, shot_amount):
		self.ammo -= shot_amount

	def restore_health(self):
		self.health = 5

	def restore_ammo(self):
		self.ammo = 30

	def screen_constrain(self):
		if self.rect.left <= 0: self.rect.left = 0
		if self.rect.right >= screen_size[0]: self.rect.right = screen_size[0]
		if self.rect.top <= 0: self.rect.top = 0
		if self.rect.bottom >= screen_size[1] - 50: self.rect.bottom = screen_size[1] - 50

	# spaceship animation when the player moves the mouse
	def rotate(self):
		mouse_rel = pygame.mouse.get_rel()

		# mouse movement - left
		if mouse_rel[0] < 0:
			self.image = self.rot_center(self.clean_image, 15)  # tilt the spaceship 15 degrees left
			return

		# mouse movement - right
		if mouse_rel[0] > 0:
			self.image = self.rot_center(self.clean_image, -15)  # tilt the spaceship 15 degrees right
			return

		# mouse movement - stopped
		if mouse_rel[0] == 0:
			self.image = self.rot_center(self.clean_image, 0)  # reset
			return

	def rot_center(self, image, angle):
		orig_rect = image.get_rect()

		rot_image = pygame.transform.rotate(image, angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()

		return rot_image

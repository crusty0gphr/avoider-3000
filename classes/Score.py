import pygame
from config.configs import screen_size


class Score():
	def __init__(self, screen):
		self.score = 0
		self.screen = screen

	def reset(self):
		self.score = 0

	def add_score(self, score_to_add):
		self.score += score_to_add

	def get_score(self):
		return self.score

	def draw(self):
		score_font = pygame.font.Font('assets/fonts/retro-gaming.ttf', 26)
		text_surface_center = (screen_size[0] / 2, 30)
		text_surface = score_font.render(str(self.score), False, (255, 255, 255))
		text_rect = text_surface.get_rect(center = text_surface_center)
		self.screen.blit(text_surface, text_rect)

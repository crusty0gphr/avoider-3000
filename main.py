from typing import Tuple
import pygame, sys, random

from config.configs import *
from classes.SpaceShip import SpaceShip
from classes.Meteor import Meteor
from classes.Background import Background
from classes.Laser import Laser
from classes.Score import Score
from classes.Powerup import Powerup

pygame.init()
pygame.display.set_caption(game_name)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# sprites groups
spaceship_group = pygame.sprite.GroupSingle()
explosion_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()
healing_group = pygame.sprite.Group()
ammo_group = pygame.sprite.Group()

# continius timer
METEOR_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT, 250)

# spaceship - player sprite
SpaceShip = SpaceShip(400, 500, screen)
spaceship_group.add(SpaceShip)
# score obj
Score = Score(screen)

def game_menu():
	global screen
	render_msg('-= AVOIDER =-', 100, (screen_size[0]/2, screen_size[1]/2 - 200))
	render_msg('3000', 72, (screen_size[0]/2, screen_size[1]/2 - 100))
	render_msg('Click to start!', 32, (screen_size[0]/2, screen_size[1]/2 + 180))

	hot_dog = pygame.image.load('assets/powerups/hot-dog.png')
	screen.blit(hot_dog, (screen_size[0]/2 - 30, screen_size[1]/2 + 20))

	render_msg('- Designed by: Sargis Mardirossian - Developer: Harout Mardirossian -', 18, (screen_size[0]/2, screen_size[1] - 80))
	render_msg('@Corrupted.bit', 18, (screen_size[0]/2, screen_size[1] - 40))

def init_powerups(powerup_path, powerup_group):
	random_x_pos = random.randrange(50, screen_size[0] - 50)
	random_y_pos = random.randrange(-200, -50)

	powerup = Powerup(powerup_path, random_x_pos, random_y_pos)
	powerup_group.add(powerup)

def init_background():
	# draw stars
	star_group.draw(screen)
	star_group.update()

def init_game_pross(score_obj):
	# hide the mouse cursor
	pygame.mouse.set_visible(False)

	global laser_timer
	global laser_ready
	# draw meteor
	meteor_group.draw(screen)
	meteor_group.update()
	# draw laser
	laser_group.draw(screen)
	laser_group.update()
	# draw healing hot dog
	healing_group.draw(screen)
	healing_group.update()
	# draw draw ammo
	ammo_group.draw(screen)
	ammo_group.update()
	# draw player
	spaceship_group.draw(screen)
	spaceship_group.update()
	# game score
	Score.draw()

	''' --------- Check collisions --------- '''
	if pygame.sprite.spritecollide(spaceship_group.sprite, meteor_group, True):
		damage = random.randrange(1, 3)
		spaceship_group.sprite.get_damage(damage)

	if pygame.sprite.spritecollide(spaceship_group.sprite, healing_group, True):
		spaceship_group.sprite.restore_health()

	if pygame.sprite.spritecollide(spaceship_group.sprite, ammo_group, True):
		spaceship_group.sprite.restore_ammo()

	for laser in laser_group:
		if pygame.sprite.spritecollide(laser, meteor_group, True):
			laser_group.remove(laser)

			score = random.randrange(10, 50, 5)
			score_obj.add_score(score)

	if pygame.time.get_ticks() - laser_timer >= 125:
		laser_ready = True

def init_game_over():
	# hide the mouse cursor
	pygame.mouse.set_visible(True)
	score = Score.get_score()

	render_msg('GAME OVER', 58, (screen_size[0]/2, screen_size[1]/2 - 100))
	render_msg(str(score), 48, (screen_size[0]/2, screen_size[1]/2 - 40))
	render_msg('Click to continue!', 32, (screen_size[0]/2, screen_size[1]/2 + 100))

def render_msg(msg, font_size, text_pos):
	font = pygame.font.Font('assets/fonts/retro-gaming.ttf', font_size)

	text_surface_center = text_pos
	text_surface = font.render(msg, False, (255, 255, 255))
	text_rect = text_surface.get_rect(center = text_surface_center)
	screen.blit(text_surface, text_rect)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
			game_started = True

		if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.health <= 0:
			''' ------------------ Reset the game and restore everything ------------------ '''
			spaceship_group.sprite.health = 5
			meteor_group.empty()
			star_group.empty()
			Score.reset()
			spaceship_group.sprite.restore_ammo()
			spaceship_group.sprite.restore_health()

		if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.ammo > 0 and laser_ready:
			''' ------------------ Shooting from laser ------------------ '''
			laser = Laser(laser_path, pygame.mouse.get_pos(), 20)
			spaceship_group.sprite.decrease_ammo(1)
			laser_group.add(laser)
			laser_timer = pygame.time.get_ticks()
			laser_ready = False

		if event.type == METEOR_EVENT:
			if game_started:
				''' ------------------ Add random Meteors into the group ------------------ '''
				meteor_path = random.choice(meteor_assets_tuple)

				random_x_pos = random.randrange(5, screen_size[0] - 5)
				random_y_pos = random.randrange(-200, -50)
				random_x_speed = random.randrange(-2, 2)
				random_y_speed = random.randrange(1, 5)
				rotation_speed = random.randrange(3, 8)

				meteor = Meteor(meteor_path, random_x_pos, random_y_pos, random_x_speed, random_y_speed, rotation_speed)
				meteor_group.add(meteor)

				''' ------------------ Add random PowerUp into the group ------------------ '''
				if powerup_count == 0:
					init_powerups(hot_god_powerup_path, healing_group)
				elif powerup_count < 0:
					powerup_count = 50

				if ammo_count == 0:
					init_powerups(ammo_powerup_path, ammo_group)
				elif ammo_count < 0:
					ammo_count = 25

				powerup_count -= 1
				ammo_count -= 1

			''' ------------------ Add random stars into the group ------------------ '''
			random_x_pos = random.randrange(50, screen_size[0] - 50)
			random_y_pos = random.randrange(-50, 0)
			random_x_speed = 0
			random_y_speed = 3

			star = Background(star_asset_path, random_x_pos, random_y_pos, random_x_speed, random_y_speed)
			star_group.add(star)

	screen.fill((20, 20, 0))

	''' --------- Draw assets into the screen --------- '''
	init_background()

	if (game_started):
		if spaceship_group.sprite.health > 0:
			init_game_pross(Score)
		else:
			init_game_over()
	else:
		game_menu()

	pygame.display.update()
	clock.tick(50)

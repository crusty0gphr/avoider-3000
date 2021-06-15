import os
import re

import pygame

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
game_started = False

pygame.init()
display_info = pygame.display.Info()
screen_size_calculated = (display_info.current_w, display_info.current_h)
screen_size = screen_size_calculated

game_name = 'Avoider-3000'
laser_shot_count = 0
slow_down_timer_count = 120
powerup_count = 90
ammo_count = 35
game_timer = 0

laser_ready = False

# assets - images
spaceship_assets_path = ROOT_DIR + '/assets/spaceship/'
meteor_assets_path = ROOT_DIR + '/assets/meteors/'
star_asset_path = ROOT_DIR + '/assets/star.png'
laser_path = ROOT_DIR + '/assets/laser.png'
hot_god_powerup_path = ROOT_DIR + '/assets/powerups/hot-dog.png'
ammo_powerup_path = ROOT_DIR + '/assets/powerups/nuclear-buletons.png'
slow_down_timer = ROOT_DIR + '/assets/powerups/slow-down-timer.gif'

meteor_assets_tuple = ('asteroid/', 'planetoid/', 'space-door/', 'comet/')

# assets = sounds
laser_sound_effect = ROOT_DIR + '/assets/sounds/laser-shot.wav'


def natural_sort(l):
	convert = lambda text: int(text) if text.isdigit() else text.lower()
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
	return sorted(l, key=alphanum_key)

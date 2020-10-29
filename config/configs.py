import re

game_started = False

game_name = 'Avoider-3000'
screen_size = (1280, 768)
laser_shot_count = 0
powerup_count = 50
ammo_count = 25
laser_timer = 0
laser_ready = False

spaceship_assets_path = 'assets/spaceship/'
meteor_assets_path = 'assets/meteors/'
star_asset_path = 'assets/star.png'
laser_path = 'assets/laser.png'
hot_god_powerup_path = 'assets/powerups/hot-dog.png'
ammo_powerup_path = 'assets/powerups/nuclear-buletons.png'

meteor_assets_tuple = ('asteroid/', 'planetoid/', 'space-door/', 'comet/')

def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)

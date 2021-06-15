import os
import sys
import random
from classes.background import Background
from classes.laser import Laser
from classes.meteors import Meteor
from classes.powerup import PowerUp
from classes.scoreboard import Score
from classes.spaceship import SpaceShip
from configs import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

pygame.init()
pygame.display.set_caption(game_name)
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
clock = pygame.time.Clock()

# sprites groups
spaceship_group = pygame.sprite.GroupSingle()
explosion_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()
healing_group = pygame.sprite.Group()
slow_down_group = pygame.sprite.Group()
ammo_group = pygame.sprite.Group()

# continuous timer
METEOR_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT, 250)

# spaceship - player sprite
SpaceShip = SpaceShip(400, 500, screen)
spaceship_group.add(SpaceShip)
# score obj
Score = Score(screen)


def game_menu():
    global screen
    render_msg('-= AVOIDER =-', 100, (screen_size[0] / 2, 100))
    render_msg('3000', 72, (screen_size[0] / 2, 200))

    hot_dog = pygame.image.load(ROOT_DIR + '/assets/powerups/hot-dog.png')
    screen.blit(hot_dog, (screen_size[0] / 2 - 30, screen_size[1] / 2 - 60))
    render_msg('Press SPACE to start!', 32,
               (screen_size[0] / 2, screen_size[1] / 2 + 100))
    render_msg('Press Q to quit!', 22,
               (screen_size[0] / 2, screen_size[1] / 2 + 140))

    render_msg('- Designed by: Sargis Mardirossian - Developed by: Harutyun Mardirossian -', 18,
               (screen_size[0] / 2, screen_size[1] - 70))
    render_msg('@Corrupted.bit', 20,
               (screen_size[0] / 2, screen_size[1] - 40))


def init_power_ups(power_up_path, power_up_group):
    random_x_pos_pu = random.randrange(50, screen_size[0] - 50)
    random_y_pos_pu = random.randrange(-200, -50)

    powerup = PowerUp(power_up_path, random_x_pos_pu, random_y_pos_pu)
    power_up_group.add(powerup)


def init_background():
    # draw stars
    star_group.draw(screen)
    star_group.update()


def init_game_pross(score_obj):
    # hide the mouse cursor
    pygame.mouse.set_visible(False)

    global game_timer
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
    # draw slow down timer
    slow_down_group.draw(screen)
    slow_down_group.update()
    # draw player
    spaceship_group.draw(screen)
    spaceship_group.update()
    # game score
    Score.draw()

    ''' --------- Check collisions with the SpaceShip --------- '''
    if pygame.sprite.spritecollide(spaceship_group.sprite, meteor_group, True):
        damage = random.randrange(1, 3)
        spaceship_group.sprite.get_damage(damage)
        play_sound_effect(metal_impact_sound_effect)

    if pygame.sprite.spritecollide(spaceship_group.sprite, healing_group, True):
        spaceship_group.sprite.restore_health()
        play_sound_effect(healing_sound_effect)

    if pygame.sprite.spritecollide(spaceship_group.sprite, ammo_group, True):
        spaceship_group.sprite.restore_ammo()
        play_sound_effect(laser_reload_sound_effect)

    if pygame.sprite.spritecollide(spaceship_group.sprite, slow_down_group, True):
        for meteor in meteor_group.sprites():
            if not meteor.slow_speed:
                meteor.slow_down_movement_speed()

    for laser in laser_group:
        if pygame.sprite.spritecollide(laser, meteor_group, True):
            laser_group.remove(laser)

            score = random.randrange(10, 50, 5)
            score_obj.add_score(score)
            play_sound_effect(explosion_sound_effect)

    if pygame.time.get_ticks() - game_timer >= 125:
        laser_ready = True


def play_sound_effect(effect_path):
    soundObj = pygame.mixer.Sound(effect_path)
    soundObj.play()


def init_game_over():
    # hide the mouse cursor
    pygame.mouse.set_visible(True)
    score = Score.get_score()

    render_msg('GAME OVER', 58, (screen_size[0] / 2, screen_size[1] / 2 - 100))
    render_msg(str(score), 48, (screen_size[0] / 2, screen_size[1] / 2 - 40))
    render_msg('Press SPACE to try again!', 32,
               (screen_size[0] / 2, screen_size[1] / 2 + 100))
    render_msg('Press Q to quit the game', 22,
               (screen_size[0] / 2, screen_size[1] / 2 + 160))


def render_msg(msg, font_size, text_pos):
    font = pygame.font.Font(
        ROOT_DIR + '/assets/fonts/retro-gaming.ttf', font_size)

    text_surface_center = text_pos
    text_surface = font.render(msg, False, (255, 255, 255))
    text_rect = text_surface.get_rect(center=text_surface_center)
    screen.blit(text_surface, text_rect)


def reset_game():
    spaceship_group.sprite.health = 5
    meteor_group.empty()
    star_group.empty()
    Score.reset()
    spaceship_group.sprite.restore_ammo()
    spaceship_group.sprite.restore_health()


def start_main_music():
    ''' --- Start Main Music --- '''
    play_sound_effect(main_gameplay_music)


start_main_music()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_started = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_started:
            game_started = True
            reset_game()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and spaceship_group.sprite.health <= 0:
            ''' ------------------ Reset the game and restore everything ------------------ '''
            reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.ammo > 0 and laser_ready:
            ''' ------------------ Shooting from laser ------------------ '''
            play_sound_effect(laser_sound_effect)
            laser = Laser(laser_path, pygame.mouse.get_pos(), 20)
            spaceship_group.sprite.decrease_ammo(1)
            laser_group.add(laser)
            game_timer = pygame.time.get_ticks()
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

                meteor = Meteor(meteor_path, random_x_pos, random_y_pos,
                                random_x_speed, random_y_speed, rotation_speed)
                meteor_group.add(meteor)

                ''' ------------------ Add random PowerUp into the group ------------------ '''

                if slow_down_timer_count == 0:
                    init_power_ups(slow_down_timer, slow_down_group)
                elif slow_down_timer_count < 0:
                    slow_down_timer_count = 120

                if powerup_count == 0:
                    init_power_ups(hot_god_powerup_path, healing_group)
                elif powerup_count < 0:
                    powerup_count = 90

                if ammo_count == 0:
                    init_power_ups(ammo_powerup_path, ammo_group)
                elif ammo_count < 0:
                    ammo_count = 35

                slow_down_timer_count -= 1
                powerup_count -= 1
                ammo_count -= 1

            ''' ------------------ Add random stars into the group ------------------ '''
            random_x_pos = random.randrange(50, screen_size[0] - 50)
            random_y_pos = random.randrange(-50, 0)
            random_x_speed = 0
            random_y_speed = 3

            star = Background(star_asset_path, random_x_pos,
                              random_y_pos, random_x_speed, random_y_speed)
            star_group.add(star)

    screen.fill((20, 20, 0))

    ''' --------- Draw assets into the screen --------- '''
    init_background()

    if game_started:
        if spaceship_group.sprite.health > 0:
            init_game_pross(Score)
        else:
            init_game_over()
    else:
        game_menu()

    pygame.display.update()
    clock.tick(50)

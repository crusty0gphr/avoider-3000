"""
	Class: Meteor
	Info: for collide objects on the screen and obstacles to avoid
"""
import glob

import pygame

from configs import meteor_assets_path, natural_sort, screen_size


class Meteor(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, x_speed, y_speed, rotation_speed):
        super().__init__()
        self.angle = 0
        self.slow_speed = False

        self.meteor_collection_path = meteor_assets_path + path
        self.images = natural_sort(
            glob.glob(self.meteor_collection_path + '*.gif'))

        self.image_index = 0
        self.image = pygame.image.load(self.images[self.image_index])
        self.clean_image = self.image.copy()

        # movement dimensions
        self.x_speed = x_speed
        self.y_speed = y_speed

        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.rotation_speed = rotation_speed

    def update(self):
        self.image_index += 1
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

        self.animate_meteors()

        if 'planetoid' not in self.meteor_collection_path:
            self.rotate_meteors()

        # remove offscreen meteors
        # remove everything that left the screen for 50+ px
        if self.rect.centery > screen_size[1] + 50 or self.rect.centerx < -50 or self.rect.centerx > screen_size[
                0] + 50:
            self.kill()

    def slow_down_movement_speed(self):
        self.slow_speed = True
        self.x_speed = round((self.x_speed * 40) / 100)
        self.y_speed = round((self.y_speed * 40) / 100)

    # obstacles rotating animation
    def animate_meteors(self):
        if self.image_index >= len(self.images):
            self.image_index = 0

        self.image = pygame.image.load(self.images[self.image_index])
        # copy base image for the original orientation and dimensions
        self.clean_image = self.image.copy()

    def rotate_meteors(self):
        rotation_tuple = self.rot_center(
            self.clean_image, self.angle)  # get image center

        self.image = rotation_tuple[0]
        self.rect = rotation_tuple[1]
        self.angle += self.rotation_speed

    def rot_center(self, image, angle):
        rotated_image = pygame.transform.rotate(image, angle)  # rotate
        new_rect = rotated_image.get_rect(center=self.rect.center)

        return rotated_image, new_rect

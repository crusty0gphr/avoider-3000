"""
    Class: SpaceShip
    Info: Player character class with animation, health, ammo, and movement
"""
import pygame

from configs import screen_size
from classes.asset_manager import assets


class SpaceShip(pygame.sprite.Sprite):
    # Animation settings
    FRAME_DURATION = 40  # milliseconds per animation frame

    # Invincibility settings
    INVINCIBILITY_DURATION = 1000  # milliseconds of immunity after taking damage
    BLINK_INTERVAL = 100  # milliseconds between visibility toggles when invincible

    # Player stats
    MAX_HEALTH = 5
    MAX_AMMO = 30

    def __init__(self, x_pos, y_pos, screen_obj):
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.screen = screen_obj

        # Use pre-loaded frames from asset manager
        self.frames = assets.get_frames('spaceship')
        self.image_index = 0
        self.image = self.frames[self.image_index]
        self.clean_image = self.image.copy()
        self.center = (x_pos, y_pos)
        self.rect = self.image.get_rect(center=self.center)

        # Pre-loaded heart image for health display
        self.shield_surface = assets.get_image('heart')

        # Player stats
        self.health = self.MAX_HEALTH
        self.ammo = self.MAX_AMMO

        # Delta-time animation tracking
        self.last_update = pygame.time.get_ticks()
        self.animation_timer = 0

        # Invincibility state
        self.invincible = False
        self.invincible_timer = 0
        self.blink_timer = 0
        self.visible = True

    def update(self):
        now = pygame.time.get_ticks()
        dt = now - self.last_update
        self.last_update = now

        self.rect.center = pygame.mouse.get_pos()

        self.animate_space_ship(dt)
        self.update_invincibility(dt)
        self.display_health()
        self.display_ammo()
        self.screen_constrain()
        self.rotate()

    def animate_space_ship(self, dt):
        """Delta-time based animation - consistent speed regardless of framerate"""
        self.animation_timer += dt
        if self.animation_timer >= self.FRAME_DURATION:
            self.animation_timer = 0
            self.image_index = (self.image_index + 1) % len(self.frames)

        self.image = self.frames[self.image_index]
        self.clean_image = self.image.copy()

    def update_invincibility(self, dt):
        """Handle invincibility timer and blinking effect"""
        if self.invincible:
            self.invincible_timer -= dt
            self.blink_timer += dt

            # Toggle visibility for blinking effect
            if self.blink_timer >= self.BLINK_INTERVAL:
                self.blink_timer = 0
                self.visible = not self.visible

            # End invincibility
            if self.invincible_timer <= 0:
                self.invincible = False
                self.visible = True

            # Apply visibility to image alpha
            if not self.visible:
                self.image = self.image.copy()
                self.image.set_alpha(100)

    def display_health(self):
        for index in range(self.health):
            self.screen.blit(
                self.shield_surface,
                ((index + 1) * 25, screen_size[1] - 40)
            )

    def display_ammo(self):
        font = assets.get_font(18)
        text_surface_center = (screen_size[0] - 70, screen_size[1] - 23)
        text_surface = font.render(
            'AMMO: ' + str(self.ammo), False, (255, 255, 255)
        )
        text_rect = text_surface.get_rect(center=text_surface_center)
        self.screen.blit(text_surface, text_rect)

    def get_damage(self, damage_amount):
        """
        Apply damage to player if not invincible.
        Returns True if damage was applied, False if blocked by invincibility.
        """
        if not self.invincible:
            self.health -= damage_amount
            self.invincible = True
            self.invincible_timer = self.INVINCIBILITY_DURATION
            self.blink_timer = 0
            return True
        return False

    def decrease_ammo(self, shot_amount):
        """Decrease ammo when player shoots"""
        self.ammo -= shot_amount

    def restore_health(self):
        self.health = self.MAX_HEALTH

    def restore_ammo(self):
        self.ammo = self.MAX_AMMO

    def screen_constrain(self):
        """Keep player within screen boundaries"""
        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.right >= screen_size[0]:
            self.rect.right = screen_size[0]

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= screen_size[1] - 50:
            self.rect.bottom = screen_size[1] - 50

    def rotate(self):
        """Tilt spaceship based on mouse movement direction"""
        mouse_rel = pygame.mouse.get_rel()

        if mouse_rel[0] < 0:
            # Tilt left when moving left
            self.image = self.rotate_from_center(self.clean_image, 15)
        elif mouse_rel[0] > 0:
            # Tilt right when moving right
            self.image = self.rotate_from_center(self.clean_image, -15)
        else:
            # Reset to upright when not moving
            self.image = self.rotate_from_center(self.clean_image, 0)

    def rotate_from_center(self, image, angle):
        """Rotate image around its center without changing dimensions"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

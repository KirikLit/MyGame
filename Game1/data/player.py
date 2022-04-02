import pygame
import data.tileset_loader as tilesheet
from data.config import *


class Player:
    def __init__(self, x, y):
        self.alive = True
        self.speed = 5
        self.action = 0
        self.action_frame = 0
        self.direction = 1
        self.flip = False
        self.update_time = pygame.time.get_ticks()
        self.vel_y = 0
        self.in_air = False
        self.jump = False
        self.after_jump = False
        self.attack = False
        self.health = 100
        self.visible = True
        self.hit_counter = 0
        self.key = False

        # load images
        anim_types = ['idle', 'run', 'jump_up', 'jump_down', 'attack', 'death', 'hit', 'sword', 'before_after_jump']
        self.anim_list = tilesheet.unpack_spritesheet(f'data/img/player', anim_types, 2.5, 16)
        self.image = self.anim_list[self.action][self.action_frame]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.hit_counter > 0:
            self.hit_counter -= 1
        self.update_anim()
        self.check_alive()

    def draw(self, surface):
        if self.visible:
            surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def move(self, moving_left, moving_right):
        # reset vars
        dx, dy = 0, 0

        # move left / right
        if not self.attack:
            if moving_left:
                dx -= self.speed
                self.flip = True
                self.direction = -1
            elif moving_right:
                dx += self.speed
                self.flip = False
                self.direction = 1

        # jump
        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # temp collision
        if self.rect.bottom + dy >= 300:
            dy = 300 - self.rect.bottom
            if self.in_air:
                self.in_air = False
                self.after_jump = True

        # Update pos
        self.rect.x += dx
        self.rect.y += dy

    def update_action(self, new_action):
        if new_action != self.action and self.action != 6:
            self.action = new_action
            # update anim settings
            self.action_frame = 0
            self.update_time = pygame.time.get_ticks()

    def update_anim(self):
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.action_frame += 1
        if self.action_frame == len(self.anim_list[self.action]):
            if self.action == 6:
                self.action = 0
                self.action_frame = 0
            elif self.action == 5:
                self.visible = False
            elif self.action == 8:
                self.update_action(0)
                self.after_jump = False
            self.action_frame = 0
        self.image = self.anim_list[self.action][self.action_frame]

    def hit(self, damage):
        if self.hit_counter == 0 and self.alive:
            self.hit_counter = HIT_COOLDOWN
            self.update_action(6)
            self.health -= damage

    def check_alive(self):
        if self.health <= 0:
            self.update_action(5)
            self.alive = False


class Sword(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.images = player.anim_list[7]
        self.img_index = 0
        self.image = self.images[self.img_index]
        self.rect = self.image.get_rect()
        self.update_time = pygame.time.get_ticks()
        self.player = player
        self.used = False

    def update(self, enemy_group):
        self.rect.centerx = self.player.rect.centerx + ((self.player.image.get_width() / 2 + 15) * self.player.direction)
        self.rect.centery = self.player.rect.centery

        if not self.used:
            for enemy in enemy_group:
                if pygame.sprite.collide_rect(enemy, self):
                    enemy.hit(enemy_config[enemy.enemy_type]['selfdamage'])
                    self.used = True

    def draw(self, surface):
        surface.blit(pygame.transform.flip(self.image, self.player.flip, False), self.rect)

    def anim(self):
        if pygame.time.get_ticks() - self.update_time > 50:
            self.update_time = pygame.time.get_ticks()
            self.img_index += 1
        if self.img_index >= len(self.images):
            return True
        else:
            self.image = self.images[self.img_index]

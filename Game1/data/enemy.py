import pygame
import random
import data.tileset_loader as tilesheet
from data.config import *


class Enemy:
    def __init__(self, enemy_type, x, y):
        self.anim_list = []
        self.x = x
        self.y = y
        self.health = 100
        self.speed = 1
        self.action_frame = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.alive = True
        self.dead = False
        self.direction = 1
        self.flip = False
        self.vel_y = 0
        self.idling = False
        self.idling_counter = 0
        self.move_counter = 0
        self.moving_left = False
        self.moving_right = False
        self.hit_counter = 0
        self.move_timer = False
        self.enemy_type = enemy_type

        # anim types
        anim_types = ['idle', 'walk', 'hit', 'death']
        if enemy_type == 'goblin':
            anim_types.append('attack')
        elif enemy_type == 'worm':
            anim_types[0] = 'walk'
        # load images
        for anim in anim_types:
            if anim == 'attack':
                img = tilesheet.load_sprite_sheet(f'data/img/enemy/{enemy_type}/{anim}.png', 1, 24)
            else:
                img = tilesheet.load_sprite_sheet(f'data/img/enemy/{enemy_type}/{anim}.png', 1, 16)
            self.anim_list.append(img)
        self.image = self.anim_list[self.action][self.action_frame]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        # scroll
        self.rect.x -= scroll
        # update hit counter
        if self.hit_counter > 0:
            self.hit_counter -= 1
        self.move_timer = not self.move_timer
        # update all
        self.update_anim()
        self.check_alive()

    def draw(self, surface, scroll):
        slime_flip = lambda: not self.flip if self.enemy_type == 'slime' else self.flip
        surface.blit(pygame.transform.flip(self.image, slime_flip(), False), self.rect)

    def move(self, obstacle_list):
        # reset vars
        dx, dy = 0, 0

        # move left / right
        if self.moving_left:
            dx -= self.speed
            self.flip = True
            self.direction = -1
        elif self.moving_right:
            dx += self.speed
            self.flip = False
            self.direction = 1

        # gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        # apply velocity
        dy += self.vel_y

        # collision
        for tile in obstacle_list:
            # check x collision
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
                # if ai hit the wall then turn around
                self.direction *= -1
                self.move_counter = 0
            # check y collision
            if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                # check if jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile.rect.bottom - self.rect.top
                else:
                    dy = tile.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False

        # Update pos
        self.rect.x += dx
        self.rect.y += dy

    def ai(self, obst):
        if random.randint(1, 300) == 1 and not self.idling and self.enemy_type != 'worm':
            self.idling = True
            self.idling_counter = 180
            self.update_action(0)
        elif not self.idling:
            if self.direction == 1:
                self.moving_right = True
            else:
                self.moving_right = False
            self.moving_left = not self.moving_right
            self.update_action(1)
            if self.move_timer:
                self.move(obst)
            self.move_counter += 1
            # update vision

            if self.move_counter > TILE_SIZE * 3:
                self.direction *= -1
                self.move_counter *= -1
        else:
            self.idling_counter -= 1
            if self.idling_counter <= 1:
                self.idling = False

    def update_action(self, new_action):
        if new_action != self.action and self.action != 2 and self.action != 4:
            self.action = new_action
            # update anim settings
            self.action_frame = 0
            self.update_time = pygame.time.get_ticks()

    def update_anim(self):
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.action_frame += 1
        if self.action_frame == len(self.anim_list[self.action]):
            if self.action == 2:
                self.action = 0
                self.action_frame = 0
                self.idling = False
            elif self.action == 3:
                self.dead = True
                self.action_frame = len(self.anim_list[self.action]) - 1
            elif self.action == 4:
                self.action = 0
                self.action_frame = 0
            else:
                self.action_frame = 0
        self.image = self.anim_list[self.action][self.action_frame]

    def hit(self, damage):
        if self.alive:
            self.update_action(2)
            self.health -= damage
            self.idling = True

    def check_alive(self):
        if self.health <= 0:
            self.update_action(3)
            self.alive = False
            self.moving_left, self.moving_right = False, False

import pygame
from .config import ANIMATION_COOLDOWN
from .tileset_loader import unpack_spritesheet, load_sprite_sheet


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, scale, name, animated=False, interactive=False, dokill=False):
        pygame.sprite.Sprite.__init__(self)
        self.type = name
        self.x = x
        self.y = y
        self.animated = animated
        self.interactive = interactive
        self.action = 0
        self.action_frame = 0
        self.update_time = pygame.time.get_ticks()
        self.dokill = dokill
        # load image
        if animated and not interactive:
            self.anim_list = unpack_spritesheet(f'data/img/object', [name], scale, width)
            self.image = self.anim_list[self.action][self.action_frame]
        elif interactive and animated:
            self.anim_list = unpack_spritesheet(f'data/img/object', [f'{name}_idle', f'{name}_interact'], scale, width)
            self.image = self.anim_list[self.action][self.action_frame]
        else:
            self.image = pygame.image.load(f'data/img/object/{name}.png')
            self.image = pygame.transform.scale(self.image, (width * scale, self.image.get_height() * scale))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def update(self, scroll):
        if self.animated:
            self.update_anim()
        # scroll
        self.rect.x -= scroll

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            # update anim settings
            self.action_frame = 0
            self.update_time = pygame.time.get_ticks()

    def update_anim(self):
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.action_frame += 1
        if self.action_frame == len(self.anim_list[self.action]):
            if self.action == 1:
                self.action_frame = len(self.anim_list[self.action]) - 1
                if self.dokill:
                    self.kill()
            else:
                self.action_frame = 0
        self.image = self.anim_list[self.action][self.action_frame]
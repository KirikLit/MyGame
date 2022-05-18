import pygame

# load background
background0 = pygame.image.load(f'data/img/background/bg_0.png')
background1 = pygame.image.load(f'data/img/background/bg_1.png')
background2 = pygame.image.load(f'data/img/background/bg_2.png')


def draw_bg(surface, bg_scroll):
    surface.fill((0, 0, 0))
    for x in range(6):
        surface.blit(background0, ((0 + x * 384) - bg_scroll * 0.6, 0))
        surface.blit(background1, ((0 + x * 384) - bg_scroll * 0.7, 0))
        surface.blit(background2, ((0 + x * 384) - bg_scroll * 0.8, 0))

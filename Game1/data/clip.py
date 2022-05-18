import pygame


def clip(surf, x, y, x_size, y_size, scale):
    clipR = pygame.Rect(x, y, x_size, y_size)
    image = surf.subsurface(clipR).convert_alpha()
    image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
    return image

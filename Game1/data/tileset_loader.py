import pygame
from data.clip import clip


def load_tileset(path, scale):
    tileset_img = pygame.image.load(path).convert_alpha()
    tileset_img.set_colorkey((0, 0, 0))
    tile_size = [16, 16]
    rows = tileset_img.get_height() // tile_size[1]
    cols = tileset_img.get_width() // tile_size[0]
    images = []
    for row in range(rows):
        for tile in range(cols):
            images.append(clip(tileset_img, tile * tile_size[0], row * tile_size[1], tile_size[0], tile_size[1], scale))

    return images


def load_sprite_sheet(path, scale, width):
    tileset_img = pygame.image.load(path).convert_alpha()
    tileset_img.set_colorkey((0, 0, 0))
    tile_size = (tileset_img.get_height(), width)
    cols = tileset_img.get_width() // width
    images = []
    for tile in range(cols):
        images.append(clip(tileset_img, tile * tile_size[1], 0, tile_size[1], tile_size[0], scale))

    return images


def unpack_spritesheet(path, types, scale, width):
    temp_list = []

    for anim in types:
        anim = load_sprite_sheet(f'{path}/{anim}.png', scale, width)
        temp_list.append(anim)

    return temp_list

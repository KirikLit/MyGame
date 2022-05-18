import pygame
import json
from .config import obstacle_list, TILE_SIZE
from .tileset_loader import load_tileset
from .player import Player
from .objects import Object
from .enemy import Enemy
from .tile import Tile


class World:
    def __init__(self, world_data):
        with open('data/levels/level_data.json') as data:
            self.json_data = json.load(data)
            data.close()
            self.world_data = world_data
        self.img_list = load_tileset('data/img/tileset.png', 1)

    def read_data(self):
        obstacle_group = pygame.sprite.Group()
        decoration_group = pygame.sprite.Group()

        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                if tile in obstacle_list:
                    img = self.img_list[tile]
                    tile = Tile(img, x * TILE_SIZE, y * TILE_SIZE)
                    obstacle_group.add(tile)
                elif tile not in obstacle_list:
                    img = self.img_list[tile]
                    tile = Tile(img, x * TILE_SIZE, y * TILE_SIZE)
                    decoration_group.add(tile)

        return obstacle_group, decoration_group

    def read_json(self):
        enemy_group = []
        object_group = pygame.sprite.Group()
        interactive_group = pygame.sprite.Group()
        sword_interactive_group = pygame.sprite.Group()

        for enemy in self.json_data['level_1']['enemies']:
            for coord in self.json_data['level_1']['enemies'][enemy]:
                enem = Enemy(enemy, coord[0], coord[1])
                enemy_group.append(enem)

        for dec in self.json_data['level_1']['decorations']:
            for coord in self.json_data['level_1']['decorations'][dec]:
                if dec == 'vase':
                    args = [coord[0], coord[1], 16, 1, 'vase', True, True]
                    obj = Object(*args)
                    sword_interactive_group.add(obj)
                else:
                    args = [coord[0], coord[1], 8, 1, 'torch', True]
                    obj = Object(*args)
                object_group.add(obj)

        for hel in self.json_data['level_1']['health']:
            for coord in self.json_data['level_1']['health'][hel]:
                health = Object(coord[0], coord[1], 8, 1, hel)
                object_group.add(health)
                interactive_group.add(health)

        return enemy_group, object_group, interactive_group, sword_interactive_group

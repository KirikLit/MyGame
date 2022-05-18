import pygame
from data.config import *


class HealthBar:
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, surface, health):
        # update health
        self.health = health
        # calculate ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(surface, BLACK, (self.x - 1, self.y - 1, 77, 12))
        pygame.draw.rect(surface, RED, (self.x, self.y, 75, 10))
        pygame.draw.rect(surface, GREEN, (self.x, self.y, 75 * ratio, 10))

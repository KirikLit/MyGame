import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        # self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.x = x
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        self.rect.x -= scroll

    def draw(self, surface, bg):
        surface.blit(self.image, pygame.Rect(self.x - bg, self.rect.y, self.rect.width, self.rect.height))

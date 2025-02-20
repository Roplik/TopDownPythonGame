import pygame
from pytmx import *
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, tile_index, sprite_type, tile_size=(16, 16)):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = self.load_tile(tile_index, tile_size)
        self.rect = self.image.get_rect(topleft=pos)
        # self.hitbox = self.rect.inflate(10, -10)

    def load_tile(self, tile_index, tile_size=(16, 16), scale_size=(32, 32)):
        # Загружаем тайлсет
        tileset = pygame.image.load("image/gothic_city_tiles.png").convert_alpha()

        # Вычисляем координаты в тайлсете
        tiles_per_row = tileset.get_width() // tile_size[0]
        x = (tile_index % tiles_per_row) * tile_size[0]
        y = (tile_index // tiles_per_row) * tile_size[1]

        # Вырезаем нужный спрайт из тайлсета
        tile_rect = pygame.Rect(x, y, tile_size[0], tile_size[1])
        tile = tileset.subsurface(tile_rect)

        # Увеличиваем размер спрайта до 64x64
        scaled_tile = pygame.transform.scale(tile, scale_size)

        return scaled_tile


class Decoration(pygame.sprite.Sprite):
    def __init__(self, pos, groups, tile_index, sprite_type, tile_size=(16, 16)):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = self.load_tile(tile_index, tile_size)
        self.rect = self.image.get_rect(topleft=pos)

    def load_tile(self, tile_index, tile_size=(16, 16), scale_size=(32, 32)):
        # Загружаем тайлсет
        tileset = pygame.image.load("image/gothic_city_tiles.png").convert_alpha()

        # Вычисляем координаты в тайлсете
        tiles_per_row = tileset.get_width() // tile_size[0]
        x = (tile_index % tiles_per_row) * tile_size[0]
        y = (tile_index // tiles_per_row) * tile_size[1]

        # Вырезаем нужный спрайт из тайлсета
        tile_rect = pygame.Rect(x, y, tile_size[0], tile_size[1])
        tile = tileset.subsurface(tile_rect)

        # Увеличиваем размер спрайта до 64x64
        scaled_tile = pygame.transform.scale(tile, scale_size)

        return scaled_tile
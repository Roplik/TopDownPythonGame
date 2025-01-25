import os
import sys

import pygame

import level1
from settings import Settings
from player import Player
from level1 import Level


class Game:
    def __init__(self):
        # Инициализация Pygame
        pygame.init()
        self.settings = Settings()
        self.settings.load_settings()
        # Создание окна
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Game")
        self.level = Level()
        self.level.play_music()

    def draw_colliders(self):
        obstacles_sprites = self.level.obstacles_sprites
        for sprite in obstacles_sprites:
            # Отрисовка коллайдера препятствия
            pygame.draw.rect(self.screen, (255, 0, 0), sprite.rect, 2)  # Красный прямоугольник

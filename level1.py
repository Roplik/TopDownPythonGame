import pygame
import settings
from tile import Tile
from player import Player
from debug import debug
from support import *
from gui import *
from Mobs import *
import random

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.enemy_array = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        self.create_map()
        self.music_path = 'music/Yoann Laulan - 1-Dead Cells.mp3'
        self.setting = settings.Settings()
        self.setting.load_settings()
        self.timer = Timer(pygame.time.get_ticks())
        self.complete_level = False
        self.player_die = False

    def check_change_scene(self):
        if self.timer.second >= 1500:
            pygame.mixer.music.stop()
            self.complete_level = True
        elif self.player.die:
            pygame.mixer.music.stop()
            self.player_die = True

    def play_music(self):  # музыка
        pygame.mixer.music.load(self.music_path)  # Укажите путь к вашему файлу
        pygame.mixer.music.set_volume(self.setting.volume)
        pygame.mixer.music.play(-1)

    def create_map(self):
        layout = import_csv_layout("maps/main_wall.csv")

        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col != "-1":
                    x = col_index * settings.Settings().tilesize
                    y = row_index * settings.Settings().tilesize
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites], sprite_type="wall",
                         tile_index=int(col))

        # Создаем игрока после загрузки карты
        self.player = Player((650, 1000), [self.visible_sprites], self.obstacles_sprites, self.enemy_array)
        self.Skelet = Skelet((650, 600), [self.visible_sprites, self.enemy_array], self.player)

    def run(self):
        self.display_surface.fill((0, 0, 0))  # Очистка экрана
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        # Отрисовка границ коллайдера игрока
        # self.player.draw_collider(self.display_surface)
        debug(self.player.direction)
        self.timer.draw(True)
        draw_health_and_lives(pygame.display.get_surface(), self.player)
        self.check_change_scene()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # пол
        self.floor_surf = pygame.image.load("maps/main.png").convert()
        self.floor_surf = pygame.transform.scale(self.floor_surf,
                                                 (self.floor_surf.get_size()[0] * 2, self.floor_surf.get_size()[1] * 2))
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

        # Лимит мобов
        self.max_mobs = 10  # Максимальное количество мобов на карте
        self.mob_spawn_cooldown = 1  # Задержка между появлениями мобов (в миллисекундах)
        self.last_spawn_time = 0  # Время последнего появления моба

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # рисуем пол
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            # Отрисовка здоровья для врагов
            if isinstance(sprite, Skelet):  # Проверяем, является ли объект врагом
                sprite.draw_health_text(self.display_surface, self.offset)
                sprite.update_particles(screen, self.offset)
        self.spawn_mobs(player)

    def spawn_mobs(self, player):
        current_time = pygame.time.get_ticks()
        enemy_group = player.enemies_group
        if current_time - self.last_spawn_time > self.mob_spawn_cooldown and len(player.enemies_group) < self.max_mobs:
            # Генерация случайной позиции для моба
            spawn_x = random.randint(34, 1210)
            spawn_y = random.randint(86, 550)
            spawn_pos = (spawn_x, spawn_y)

            # Проверка, чтобы моб не появлялся слишком близко к игроку
            if math.hypot(spawn_x - player.rect.centerx, spawn_y - player.rect.centery) > 200:
                new_mob = Skelet(spawn_pos, self, player)  # Создаём нового моба
                enemy_group.add(new_mob)
                player.enemies_group.add(new_mob)
                self.last_spawn_time = current_time  # Обновляем время последнего появления


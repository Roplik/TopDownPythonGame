import pygame
import math
from pygame.math import Vector2
from sys import exit
import random


def draw_text(surface, text, pos, font_size=24, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)  # Шрифт и размер текста
    text_surface = font.render(text, True, color)  # Создаём поверхность с текстом
    surface.blit(text_surface, pos)  # Отрисовываем текст на экране


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles_sprites, enemy_sprites, projectile):
        super().__init__(groups)
        self.image = pygame.image.load("Char_Sprites/char_idle_up_anim.gif").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.walk_speed = 5
        self.run_speed = 8
        self.damage = 50

        self.sprite_width = 32  # ширина одного спрайта
        self.sprite_height = 32  # высота одного спрайта
        self.sprites_per_row = 4  # количество спрайтов в строке

        self.visible_sprite = groups

        self.screen = pygame.display.get_surface()

        # Инициализация жизней и здоровья
        self.max_health = 100
        self.current_health = self.max_health
        self.die = False
        self.win = False

        # Задержка перед получением следующего урона
        self.invincible_duration = 2000  # 2000 мс (2 секунды)
        self.last_damage_time = 0
        self.invincible = False

        self.enemies_group = enemy_sprites
        self.fireballs = projectile

        # Таймер для атаки
        self.attack_cooldown = 1000  # Интервал между атаками (в миллисекундах)
        self.last_attack_time = 0  # Время последней атаки
        self.attack_radius = 100

        # Система стрельбы
        self.fireball_cooldown = 1000  # Задержка между выстрелами (в миллисекундах)
        self.last_fireball_time = 0  # Время последнего выстрела

        self.exp = 0
        self.level = 1
        self.exp_to_next_level = 100

        # region load_sprite
        # Загружаем и масштабируем спрайты
        self.up_run = pygame.transform.scale(
            pygame.image.load("Char_Sprites/char_run_up_anim_strip_6.png").convert_alpha(),
            (self.sprite_width * 6, self.sprite_height))
        self.down_run = pygame.transform.scale(
            pygame.image.load("Char_Sprites/char_run_down_anim_strip_6.png").convert_alpha(),
            (self.sprite_width * 6, self.sprite_height))
        self.left_run = pygame.transform.scale(
            pygame.image.load("Char_Sprites/char_run_left_anim_strip_6.png").convert_alpha(),
            (self.sprite_width * 6, self.sprite_height))
        self.right_run = pygame.transform.scale(
            pygame.image.load("Char_Sprites/char_run_right_anim_strip_6.png").convert_alpha(),
            (self.sprite_width * 6, self.sprite_height))

        self.up_idle = pygame.transform.scale(
            pygame.image.load("Char_Sprites/char_idle_up_anim_strip_6.png").convert_alpha(),
            (self.sprite_width * 6, self.sprite_height))
        self.down_idle = pygame.transform.scale(
            pygame.image.load("Char_Sprites/char_idle_down_anim_strip_6.png").convert_alpha(),
            (self.sprite_width * 6, self.sprite_height))
        self.left_idle = pygame.transform.scale(
            pygame.image.load("Char_Sprites/char_idle_left_anim_strip_6.png").convert_alpha(),
            (self.sprite_width * 6, self.sprite_height))
        self.right_idle = pygame.transform.scale(
            pygame.image.load("Char_Sprites/char_idle_right_anim_strip_6.png").convert_alpha(),
            (self.sprite_width * 6, self.sprite_height))
        # endregion
        self.direction_anim = "up"

        self.current_frame = 0
        self.frame_rate = 5  # скорость смены кадров
        self.frame_counter = 0

        self.obstacles_sprites = obstacles_sprites
        self.sprites_run = {
            'up': [self.get_sprite(self.up_run, i) for i in range(6)],
            'down': [self.get_sprite(self.down_run, i) for i in range(6)],
            'left': [self.get_sprite(self.left_run, i) for i in range(6)],
            'right': [self.get_sprite(self.right_run, i) for i in range(6)]
        }
        self.sprites_idle = {
            'up': [self.get_sprite(self.up_idle, i) for i in range(6)],
            'down': [self.get_sprite(self.down_idle, i) for i in range(6)],
            'left': [self.get_sprite(self.left_idle, i) for i in range(6)],
            'right': [self.get_sprite(self.right_idle, i) for i in range(6)]
        }

        # Список всех возможных улучшений

        # Список всех возможных улучшений с весами
        self.all_upgrades = [
            {
                "name": "Increase Health",
                "effect": lambda: (setattr(self, 'max_health', self.max_health + 20),
                                   setattr(self, 'current_health', self.max_health)),
                "description": "Max health +20",
                "weight": 3  # Высокий шанс выпадения
            },
            {
                "name": "Increase Speed",
                "effect": lambda: (setattr(self, 'walk_speed', self.walk_speed + 0.5),
                                   setattr(self, 'run_speed', self.run_speed + 0.5)),
                "description": "Movement speed +0.5",
                "weight": 2  # Средний шанс выпадения
            },
            {
                "name": "Increase Damage",
                "effect": lambda: setattr(self, 'damage', self.damage + 5),
                "description": "Attack damage +5",
                "weight": 2  # Средний шанс выпадения
            },
            {
                "name": "Increase Attack Speed",
                "effect": lambda: setattr(self, 'attack_cooldown', max(10, self.attack_cooldown - 5)),
                "description": "Attack cooldown -5",
                "weight": 1  # Низкий шанс выпадения
            },
            {
                "name": "Increase fireball throwing frequency",
                "effect": lambda: setattr(self, 'fireball_cooldown', max(10, self.fireball_cooldown - 5)),
                "description": "Throwing cooldown -5",
                "weight": 1  # Низкий шанс выпадения
            }
        ]

    def gain_exp(self):
        # Проверяем, сколько уровней игрок может поднять
        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level  # Уменьшаем опыт на необходимое количество
            self.level_up()  # Поднимаем уровень

    def level_up(self):
        self.level += 1
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        self.show_level_up_menu()

    def show_level_up_menu(self):
        # Выбираем случайные улучшения с учетом весов и без повторений
        selected_upgrades = self.select_unique_upgrades(k=3)

        # Отображаем меню с выбором
        screen = pygame.display.get_surface()
        menu_surface = pygame.Surface((400, 300))
        menu_surface.fill((50, 50, 50))
        font = pygame.font.Font(None, 36)

        # Отрисовываем текст для каждого улучшения
        y_offset = 20
        for i, upgrade in enumerate(selected_upgrades, start=1):
            text = font.render(f"{i}. {upgrade['description']}", True, (255, 255, 255))
            menu_surface.blit(text, (20, y_offset))
            y_offset += 50

        # Отображаем меню на экране
        screen.blit(menu_surface, (200, 150))
        pygame.display.flip()

        # Ожидаем выбора игрока
        choice = None
        while choice is None:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        choice = 0
                    elif event.key == pygame.K_2:
                        choice = 1
                    elif event.key == pygame.K_3:
                        choice = 2
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        # Применяем выбранное улучшение
        selected_upgrade = selected_upgrades[choice]
        selected_upgrade["effect"]()
        print(f"Applied upgrade: {selected_upgrade['name']}")

    def select_unique_upgrades(self, k):
        """Выбирает k уникальных улучшений с учетом весов"""
        upgrades = self.all_upgrades.copy()  # Копируем список улучшений
        selected = []

        for _ in range(k):
            if not upgrades:
                break  # Если улучшения закончились, прекращаем выбор

            # Выбираем улучшение с учетом весов
            weights = [upgrade["weight"] for upgrade in upgrades]
            chosen = random.choices(upgrades, weights=weights, k=1)[0]
            selected.append(chosen)

            # Удаляем выбранное улучшение из списка
            upgrades.remove(chosen)

        return selected

    def take_damage(self, amount):
        if not self.invincible:  # Проверяем, не находится ли игрок в неуязвимости
            self.current_health -= amount
            self.last_damage_time = pygame.time.get_ticks()  # Обновляем время последнего урона
            self.invincible = True
            if self.current_health <= 0:
                self.die = True

    def invincible_switch(self):
        if self.invincible:
            # Проверяем, истекло ли время неуязвимости
            if pygame.time.get_ticks() - self.last_damage_time > self.invincible_duration:
                self.invincible = False

    def get_sprite(self, image, index):
        return image.subsurface(index * self.sprite_width, 0, self.sprite_width, self.sprite_height)

    def animate(self):
        if self.direction.magnitude() != 0:
            self.frame_counter += 1
            if self.frame_counter >= self.frame_rate:
                self.current_frame += 1
                self.frame_counter = 0
                if self.current_frame >= len(self.sprites_run[self.direction_anim]):
                    self.current_frame = 0
            # Получаем изображение из списка спрайтов
            self.image = self.sprites_run[self.direction_anim][self.current_frame]
        else:
            self.frame_counter += 1
            if self.frame_counter >= self.frame_rate:
                self.current_frame += 1
                self.frame_counter = 0
                if self.current_frame >= len(self.sprites_idle[self.direction_anim]):
                    self.current_frame = 0
            # Получаем изображение из списка спрайтов
            self.image = self.sprites_idle[self.direction_anim][self.current_frame]

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * self.speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def input(self):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()  # Получаем состояние кнопок мыши

        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_LSHIFT]:
            self.speed = 10
        else:
            self.speed = 5

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
            self.direction_anim = "up"
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.direction_anim = "down"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.direction_anim = "right"
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.direction_anim = "left"

        # Проверяем, нажата ли левая кнопка мыши
        if mouse_buttons[0]:  # Индекс 0 соответствует левой кнопке мыши
            self.shoot_fireball()

        # Проверка на одновременное нажатие противоположных клавиш
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and (keys[pygame.K_s] or keys[pygame.K_DOWN]):
            self.direction.y = 0  # Остановка по оси Y
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.direction.x = 0  # Остановка по оси X

    def collision(self, direction):
        # Проверка на столкновения с препятствиями
        if direction == "horizontal":
            for obstacle in self.obstacles_sprites:
                if self.hitbox.colliderect(obstacle.rect):
                    # Если движение вправо
                    if self.direction.x > 0:
                        self.hitbox.right = obstacle.rect.left
                    # Если движение влево
                    if self.direction.x < 0:
                        self.hitbox.left = obstacle.rect.right

        if direction == "vertical":
            for obstacle in self.obstacles_sprites:
                if self.hitbox.colliderect(obstacle.rect):
                    # Если движение вниз
                    if self.direction.y > 0:
                        self.hitbox.bottom = obstacle.rect.top
                    # Если движение вверх
                    if self.direction.y < 0:
                        self.hitbox.top = obstacle.rect.bottom

    def draw_collider(self, surface):
        # Отрисовка коллайдера игрока
        collider_color = (255, 0, 0)  # Красный цвет для коллайдера
        pygame.draw.rect(surface, collider_color, self.rect, 2)  # Рисует прямоугольник вокруг коллайдера

    def find_nearest_enemy(self):
        nearest_enemy = None
        min_distance = float('inf')

        for enemy in self.enemies_group:
            distance = math.hypot(self.rect.centerx - enemy.rect.centerx, self.rect.centery - enemy.rect.centery)
            if distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy
        return nearest_enemy

    def auto_attack(self):
        current_time = pygame.time.get_ticks()  # Получаем текущее время
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.attack()  # Вызываем метод атаки
            self.last_attack_time = current_time  # Обновляем время последней атаки

    def attack(self):
        nearest_enemy = self.find_nearest_enemy()
        if nearest_enemy:
            distance = math.hypot(self.rect.centerx - nearest_enemy.rect.centerx,
                                  self.rect.centery - nearest_enemy.rect.centery)
            if distance <= self.attack_radius:
                # Наносим урон ближайшему врагу
                nearest_enemy.take_damage(self.damage)  # Пример нанесения урона

    def shoot_fireball(self):
        current_time = pygame.time.get_ticks()

        # --------------------------------тут начинается жесткий посдсчет смещения камеры----------------------------- #
        half_width = self.screen.get_size()[0] // 2
        half_height = self.screen.get_size()[1] // 2
        offset = Vector2()
        offset.x = self.rect.centerx - half_width
        offset.y = self.rect.centery - half_height
        # ------------------------------------------------------------------------------------------------------------ #

        if current_time - self.last_fireball_time > self.fireball_cooldown:
            self.last_fireball_time = current_time
            mouse_pos = pygame.mouse.get_pos()  # Получаем экранные координаты мыши
            # Преобразуем экранные координаты в мировые
            world_mouse_pos = Vector2(mouse_pos) + offset
            # Направление от игрока к курсору мыши (в мировых координатах)
            direction = world_mouse_pos - Vector2(self.rect.center)
            if direction.length() > 0:  # Проверяем, чтобы направление не было нулевым
                fireball = Fireball(self.visible_sprite, self.rect.center, direction, self.enemies_group,
                                    self.obstacles_sprites)
                self.fireballs.add(fireball)  # Добавляем фаерболл в группу спрайтов

    def update(self):
        self.input()
        self.move()
        self.animate()
        self.invincible_switch()
        self.auto_attack()
        self.gain_exp()


# Класс фаерболла
class Fireball(pygame.sprite.Sprite):
    def __init__(self, spite_group, pos, direction, enemies_group, object_group):
        super().__init__(spite_group)
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (8, 8), 8)
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction.normalize()
        self.speed = 10
        self.damage = 20
        self.enemy_group = enemies_group
        self.object_group = object_group

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        # Проверяем столкновения с врагами
        for enemy in pygame.sprite.spritecollide(self, self.enemy_group, False):
            enemy.take_damage(self.damage)  # Наносим урон врагу
            self.kill()  # Удаляем фаерболл
        if pygame.sprite.spritecollide(self, self.object_group, False):
            self.kill()  # Удаляем фаерболл

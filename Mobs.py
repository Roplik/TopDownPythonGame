import pygame
import math
from particl import *
import random

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

frames = []


# Функция для разделения спрайт-листа
def split_spritesheet(spritesheet, rows, cols, width, height):
    global frames
    for row in range(rows):
        for col in range(cols):
            x = col * width
            y = row * height
            frame = spritesheet.subsurface(pygame.Rect(x, y, width, height))
            frames.append(frame)
    return frames


# Класс моба
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, image, health, damage, speed, exp, distance):
        super().__init__(groups)
        self.orig_images = image
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)  # Уменьшаем hitbox для столкновений
        self.speed = speed  # Скорость движения врага
        self.player = player  # Ссылка на игрока
        self.chasing = False  # Флаг для отслеживания состояния погони
        self.damage = damage
        self.health = health
        self.max_health = health
        self.direction_word = "right"
        self.hit_particles = []  # Список для хранения частиц удара
        self.give_exp = exp
        self.distance = distance

        self.death_sound = pygame.mixer.Sound('sound/death_sound.mp3')
        self.death_sound.set_volume(0.5 * self.player.settings.volume)

    def check_collision_with_enemies(self):

        # Получаем список всех врагов в группе
        for enemy in self.player.enemies_group:
            if enemy != self and not isinstance(enemy, Boss) and not isinstance(self, Boss) and self.hitbox.colliderect(
                    enemy.hitbox):  # Проверяем столкновение с другим врагом
                self.resolve_collision(enemy)

    def resolve_collision(self, other_enemy):
        # Вычисляем вектор отталкивания
        dx = self.hitbox.centerx - other_enemy.hitbox.centerx
        dy = self.hitbox.centery - other_enemy.hitbox.centery
        distance = math.hypot(dx, dy)

        if distance == 0:
            return  # Избегаем деления на ноль

        # Нормализуем вектор
        dx /= distance
        dy /= distance

        # Отталкиваем врагов друг от друга
        overlap = (self.hitbox.width + other_enemy.hitbox.width) / 2 - distance
        if overlap > 0:
            self.hitbox.x += dx * overlap / 2
            self.hitbox.y += dy * overlap / 2
            other_enemy.hitbox.x -= dx * overlap / 2
            other_enemy.hitbox.y -= dy * overlap / 2

            # Обновляем позицию спрайта
            self.rect.center = self.hitbox.center
            other_enemy.rect.center = other_enemy.hitbox.center

    def main(self):
        # Проверка расстояния до игрока
        distance_to_player = self.rect.centerx - self.player.rect.centerx, self.rect.centery - self.player.rect.centery
        distance = math.hypot(*distance_to_player)
        # Если игрок находится в области видимости (например, 100 пикселей)
        if distance < self.distance:
            self.chasing = True
        else:
            self.chasing = False

        # Если враг преследует игрока
        if self.chasing:
            direction = pygame.math.Vector2(self.player.rect.center) - pygame.math.Vector2(self.rect.center)
            if direction.magnitude() != 0:
                direction = direction.normalize()
                self.hitbox.x += direction.x * self.speed
                self.hitbox.y += direction.y * self.speed
                self.rect.center = self.hitbox.center  # Обновляем позицию спрайта

                # Определяем направление движения
                if direction.x > 0:
                    self.direction_word = "right"
                elif direction.x < 0:
                    self.direction_word = "left"

                # Поворачиваем спрайт в зависимости от направления
                if self.direction_word == "left":
                    self.image = pygame.transform.flip(self.orig_images, True, False)  # Отражаем по горизонтали
                else:
                    self.image = self.orig_images  # Оригинальный спрайт

            # Проверка на столкновение с игроком
            if self.rect.colliderect(self.player.hitbox):
                self.player.take_damage(self.damage)  # Уменьшаем здоровье игрока на 10 при столкновении

        # Проверка коллизий с другими врагами
        self.check_collision_with_enemies()

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()
        else:
            self.create_hit_particles()  # Создаём частицы при получении урона

    def draw_health_text(self, screen, offset):
        # Создаём шрифт для отображения текста
        font = pygame.font.Font(None, 24)  # Шрифт и размер текста
        health_text = f"HP: {self.health}/{self.max_health}"  # Текст с текущим здоровьем
        text_surface = font.render(health_text, True, (255, 255, 255))  # Белый цвет текста

        # Позиция текста (над головой врага)
        text_x = self.rect.centerx - offset.x - text_surface.get_width() // 2  # Центрируем текст
        text_y = self.rect.y - offset.y - 20  # Над спрайтом

        # Рисуем текст на экране
        screen.blit(text_surface, (text_x, text_y))

    def create_hit_particles(self):
        # Создаём 10 частиц при ударе
        for _ in range(10):
            particle = HitParticle(self.rect.center, image=pygame.image.load("sprites/kost.png").convert_alpha())
            self.hit_particles.append(particle)

    def update_particles(self, screen, offset):
        # Обновляем и отрисовываем частицы
        for particle in self.hit_particles[:]:  # Используем копию списка для безопасного удаления
            particle.update()
            particle.draw(screen, offset)
            if particle.lifetime <= 0 or particle.size <= 0:
                self.hit_particles.remove(particle)  # Удаляем "мёртвые" частицы

    def die(self, give=True):
        if give:
            self.player.exp += self.give_exp
        print(self.player.exp)
        self.death_sound.play()
        self.kill()

    def update(self):
        self.main()


# Класс Skelet
class Skelet(Enemy):
    def __init__(self, pos, groups, player):
        global frames
        # Загружаем спрайты для скелета
        orig_images = frames[13]
        orig_images = pygame.transform.scale(orig_images, (32, 32))

        # Вызываем конструктор базового класса
        super().__init__(
            pos=pos,
            groups=groups,
            player=player,
            image=orig_images,  # Спрайт скелета
            health=100,  # Здоровье скелета
            damage=50,  # Урон скелета
            speed=4,  # Скорость скелета
            exp=100,  # Сколько опыта дается за склета
            distance=300
        )


class LostSoul(Enemy):
    def __init__(self, pos, groups, player):
        global frames
        orig_images = frames[8]
        orig_images = pygame.transform.scale(orig_images, (32, 32))

        # Вызываем конструктор базового класса
        super().__init__(
            pos=pos,
            groups=groups,
            player=player,
            image=orig_images,
            health=100,
            damage=50,
            speed=3,
            exp=200,
            distance=100000
        )
        self.boss = None

    def create_hit_particles(self):
        # Создаём 10 частиц при ударе
        for _ in range(10):
            particle = CytoplasmParticle(self.rect.center)
            self.hit_particles.append(particle)

    def die(self):
        if self.boss:
            self.boss.minions_count -= 1
        super().die()


# Класс босса
class Boss(Enemy):
    def __init__(self, pos, groups, player):
        orig_images = frames[9]
        boss_image = pygame.transform.scale(orig_images, (32, 32))
        boss_image = pygame.transform.scale(boss_image, (64, 64))  # Босс больше обычных врагов
        # Вызываем конструктор базового класса
        super().__init__(
            pos=pos,
            groups=groups,
            player=player,
            image=boss_image,
            health=500,  # Больше здоровья
            damage=50,  # Больше урона
            speed=2,  # Меньше скорости (босс медленный, но мощный)
            exp=100,
            distance=10000
        )

        # Уникальные атрибуты босса
        self.last_ability_time = 0  # Время последней способности
        self.ability_cooldown = 5000  # Задержка между способностями (в миллисекундах)
        self.minions_count = 0
        self.max_minions = 2

    def update(self):
        super().update()  # Вызываем обновление из базового класса
        self.use_abilities()  # Используем уникальные способности босса

    def create_hit_particles(self):
        # Создаём 10 частиц при ударе
        for _ in range(10):
            particle = BloodParticle(self.rect.center)
            self.hit_particles.append(particle)

    def use_abilities(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_ability_time > self.ability_cooldown:
            self.last_ability_time = current_time
            self.spawn_minions()  # Босс вызывает миньонов

    def spawn_minions(self):
        if self.minions_count < self.max_minions:
            # Создаём несколько миньонов вокруг босса
            for _ in range(3):
                if self.minions_count >= self.max_minions:
                    break
                minion_pos = (self.rect.centerx + random.randint(-50, 50),
                              self.rect.centery + random.randint(-50, 50))
                minion = LostSoul(minion_pos, self.groups(), self.player)  # Создаём миньона
                self.minions_count += 1
                minion.boss = self

    def die(self):
        # Убиваем всех мобов в группе
        for enemy in self.groups()[0]:  # Предполагаем, что группа врагов — это первая группа
            if enemy != self:  # Не убиваем самого босса
                try:
                    enemy.die(False)  # Вызываем метод die у каждого моба
                except:
                    pass
                # Создаем портал после смерти босса
        self.player.pos_teleport = self.rect.center
        self.player.boss_defeating = True
        # Вызываем метод die из базового класса
        super().die()


class Portal(pygame.sprite.Sprite):
    def __init__(self, group, player):
        super().__init__(group)
        self.player = player

        # Загрузка текстуры портала
        self.image = pygame.image.load("image/portal.png").convert_alpha()  # Укажите путь к изображению
        self.image = pygame.transform.scale(self.image, (50, 50))  # Масштабируем под нужный размер

        # Прямоугольник для позиционирования
        self.rect = self.image.get_rect()

    def teleport(self):
        if self.rect.colliderect(self.player.hitbox):
            self.player.win = True

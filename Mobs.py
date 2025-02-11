import pygame
import math
from particl import HitParticle

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
    def __init__(self, pos, groups, player, image, health, damage, speed, exp):
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

    def main(self):
        # Проверка расстояния до игрока
        distance_to_player = self.rect.centerx - self.player.rect.centerx, self.rect.centery - self.player.rect.centery
        distance = math.hypot(*distance_to_player)
        # Если игрок находится в области видимости (например, 100 пикселей)
        if distance < 300:
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

    def die(self):
        self.player.exp += self.give_exp
        print(self.player.exp)
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
            exp=1000000  # Сколько опыта дается за склета
        )

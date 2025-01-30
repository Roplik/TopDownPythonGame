import pygame
import math

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


# Класс моба
class Skelet(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.image = pygame.Surface((32, 32))  # Создаем поверхность для спрайта
        self.image.fill((255, 0, 0))  # Заполняем поверхность красным цветом
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)  # Уменьшаем hitbox для столкновений
        self.speed = 2  # Скорость движения врага
        self.player = player  # Ссылка на игрока
        self.chasing = False  # Флаг для отслеживания состояния погони
        self.damage = 50

    def update(self):
        # Проверка расстояния до игрока
        distance_to_player = self.rect.centerx - self.player.rect.centerx, self.rect.centery - self.player.rect.centery
        distance = math.hypot(*distance_to_player)

        # Если игрок находится в области видимости (например, 100 пикселей)
        if distance < 500:
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

            # Проверка на столкновение с игроком
            if self.rect.colliderect(self.player.hitbox):
                self.player.take_damage(self.damage)  # Уменьшаем здоровье игрока на 10 при столкновении

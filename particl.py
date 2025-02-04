import random
import pygame


class HitParticle:
    def __init__(self, pos, image):
        self.pos = pygame.math.Vector2(pos)  # Позиция частицы
        self.velocity = pygame.math.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))  # Случайная скорость
        self.lifetime = random.randint(20, 40)  # Время жизни частицы
        self.size = random.randint(15, 20)  # Размер частицы
        self.color = (255, random.randint(100, 200), 0)  # Цвет (оранжевый/жёлтый)
        self.image = pygame.transform.scale(image, (self.size, self.size))  # Изображение частицы
        self.angle = random.uniform(0, 360)  # Случайный угол вращения

    def update(self):
        self.pos += self.velocity  # Двигаем частицу
        self.lifetime -= 1  # Уменьшаем время жизни
        self.size -= 0.1  # Уменьшаем размер
        if self.size < 0:
            self.size = 0

        # Обновляем размер изображения в зависимости от текущего размера
        self.image = pygame.transform.scale(self.image, (int(self.size), int(self.size)))
        # Обновляем угол вращения (можно добавить небольшое изменение)
        self.angle += random.uniform(-1, 1)  # Случайное изменение угла

    def draw(self, screen, offset):
        # Отрисовываем частицу с учётом смещения камеры
        pos = self.pos - offset
        if self.lifetime > 0 and self.size > 0:
            rotated_image = pygame.transform.rotate(self.image, self.angle)  # Поворачиваем изображение
            rect = rotated_image.get_rect(
                center=(int(pos.x), int(pos.y)))  # Получаем прямоугольник для позиционирования
            screen.blit(rotated_image, rect.topleft)  # Отрисовываем повернутое изображение


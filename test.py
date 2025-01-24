'''import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


# Класс для анимации персонажа
class AnimatedSprite:
    def __init__(self, sprite_sheet, frame_width, frame_height, scale_factor=1):
        self.sprite_sheet = sprite_sheet
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frames = self.load_frames(scale_factor)
        self.current_frame = 0
        self.animation_speed = 10  # Скорость анимации (кадры в секунду)
        self.last_update = pygame.time.get_ticks()

    def load_frames(self, scale_factor):
        frames = []
        sheet_width, sheet_height = self.sprite_sheet.get_size()
        for y in range(sheet_height // self.frame_height):
            for x in range(sheet_width // self.frame_width):
                rect = (x * self.frame_width, y * self.frame_height,
                        self.frame_width, self.frame_height)
                frame = self.sprite_sheet.subsurface(rect)
                # Масштабируем кадр
                if scale_factor != 1:
                    frame = pygame.transform.scale(frame,
                                                   (int(self.frame_width * scale_factor),
                                                    int(self.frame_height * scale_factor)))
                frames.append(frame)
        return frames

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > (1000 / self.animation_speed):
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

    def draw(self, surface, x, y):
        # Рисуем сам спрайт
        surface.blit(self.frames[self.current_frame], (x, y))

        # Определяем хитбокс
        hitbox_rect = pygame.Rect(x, y, self.frame_width * scale_factor, self.frame_height * scale_factor)

        # Рисуем обводку хитбокса
        pygame.draw.rect(surface, (255, 0, 0), hitbox_rect, 2)  # Красная обводка с толщиной 2 пикселя


# Загрузка спрайт-листа
sprite_sheet_image = pygame.image.load('Char_Sprites/char_idle_down_anim_strip_6.png').convert_alpha()
frame_width = 16  # Ширина одного кадра
frame_height = 16  # Высота одного кадра
scale_factor = 10  # Коэффициент масштабирования (например, 2 для удвоения размера)

# Создание экземпляра AnimatedSprite
animated_sprite = AnimatedSprite(sprite_sheet_image, frame_width, frame_height, scale_factor)

# Игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Обновление анимации
    animated_sprite.update()

    # Отрисовка
    screen.fill((255, 255, 255))  # Очистка экрана
    animated_sprite.draw(screen, 100, 100)  # Рисуем спрайт на позиции (100, 100)

    pygame.display.flip()  # Обновляем экран
'''
'''
import pygame
import pytmx

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    screen.fill((0, 0, 0))

    # Загрузка карты
    tmx_data = pytmx.load_pygame('maps/main.tmx')  # файл карты
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))



    # Обновление дисплея
    pygame.display.flip()


pygame.quit()'''
'''import pygame
import sys

# Инициализация Pygame
pygame.init()

# Параметры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Animation Preview")


# Загрузка изображений и подготовка спрайтов
class Character:
    def __init__(self):
        self.up = pygame.image.load("Char_Sprites/char_run_up_anim_strip_6.png").convert_alpha()
        self.down = pygame.image.load("Char_Sprites/char_run_down_anim_strip_6.png").convert_alpha()
        self.left = pygame.image.load("Char_Sprites/char_run_left_anim_strip_6.png").convert_alpha()
        self.right = pygame.image.load("Char_Sprites/char_run_right_anim_strip_6.png").convert_alpha()

        self.sprite_width = 16  # Укажите ширину спрайта
        self.sprite_height = 16  # Укажите высоту спрайта

        self.sprites = {
            'up': [self.get_sprite(self.up, i) for i in range(6)],
            'down': [self.get_sprite(self.down, i) for i in range(6)],
            'left': [self.get_sprite(self.left, i) for i in range(6)],
            'right': [self.get_sprite(self.right, i) for i in range(6)],
        }

        self.current_frame = 0
        self.frame_rate = 5
        self.frame_counter = 0
        self.direction_anim = 'left'  # Измените на 'down', 'left' или 'right', чтобы просмотреть другие анимации

    def get_sprite(self, image, index):
        return image.subsurface(index * self.sprite_width, 0, self.sprite_width, self.sprite_height)

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.sprites[self.direction_anim])
            self.frame_counter = 0

    def draw(self, surface):
        sprite = self.sprites[self.direction_anim][self.current_frame]
        surface.blit(sprite, (screen_width // 2 - self.sprite_width // 2, screen_height // 2 - self.sprite_height // 2))


# Основной игровой цикл
character = Character()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Обновление состояния персонажа
    character.update()

    # Отрисовка
    screen.fill((255, 255, 255))  # Очистка экрана белым цветом
    character.draw(screen)

    pygame.display.flip()  # Обновление экрана
    pygame.time.delay(100)  # Задержка для управления скоростью анимации'''
'''import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Таймер в Pygame")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Шрифт для отображения времени
font = pygame.font.Font(None, 74)

# Переменные для таймера
start_ticks = pygame.time.get_ticks()  # Начальное время

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Вычисление прошедшего времени
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # Время в секундах

    # Отображение таймера
    screen.fill(WHITE)  # Очистка экрана
    timer_text = font.render(str(int(seconds)), True, BLACK)  # Преобразование времени в текст
    screen.blit(timer_text, (screen_width // 2, screen_height // 2))  # Отображение текста

    pygame.display.flip()  # Обновление экрана
    pygame.time.Clock().tick(60)  # Ограничение FPS до 60'''

import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Секундомер")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Шрифт
font = pygame.font.Font(None, 74)

# Переменные для секундомера
start_ticks = pygame.time.get_ticks()  # Начальное время
running = False

# Основной цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Нажмите пробел для старта/остановки
                running = not running
                if running:
                    start_ticks = pygame.time.get_ticks()  # Сброс времени

    screen.fill(WHITE)

    if running:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # Прошедшее время в секундах
    else:
        elapsed_time = 0

    # Форматирование времени до сотых
    timer_text = f"{elapsed_time:.2f}"  # Форматируем до двух знаков после запятой

    # Создание текста с черной обводкой
    timer_surface = font.render(timer_text, True, BLACK)
    outline_surface = font.render(timer_text, True, WHITE)

    # Рисуем обводку (сначала черный текст, затем белый)
    screen.blit(timer_surface, (width // 2 - timer_surface.get_width() // 2 - 2, 10))  # Черная обводка
    screen.blit(outline_surface, (width // 2.05- outline_surface.get_width() // 2, 10))  # Белый текст

    pygame.display.flip()
    pygame.time.delay(100)  # Задержка для уменьшения нагрузки на процессор

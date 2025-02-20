import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Таймер в Pygame")

# Настройки шрифта
font = pygame.font.Font(None, 36)

# Переменные для таймера
start_ticks = None  # Время старта таймера (изначально None)
running = False  # Флаг, указывающий, идет ли таймер


class Timer:
    def __init__(self, start_ticks):
        self.start_ticks = start_ticks
        self.second = 0

    def draw(self, running):
        if running:
            seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000  # Переводим в секунды
        else:
            seconds = self.second
        self.second = seconds
        timer_text = font.render(f"Время: {seconds:.2f} секунд", True, (255, 255, 255))

        # Отрисовка обводки текста
        outline_text = font.render(f"Время: {seconds:.2f} секунд", True, (0, 0, 0))  # Черный цвет для обводки

        # Получаем прямоугольники текста
        text_rect = timer_text.get_rect(
            center=(screen.get_width() // 2, 30))  # Центрируем по ширине, но устанавливаем высоту на 30 пикселей
        outline_rect = outline_text.get_rect(center=(screen.get_width() // 2, 30))

        # Сначала рисуем обводку
        screen.blit(outline_text, outline_rect)
        # Затем основной текст
        screen.blit(timer_text, text_rect)


def draw_text(surface, text, pos, font_size=24, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)  # Шрифт и размер текста
    text_surface = font.render(text, True, color)  # Создаём поверхность с текстом
    surface.blit(text_surface, pos)  # Отрисовываем текст на экране


def player_stats(screen, player):
    # Позиция текста (левый нижний угол)
    pos_x = 20  # Отступ слева
    pos_y = screen.get_height() - 150  # Отступ снизу

    # Отображаем характеристики
    draw_text(screen, f"Health: {player.current_health}/{player.max_health}", (pos_x, pos_y))
    draw_text(screen, f"Level: {player.level}", (pos_x, pos_y + 30))
    draw_text(screen, f"Exp: {player.exp}/{player.exp_to_next_level}", (pos_x, pos_y + 60))
    draw_text(screen, f"Damage: {player.damage}", (pos_x, pos_y + 90))
    draw_text(screen, f"Speed: {round(player.speed, 3)}", (pos_x, pos_y + 120))

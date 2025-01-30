import pygame
from PIL import Image
import sys
import settings


class DeadScreen:
    def __init__(self):

        pygame.init()

        self.settings = settings.Settings()
        self.settings.load_settings()

        # Установка размеров окна
        self.screen_width = self.settings.screen_width  # Увеличили ширину
        self.screen_height = self.settings.screen_height  # Увеличили высоту
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("YOU ARE DEAD")
        # Размеры для уменьшенной гифки
        self.gif_scale_size = (300, 300)  # Укажите желаемые размеры (ширина, высота)

        # Загрузка кадров гифки
        self.gif_frames = self.load_gif("image/ultrakill-death.gif", self.gif_scale_size)
        self.current_frame = 0
        self.frame_count = len(self.gif_frames)

        # Загрузка звука
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound("music/ultrakill-ha-computer-laughing.mp3")
        self.sound.set_volume(self.settings.volume)

        # Основной цикл
        self.clock = pygame.time.Clock()
        self.last_sound_time = pygame.time.get_ticks()  # Время последнего воспроизведения звука

        # Шрифты
        self.font = pygame.font.Font(None, 74)  # Шрифт для надписи "Вы мертвы"
        self.restart_font = pygame.font.Font(None, 48)  # Шрифт для надписи "Нажмите [R]"

        # Загрузка гифки и создание списка кадров

    def load_gif(self, filename, scale_size):
        img = Image.open(filename)
        frames = []
        try:
            while True:
                frame = img.copy()
                frame = frame.convert("RGBA")
                frame_data = pygame.image.fromstring(frame.tobytes(), frame.size, "RGBA")
                # Изменение размера кадра
                frame_data = pygame.transform.scale(frame_data, scale_size)
                frames.append(frame_data)
                img.seek(len(frames))  # Переход к следующему кадру
        except EOFError:
            pass  # Конец гифки
        return frames

    def run_dead_screen(self):
        # Очистка экрана (черный фон)
        self.screen.fill((0, 0, 0))

        # Отображение текущего кадра по центру экрана
        if self.frame_count > 0:
            frame_rect = self.gif_frames[self.current_frame].get_rect(
                center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(self.gif_frames[self.current_frame], frame_rect)

            # Переход к следующему кадру
            self.current_frame = (self.current_frame + 1) % self.frame_count

        # Проверка времени для воспроизведения звука
        current_time = pygame.time.get_ticks()
        if current_time - self.last_sound_time >= 1000:  # Каждую секунду
            self.sound.play()
            self.last_sound_time = current_time

        # Отображение текста "Вы мертвы" сверху
        dead_text = self.font.render("Вы мертвы", True, (255, 0, 0))  # Красный цвет
        self.screen.blit(dead_text, (self.screen_width // 2 - dead_text.get_width() // 2, 50))

        # Отображение текста "Нажмите [R] чтобы начать уровень сначала" снизу
        restart_text = self.restart_font.render("Нажмите [R] чтобы начать уровень сначала", True,
                                                (255, 255, 255))  # Белый цвет
        self.screen.blit(restart_text,
                         (self.screen_width // 2 - restart_text.get_width() // 2, self.screen_height - 100))

        # Обновление экрана
        pygame.display.flip()

        # Установка FPS (количество кадров в секунду)
        self.clock.tick(14.3)  # Можно изменить значение для регулировки скорости анимации

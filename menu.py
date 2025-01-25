import pygame
import sys

import MenuSetting
from gamescript import *
import settings
from MenuSetting import *

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 735, 413
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# Загрузка изображения фона
background_image = pygame.image.load("image/background.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Шрифты
font = pygame.font.Font(None, 50)

# Сцена
current_index_scene = 0


# Меню
class Menu:
    def __init__(self):

        os.environ['SDL_VIDEO_CENTERED'] = '1'

        self.options = ["Играть", "Настройки", "Выйти"]
        self.current_option_index = 0
        self.setting = settings.Settings()
        self.setting.load_settings()
        pygame.mixer.music.set_volume(self.setting.volume)

    def reload_settings(self):
        self.setting.load_settings()
        pygame.mixer.music.set_volume(self.setting.volume)

    def draw(self):
        # Отрисовка кнопок меню
        for index, option in enumerate(self.options):
            if index == self.current_option_index:
                text_surface = font.render(option, True, (128, 128, 128))
            else:
                text_surface = font.render(option, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + index * 60))
            screen.blit(text_surface, text_rect)

    def move_up(self):
        if self.current_option_index > 0:
            self.current_option_index -= 1

    def move_down(self):
        if self.current_option_index < len(self.options) - 1:
            self.current_option_index += 1

    def select(self):
        global current_index_scene
        if self.current_option_index == 0:
            pygame.mixer.music.stop()
            current_index_scene = 1
            # Здесь можно добавить код для начала игры
        elif self.current_option_index == 1:
            pygame.mixer.music.stop()
            current_index_scene = 2
            # Здесь можно добавить код для настроек
        elif self.current_option_index == 2:
            pygame.quit()
            sys.exit()

    def update_selection(self, mouse_pos):
        for index in range(len(self.options)):
            text_surface = font.render(self.options[index], True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + index * 60))
            if text_rect.collidepoint(mouse_pos):
                self.current_option_index = index
                return True

    def select_with_mouse(self, mouse_pos):
        global current_index_scene
        last_index = current_index_scene
        if self.update_selection(mouse_pos):
            menu.select()
            if last_index != current_index_scene:
                return True


menu = Menu()


def scene_menu():
    menu.reload_settings()
    # Загрузка музыки
    pygame.mixer.music.load("music/Miura Jam - Tell Me Why (Berserk).mp3")
    pygame.mixer.music.play(-1)

    # Настройка главного меню
    pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")

    running = True
    global current_index_scene
    # Основной игровой цикл
    while running:
        # Обновление выбора на основе позиции мыши
        mouse_pos = pygame.mouse.get_pos()
        menu.update_selection(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                running = False
                current_index_scene = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu.move_up()
                elif event.key == pygame.K_DOWN:
                    menu.move_down()
                elif event.key == pygame.K_RETURN:
                    menu.select()
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if menu.select_with_mouse(mouse_pos):
                        running = False

        # Отрисовка
        screen.blit(background_image, (0, 0))
        menu.draw()
        pygame.display.flip()


def setting_window():
    setting_menu = MenuSetting.SettingMenu()
    events = pygame.event.get()
    while setting_menu.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                setting_menu.running = False
                sys.exit()

        setting_menu.win.fill((255, 255, 255))  # Очистка экрана
        setting_menu.win.blit(setting_menu.background_image, (0, 0))  # Отрисовка фона
        setting_menu.slider.draw()  # Отрисовка слайдера
        setting_menu.dropdown.draw()  # Отрисовка выпадающего списка
        setting_menu.volume_text.draw()  # Отрисовка текста громкости
        setting_menu.dropdown_text.draw()  # Отрисовка текста выбора разрешения
        setting_menu.save.draw()  # Отрисовка кнопки сохранения
        setting_menu.back.draw()  # Отрисовка кнопки "Назад"
        setting_menu.output_music_volume.draw()  # Отрисовка громкости звука
        pygame.mixer.music.set_volume(setting_menu.change_music_volume() / 100)
        pygame.display.update()
        pygame_widgets.update(events)

    global current_index_scene
    current_index_scene = 0


def run_game():
    global current_index_scene
    game_run = True
    # Основной цикл игры
    while game_run:
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_run = False
        if game_run:
            game.level.run()
            pygame.display.flip()  # Обновление экрана
            # self.draw_colliders()

    current_index_scene = 0


# Смена сцен
while current_index_scene is not None:
    if current_index_scene == 0:
        scene_menu()
    elif current_index_scene == 1:
        game = Game()
        run_game()
    elif current_index_scene == 2:
        setting_window()

sys.exit()

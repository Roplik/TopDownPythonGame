import pygame_widgets
import pygame
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
import settings


class SettingMenu:
    def __init__(self):
        self.setting = settings.Settings()
        self.setting.load_settings()

        # Загрузка изображения фона
        self.background_image = pygame.image.load("image/setting.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (1000, 600))

        pygame.init()
        self.win = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Настройки")

        self.volume_text = TextBox(self.win, 50, 100, 130, 50, fontSize=30)
        self.volume_text.setText("Volume:")

        self.slider = Slider(self.win, 210, 100, 400, 40, min=0, max=100, step=1, handleColour=(105, 105, 105))
        self.slider.setValue(int(self.setting.volume * 100))
        self.output = TextBox(self.win, 650, 100, 60, 50, fontSize=30)
        self.dropdown_text = TextBox(self.win, 50, 200, 250, 50, fontSize=30)
        self.dropdown_text.setText("Select resolution:")

        self.dropdown = Dropdown(
            self.win, 310, 200, 120, 50,
            name=f'{self.setting.screen_width} x {self.setting.screen_height}',
            choices=['1920 x 1080', '1200 x 800'],
            borderRadius=3,
            colour=pygame.Color('grey'),
            values=[(1920, 1080), (1200, 800)],
            direction='down',
            textHAlign='left'
        )

        self.save = Button(
            self.win,
            295,
            450,
            200,
            100,
            text='Save',
            fontSize=30,
            margin=20,
            inactiveColour=pygame.Color("grey"),
            hoverColour=(105, 105, 105),
            pressedColour=(64, 64, 64),
            radius=20,
            onClick=lambda: self.write_config()
        )

        self.back = Button(
            self.win,
            505,
            450,
            200,
            100,
            text='Back',
            fontSize=30,
            margin=20,
            inactiveColour=pygame.Color("grey"),
            hoverColour=(105, 105, 105),
            pressedColour=(64, 64, 64),
            radius=20,
            onClick=lambda: self.back_to_menu()
        )

        # Отключаем текстовые поля
        self.dropdown_text.disable()
        self.volume_text.disable()
        self.output.disable()

    def write_config(self):
        if self.dropdown.getSelected():
            screen_width, screen_height = self.dropdown.getSelected()
        else:
            screen_width, screen_height = (self.setting.screen_width, self.setting.screen_height)

        with open('cfg.txt', 'w') as config_file:
            config_file.write(f'screen_width={screen_width}\n')
            config_file.write(f'screen_height={screen_height}\n')
            config_file.write(f'volume={self.slider.getValue()}\n')

    def draw(self):
        # Отрисовка фона
        self.win.blit(self.background_image, (0, 0))

        # Отрисовка всех элементов интерфейса
        self.volume_text.draw()
        self.slider.draw()
        self.output.draw()
        self.dropdown_text.draw()
        self.dropdown.draw()
        self.save.draw()
        self.back.draw()

        # Обновление экрана
        pygame.display.flip()

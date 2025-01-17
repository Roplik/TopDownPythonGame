class Settings:
    def __init__(self):
        self.screen_width = 1920  # 1200
        self.screen_height = 1080  # 800
        self.bg_color = (230, 230, 230)  # Светло-серый фон
        self.tilesize = 32
        self.volume = 1

    def load_settings(self):
        with open('cfg.txt', 'r') as f:
            for line in f:
                key, value = line.strip().split('=')
                if key == 'screen_width':
                    self.screen_width = int(value)
                elif key == 'screen_height':
                    self.screen_height = int(value)
                elif key == "volume":
                    self.volume = int(value) / 100

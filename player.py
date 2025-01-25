import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("Char_Sprites/char_idle_up_anim.gif").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5

        self.sprite_width = 32  # ширина одного спрайта
        self.sprite_height = 32  # высота одного спрайта
        self.sprites_per_row = 4  # количество спрайтов в строке

        # Загружаем и масштабируем спрайты
        self.up_run = pygame.transform.scale(
            pygame.image.load("Char_Sprites/char_run_up_anim_strip_6.png").convert_alpha(),
            (self.sprite_width * 6, self.sprite_height))
        self.down_run = pygame.transform.scale(
            pygame.image.load("Char_Sprites/char_run_down_anim_strip_6.png").convert_alpha(),
            (self.sprite_width * 6, self.sprite_height))
        self.left_run = pygame.transform.scale(
            pygame.image.load("Char_Sprites/char_run_left_anim_strip_6.png").convert_alpha(),
            (self.sprite_width * 6, self.sprite_height))
        self.right_run = pygame.transform.scale(
            pygame.image.load("Char_Sprites/char_run_right_anim_strip_6.png").convert_alpha(),
            (self.sprite_width * 6, self.sprite_height))

        self.up_idle = pygame.transform.scale(
            pygame.image.load("Char_Sprites/char_idle_up_anim_strip_6.png").convert_alpha(),
            (self.sprite_width * 6, self.sprite_height))
        self.down_idle = pygame.transform.scale(
            pygame.image.load("Char_Sprites/char_idle_down_anim_strip_6.png").convert_alpha(),
            (self.sprite_width * 6, self.sprite_height))
        self.left_idle = pygame.transform.scale(
            pygame.image.load("Char_Sprites/char_idle_left_anim_strip_6.png").convert_alpha(),
            (self.sprite_width * 6, self.sprite_height))
        self.right_idle = pygame.transform.scale(
            pygame.image.load("Char_Sprites/char_idle_right_anim_strip_6.png").convert_alpha(),
            (self.sprite_width * 6, self.sprite_height))

        self.direction_anim = "up"

        self.current_frame = 0
        self.frame_rate = 5  # скорость смены кадров
        self.frame_counter = 0

        self.obstacles_sprites = obstacles_sprites
        self.sprites_run = {
            'up': [self.get_sprite(self.up_run, i) for i in range(6)],
            'down': [self.get_sprite(self.down_run, i) for i in range(6)],
            'left': [self.get_sprite(self.left_run, i) for i in range(6)],
            'right': [self.get_sprite(self.right_run, i) for i in range(6)]
        }
        self.sprites_idle = {
            'up': [self.get_sprite(self.up_idle, i) for i in range(6)],
            'down': [self.get_sprite(self.down_idle, i) for i in range(6)],
            'left': [self.get_sprite(self.left_idle, i) for i in range(6)],
            'right': [self.get_sprite(self.right_idle, i) for i in range(6)]
        }

    def get_sprite(self, image, index):
        return image.subsurface(index * self.sprite_width, 0, self.sprite_width, self.sprite_height)

    def animate(self):
        if self.direction.magnitude() != 0:
            self.frame_counter += 1
            if self.frame_counter >= self.frame_rate:
                self.current_frame += 1
                self.frame_counter = 0
                if self.current_frame >= len(self.sprites_run[self.direction_anim]):
                    self.current_frame = 0
            # Получаем изображение из списка спрайтов
            self.image = self.sprites_run[self.direction_anim][self.current_frame]
        else:
            self.frame_counter += 1
            if self.frame_counter >= self.frame_rate:
                self.current_frame += 1
                self.frame_counter = 0
                if self.current_frame >= len(self.sprites_idle[self.direction_anim]):
                    self.current_frame = 0
            # Получаем изображение из списка спрайтов
            self.image = self.sprites_idle[self.direction_anim][self.current_frame]

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * self.speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0
        if keys[pygame.K_LSHIFT]:
            self.speed = 8
        else:
            self.speed = 5
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
            self.direction_anim = "up"
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.direction_anim = "down"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.direction_anim = "right"
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.direction_anim = "left"
        # Проверка на одновременное нажатие противоположных клавиш
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and (keys[pygame.K_s] or keys[pygame.K_DOWN]):
            self.direction.y = 0  # Остановка по оси Y
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.direction.x = 0  # Остановка по оси X

    def collision(self, direction):
        # Проверка на столкновения с препятствиями
        if direction == "horizontal":
            for obstacle in self.obstacles_sprites:
                if self.hitbox.colliderect(obstacle.rect):
                    # Если движение вправо
                    if self.direction.x > 0:
                        self.hitbox.right = obstacle.rect.left
                    # Если движение влево
                    if self.direction.x < 0:
                        self.hitbox.left = obstacle.rect.right

        if direction == "vertical":
            for obstacle in self.obstacles_sprites:
                if self.hitbox.colliderect(obstacle.rect):
                    # Если движение вниз
                    if self.direction.y > 0:
                        self.hitbox.bottom = obstacle.rect.top
                    # Если движение вверх
                    if self.direction.y < 0:
                        self.hitbox.top = obstacle.rect.bottom

    def draw_collider(self, surface):
        # Отрисовка коллайдера игрока
        collider_color = (255, 0, 0)  # Красный цвет для коллайдера
        pygame.draw.rect(surface, collider_color, self.rect, 2)  # Рисует прямоугольник вокруг коллайдера

    def update(self):
        self.input()
        self.move()
        self.animate()

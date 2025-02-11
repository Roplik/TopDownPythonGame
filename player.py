import pygame
import math


def draw_text(surface, text, pos, font_size=24, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)  # Шрифт и размер текста
    text_surface = font.render(text, True, color)  # Создаём поверхность с текстом
    surface.blit(text_surface, pos)  # Отрисовываем текст на экране


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles_sprites, enemy_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("Char_Sprites/char_idle_up_anim.gif").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.walk_speed = 5
        self.run_speed = 8
        self.damage = 50

        self.sprite_width = 32  # ширина одного спрайта
        self.sprite_height = 32  # высота одного спрайта
        self.sprites_per_row = 4  # количество спрайтов в строке

        # Инициализация жизней и здоровья
        self.max_health = 100
        self.current_health = self.max_health
        self.die = False

        # Задержка перед получением следующего урона
        self.invincible_duration = 2000  # 2000 мс (2 секунды)
        self.last_damage_time = 0
        self.invincible = False

        self.enemies_group = enemy_sprites

        # Таймер для атаки
        self.attack_cooldown = 1000  # Интервал между атаками (в миллисекундах)
        self.last_attack_time = 0  # Время последней атаки
        self.attack_radius = 100

        self.exp = 0
        self.level = 1
        self.exp_to_next_level = 100
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

    def gain_exp(self):
        # Проверяем, сколько уровней игрок может поднять
        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level  # Уменьшаем опыт на необходимое количество
            self.level_up()  # Поднимаем уровень

    def level_up(self):
        self.level += 1
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)  # Увеличиваем требуемый опыт для следующего уровня
        self.show_level_up_menu()  # Показываем меню выбора улучшений

    def show_level_up_menu(self):
        screen = pygame.display.get_surface()
        # Создаём поверхность для меню
        menu_surface = pygame.Surface((300, 200))
        menu_surface.fill((50, 50, 50))
        font = pygame.font.Font(None, 36)

        # Текст улучшений
        text1 = font.render("1. Increase Health", True, (255, 255, 255))
        text2 = font.render("2. Increase Speed", True, (255, 255, 255))
        text3 = font.render("3. Increase Damage", True, (255, 255, 255))
        text4 = font.render("4.Increase Attak speed", True, (255, 255, 255))

        # Отрисовка текста
        menu_surface.blit(text1, (20, 20))
        menu_surface.blit(text2, (20, 70))
        menu_surface.blit(text3, (20, 120))
        menu_surface.blit(text4, (20, 170))

        # Отображение меню на экране
        screen.blit(menu_surface, (250, 200))
        pygame.display.flip()

        # Ожидание выбора игрока
        choice = None
        while choice is None:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        choice = "1"
                    elif event.key == pygame.K_2:
                        choice = "2"
                    elif event.key == pygame.K_3:
                        choice = "3"
                    elif event.key == pygame.K_4:
                        choice = "4"

        self.apply_upgrade(choice)

    def apply_upgrade(self, choice):
        if choice == "1":
            self.max_health += 5
            self.current_health = self.max_health
            print(self.max_health)
            print("Health increased!")
        elif choice == "2":
            self.walk_speed += 0.2
            self.run_speed += 0.2
            print(self.walk_speed)
            print("Speed increased!")
        elif choice == "3":
            self.damage += 5
            print(self.damage)
            print("Damage increased!")
        elif choice == "4":
            self.attack_cooldown -= 5
            print(self.attack_cooldown)
            print("Attak speed increased!")
        else:
            print("Invalid choice. No upgrade applied.")

    def take_damage(self, amount):
        if not self.invincible:  # Проверяем, не находится ли игрок в неуязвимости
            self.current_health -= amount
            self.last_damage_time = pygame.time.get_ticks()  # Обновляем время последнего урона
            self.invincible = True
            if self.current_health <= 0:
                self.die = True

    def invincible_switch(self):
        if self.invincible:
            # Проверяем, истекло ли время неуязвимости
            if pygame.time.get_ticks() - self.last_damage_time > self.invincible_duration:
                self.invincible = False

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
            self.speed = self.run_speed
        else:
            self.speed = self.walk_speed
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

    def find_nearest_enemy(self):
        nearest_enemy = None
        min_distance = float('inf')

        for enemy in self.enemies_group:
            distance = math.hypot(self.rect.centerx - enemy.rect.centerx, self.rect.centery - enemy.rect.centery)
            if distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy
        return nearest_enemy

    def auto_attack(self):
        current_time = pygame.time.get_ticks()  # Получаем текущее время
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.attack()  # Вызываем метод атаки
            self.last_attack_time = current_time  # Обновляем время последней атаки

    def attack(self):
        nearest_enemy = self.find_nearest_enemy()
        if nearest_enemy:
            distance = math.hypot(self.rect.centerx - nearest_enemy.rect.centerx,
                                  self.rect.centery - nearest_enemy.rect.centery)
            if distance <= self.attack_radius:
                # Наносим урон ближайшему врагу
                nearest_enemy.take_damage(self.damage)  # Пример нанесения урона


    def update(self):
        self.input()
        self.move()
        self.animate()
        self.invincible_switch()
        self.auto_attack()
        self.gain_exp()

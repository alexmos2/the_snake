from random import randrange

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Класс базового игрового объекта"""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 body_color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовка базового объекта"""
        pass


class Apple(GameObject):
    """Класс Яблоко"""

    def randomize_position(self):
        """Рандомизация координат яблока"""
        x = randrange(0, SCREEN_WIDTH, GRID_SIZE)
        y = randrange(0, SCREEN_HEIGHT, GRID_SIZE)
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовка яблока"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def __init__(self):
        self.body_color = APPLE_COLOR
        self.randomize_position()


class Snake(GameObject):
    """Класс Змейка"""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Смена направления, если нужно"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обработка движения змейки"""
        head = self.get_head_position()
        if self.direction == UP:
            if head[1] == 0:
                self.positions.insert(0, (head[0], SCREEN_HEIGHT))
                self.last = self.positions.pop()
            else:
                self.positions.insert(0, (head[0], head[1] - GRID_SIZE))
                self.last = self.positions.pop()
        elif self.direction == DOWN:
            if head[1] == SCREEN_HEIGHT - GRID_SIZE:
                self.positions.insert(0, (head[0], 0))
                self.last = self.positions.pop()
            else:
                self.positions.insert(0, (head[0], head[1] + GRID_SIZE))
                self.last = self.positions.pop()
        elif self.direction == RIGHT:
            if head[0] == SCREEN_WIDTH - GRID_SIZE:
                self.positions.insert(0, (0, head[1]))
                self.last = self.positions.pop()
            else:
                self.positions.insert(0, (head[0] + GRID_SIZE, head[1]))
                self.last = self.positions.pop()
        elif self.direction == LEFT:
            if head[0] == 0:
                self.positions.insert(0, (SCREEN_WIDTH - GRID_SIZE, head[1]))
                self.last = self.positions.pop()
            else:
                self.positions.insert(0, (head[0] - GRID_SIZE, head[1]))
                self.last = self.positions.pop()

    def draw(self, surface):
        """Отрисовка змейки"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Получения координат головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сброс змейки до начального состояния"""
        print('reset')
        for pos in self.positions:
            rect = pygame.Rect(
                (pos[0], pos[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        rect = pygame.Rect(
            (self.last[0], self.last[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        self.__init__()


def handle_keys(game_object):
    """Обработка нажатий клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры"""
    # Тут нужно создать экземпляры классов.
    player = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        # print(player.positions, ' ', player.direction)
        handle_keys(player)
        player.update_direction()
        player.move()
        head = player.get_head_position()
        if head == apple.position:
            player.positions.insert(0, apple.position)
            apple.randomize_position()
            apple.draw(screen)
        if len(player.positions) > 4:
            head = player.get_head_position()
            other_cells = player.positions[2:]
            print(other_cells)
            if head in other_cells:
                player.reset()
        player.draw(screen)
        apple.draw(screen)
        pygame.display.update()

        # Тут опишите основную логику игры.
        # ...


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self, surface):
#     rect = pygame.Rect(
#         (self.position[0], self.position[1]),
#         (GRID_SIZE, GRID_SIZE)
#     )
#     pygame.draw.rect(surface, self.body_color, rect)
#     pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self, surface):
#     for position in self.positions[:-1]:
#         rect = (
#             pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
#         )
#         pygame.draw.rect(surface, self.body_color, rect)
#         pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(surface, self.body_color, head_rect)
#     pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(
#             (self.last[0], self.last[1]),
#             (GRID_SIZE, GRID_SIZE)
#         )
#         pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#   for event in pygame.event.get():
#       if event.type == pygame.QUIT:
#           pygame.quit()
#           raise SystemExit
#       elif event.type == pygame.KEYDOWN:
#           if event.key == pygame.K_UP and game_object.direction != DOWN:
#               game_object.next_direction = UP
#           elif event.key == pygame.K_DOWN and game_object.direction != UP:
#               game_object.next_direction = DOWN
#           elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#               game_object.next_direction = LEFT
#           elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#               game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None

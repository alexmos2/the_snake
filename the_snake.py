from random import randrange

import pygame

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
        print(f'Вы забыли переопределить метод в классе'
              f'{self.__class__.__name__}')
        raise NotImplementedError

    def draw_rectangle(self, x, y, surface):
        """Отрисовка квадратной области"""
        rect = pygame.Rect(
            (x, y),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс Яблоко"""

    def __init__(self, position=None,
                 body_color=APPLE_COLOR):
        self.body_color = body_color
        if position is None:
            self.randomize_position()
        else:
            self.position = position

    def randomize_position(self):
        """Рандомизация координат яблока"""
        x = randrange(0, SCREEN_WIDTH, GRID_SIZE)
        y = randrange(0, SCREEN_HEIGHT, GRID_SIZE)
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовка яблока"""
        self.draw_rectangle(self.position[0], self.position[1], surface)


class Snake(GameObject):
    """Класс Змейка"""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 body_color=SNAKE_COLOR):
        super().__init__()
        self.length = 1
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = body_color
        self.last = None

    def update_direction(self):
        """Смена направления, если нужно"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обработка движения змейки"""
        head = self.get_head_position()
        x = head[0] + self.direction[0] * GRID_SIZE
        y = head[1] + self.direction[1] * GRID_SIZE
        new_head = (x, y)
        if new_head[1] < 0:
            self.positions.insert(0, (new_head[0], SCREEN_HEIGHT))
        elif new_head[1] >= SCREEN_HEIGHT:
            self.positions.insert(0, (new_head[0], 0))
        elif new_head[0] >= SCREEN_WIDTH:
            self.positions.insert(0, (0, new_head[1]))
        elif new_head[0] < 0:
            self.positions.insert(0, (SCREEN_WIDTH - GRID_SIZE, new_head[1]))
        else:
            self.positions.insert(0, (new_head[0], new_head[1]))
        self.last = self.positions.pop()

    def draw(self, surface):
        """Отрисовка змейки"""
        for position in self.positions[:-1]:
            self.draw_rectangle(position[0], position[1], surface)

        # Отрисовка головы змейки
        self.draw_rectangle(self.positions[0][0],
                            self.positions[0][1], surface)

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
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None


def handle_keys(game_object):
    """Обработка нажатий клавиш"""
    arrowkeys_dict = {
        pygame.K_UP: (DOWN, UP),
        pygame.K_DOWN: (UP, DOWN),
        pygame.K_LEFT: (RIGHT, LEFT),
        pygame.K_RIGHT: (LEFT, RIGHT),
    }
    global SPEED
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key in arrowkeys_dict:
                if game_object.direction != arrowkeys_dict[event.key][0]:
                    game_object.next_direction = arrowkeys_dict[event.key][1]
            elif event.key == pygame.K_KP_MINUS:
                if SPEED > 10:
                    SPEED -= 1
            elif event.key == pygame.K_KP_PLUS:
                if SPEED < 30:
                    SPEED += 1


def main():
    """Основная функция игры"""
    # Инициализация PyGame:
    pygame.init()
    player = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
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
            if head in other_cells:
                player.reset()
        player.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()

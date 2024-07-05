import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 450, 450
CELL_SIZE = 25
GRID_COLOR = (221, 221, 221)
SNAKE_COLOR = (0, 0, 255)
FOOD_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
HUD_COLOR = (0, 0, 255)
FONT_SIZE = 14

# Set up display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("monospace", FONT_SIZE)

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def draw(self, window):
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(window, GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(window, GRID_COLOR, (0, y), (WIDTH, y))

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = FOOD_COLOR

    def get_position(self):
        return self.x * CELL_SIZE, self.y * CELL_SIZE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

class Snake:
    def __init__(self, x, y):
        self.body = [{'x': x, 'y': y, 'color': SNAKE_COLOR}]

    def get_position(self):
        head = self.body[0]
        return head['x'] * CELL_SIZE, head['y'] * CELL_SIZE

    def grow(self):
        last_segment = self.body[-1]
        self.body.append({'x': last_segment['x'], 'y': last_segment['y'], 'color': (135, 206, 235)})

    def check_collision(self):
        head = self.body[0]
        for segment in self.body[1:]:
            if head['x'] == segment['x'] and head['y'] == segment['y']:
                return True
        return False

    def update(self, move):
        prev_x, prev_y = self.body[0]['x'], self.body[0]['y']
        self.body[0]['x'] += move[0]
        self.body[0]['y'] += move[1]

        for i in range(1, len(self.body)):
            self.body[i]['x'], prev_x = prev_x, self.body[i]['x']
            self.body[i]['y'], prev_y = prev_y, self.body[i]['y']

    def draw(self, window):
        for segment in self.body:
            pygame.draw.rect(window, segment['color'], (segment['x'] * CELL_SIZE, segment['y'] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

class Game:
    def __init__(self, window):
        self.window = window
        self.grid = Grid(WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE)
        self.snake = Snake(5, 5)
        self.food = Food(10, 15)
        self.move = [0, 0]
        self.direction = "none"
        self.game_speed = 10
        self.last_render_time = 0
        self.running = True

    def handle_keydown(self, event):
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            if self.direction != "down":
                self.move = [0, -1]
                self.direction = "up"
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            if self.direction != "up":
                self.move = [0, 1]
                self.direction = "down"
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            if self.direction != "right":
                self.move = [-1, 0]
                self.direction = "left"
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            if self.direction != "left":
                self.move = [1, 0]
                self.direction = "right"

    def eat_food(self):
        self.snake.grow()
        self.respawn_food()

    def respawn_food(self):
        max_x = WIDTH // CELL_SIZE
        max_y = HEIGHT // CELL_SIZE
        self.food.x = random.randint(0, max_x - 1)
        self.food.y = random.randint(0, max_y - 1)

    def update(self):
        self.snake.update(self.move)
        head = self.snake.body[0]

        if (
            head['x'] >= self.grid.cols or
            head['x'] < 0 or
            head['y'] < 0 or
            head['y'] >= self.grid.rows or
            self.snake.check_collision()
        ):
            self.reset_snake()

        food_x, food_y = self.food.get_position()
        snake_x, snake_y = self.snake.get_position()
        if snake_x == food_x and snake_y == food_y:
            self.eat_food()

    def reset_snake(self):
        self.snake = Snake(5, 5)
        self.move = [0, 0]
        self.direction = "none"

    def draw_hud(self):
        snake_x, snake_y = self.snake.get_position()
        length = len(self.snake.body)
        text_snake = font.render(f"SNAKE: {snake_x // CELL_SIZE},{snake_y // CELL_SIZE}", True, HUD_COLOR)
        text_length = font.render(f"LENGTH: {length}", True, HUD_COLOR)
        self.window.blit(text_snake, (140, 25))
        self.window.blit(text_length, (240, 25))

    def draw(self):
        self.window.fill(BACKGROUND_COLOR)
        self.grid.draw(self.window)
        self.snake.draw(self.window)
        self.food.draw(self.window)
        self.draw_hud()
        pygame.display.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)

            self.update()
            self.draw()
            clock.tick(self.game_speed)

        pygame.quit()

# Run the game
game = Game(window)
game.snake.body = [{'x': 0, 'y': 0, 'color': SNAKE_COLOR}, {'x': 0, 'y': 0, 'color': (135, 206, 235)}, {'x': 0, 'y': 0, 'color': (135, 206, 235)}]
game.run()


import sys
import pygame
import random

pygame.init()

# Screen dimensions
WIDTH = 640
HEIGHT = 480
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock
clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (0, -CELL_SIZE)

    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        self.positions.insert(0, new_head)
        self.positions.pop()

    def grow(self):
        self.positions.append(self.positions[-1])

    def change_direction(self, new_direction):
        self.direction = new_direction

    def draw(self, screen):
        for position in self.positions:
            pygame.draw.rect(screen, GREEN, pygame.Rect(
                position[0], position[1], CELL_SIZE, CELL_SIZE))


class Food:
    def __init__(self, snake):
        self.position = self.generate_new_position(snake)

    def generate_new_position(self, snake):
        while True:
            x = random.randrange(0, WIDTH, CELL_SIZE)
            y = random.randrange(0, HEIGHT, CELL_SIZE)
            if (x, y) not in snake.positions:
                return (x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, pygame.Rect(
            self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))


def check_collision(snake):
    head = snake.positions[0]
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or head in snake.positions[1:]:
        return True
    return False


def main():
    snake = Snake()
    food = Food(snake)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, CELL_SIZE):
                    snake.change_direction((0, -CELL_SIZE))
                elif event.key == pygame.K_DOWN and snake.direction != (0, -CELL_SIZE):
                    snake.change_direction((0, CELL_SIZE))
                elif event.key == pygame.K_LEFT and snake.direction != (CELL_SIZE, 0):
                    snake.change_direction((-CELL_SIZE, 0))
                elif event.key == pygame.K_RIGHT and snake.direction != (-CELL_SIZE, 0):
                    snake.change_direction((CELL_SIZE, 0))

        snake.move()

        if check_collision(snake):
            snake = Snake()
            food = Food(snake)

        if snake.positions[0] == food.position:
            snake.grow()
            food = Food(snake)

        screen.fill(BLACK)
        snake.draw(screen)

        food.draw(screen)

        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()

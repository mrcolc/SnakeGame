import pygame
import sys
import random
from snake import Snake
from grid import Grid

# Window size
frame_size_x = 720
frame_size_y = 480

# Difficulty settings
difficulty = 25

# Initialise game window
pygame.init()
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x + 150, frame_size_y))

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


def game_over():
    pygame.quit()
    sys.exit()


def main():
    snake = Snake()
    grid = Grid(frame_size_x, frame_size_y)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            elif event.type == pygame.KEYDOWN:
                snake.change_direction(event)

        snake.move()
        food_eaten = snake.grow(grid.food_pos)
        if food_eaten:
            grid.spawn_food(snake.snake_body)
            grid.increase_score()

        grid.draw(game_window, snake.snake_body, snake.direction)

        if grid.check_collision(snake.snake_pos) or grid.check_self_collision(snake.snake_body):
            game_over()

        pygame.display.update()
        fps_controller.tick(difficulty)


if __name__ == "__main__":
    main()

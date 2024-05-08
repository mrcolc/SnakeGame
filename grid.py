import pygame
import random


class Grid:
    def __init__(self, frame_size_x, frame_size_y):
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]

    def spawn_food(self):
        self.food_pos = [random.randrange(1, (self.frame_size_x // 10)) * 10, random.randrange(1, (self.frame_size_y // 10)) * 10]

    def draw(self, game_window, snake_body, snake_pos):
        game_window.fill((0, 0, 0))
        pygame.draw.rect(game_window, (255, 255, 255), (self.food_pos[0], self.food_pos[1], 10, 10))
        for pos in snake_body:
            pygame.draw.rect(game_window, (0, 255, 0), (pos[0], pos[1], 10, 10))

    def check_collision(self, snake_pos):
        return (snake_pos[0] < 0 or snake_pos[0] > self.frame_size_x - 10 or
                snake_pos[1] < 0 or snake_pos[1] > self.frame_size_y - 10)

    def check_self_collision(self, snake_body):
        for block in snake_body[1:]:
            if snake_body[0][0] == block[0] and snake_body[0][1] == block[1]:
                return True
        return False

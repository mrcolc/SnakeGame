import pygame
import numpy as np
from enum import Enum

class Snake:
    def __init__(self, gamemode):
        # gamemode decides how change_direction function works.
        self.gamemode = gamemode
        # snake_pos[0] is x pos
        # snake_pos[1] is y pos
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]
        self.direction = Direction.RIGHT
        self.change_to = self.direction
        self.snake_score = 0

    def change_direction(self, event, gamemode, action):
        if gamemode == 0:
            if event.key == pygame.K_UP or event.key == ord('w'):
                self.change_to = Direction.UP
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                self.change_to = Direction.DOWN
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                self.change_to = Direction.LEFT
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                self.change_to = Direction.RIGHT
        if gamemode == 1:
            clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
            idx = clockwise.index(self.direction)
            # 35.01
            # TODO: AI driven direction changer
            if np.array_equal(action, [1, 0, 0]): # STRAIGHT: No change
                self.change_to = clockwise[idx]
            elif np.array_equal(action, [0, 1, 0]): # RIGHT: Next direction in the clockwise list 
                new_idx = (idx + 1) % 4
                self.change_to = clockwise[new_idx]
            elif np.array_equal(action, [0, 0, 1]): # LEFT: Previous direction in the clockwise list
                new_idx = (idx - 1) % 4
                self.change_to = clockwise[new_idx]
            print("This is AI driven directions")

    def move(self):
        if self.change_to == Direction.UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        if self.change_to == Direction.DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN
        if self.change_to == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        if self.change_to == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT

        if self.direction == Direction.UP:
            self.snake_pos[1] -= 10
        if self.direction == Direction.DOWN:
            self.snake_pos[1] += 10
        if self.direction == Direction.LEFT:
            self.snake_pos[0] -= 10
        if self.direction == Direction.RIGHT:
            self.snake_pos[0] += 10

    def grow(self, food_pos):
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == food_pos[0] and self.snake_pos[1] == food_pos[1]:
            return True
        else:
            self.snake_body.pop()
            return False

    def shrink(self, bomb_pos):
        if self.snake_pos[0] == bomb_pos[0] and self.snake_pos[1] == bomb_pos[1]:
            self.snake_body.pop()
            self.snake_body.pop()
            bomb_pos[0], bomb_pos[1] = -1, -1
            return True
        return False

class Direction(Enum):
    #3643
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
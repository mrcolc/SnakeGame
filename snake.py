import pygame
import numpy as np
from enum import Enum


# The Snake Class to represent snake in the game grid
class Snake:
    def __init__(self):
        # snake_pos[0] is x pos
        # snake_pos[1] is y pos
        self.snake_pos = [100, 50]
        # position of the snake's body
        self.snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]
        # setting score to be 0
        self.snake_score = 0
        # -------- STATE SPACE VARIABLES --------
        # danger zone for snake head. (left, right, below, and above of snake's head)
        self.dangerzone = [[self.snake_pos[0] - 10, self.snake_pos[1]],  # left
                           [self.snake_pos[0] + 10, self.snake_pos[1]],  # right
                           [self.snake_pos[0], self.snake_pos[1] - 10],  # below
                           [self.snake_pos[0], self.snake_pos[1] + 10]]  # above
        # direction to be right initially
        self.direction = Direction.RIGHT
        # shows to next direction
        self.change_to = self.direction

    # A method to change the direction of the snake
    def change_direction(self, event):
        # if arrow up or w pressed
        if event.key == pygame.K_UP or event.key == ord('w'):
            # change direction to the up
            self.change_to = Direction.UP
        # if arrow down or s pressed
        if event.key == pygame.K_DOWN or event.key == ord('s'):
            # change direction to the down
            self.change_to = Direction.DOWN
        # if arrow left or a pressed
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            # change direction to the left
            self.change_to = Direction.LEFT
        # if arrow right or r pressed
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            # change direction to the right
            self.change_to = Direction.RIGHT

    # A method to predict the next direction of the snake
    def predict_direction(self, action):
        # array of directions in the clockwise direction
        clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        # assigning idx to be current position index in the clockwise direction
        idx = clockwise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):  # STRAIGHT: No change
            self.change_to = clockwise[idx]
        elif np.array_equal(action, [0, 1, 0]):  # RIGHT: Next direction in the clockwise list
            new_idx = (idx + 1) % 4
            self.change_to = clockwise[new_idx]
        elif np.array_equal(action, [0, 0, 1]):  # LEFT: Previous direction in the clockwise list
            new_idx = (idx - 1) % 4
            self.change_to = clockwise[new_idx]

    # A method to move the snake on the grid
    def move(self):
        # change direction to Up
        if self.change_to == Direction.UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        # change direction to Down
        elif self.change_to == Direction.DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN
        # change direction to Left
        elif self.change_to == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        # change direction to Right
        elif self.change_to == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT

        # Based on the direction update the snake's position
        if self.direction == Direction.UP:
            self.snake_pos[1] -= 10
        elif self.direction == Direction.DOWN:
            self.snake_pos[1] += 10
        elif self.direction == Direction.LEFT:
            self.snake_pos[0] -= 10
        elif self.direction == Direction.RIGHT:
            self.snake_pos[0] += 10

        # update danger zone (left, right, below, and above of snake's head)
        self.dangerzone = [[self.snake_pos[0] - 10, self.snake_pos[1]],  # left
                           [self.snake_pos[0] + 10, self.snake_pos[1]],  # right
                           [self.snake_pos[0], self.snake_pos[1] - 10],  # below
                           [self.snake_pos[0], self.snake_pos[1] + 10]]  # above

    # A method to grow the length of the snake when the food is eaten
    def grow(self, food_pos):
        # increase the body length by one
        self.snake_body.insert(0, list(self.snake_pos))
        # if the food and the snake are in the same area, that means food is eaten
        if self.snake_pos[0] == food_pos[0] and self.snake_pos[1] == food_pos[1]:
            # return true
            return True
        else:
            # if it is not, decrement the size by one
            self.snake_body.pop()
            # return false
            return False

    # A method to shrink the length of the snake when the bomb is eaten
    def shrink(self, bomb_pos):
        # if the bomb and the snake are in the same area, that means bomb is eaten
        if self.snake_pos[0] == bomb_pos[0] and self.snake_pos[1] == bomb_pos[1]:
            # decrement the size of the snake by two
            self.snake_body.pop()
            self.snake_body.pop()
            # bomb position to be -1,-1 which is deleted in the grid
            bomb_pos[0], bomb_pos[1] = -1, -1
            return True
        return False


# The Direction class to present the direction in enum
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

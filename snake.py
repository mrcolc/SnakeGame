import pygame


class Snake:
    def __init__(self):
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]
        self.direction = 'RIGHT'
        self.change_to = self.direction

    def change_direction(self, event):
        if event.key == pygame.K_UP or event.key == ord('w'):
            self.change_to = 'UP'
        if event.key == pygame.K_DOWN or event.key == ord('s'):
            self.change_to = 'DOWN'
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            self.change_to = 'LEFT'
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            self.change_to = 'RIGHT'

    def move(self):
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        if self.direction == 'UP':
            self.snake_pos[1] -= 10
        if self.direction == 'DOWN':
            self.snake_pos[1] += 10
        if self.direction == 'LEFT':
            self.snake_pos[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_pos[0] += 10

    def grow(self, food_pos):
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == food_pos[0] and self.snake_pos[1] == food_pos[1]:
            return True
        else:
            self.snake_body.pop()
            return False

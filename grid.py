import os
import pygame
import random

# loading photo at the start
current_dir = os.path.dirname(os.path.realpath(__file__))
background = pygame.image.load(os.path.join(current_dir, "lib", "background.png"))
right_panel = pygame.image.load(os.path.join(current_dir, "lib", "right_panel.png"))
food = pygame.image.load(os.path.join(current_dir, "lib", "food.png"))
bomb = pygame.image.load(os.path.join(current_dir, "lib", "bomb.png"))
snakes_head = pygame.image.load(os.path.join(current_dir, "lib", "snake_head.png"))
snakes_body = pygame.image.load(os.path.join(current_dir, "lib", "snake_body.png"))
wall_image = pygame.image.load(os.path.join(current_dir, "lib", "wall_image.png"))

class Grid:
    def __init__(self, frame_size_x, frame_size_y):
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.food_pos = [random.randrange(10, (frame_size_x // 10) - 1) * 10,
                         random.randrange(10, (frame_size_y // 10) - 1) * 10]
        self.bomb_pos = [-1, -1]
        self.wall_positions = []
        while len(self.wall_positions) < 10:
            x = random.randrange(10, (frame_size_x // 10) - 1) * 10
            y = random.randrange(10, (frame_size_y // 10) - 1) * 10
            # Check if there is a wall already in this position or within a 10-pixel gap
            if all(abs(x - w[0]) > 10 or abs(y - w[1]) > 10 for w in self.wall_positions):
                self.wall_positions.append((x, y))

    def spawn_food(self, snake_body):
        self.food_pos = [random.randrange(10, (self.frame_size_x // 10) - 1) * 10,
                         random.randrange(10, (self.frame_size_y // 10) - 1) * 10]
        
        for pos in self.wall_positions:
            if self.food_pos[0] == pos[0] and self.food_pos[1] == pos[1]:
                self.spawn_food(snake_body)
                
        for pos in snake_body:
            if self.food_pos[0] == pos[0] and self.food_pos[1] == pos[1]:
                self.spawn_food(snake_body)

    def spawn_bomb(self, snake_body):
        self.bomb_pos = [random.randrange(10, (self.frame_size_x // 10) - 1) * 10,
                         random.randrange(10, (self.frame_size_y // 10) - 1) * 10]

        for pos in self.wall_positions:
            if self.bomb_pos[0] == pos[0] and self.bomb_pos[1] == pos[1]:
                self.spawn_bomb(snake_body)
                
        for pos in snake_body:
            if self.bomb_pos[0] == pos[0] and self.bomb_pos[1] == pos[1]:
                self.spawn_bomb(snake_body)

        if self.bomb_pos == self.food_pos:
            self.spawn_bomb(snake_body)

    def draw(self, game_window, snake_body, snake_direction, snake_score, high_scores, ai_high_score):
        game_window.blit(background, (0, 0))
        for pos in self.wall_positions:
            game_window.blit(wall_image, (pos[0], pos[1]))
            
        game_window.blit(right_panel, (720, 0))
        game_window.blit(food, (self.food_pos[0], self.food_pos[1]))
        if self.bomb_pos[0] != -1 and self.bomb_pos[1] != -1:
            game_window.blit(bomb, (self.bomb_pos[0], self.bomb_pos[1]))
        # Draw the score in the right panel
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Score", True, (255, 255, 255))
        game_window.blit(text, (755, 80))

        score_text = font.render(str(snake_score), True, (255, 255, 255))
        game_window.blit(score_text, (785, 110))

        high_scores_text = font.render("Records" , True, (255, 255, 255))
        game_window.blit(high_scores_text, (735, 160))

        high_1 = font.render(str(high_scores[0]), True, (255, 255, 255))
        game_window.blit(high_1, (785, 190))
        high_2 = font.render(str(high_scores[1]), True, (255, 255, 255))
        game_window.blit(high_2, (785, 220))
        high_3 = font.render(str(high_scores[2]), True, (255, 255, 255))
        game_window.blit(high_3, (785, 250))
        high_ai = font.render(str(ai_high_score), True, (255, 255, 255))
        game_window.blit(high_ai, (785, 280))

        flag = 0
        for pos in snake_body:
            if flag == 0:
                match snake_direction:
                    case 'UP':
                        game_window.blit(snakes_head, (pos[0], pos[1]))
                    case 'DOWN':
                        game_window.blit(pygame.transform.rotate(snakes_head, 180), (pos[0], pos[1]))
                    case 'LEFT':
                        game_window.blit(pygame.transform.rotate(snakes_head, 90), (pos[0], pos[1]))
                    case 'RIGHT':
                        game_window.blit(pygame.transform.rotate(snakes_head, -90), (pos[0], pos[1]))
                flag = 1
            else:
                game_window.blit(snakes_body, (pos[0], pos[1]))

    def check_collision(self, snake_pos):
        for pos in self.wall_positions:
            if snake_pos[0] == pos[0] and snake_pos[1] == pos[1]:
                return True
        return (snake_pos[0] < 10 or snake_pos[0] > self.frame_size_x - 20 or
                snake_pos[1] < 10 or snake_pos[1] > self.frame_size_y - 20)

    def increase_score(self, snake):
        snake.snake_score += 1

    def decrease_score(self, snake):
        snake.snake_score -= 2

    def check_self_collision(self, snake_body):
        for block in snake_body[1:]:
            if snake_body[0][0] == block[0] and snake_body[0][1] == block[1]:
                return True
        return False
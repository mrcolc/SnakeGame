import pygame
import random


class Grid:
    def __init__(self, frame_size_x, frame_size_y):
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.food_pos = [random.randrange(10, (frame_size_x // 10) - 1) * 10, random.randrange(10, (frame_size_y // 10) - 1) * 10]        

    def spawn_food(self, snake_body):
        self.food_pos = [random.randrange(10, (self.frame_size_x // 10) - 1) * 10, random.randrange(10, (self.frame_size_y // 10) - 1) * 10]

        for pos in snake_body:
            if self.food_pos[0] == pos[0] and self.food_pos[1] == pos[1]:
                self.spawn_food(snake_body)
    def draw(self, game_window, snake_body, snake_direction,snake_score):
        background = pygame.image.load("background.png")
        game_window.blit(background, (0,0))
        right_panel = pygame.image.load("right_panel.png") # 150 *480
        game_window.blit(right_panel, (720,0))
        food = pygame.image.load("food.png")
        game_window.blit(food, (self.food_pos[0], self.food_pos[1]))
         # Draw the score in the right panel
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Score", True, (255, 255, 255))        
        game_window.blit(text, (755,80))

        score_text = font.render(str(snake_score), True, (255, 255, 255))
        game_window.blit(score_text, (785,110))
        flag = 0
        snakes_head = pygame.image.load("snake_head.png")
        snakes_body = pygame.image.load("snake_body.png")
        for pos in snake_body:
            if flag == 0:
                match snake_direction:
                    case 'DOWN':
                        snakes_head = pygame.transform.rotate(snakes_head, 180)
                    case 'LEFT':
                        snakes_head = pygame.transform.rotate(snakes_head, 90)
                    case 'RIGHT':
                        snakes_head = pygame.transform.rotate(snakes_head, -90)
                game_window.blit(snakes_head, (pos[0], pos[1]))
                flag = 1
            else:
                game_window.blit(snakes_body, (pos[0], pos[1]))

    def check_collision(self, snake_pos):
        return (snake_pos[0] < 10 or snake_pos[0] > self.frame_size_x - 20 or
                snake_pos[1] < 10 or snake_pos[1] > self.frame_size_y - 20)
    def increase_score(self,snake):
        snake.snake_score += 1
    def check_self_collision(self, snake_body):
        for block in snake_body[1:]:
            if snake_body[0][0] == block[0] and snake_body[0][1] == block[1]:
                return True
        return False

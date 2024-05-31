import os  # to get the path of a file
import pygame
import random

# loading photos from the lib at the start
# getting the current path
current_dir = os.path.dirname(os.path.realpath(__file__))
# adding folder name and the file name to current directory to access pngs
background = pygame.image.load(os.path.join(current_dir, "lib", "background.png"))
right_panel = pygame.image.load(os.path.join(current_dir, "lib", "right_panel.png"))
food = pygame.image.load(os.path.join(current_dir, "lib", "food.png"))
bomb = pygame.image.load(os.path.join(current_dir, "lib", "bomb.png"))
snakes_head = pygame.image.load(os.path.join(current_dir, "lib", "snake_head.png"))
snakes_body = pygame.image.load(os.path.join(current_dir, "lib", "snake_body.png"))
wall_image = pygame.image.load(os.path.join(current_dir, "lib", "wall_image.png"))


# The Grid class to represent the snake in the grid and the right panel
class Grid:
    def __init__(self, frame_size_x, frame_size_y):
        # assigning x and y size of the frame
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        # creating the food position
        self.food_pos = [random.randrange(10, (frame_size_x // 10) - 1) * 10,
                         random.randrange(10, (frame_size_y // 10) - 1) * 10]
        # bomb position to be -1,-1 that means off the grid
        self.bomb_pos = [-1, -1]
        # wall positions array created
        self.wall_positions = []
        # random wall creating mechanism
        while len(self.wall_positions) < 10:
            # creating random x and y values
            x = random.randrange(10, (frame_size_x // 10) - 1) * 10
            y = random.randrange(10, (frame_size_y // 10) - 1) * 10
            # check if there is a wall already in this position or within a 10-pixel gap
            if all(abs(x - w[0]) > 10 or abs(y - w[1]) > 10 for w in self.wall_positions):
                self.wall_positions.append((x, y))

    # A method to spawn the food in the grid
    def spawn_food(self, snake_body):
        # creating random positions for the food
        self.food_pos = [random.randrange(10, (self.frame_size_x // 10) - 1) * 10,
                         random.randrange(10, (self.frame_size_y // 10) - 1) * 10]

        # checking if the position of the food inside the walls
        for pos in self.wall_positions:
            if self.food_pos[0] == pos[0] and self.food_pos[1] == pos[1]:
                # if it is create new random values for position of the food
                self.spawn_food(snake_body)

        # checking if the position of the food inside the snake's body
        for pos in snake_body:
            if self.food_pos[0] == pos[0] and self.food_pos[1] == pos[1]:
                # if it is create new random values for position of the food
                self.spawn_food(snake_body)

    # A method to spawn the bomb on the grid
    def spawn_bomb(self, snake_body):
        # creating random position for the bomb
        self.bomb_pos = [random.randrange(10, (self.frame_size_x // 10) - 1) * 10,
                         random.randrange(10, (self.frame_size_y // 10) - 1) * 10]

        # checking if the position of the bomb inside the walls
        for pos in self.wall_positions:
            if self.bomb_pos[0] == pos[0] and self.bomb_pos[1] == pos[1]:
                # if it is create new random values for position of the bomb
                self.spawn_bomb(snake_body)

        # checking if the position of the bomb inside the snake's body
        for pos in snake_body:
            if self.bomb_pos[0] == pos[0] and self.bomb_pos[1] == pos[1]:
                # if it is create new random values for position of the bomb
                self.spawn_bomb(snake_body)

        # checking if the position of the bomb is the same with the food position
        if self.bomb_pos == self.food_pos:
            # if it is create new random values for position of the bomb
            self.spawn_bomb(snake_body)

    # A amethod to draw the grid
    def draw(self, game_window, snake_body, snake_direction, current_score, high_scores, ai_high_score):
        # adjusting the background
        game_window.blit(background, (0, 0))
        # draw the walls based on the position of the walls
        for pos in self.wall_positions:
            game_window.blit(wall_image, (pos[0], pos[1]))

        # create the right panel
        game_window.blit(right_panel, (720, 0))
        # draw the food on the grid
        game_window.blit(food, (self.food_pos[0], self.food_pos[1]))
        # if the bomb positions are not -1,-1, draw the bomb on the grid
        if self.bomb_pos[0] != -1 and self.bomb_pos[1] != -1:
            game_window.blit(bomb, (self.bomb_pos[0], self.bomb_pos[1]))

        # write the current score on the right panel
        font = pygame.font.Font('freesansbold.ttf', 22)
        text = font.render("Score: ", True, (255, 255, 255))
        game_window.blit(text, (740, 60))
        score = font.render(str(current_score), True, (255, 255, 255))
        game_window.blit(score, (815, 60))

        # write the top 3 high scores on the right panel
        text = font.render("Records", True, (255, 255, 255))
        game_window.blit(text, (745, 110))
        high_1 = font.render("1st: " + str(high_scores[0]), True, (255, 255, 255))
        game_window.blit(high_1, (755, 140))
        high_2 = font.render("2nd: " + str(high_scores[1]), True, (255, 255, 255))
        game_window.blit(high_2, (755, 170))
        high_3 = font.render("3rd: " + str(high_scores[2]), True, (255, 255, 255))
        game_window.blit(high_3, (755, 200))

        # write the AI's high score on the right panel
        text = font.render("AI Record", True, (255, 255, 255))
        game_window.blit(text, (740, 240))
        high_ai = font.render(str(ai_high_score), True, (255, 255, 255))
        game_window.blit(high_ai, (785, 270))

        # write instructions on the right panel
        text = font.render("Press P", True, (255, 255, 255))
        game_window.blit(text, (750, 310))
        text = font.render("to pause", True, (255, 255, 255))
        game_window.blit(text, (745, 340))
        text = font.render("or exit", True, (255, 255, 255))
        game_window.blit(text, (750, 370))

        # based on the direction draw the snake body
        flag = 0
        for pos in snake_body:
            if flag == 0:
                match snake_direction:
                    # for the snake head
                    case 'UP':
                        # if it is up draw the snake head
                        game_window.blit(snakes_head, (pos[0], pos[1]))
                    case 'DOWN':
                        # if it is down, rotate the snake head 180 degrees and draw
                        game_window.blit(pygame.transform.rotate(snakes_head, 180), (pos[0], pos[1]))
                    case 'LEFT':
                        # if it is left, rotate the snake head 90 degrees and draw
                        game_window.blit(pygame.transform.rotate(snakes_head, 90), (pos[0], pos[1]))
                    case 'RIGHT':
                        # if it is right, rotate the snake head -90 degrees and draw
                        game_window.blit(pygame.transform.rotate(snakes_head, -90), (pos[0], pos[1]))
                flag = 1 # setting flag to 1, that means snake head is drawn
            else:
                # draw the snake body
                game_window.blit(snakes_body, (pos[0], pos[1]))

    # A method to checking the collision of the snake with the walls
    def check_collision(self, snake_pos):
        # checking if the snake hit the inner random walls
        for pos in self.wall_positions:
            if snake_pos[0] == pos[0] and snake_pos[1] == pos[1]:
                return True
        # checking if the snake hit the outer walls
        return (snake_pos[0] < 10 or snake_pos[0] > self.frame_size_x - 20 or
                snake_pos[1] < 10 or snake_pos[1] > self.frame_size_y - 20)

    # A method to increase the score of the snake
    def increase_score(self, snake):
        snake.snake_score += 1

    # A method to decrease the score of the snake
    def decrease_score(self, snake):
        snake.snake_score -= 2

    # A method to checking the collision of the snake with itself
    def check_self_collision(self, snake_body):
        # checking if the head is in the body
        for block in snake_body[1:]:
            if snake_body[0][0] == block[0] and snake_body[0][1] == block[1]:
                return True
        return False

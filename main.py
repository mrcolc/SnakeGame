import pygame
import sys
import os
import random
import numpy as np
import torch
from snake import Snake
from grid import Grid
from agent import Agent
from pygame import mixer

# Starting the mixer 
mixer.init()
current_dir = os.path.dirname(os.path.realpath(__file__))

playlist = ["song1.mp3", "song2.mp3", "song3.mp3"]

first_song = playlist[random.randint(0, len(playlist) - 1)]

MUSIC_END = pygame.USEREVENT + 1
# Loading the song 
mixer.music.load(os.path.join(current_dir, "lib", first_song))

# Setting the volume 
mixer.music.set_volume(0.02)
# Start playing the song 
mixer.music.play()

# loading photos at the start
main_menu = pygame.image.load(os.path.join(current_dir, 'lib', 'main_menu.png'))
game_over_menu_img = pygame.image.load(os.path.join(current_dir, 'lib', 'game_over_menu.png'))
difficulty_menu_img = pygame.image.load(os.path.join(current_dir, 'lib', 'difficulty_menu_img.png'))
blink_button = pygame.image.load(os.path.join(current_dir, 'lib', 'blink_button.png'))

# Window size
frame_size_x = 720
frame_size_y = 480

# Initialise game window
pygame.init()
pygame.display.set_caption('Snake Game')
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

def start_playlist():
    song_to_play = playlist[random.randint(0, len(playlist) - 1)]
    if song_to_play == first_song:
        start_playlist()
    pygame.mixer.music.load(os.path.join(current_dir, 'lib', song_to_play))
    pygame.mixer.music.play()

def show_menu():
    button_width = 200
    button_height = 50
    play_button_x = 335
    play_button_y = 250
    aiDriven_button_x = 335
    aiDriven_button_y = 320
    prediction_only_button_x = 335
    prediction_only_button_y = 390
    
    font = pygame.font.Font('freesansbold.ttf', 30)
    play_text = font.render("Play", True, black)
    ai_driven_text = font.render("AI Trainer", True, black)
    prediction_only_text = font.render("AI Player", True, black)
    
    game_window.blit(main_menu, (0, 0))

    game_window.blit(blink_button, (play_button_x, play_button_y))
    game_window.blit(play_text, (play_button_x + button_width // 2 - play_text.get_width() // 2, play_button_y + button_height // 2 - play_text.get_height() // 2))

    game_window.blit(blink_button, (aiDriven_button_x, aiDriven_button_y))
    game_window.blit(ai_driven_text, (aiDriven_button_x + button_width // 2 - ai_driven_text.get_width() // 2, aiDriven_button_y + button_height // 2 - ai_driven_text.get_height() // 2))

    game_window.blit(blink_button, (prediction_only_button_x, prediction_only_button_y))
    game_window.blit(prediction_only_text, (prediction_only_button_x + button_width // 2 - prediction_only_text.get_width() // 2, prediction_only_button_y + button_height // 2 - prediction_only_text.get_height() // 2))

    pygame.display.update()

    start_game = False
    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if play_button_x <= mouse_x <= play_button_x + button_width and play_button_y <= mouse_y <= play_button_y + button_height:
                    # Mode select (0 for player, 1 for AI)
                    gamemode = 0
                    difficulty = difficulty_menu()
                    start_game = True
                elif aiDriven_button_x <= mouse_x <= aiDriven_button_x + button_width and aiDriven_button_y <= mouse_y <= aiDriven_button_y + button_height:
                    # Mode select (0 for player, 1 for AI)
                    gamemode = 1
                    difficulty = 1600
                    start_game = True
                elif prediction_only_button_x <= mouse_x <= prediction_only_button_x + button_width and prediction_only_button_y <= mouse_y <= prediction_only_button_y + button_height:
                    gamemode = 2
                    difficulty = 50  # Use a fixed difficulty for prediction only
                    start_game = True
        fps_controller.tick(30)
    return gamemode, difficulty

def game_over_menu(snake: Snake):
    button_width = 200
    button_height = 50
    score_text_x = 375
    score_text_y = 250
    main_menu_button_x = 335
    main_menu_button_y = 300
    quit_button_x = 335
    quit_button_y = 370

    game_window.blit(game_over_menu_img, (0, 0))

    font = pygame.font.Font('freesansbold.ttf', 30)
    text = font.render("Score: " + str(snake.snake_score), True, white)  # str(snake_score)
    main_menu_text = font.render("Main Menu", True, black)
    quit_text = font.render("Quit", True, black)
    
    game_window.blit(text, (score_text_x, score_text_y))

    game_window.blit(blink_button, (main_menu_button_x, main_menu_button_y))
    game_window.blit(main_menu_text, (main_menu_button_x + button_width // 2 - main_menu_text.get_width() // 2, main_menu_button_y + button_height // 2 - main_menu_text.get_height() // 2))

    game_window.blit(blink_button, (quit_button_x, quit_button_y))
    game_window.blit(quit_text, (quit_button_x + button_width // 2 - quit_text.get_width() // 2, quit_button_y + button_height // 2 - quit_text.get_height() // 2))

    pygame.display.update()

    finish_game = False
    while not finish_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if main_menu_button_x <= mouse_x <= main_menu_button_x + button_width and main_menu_button_y <= mouse_y <= main_menu_button_y + button_height:
                    main()
                elif quit_button_x <= mouse_x <= quit_button_x + button_width and quit_button_y <= mouse_y <= quit_button_y + button_height:
                    finish_game = True
        fps_controller.tick(30)

def pause_menu():
    global is_paused
    is_paused = False
    
    button_width = 200
    button_height = 50
    resume_button_x = 335
    resume_button_y = 250
    main_menu_button_x = 335
    main_menu_button_y = 320
    quit_button_x = 335
    quit_button_y = 390
    
    font = pygame.font.Font('freesansbold.ttf', 30)
    resume_text = font.render("Resume", True, black)
    main_menu_text = font.render("Main Menu", True, black)
    quit_text = font.render("Quit", True, black)

    game_window.blit(main_menu, (0, 0))

    game_window.blit(blink_button, (resume_button_x, resume_button_y))
    game_window.blit(resume_text, (resume_button_x + button_width // 2 - resume_text.get_width() // 2, resume_button_y + button_height // 2 - resume_text.get_height() // 2))
    
    game_window.blit(blink_button, (main_menu_button_x, main_menu_button_y))
    game_window.blit(main_menu_text, (main_menu_button_x + button_width // 2 - main_menu_text.get_width() // 2, main_menu_button_y + button_height // 2 - main_menu_text.get_height() // 2))
    
    game_window.blit(blink_button, (quit_button_x, quit_button_y))
    game_window.blit(quit_text, (quit_button_x + button_width // 2 - quit_text.get_width() // 2, quit_button_y + button_height // 2 - quit_text.get_height() // 2))

    pygame.display.update()

    start_game = False
    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if resume_button_x <= mouse_x <= resume_button_x + button_width and resume_button_y <= mouse_y <= resume_button_y + button_height:
                    return
                    
                elif main_menu_button_x <= mouse_x <= main_menu_button_x + button_width and main_menu_button_y <= mouse_y <= main_menu_button_y + button_height:
                    main()
                    
                elif quit_button_x <= mouse_x <= quit_button_x + button_width and quit_button_y <= mouse_y <= quit_button_y + button_height:
                    pygame.quit()
                    sys.exit()
                    
        fps_controller.tick(30)
        
def difficulty_menu():
    difficulty = 0
    button_width = 200
    button_height = 50
    choose_difficulty_x = 290
    choose_difficulty_y = 200
    easy_button_x = 335
    easy_button_y = 250
    normal_button_x = 335
    normal_button_y = 320
    hard_button_x = 335
    hard_button_y = 390
    
    font = pygame.font.Font('freesansbold.ttf', 30)
    easy_text = font.render("Easy", True, black)
    medium_text = font.render("Medium", True, black)
    hard_text = font.render("Hard", True, black)
    choose_difficulty_text = font.render("Choose a difficulty", True, white)

    game_window.blit(main_menu, (0, 0))
    
    game_window.blit(choose_difficulty_text, (choose_difficulty_x, choose_difficulty_y))

    game_window.blit(blink_button, (easy_button_x, easy_button_y))
    game_window.blit(easy_text, (easy_button_x + button_width // 2 - easy_text.get_width() // 2, easy_button_y + button_height // 2 - easy_text.get_height() // 2))

    game_window.blit(blink_button, (normal_button_x, normal_button_y))
    game_window.blit(medium_text, (normal_button_x + button_width // 2 - medium_text.get_width() // 2, normal_button_y + button_height // 2 - medium_text.get_height() // 2))

    game_window.blit(blink_button, (hard_button_x, hard_button_y))
    game_window.blit(hard_text, (hard_button_x + button_width // 2 - hard_text.get_width() // 2, hard_button_y + button_height // 2 - hard_text.get_height() // 2))

    pygame.display.update()

    start_game = False
    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if easy_button_x <= mouse_x <= easy_button_x + button_width and easy_button_y <= mouse_y <= easy_button_y + button_height:
                    start_game = True
                    difficulty = 15
                elif normal_button_x <= mouse_x <= normal_button_x + button_width and normal_button_y <= mouse_y <= normal_button_y + button_height:
                    start_game = True
                    difficulty = 25
                elif hard_button_x <= mouse_x <= hard_button_x + button_width and hard_button_y <= mouse_y <= hard_button_y + button_height:
                    start_game = True
                    difficulty = 35

        fps_controller.tick(30)
    return difficulty

def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def create_game(gamemode, difficulty, reward, agent: Agent, training_count, self_collision_count):
    snake = Snake()
    grid = Grid(frame_size_x, frame_size_y)
    agent.snake = snake
    agent.grid = grid
    value_to_spawn_bomb = 5
    is_paused = False
    frame_iteration = 0

    if gamemode == 0:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over()
                elif event.type == pygame.KEYDOWN:
                    snake.change_direction(event)
                    if event.key == pygame.K_p:  # Check if 'P' key is pressed
                        is_paused = True
                        if is_paused:
                            pause_menu()
                            is_paused = False
                if event.type == MUSIC_END:
                    start_playlist()
            if is_paused:
                continue

            pygame.mixer.music.set_endevent(MUSIC_END)

            snake.move()

            food_eaten = snake.grow(grid.food_pos)
            if food_eaten:
                grid.spawn_food(snake.snake_body)
                grid.increase_score(snake)

            # Update UI
            grid.draw(game_window, snake.snake_body, snake.direction, snake.snake_score)

            if grid.check_collision(snake.snake_pos) or grid.check_self_collision(snake.snake_body):
                game_over_menu(snake)
                game_over()
                break

            if snake.snake_score == value_to_spawn_bomb:
                grid.spawn_bomb(snake.snake_body)
                value_to_spawn_bomb += 5

            if snake.snake_score == value_to_spawn_bomb - 2:
                grid.bomb_pos[0], grid.bomb_pos[1] = -1, -1

            if snake.shrink(grid.bomb_pos):
                grid.decrease_score(snake)

            pygame.display.update()
            fps_controller.tick(difficulty)
    
    if gamemode == 1 and training_count < 1000: # if counter goes high above a certain number, stop training.
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Check if 'P' key is pressed
                        is_paused = True
                        if is_paused:
                            pause_menu()
                            is_paused = False
                    if event.type == MUSIC_END:
                        start_playlist()
                if is_paused:
                    continue
                pygame.mixer.music.set_endevent(MUSIC_END)

            # This game has not finished yet.
            done = 0

            old_pos = snake.snake_pos
            food_pos = grid.food_pos
            old_distance = calculate_distance(old_pos, food_pos)

            # Get move and train.
            state_current, action = agent.generate_action()
            snake.predict_direction(action) 
            snake.move()

            new_pos = snake.snake_pos
            new_distance = calculate_distance(new_pos, food_pos)

            # Set reward back to 0 before another evaluation.
            reward = 0

            if new_distance < old_distance:
                reward += 10
            else:
                reward += -5

            # Update reward for food eaten.
            food_eaten = snake.grow(grid.food_pos)
            if food_eaten:
                reward += 15
                frame_iteration = 0
                grid.spawn_food(snake.snake_body)
                grid.increase_score(snake)

            agent.train(state_current, action, reward, done)

            # Update UI
            grid.draw(game_window, snake.snake_body, snake.direction, snake.snake_score)

            # Update reward for collision and end the game if collision happens.
            if grid.check_collision(snake.snake_pos) or frame_iteration > 1000:
                reward += -10
                break

            if grid.check_self_collision(snake.snake_body):
                self_collision_count += 1
                print("Self collision: " + str(self_collision_count))
                reward = -15
                break

            # NO BOMBS FOR AI TRAINING: THEY CONTRADICT WITH LEARNING CURVE.
            '''
            if snake.snake_score == value_to_spawn_bomb:
                grid.spawn_bomb(snake.snake_body)
                value_to_spawn_bomb += 5

            if snake.snake_score == value_to_spawn_bomb - 2:
                grid.bomb_pos[0], grid.bomb_pos[1] = -1, -1
            '''

            if snake.shrink(grid.bomb_pos):
                grid.decrease_score(snake)
            
            frame_iteration += 1
            pygame.display.update()
            fps_controller.tick(difficulty)

        # Train for collision (since collision breaks the loop and ends the game)
        done = 1
        agent.train(state_current, action, reward, done)
        create_game(gamemode, difficulty, reward, agent, training_count + 1, self_collision_count)

    if gamemode == 2:
        agent.model.load_state_dict(torch.load('absolute_model/absolute_model.pth'))
        agent.model.eval()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Check if 'P' key is pressed
                        is_paused = True
                        if is_paused:
                            pause_menu()
                            is_paused = False
                    if event.type == MUSIC_END:
                        start_playlist()
                if is_paused:
                    continue
                pygame.mixer.music.set_endevent(MUSIC_END)

            state_current, action = agent.predict_action()
            snake.predict_direction(action) 
            snake.move()

            # Update reward for food eaten.
            food_eaten = snake.grow(grid.food_pos)
            if food_eaten:
                grid.spawn_food(snake.snake_body)
                grid.increase_score(snake)

            # Update UI
            grid.draw(game_window, snake.snake_body, snake.direction, snake.snake_score)

            # Update reward for collision and end the game if collision happens.
            if grid.check_collision(snake.snake_pos) or grid.check_self_collision(snake.snake_body):
                break

            if snake.snake_score == value_to_spawn_bomb:
                grid.spawn_bomb(snake.snake_body)
                value_to_spawn_bomb += 5

            if snake.snake_score == value_to_spawn_bomb - 2:
                grid.bomb_pos[0], grid.bomb_pos[1] = -1, -1

            if snake.shrink(grid.bomb_pos):
                grid.decrease_score(snake)

            pygame.display.update()
            fps_controller.tick(difficulty)

        create_game(gamemode, difficulty, reward, agent, training_count, self_collision_count)

def main():
    gamemode, difficulty = show_menu()
    
    # SETUP FOR AGENT
    snake = Snake()
    grid = Grid(frame_size_x, frame_size_y)
    agent = Agent(snake, grid)
    
    reward = 0
    training_count = 0
    self_collision_count = 0
    
    create_game(gamemode, difficulty, reward, agent, training_count, self_collision_count)

if __name__ == "__main__":
    main()

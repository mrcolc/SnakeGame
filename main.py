import pygame
import sys
import os
import random
import numpy as np
import torch
import plotter as pt
from snake import Snake
from grid import Grid
from agent import Agent
from pygame import mixer

# Starting the mixer 
mixer.init()
# Get the directory of the script
current_dir = os.path.dirname(os.path.realpath(__file__))

# List of songs
playlist = ["song1.mp3", "song2.mp3", "song3.mp3"]

# Randomly select the first song from the playlist
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
# Create the game window with additional space for the score panel 
game_window = pygame.display.set_mode((frame_size_x + 150, frame_size_y))

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# FPS (frames per second) controller to manage the game's speed
fps_controller = pygame.time.Clock()

def game_over():
    """
    Function to handle game over scenario.
    Quits the game and closes the window.
    """
    pygame.quit()
    sys.exit()

def start_playlist():
    """
    Function to start playing a random song from the playlist.
    Ensures the same song doesn't play consecutively.
    """
    
    song_to_play = playlist[random.randint(0, len(playlist) - 1)]
    if song_to_play == first_song:
        start_playlist()
    pygame.mixer.music.load(os.path.join(current_dir, 'lib', song_to_play))
    pygame.mixer.music.play()

def show_menu():
    
    # Function for displaying the main menu and handling user interaction.
    
    # Button dimensions
    button_width = 200
    button_height = 50
    
    # Button positions
    play_button_x = 335
    play_button_y = 250
    aiDriven_button_x = 335
    aiDriven_button_y = 320
    prediction_only_button_x = 335
    prediction_only_button_y = 390
    
    # Font settings for text
    font = pygame.font.Font('freesansbold.ttf', 30)
    play_text = font.render("Play", True, black)
    ai_driven_text = font.render("AI Trainer", True, black)
    prediction_only_text = font.render("AI Player", True, black)
    
    # Here draw the main menu background
    game_window.blit(main_menu, (0, 0))

    # Draw the play button and its text
    game_window.blit(blink_button, (play_button_x, play_button_y))
    game_window.blit(play_text, (play_button_x + button_width // 2 - play_text.get_width() // 2, play_button_y + button_height // 2 - play_text.get_height() // 2))

    # Draw the AI Trainer button and its text
    game_window.blit(blink_button, (aiDriven_button_x, aiDriven_button_y))
    game_window.blit(ai_driven_text, (aiDriven_button_x + button_width // 2 - ai_driven_text.get_width() // 2, aiDriven_button_y + button_height // 2 - ai_driven_text.get_height() // 2))
    
    # Draw the AI Player button and its text
    game_window.blit(blink_button, (prediction_only_button_x, prediction_only_button_y))
    game_window.blit(prediction_only_text, (prediction_only_button_x + button_width // 2 - prediction_only_text.get_width() // 2, prediction_only_button_y + button_height // 2 - prediction_only_text.get_height() // 2))
    # Update the display and show the menu
    pygame.display.update()

    
    start_game = False
    while not start_game:
        # handling user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game if the user closes the window
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # here we get the position of mouse click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if the Play button was clicked
                if play_button_x <= mouse_x <= play_button_x + button_width and play_button_y <= mouse_y <= play_button_y + button_height:
                    # Mode select (0 for player, 1 for AI)
                    gamemode = 0
                    # send the user difficulty menu for choosing difficulty
                    difficulty = difficulty_menu()
                    start_game = True
                # Check if the AI Trainer button was clicked    
                elif aiDriven_button_x <= mouse_x <= aiDriven_button_x + button_width and aiDriven_button_y <= mouse_y <= aiDriven_button_y + button_height:
                    # Mode select (0 for player, 1 for AI)
                    gamemode = 1
                    difficulty = 1600
                    start_game = True
                # Check if the AI Player button was clicked
                elif prediction_only_button_x <= mouse_x <= prediction_only_button_x + button_width and prediction_only_button_y <= mouse_y <= prediction_only_button_y + button_height:
                    gamemode = 2
                    difficulty = 50  # Use a fixed difficulty for prediction only
                    start_game = True
        fps_controller.tick(30)
    # Return the selected game mode and difficulty
    return gamemode, difficulty

def game_over_menu(snake: Snake):
    
    #Function for displaying the game over menu and handling user interaction.
    
    # Button dimensions
    button_width = 200
    button_height = 50
    
    # Position for score text
    score_text_x = 375
    score_text_y = 260
    
    # Button positions
    main_menu_button_x = 335
    main_menu_button_y = 310
    quit_button_x = 335
    quit_button_y = 370

    # Draw the game over menu background
    game_window.blit(game_over_menu_img, (0, 0))

    # Font settings for text
    font = pygame.font.Font('freesansbold.ttf', 30)
    # Display the player's score
    text = font.render("Score: " + str(snake.snake_score), True, white)  # str(snake_score)
    main_menu_text = font.render("Main Menu", True, black)
    quit_text = font.render("Quit", True, black)

    # Draw the score text
    game_window.blit(text, (score_text_x, score_text_y))

    # Draw the main menu button and its text
    game_window.blit(blink_button, (main_menu_button_x, main_menu_button_y))
    game_window.blit(main_menu_text, (main_menu_button_x + button_width // 2 - main_menu_text.get_width() // 2, main_menu_button_y + button_height // 2 - main_menu_text.get_height() // 2))

    # Draw the quit button and its text
    game_window.blit(blink_button, (quit_button_x, quit_button_y))
    game_window.blit(quit_text, (quit_button_x + button_width // 2 - quit_text.get_width() // 2, quit_button_y + button_height // 2 - quit_text.get_height() // 2))

    # Update the display to show the game over menu 
    pygame.display.update()

    finish_game = False
    while not finish_game:
        # Handling user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game if the user closes the window
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # here we get the position of mouse click
                mouse_x, mouse_y = pygame.mouse.get_pos()    
                # Check if the main menu button was clicked    
                if main_menu_button_x <= mouse_x <= main_menu_button_x + button_width and main_menu_button_y <= mouse_y <= main_menu_button_y + button_height:
                    main()# send the user main menu 
                # Check if the quit button was clicked    
                elif quit_button_x <= mouse_x <= quit_button_x + button_width and quit_button_y <= mouse_y <= quit_button_y + button_height:
                    finish_game = True # Exit the loop to finish the game
        fps_controller.tick(30)

def pause_menu():
    
    #Function for displaying the pause menu and handling user interaction.
    
    global is_paused
    is_paused = False # Unpause the game by default when entering the menu
    
    # Button dimensions
    button_width = 200
    button_height = 50
    
    # Button positions
    resume_button_x = 335
    resume_button_y = 250
    main_menu_button_x = 335
    main_menu_button_y = 320
    quit_button_x = 335
    quit_button_y = 390
    
    # Font settings for text
    font = pygame.font.Font('freesansbold.ttf', 30)
    resume_text = font.render("Resume", True, black)
    main_menu_text = font.render("Main Menu", True, black)
    quit_text = font.render("Quit", True, black)
    
     # Draw the pause menu background
    game_window.blit(main_menu, (0, 0))

    # Draw the resume button and its text
    game_window.blit(blink_button, (resume_button_x, resume_button_y))
    game_window.blit(resume_text, (resume_button_x + button_width // 2 - resume_text.get_width() // 2, resume_button_y + button_height // 2 - resume_text.get_height() // 2))
   
    # Draw the main menu button and its text
    game_window.blit(blink_button, (main_menu_button_x, main_menu_button_y))
    game_window.blit(main_menu_text, (main_menu_button_x + button_width // 2 - main_menu_text.get_width() // 2, main_menu_button_y + button_height // 2 - main_menu_text.get_height() // 2))
    
    # Draw the quit button and its text
    game_window.blit(blink_button, (quit_button_x, quit_button_y))
    game_window.blit(quit_text, (quit_button_x + button_width // 2 - quit_text.get_width() // 2, quit_button_y + button_height // 2 - quit_text.get_height() // 2))

    # Update the display to show the pause menu
    pygame.display.update()

    start_game = False
    while not start_game:
        # Handling user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game if the user closes the window
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # here we get the position of mouse click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Check if the Resume button was clicked
                if resume_button_x <= mouse_x <= resume_button_x + button_width and resume_button_y <= mouse_y <= resume_button_y + button_height:
                    return # Exit the menu to resume the game
                
                # Check if the Main Menu button was clicked
                elif main_menu_button_x <= mouse_x <= main_menu_button_x + button_width and main_menu_button_y <= mouse_y <= main_menu_button_y + button_height:
                    main() # Call the main function to return to the main menu
                
                # Check if the Quit button was clicked   
                elif quit_button_x <= mouse_x <= quit_button_x + button_width and quit_button_y <= mouse_y <= quit_button_y + button_height:
                    pygame.quit()
                    sys.exit()  # Quit the game
                    
        fps_controller.tick(30)
        
def difficulty_menu():
    
    #Function for displaying the difficulty menu and handling user interaction.
    
    difficulty = 0 # Default difficulty value
    
    # Button dimensions
    button_width = 200
    button_height = 50
    
    # Button and text positions
    choose_difficulty_x = 290
    choose_difficulty_y = 200
    easy_button_x = 335
    easy_button_y = 250
    normal_button_x = 335
    normal_button_y = 320
    hard_button_x = 335
    hard_button_y = 390
    
    # Font settings for text
    font = pygame.font.Font('freesansbold.ttf', 30)
    easy_text = font.render("Easy", True, black)
    medium_text = font.render("Medium", True, black)
    hard_text = font.render("Hard", True, black)
    choose_difficulty_text = font.render("Choose a difficulty", True, white)
    
    # Draw the difficulty menu background 
    game_window.blit(main_menu, (0, 0))
    
    # Draw the "Choose a difficulty" text
    game_window.blit(choose_difficulty_text, (choose_difficulty_x, choose_difficulty_y))

    # Draw the Easy button and its text
    game_window.blit(blink_button, (easy_button_x, easy_button_y))
    game_window.blit(easy_text, (easy_button_x + button_width // 2 - easy_text.get_width() // 2, easy_button_y + button_height // 2 - easy_text.get_height() // 2))

    # Draw the Medium button and its text
    game_window.blit(blink_button, (normal_button_x, normal_button_y))
    game_window.blit(medium_text, (normal_button_x + button_width // 2 - medium_text.get_width() // 2, normal_button_y + button_height // 2 - medium_text.get_height() // 2))

    # Draw the Hard button and its text
    game_window.blit(blink_button, (hard_button_x, hard_button_y))
    game_window.blit(hard_text, (hard_button_x + button_width // 2 - hard_text.get_width() // 2, hard_button_y + button_height // 2 - hard_text.get_height() // 2))

    # Update the display to show the difficulty menu
    pygame.display.update()

    start_game = False
    while not start_game:
        # Handling user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() # Quit the game if the user closes the window
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # here we get the position of mouse click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Check if the Easy button was clicked
                if easy_button_x <= mouse_x <= easy_button_x + button_width and easy_button_y <= mouse_y <= easy_button_y + button_height:
                    start_game = True
                    difficulty = 15
                    
                # Check if the Medium button was clicked
                elif normal_button_x <= mouse_x <= normal_button_x + button_width and normal_button_y <= mouse_y <= normal_button_y + button_height:
                    start_game = True
                    difficulty = 25
                    
                # Check if the Hard button was clicked
                elif hard_button_x <= mouse_x <= hard_button_x + button_width and hard_button_y <= mouse_y <= hard_button_y + button_height:
                    start_game = True
                    difficulty = 35

        fps_controller.tick(30)
    return difficulty  # Return the selected difficulty

def calculate_distance(point1, point2):
    
    #Calculate the Euclidean distance between two points.
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def create_game(gamemode, difficulty, reward, agent: Agent, training_count, self_collision_count):
    """
    Create and run the game loop for the Snake game.
    
    Parameters:
    - gamemode: The game mode (0 for human player, 1 for AI-driven, etc.)
    - difficulty: The difficulty level affecting the game speed
    - reward: Reward system for the AI agent
    - agent: The AI agent controlling the snake (if applicable)
    - training_count: Counter for the number of training iterations (if applicable)
    - self_collision_count: Counter for self-collisions (if applicable)
    """
    
    # Initialize the snake and grid
    snake = Snake()
    grid = Grid(frame_size_x, frame_size_y)
    agent.snake = snake
    agent.grid = grid
    
    # Value at which a bomb should be spawned
    value_to_spawn_bomb = 5
    is_paused = False
    frame_iteration = 0
    
    # Retrieve high scores
    high_scores = pt.record_keeper_for_user()

    # Gamemode for human player.
    if gamemode == 0:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over() # End the game if the user closes the window
                elif event.type == pygame.KEYDOWN:
                    # Handle key press events
                    snake.change_direction(event)
                    if event.key == pygame.K_p:  # Check if 'P' key is pressed
                        is_paused = True
                        if is_paused:
                            pause_menu()
                            is_paused = False
                if event.type == MUSIC_END:
                     # Restart the playlist when the current song ends
                    start_playlist()
            if is_paused:
                continue

            # Set event for when the music ends
            pygame.mixer.music.set_endevent(MUSIC_END)

            snake.move()# Move the snake

            # Check if the snake has eaten food
            food_eaten = snake.grow(grid.food_pos)
            if food_eaten:
                grid.spawn_food(snake.snake_body)
                grid.increase_score(snake)

            # Get highscore
            highscore = Agent.get_highscore()

            # Update UI
            grid.draw(game_window, snake.snake_body, snake.direction, snake.snake_score, high_scores, highscore)

            # Check for collisions
            if grid.check_collision(snake.snake_pos) or grid.check_self_collision(snake.snake_body):
                pt.save_record(snake.snake_score)
                game_over_menu(snake)
                game_over()
                break

            # Spawn a bomb at certain score thresholds
            if snake.snake_score == value_to_spawn_bomb:
                grid.spawn_bomb(snake.snake_body)
                value_to_spawn_bomb += 5

            # Remove the bomb after a short period
            if snake.snake_score == value_to_spawn_bomb - 2:
                grid.bomb_pos[0], grid.bomb_pos[1] = -1, -1

            # Check if the snake hits the bomb and decrease score
            if snake.shrink(grid.bomb_pos):
                grid.decrease_score(snake)

            # Update the display and control the frame rate
            pygame.display.update()
            fps_controller.tick(difficulty)
    
    # Gamemode for AI training. 
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

            # Get highscore
            highscore = Agent.get_highscore()

            # Update UI
            grid.draw(game_window, snake.snake_body, snake.direction, snake.snake_score, high_scores, highscore)

            # Update reward for collision and end the game if collision happens.
            if grid.check_collision(snake.snake_pos) or frame_iteration > 1000:
                reward += -10
                break

            if grid.check_self_collision(snake.snake_body):
                self_collision_count += 1
                print("Self collision: " + str(self_collision_count))
                reward = -15
                break

            if snake.shrink(grid.bomb_pos):
                grid.decrease_score(snake)
            
            frame_iteration += 1
            pygame.display.update()
            fps_controller.tick(difficulty)

        # Train for collision (since collision breaks the loop and ends the game)
        done = 1
        agent.train(state_current, action, reward, done)
        create_game(gamemode, difficulty, reward, agent, training_count + 1, self_collision_count)

    # Gamemode for AI player.
    if gamemode == 2:
        # Loading the trained model.
        # Model 2 is more improved than Model 1.
        # If desired, models can be changed through the game code.
        agent.model.load_state_dict(torch.load('absolute_model/model2.pth'))
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

            # Get highscore
            highscore = Agent.get_highscore()

            # Update UI
            grid.draw(game_window, snake.snake_body, snake.direction, snake.snake_score, high_scores, highscore)

            # Update reward for collision and end the game if collision happens.
            if grid.check_collision(snake.snake_pos) or grid.check_self_collision(snake.snake_body):
                if snake.snake_score > highscore:
                    Agent.set_highscore(snake.snake_score)
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

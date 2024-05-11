import pygame
import sys
import random
from snake import Snake
from grid import Grid
from pygame import mixer 
  
# Starting the mixer 
mixer.init() 
  
# Loading the song 
mixer.music.load("song.mp3") 
  
# Setting the volume 
mixer.music.set_volume(0.7) 
  
# Start playing the song 
mixer.music.play() 
  

# Window size
frame_size_x = 720
frame_size_y = 480


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

def show_menu():
    button_width = 200
    button_height = 50
    play_button_x = 335
    play_button_y = 250
    aiDriven_button_x = 335
    aiDriven_button_y = 320

    
    background_menu = pygame.image.load("main_menu.png")
    game_window.blit(background_menu, (0,0))
    
    play_button = pygame.image.load("play_button.png")
    aiDriven_button = pygame.image.load("ai_driven.png")
    game_window.blit(play_button, (play_button_x, play_button_y))
    game_window.blit(aiDriven_button, (aiDriven_button_x, aiDriven_button_y))
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
                    difficulty_menu()
                    start_game = True
        fps_controller.tick(30)
        
def game_over_menu(snake):
    
    button_width = 200
    button_height = 50
    score_text_x = 375
    score_text_y = 250
    main_menu_button_x = 335
    main_menu_button_y = 300
    quit_button_x = 335
    quit_button_y = 370
    
    
    
    background_menu = pygame.image.load("game_over_menu.png")
    game_window.blit(background_menu, (0,0))
    
    font = pygame.font.Font('freesansbold.ttf', 30)
    text = font.render("Score: "+ str(snake.snake_score), True, (255, 255, 255))      #str(snake_score)  
    game_window.blit(text, (score_text_x,score_text_y))
    
    main_menu_button = pygame.image.load("main_menu_button.png")
    quit_button = pygame.image.load("quit_button.png")
    
    game_window.blit(text, (score_text_x,score_text_y))
    game_window.blit(main_menu_button, (main_menu_button_x, main_menu_button_y))
    game_window.blit(quit_button, (quit_button_x, quit_button_y))
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
              
def difficulty_menu():
    global difficulty
    
    button_width = 200
    button_height = 50
    easy_button_x = 335
    easy_button_y = 250
    normal_button_x = 335
    normal_button_y = 320
    hard_button_x = 335
    hard_button_y = 390

    
    background_menu = pygame.image.load("difficulty_menu.png")
    game_window.blit(background_menu, (0,0))
    
    easy_button = pygame.image.load("easy_button.png")
    normal_button = pygame.image.load("medium_button.png")
    hard_button = pygame.image.load("hard_button.png")
    game_window.blit(easy_button, (easy_button_x, easy_button_y))
    game_window.blit(normal_button, (normal_button_x, normal_button_y))
    game_window.blit(hard_button, (hard_button_x, hard_button_y))
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

def main():
    show_menu()
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
            grid.increase_score(snake)

        grid.draw(game_window, snake.snake_body, snake.direction,snake.snake_score)

        if grid.check_collision(snake.snake_pos) or grid.check_self_collision(snake.snake_body):
            game_over_menu(snake)
            game_over()

        pygame.display.update()
        fps_controller.tick(difficulty)


if __name__ == "__main__":
    main()

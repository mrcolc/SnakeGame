import torch
import random
import numpy as np
from collections import deque
from snake import Snake, Direction
from grid import Grid
from model import QTrainer, Linear_QNet
from plotter import plot

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self, snake: Snake, grid: Grid):
        self.snake = snake # FOR GATHERING STATE SPACE VARIABLES.
        self.grid = grid # FOR CHECKING COLLISIONS AND FINDING FOOD POS.

        self.n_games = 0 # number of games
        self.epsilon = 0 # controls randomness
        self.gamma = 0 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft() when max length is reached

        self.record = 0
        self.total_score = 0
        self.plot_scores = []
        self.plot_mean_scores = []

        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self):
        head_pos = self.snake.snake_pos
        food_pos = self.grid.food_pos

        dangerzone = self.snake.dangerzone
        head_l = dangerzone[0]
        head_r = dangerzone[1]
        head_u = dangerzone[2]
        head_d = dangerzone[3]

        dir_l = self.snake.direction == Direction.LEFT
        dir_r = self.snake.direction == Direction.RIGHT
        dir_u = self.snake.direction == Direction.UP
        dir_d = self.snake.direction == Direction.DOWN

        state = [
            # Wall straight
            (dir_r and self.grid.check_collision(head_r)) or
            (dir_l and self.grid.check_collision(head_l)) or
            (dir_u and self.grid.check_collision(head_u)) or
            (dir_d and self.grid.check_collision(head_d)),
            
            # Wall right
            (dir_r and self.grid.check_collision(head_d)) or
            (dir_l and self.grid.check_collision(head_u)) or
            (dir_u and self.grid.check_collision(head_r)) or
            (dir_d and self.grid.check_collision(head_l)),

            # Wall left
            (dir_r and self.grid.check_collision(head_u)) or
            (dir_l and self.grid.check_collision(head_d)) or
            (dir_u and self.grid.check_collision(head_l)) or
            (dir_d and self.grid.check_collision(head_r)),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location (TODO: check up and down)
            food_pos[0] < head_pos[0], # Food left
            food_pos[0] > head_pos[0], # Food right
            food_pos[1] < head_pos[1], # Food up
            food_pos[1] > head_pos[1], # Food down

            # TODO: Bomb location
        ]
        
        # Turn true/falses to 0/1s and return.
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # Create sample from 1000 elements out of 100,000.
        else:
            mini_sample = self.memory # Create sample from the whole of memory since it doesn't exceed 1000 yet.

        # Zip every state, actions... etc. from the mini sample into these variables. 
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        # Train over these zipped values.
        self.trainer.train_step(states, actions, rewards, next_states, dones)
    
    def train_short_memory(self, state, action, reward, next_state, done):
        # Train over these singular values.
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # Generating move: Tradeoff between exploration and exploitation.
        # Exploration: Random move
        # Exploitation: Move via model
        self.epsilon = max(50 - self.n_games // 10, 10)  # Adjust epsilon decay rate
        final_move = [0, 0, 0]
        if random.randint(0,100) < self.epsilon:  
            move = random.randint(0,2) # Make random move if random number < epsilon
        else:
            state0 = torch.tensor(state, dtype=torch.float) # Make prediction via model
            prediction = self.model(state0)
            move = torch.argmax(prediction).item() # Turn prediction from Tensor to Int
        final_move[move] = 1
        return final_move
    
    def generate_action(self):
        current_state = self.get_state()
        final_move = self.get_action(current_state)
        return current_state, final_move

    def train(self, state_old, final_move, reward, done):
        score = self.snake.snake_score

        state_next = self.get_state()

        self.train_short_memory(state_old, final_move, reward, state_next, done)
        self.remember(state_old, final_move, reward, state_next, done)

        if done:
            self.n_games += 1
            self.train_long_memory()

            if score > self.record:
                self.record = score
                self.model.save() # TODO: MODEL

            print('Game', self.n_games, 'Score', score, 'Record:', self.record)

            self.plot_scores.append(score)
            self.total_score += score
            mean_score = self.total_score / self.n_games
            self.plot_mean_scores.append(mean_score)
            plot(self.plot_scores, self.plot_mean_scores)
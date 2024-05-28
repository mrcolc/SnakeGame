import torch
import random
import numpy as np
from collections import deque
from snake import Snake, Direction
from grid import Grid

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self, snake, grid):
        self.snake = snake # 
        self.grid = grid #
        self.n_games = 0
        self.epsilon = 0 # controls randomness
        self.gamma = 0 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft() when max length is reached
        # TODO: model, trainer

    def get_state(self):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass
    
    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self):
        pass
    
    def train(self):
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0

        while(True):
            # get old state
            state_old = self.get_state()

            # get move
            final_move = self.get_action(state_old)

            # perform move + get new state
            # TODO: retrieve reward, done, score
            state_new = self.get_state()

            # train short mem
            self.train_short_memory(state_old, final_move, reward, state_new, done)

            # remember
            self.remember(state_old, final_move, reward, state_new, done)

            # if done: # done means game over or reset
                # game.reset()
                # agent.n_games += 1
                # agent.train_long_memory()

            if score > record:
                record = score
                # agent.model.save()

            print('Game', self.n_games, 'Score', score, 'Record:', record)

            # TODO: plot
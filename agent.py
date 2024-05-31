import torch
import random
import numpy as np
from collections import deque
from snake import Snake, Direction
from grid import Grid
from model import QTrainer, Linear_QNet
from plotter import plot

# Constants
MAX_MEMORY = 100000 # Maximum memory size for experience replay
BATCH_SIZE = 1000   # Batch size for training
LR = 0.001          # Learning rate

class Agent:
    def __init__(self, snake: Snake, grid: Grid):
        """
        Initialize the Agent with a snake instance and grid instance.
        Sets up the Q-network, trainer, and various parameters for training.
        """
        self.snake = snake # for finding snake head position, body position direction etc.
        self.grid = grid # for collision checking and food positions.

        # Training parameters
        self.n_games = 0 # number of games
        self.epsilon = 0 # exploration rate (controls random actions)
        self.gamma = 0.9 # discount rate

        # Replay memory to store experiences
        self.memory = deque(maxlen=MAX_MEMORY) # popleft() when max length is reached

        # Statistics for tracking performance
        self.highscore = 0 # highscore of AI player.
        self.record = 0 # record of AI training algorithm.
        self.total_score = 0 # total score gained.

        # Lists to store scores for plotting
        self.plot_scores = [] # array for plotting scores.
        self.plot_mean_scores = [] # array for plotting means of scores.

        # Initialize Deep Q Network (14 input state, 256 hidden state, 3 output action)
        # Input states further explained below in get_state()
        # Output (action) states:
        # Go straight = [1, 0, 0]
        # Turn right  = [0, 1, 0]
        # Turn left   = [0, 0, 1]
        self.model = Linear_QNet(14, 256, 3)
        # Initialize Q Trainer (used in training the AI using LR and gamma values)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    # State retrieval method.
    def get_state(self):
        # Get snake head and food positions.
        head_pos = self.snake.snake_pos
        food_pos = self.grid.food_pos

        # Danger zone: One block away from head in each direction. 
        dangerzone = self.snake.dangerzone
        head_l = dangerzone[0]
        head_r = dangerzone[1]
        head_u = dangerzone[2]
        head_d = dangerzone[3]

        # Boolean direction values.
        dir_l = self.snake.direction == Direction.LEFT
        dir_r = self.snake.direction == Direction.RIGHT
        dir_u = self.snake.direction == Direction.UP
        dir_d = self.snake.direction == Direction.DOWN

        # Check for body parts in front, left, and right of the snake's head
        body_left = self.is_body_part(head_l)
        body_right = self.is_body_part(head_r)
        body_up = self.is_body_part(head_u)
        body_down = self.is_body_part(head_d)

        # State representation (14 inputs):
        # 1. Is there wall in front
        # 2. Is there wall at right
        # 3. Is there wall at left
        # 4. Is there part of body in front
        # 5. Is there part of body at right
        # 6. Is there part of body at left
        # 7. Is the direction left
        # 8. Is the direction right
        # 9. Is the direction up
        # 10. Is the direction down
        # 11. Is there food at left
        # 12. Is there food at right
        # 13. Is there food above
        # 14. Is there food below

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

            # Body straight
            (dir_r and body_right) or
            (dir_l and body_left) or
            (dir_u and body_up) or
            (dir_d and body_down),

            # Body right
            (dir_r and body_down) or
            (dir_l and body_up) or
            (dir_u and body_right) or
            (dir_d and body_left),

            # Body left
            (dir_r and body_up) or
            (dir_l and body_down) or
            (dir_u and body_left) or
            (dir_d and body_right),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location
            food_pos[0] < head_pos[0], # Food left
            food_pos[0] > head_pos[0], # Food right
            food_pos[1] < head_pos[1], # Food up
            food_pos[1] > head_pos[1], # Food down
        ]
        
        # Turn true/falses to 0/1s and return.
        return np.array(state, dtype=int)
    
    # Find if a position holds a part of the snake's body.
    def is_body_part(self, position):
        for part in self.snake.snake_body:
            if part[0] == position[0] and part[1] == position[1]:
                return True
        return False

    # Update memory: Store an experience tuple in memory.
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    # Train on a sample taken from the memory.
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # Create sample from 1000 elements out of 100,000.
        else:
            mini_sample = self.memory # Create sample from the whole of memory since it doesn't exceed 1000 yet.

        # Zip every state, actions... etc. from the mini sample into these variables. 
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        # Train on these zipped values.
        self.trainer.train_step(states, actions, rewards, next_states, dones)
    
    # Train on only the current values.
    def train_short_memory(self, state, action, reward, next_state, done):
        # Train on these singular values.
        self.trainer.train_step(state, action, reward, next_state, done)

    # Find the next action to take.
    def get_action(self, state, mode):
        # Generating move: Tradeoff between exploration and exploitation.
        final_move = [0, 0, 0] # Initialize action vector

        # Epsilon function decides if a random move or a prediction is going to take place.
        self.epsilon = max(40 - self.n_games // 2, 8)

        if random.randint(0,100) < self.epsilon and mode != 1:
            # Exploration: Random move (via epsilon function)
            move = random.randint(0,2) # Make random move if random number < epsilon
        else:
            # Exploitation: Move via model prediction
            # Convert the state array to a PyTorch tensor of type float
            state0 = torch.tensor(state, dtype=torch.float) 
            # Pass the state tensor through the Q-network to get predicted Q-values for each action
            prediction = self.model(state0)
            # Select the action with the highest Q-value (index of the max value) and convert it to an integer
            move = torch.argmax(prediction).item() # Turn prediction from Tensor to Int

        final_move[move] = 1
        return final_move
    
    # Retrieves state and generates action, made for AI trainer.
    def generate_action(self):
        state_current = self.get_state()
        final_move = self.get_action(state_current, 0)
        return state_current, final_move
    
    # Retrieves state and generates action, made for AI player.
    def predict_action(self):
        state_current = self.get_state()
        final_move = self.get_action(state_current, 1)
        return state_current, final_move

    # Function used to train AI on given data.
    def train(self, state_old, final_move, reward, done):
        score = self.snake.snake_score

        # Generate next state.
        state_next = self.get_state()

        # Train the model on the current experience
        self.train_short_memory(state_old, final_move, reward, state_next, done)
        # Store the experience in memory
        self.remember(state_old, final_move, reward, state_next, done)

        # Game over (collision)
        if done:
            self.n_games += 1 # Increment game count
            # Train on a batch of experiences from memory
            self.train_long_memory()

            # Update the record if the current score is higher
            if score > self.record:
                self.record = score
                self.model.save()

            # Print game stats
            print('Game', self.n_games, 'Score', score, 'Record:', self.record)

            # Update plotting data
            self.plot_scores.append(score)
            self.total_score += score
            mean_score = self.total_score / self.n_games
            self.plot_mean_scores.append(mean_score)

            # Plot the scores
            plot(self.plot_scores, self.plot_mean_scores)
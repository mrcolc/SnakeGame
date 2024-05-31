import torch # Main PyTorch library
import torch.nn as nn # Submodule for building neural networks
import torch.optim as optim # Submodule for optimization algorithms
import torch.nn.functional as F # Functional module containing activation functions
import numpy as np
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        """
        Initialize the linear layers for the Q-network.
            input_size (int): Number of input features.
            hidden_size (int): Number of neurons in the hidden layer.
            output_size (int): Number of output actions.
        """
        # Call the constructor of the parent class (nn.Module)
        super().__init__()
        # Define the first linear layer (input to hidden)
        self.linear1 = nn.Linear(input_size, hidden_size)
        # Define the second linear layer (hidden to output)
        self.linear2 = nn.Linear(hidden_size, output_size)

    # Forward pass defines how data flows through the network.
    # Define the forward pass through the network.
    def forward(self, tensor):
        # Apply ReLU activation to the first layer
        tensor = F.relu(self.linear1(tensor))
        # Apply the second linear layer
        tensor = self.linear2(tensor) 
        return tensor

    # Save the model parameters to a file.
    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        # Save the state dictionary (the model parameters)
        torch.save(self.state_dict(), file_name)

class QTrainer:
    def __init__(self, model, lr, gamma):
        """
        Initialize the Q-learning trainer with the model, learning rate, and discount rate.
            model (nn.Module): The Q-network model.
            lr (float): Learning rate.
            gamma (float): Discount rate.
        """
        self.lr = lr
        self.gamma = gamma
        self.model = model

        # Adam optimizer for updating model parameters
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        # Mean squared error loss function
        self.criterion = nn.MSELoss()

    # Perform a single training step.
    def train_step(self, state, action, reward, next_state, done):
        # Convert states, actions, rewards to numpy arrays (speeds the general process up)
        state = np.array(state, dtype=np.float32)
        next_state = np.array(next_state, dtype=np.float32)
        action = np.array(action, dtype=np.int64)
        reward = np.array(reward, dtype=np.float32)
        
        # Convert states, actions, rewards to tensors
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        # If the state is one-dimensional, add a batch dimension
        # Happens because of train_short_memory() function
        '''
        EXAMPLE:
        >>> x = torch.tensor([1, 2, 3, 4])
        >>> torch.unsqueeze(x, 0)
        tensor([[ 1,  2,  3,  4]])
        '''
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0) # Add a batch dimension
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, ) # Convert into tuple

        # Predict Q values for the current state
        pred = self.model(state)

        # Clone the predicted Q values to update them
        target = pred.clone()

        # Update the target Q values using the Bellman equation
        for idx in range(len(done)): # Every other variable has the same size as done
            Q_new = reward[idx]
            if not done[idx]: # If the episode is not done, calculate future reward
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            # Update the target value for the action taken
            target[idx][torch.argmax(action[idx]).item()] = Q_new
    
        # Perform backpropagation: a supervised learning technique for adjusting the weights of 
        # the network to minimize the difference between the actual output and the desired output.
        self.optimizer.zero_grad() # Clears previous gradients to avoid accumulation
        loss = self.criterion(target, pred) # Calculate the loss between target Q-values and predicted Q-values.
        loss.backward() # Backward pass, compute gradients of the loss with respect to the model parameters.

        # Update model parameters based on the computed gradients.
        self.optimizer.step()
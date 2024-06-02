# Snake Game with an AI Implementation

  

## Description

  

Traditional Snake Game, improved with different gameplay mechanics and implemented AI-driven gameplay.

  

## Features

- The game was created with Pyhton Programming Language
	- Modules that used:
		- Pygame
		- Pytorch
		- Matplotlib
  		- IPython	
- The game provides:

	- Hand drawn pixel images.
	- Game interface and menu mechanism.
	- User playable and AI driven snake game.
	- Easy, Medium, Hard Difficulity Modes
	- Improvements to the traditional snake game such as bombs and randomly generated walls.
	- Snake and Score Mechanism:
		- Gain score and body length when the food is eaten.
		- Lose two scores and body length when the bomb is eaten.
		- Game over when snake hits randomly generated walls or outer walls.
	- Highscores table that holds top three records for users and top record for the AI.
	- AI training mode that updates the model that snake AI uses.
## Structure
The game overlayed on two parts:
- Game :
	- Implemented mainly using "Pygame"
	- Based on two classes named "Snake" and "Grid"
		- Snake class represents snake on the grid, it defines the position, direction and danger zone of the snake. It contains method such as move, grow, shrink, predict direction that essential for the snake mechanism.
		- Grid class is the window of the game. It randomly generates food,bomb and wall positions, draws the grid based on the positions. Checks the collision condition also updates the score.
- AI Training (Deep Q Network):
	- Using the agent, states are retrieved and actions are generated. Then the agent memory is updated with these values. Creating a sample from this memory with a given batch size, tuples of values are passed to the trainer.
	- Trainer generates Q-values and updates them, applies back propogation and updates the model with the generated parameters.
	- The model has two neural network layers, first from input (14) to hidden (256), and the second from hidden (256) to output (3), which holds the action values. These layers are analyzed and are used in Q-value generation.
## Installation
Modules Installation
```
pip install pygame
```
```
pip3 install torch torchvision torchaudio
```
```
pip  install matplotlib
```
```
pip install numpy
```
```
pip install IPython
```
## Usage
-	To run:
	-	```python main.py```
## Images
#### Image from Main Menu
**![](https://lh7-us.googleusercontent.com/docsz/AD_4nXfPY7i3aZXk6U7ZyoEnpkBHPaLGk3QCbM0sbPC7H9EBzxMerc3btQMbcHXTg-2btZkoRTtrCyI7Fgvy3eG1IOID7v2wjyVfdNZE-bC3vXDR5JaYGqPXo3xgomrVT6wbZJ5X08HK8q2WT7UlPU6_-aUgftt8?key=8D3uRCI5f_v7oXPvCjKmRA)**
#### Image from Difficulty Selection Menu
**![](https://lh7-us.googleusercontent.com/docsz/AD_4nXePrmWr2It5ZMz0JliZF8BZ7IreBCCXo0XK0u6DSXi_YKlklICf3cD5eaRnieB1KIFPreAyX4zZ3jvCjuBkxw-0XVAKvYEMXXVshR3-xB8k6Vv-4tbYycAE-eYijBeCXYbaLmTn2aHMgnRnE1JMoEOxlmM2?key=8D3uRCI5f_v7oXPvCjKmRA)**
#### Image from Gameplay
**![](https://lh7-us.googleusercontent.com/docsz/AD_4nXdP7pcuiUjTJrQ_N4uJzh9SXSjtF1p11N-5RcvoVYW2LR5OyWfXwO2G2Q2c8iJfi-o3ir7i9L4tqRZ9Wv5sfSy9CJhJkQaJ-g-tIr8wgmkAEHYP91QkDU8zUrayiUoJS66PTwrcw3LC9z6AyZ6xh--JhSPz?key=8D3uRCI5f_v7oXPvCjKmRA)**
#### Image from Game Over Menu
**![](https://lh7-us.googleusercontent.com/docsz/AD_4nXeOrMkhePeAjYc7rBdJvcg3knjqDA_nYH_CnSGu03BdShO7hG591-Uu7RyBnglwsKmSKMcSAKVH1_DC5VTxQoPzy54Fo_jHsebL0g_9svXKtx3LR3xBlqHbGLLhSnl2uymDLlEFXqwwUlIG30R8xLYUYP8i?key=8D3uRCI5f_v7oXPvCjKmRA)**
#### Image from Pause Menu
**![](https://lh7-us.googleusercontent.com/docsz/AD_4nXcmhvEs73wB30qfE-8cQY2mqUfOTfbrxDXsqlXgs3jOxBrp7jQTK5_LQrWv-SWELUcuhwc_MaONMBNe0CcPjmnPwcbbv9VV2IH2L3jCU0WjwP-jZZ8XXOZQgDTH30-xia6loQgBFvOmqN1XPqVcCXPJLD5J?key=8D3uRCI5f_v7oXPvCjKmRA)**
#### Image from AI Driven Gameplay
**![](https://lh7-us.googleusercontent.com/docsz/AD_4nXcp3pQ5kB_Cgljz3znX8LmYbZKz_epZw0_ZfXJv6dnCsvzkNtQTuG6p7IAw4PvNO4hTxoSP-Ry_EqdF0rF2FoSWFjxm5mhB-x6OLcPVmd9u4AxjYxqAVhBJsv2Kt-Vea3hlEcVMWY2bEziAybiaOYs0iMgt?key=8D3uRCI5f_v7oXPvCjKmRA)**
#### Image from AI Training
**![](https://lh7-us.googleusercontent.com/docsz/AD_4nXczEQKSoFGB6B6hNALYZQ4Jo287_Rcd6J9Xc9ZfgNPRpCIJ_D4ACTtOXgVt28VIjNJJzbY325BvJAijJ_qH5qRITMbIHppfUk5cu7a4hEeqrD4GADrbHEkwEos9vk_O3Rzd39jThuumGiY6MPDIA3Ix3d7V?key=8D3uRCI5f_v7oXPvCjKmRA)**

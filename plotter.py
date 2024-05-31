import matplotlib.pyplot as plt
from IPython import display
import os

# Turns the interactive mode on in Matplotlib, allows for real-time updates
plt.ion()

# Plots the graph using Matplotlib and IPython
def plot(scores, mean_scores):
    display.clear_output(wait=True) # Clears the output in the Jupyter notebook
    display.display(plt.gcf())  # Displays the currently active plot
    plt.clf()   #Removes the elements from the current figure
    plt.title('Training...')    # Sets a title for the plot
    # Sets the labels for the axes
    plt.xlabel('Number of Games')
    plt.ylabel('Score')

    plt.plot(scores)    # Adds the scores variable to the plot
    plt.plot(mean_scores)   # Adds the mean_scores variable to the plot
    plt.ylim(ymin=0)    # Makes sure the bottom of the plot is over 0
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))    # Shows the last score on top of the plot
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1])) # Shows the last mean score on top of the plot
    plt.show(block=False)   # Helps the code run while the plot is visible
    plt.pause(.1)   # Gives the plot enough time to update and show the changes

def load_records():
    filename = "high_scores.txt"    # Assigns the txt file to a variable
    if os.path.exists(filename):    # Checks if file exists
        # Opens and reads the file
        with open(filename, "r") as file:
            return [int(score.strip()) for score in file.readlines()]   # Returns the list of high scores
    else:
        with open(filename, "w") as file:
            for x in range(2):
                file.write(f"0\n")      # Writes '0' to the scores as default if file does not exist
            file.write("0")
            return [0, 0, 0]

def save_record(score):
    filename = "high_scores.txt"    # Assigns the txt file to a variable
    record_list = record_keeper_for_user()  # Loads the high scores
    add_score = False
    for record in record_list:
        if score > record:  # Checks if the current score is higher than record
            add_score = True
    if add_score:
        # Appends the high score to the txt file
        with open(filename, "a") as file:
            file.write(f"\n{score}")

def record_keeper_for_user():
    record_list = load_records()    # Loads the high scores into a list
    record_list.sort(reverse=True)  # Sorts the scores in reverse order
    return record_list[:3]  # Returns the highest 3 scores
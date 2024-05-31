import matplotlib.pyplot as plt
from IPython import display
import os

plt.ion()

def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)

def load_records():
    filename = "high_scores.txt"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return [int(score.strip()) for score in file.readlines()]
    else:
        with open(filename, "w") as file:
            for x in range(2):
                file.write(f"0\n")
            file.write("0")
            return [0, 0, 0]

def save_record(score):
    filename = "high_scores.txt"
    record_list = record_keeper_for_user()
    add_score = False
    for record in record_list:
        if score > record:
            add_score = True
    if add_score:
        with open(filename, "a") as file:
            file.write(f"\n{score}")

def record_keeper_for_user():
    record_list = load_records()
    record_list.sort(reverse=True)
    return record_list[:3]
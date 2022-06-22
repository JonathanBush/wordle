from wordle_solver import WordleSolver
from matplotlib import pyplot as plt

wordlist = []
with open("valid-wordle-words.txt") as file:
    for line in file:
        wordlist.append(line.strip())


def get_wordle_update(truth, guess):
    update = ""
    assert len(truth) == len(guess)
    for index in range(len(truth)):
        if truth[index] == guess[index]:
            update += guess[index].upper()
        elif guess[index] in truth:
            update += guess[index].lower()
        else:
            update += "."
    return update

tries = []
for truth in wordlist:
    print("Truth:", truth)
    solver = WordleSolver()
    try_count = 0
    while not solver.solved:
        guess, score = solver.get_best_word()
        print(guess, score)
        new_info = get_wordle_update(truth, guess)
        print("Update:", new_info)
        solver.update_belief(guess, new_info)
        try_count += 1
    tries.append(try_count)
    print("Solved '{}' in {} tries".format(truth, try_count))
    plt.clf()
    plt.hist(tries, bins=[1,2,3,4,5,6,7,8,9,10])
    plt.draw()
    plt.pause(0.001)
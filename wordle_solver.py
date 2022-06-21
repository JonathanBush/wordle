import numpy as np

###
# Greedy Wordle solver based on letter frequency
# Jonathan Bush, 2022
#
# input:
#   . = not in word (gray)
#   a = in word but not in position (yellow)
#   A = in word and in position (green)
###


def letter2num(letter):
    return ord(letter) - ord('a')


class WordleSolver:

    def __init__(self):
        self.alphabet = list("abcdefghijklmnopqrstuvwxyz")
        self.words = []
        self.solved = False
        with open("valid-wordle-words.txt") as file:
            for line in file:
                self.words.append(line.strip())
        self.letter_values = {}
        self.word_values = {}
        self.update_letter_values()
        self.update_word_values()

        self.known_letters = [None, None, None, None, None]
        self.contained_letters = []
        self.position_eliminated_letters = [[], [], [], [], []]

    def update_letter_values(self):
        letter_count = np.zeros(len(self.alphabet))
        for word in self.words:
            for letter in word:
                letter_count[letter2num(letter)] += 1

        letter_freq = letter_count / sum(letter_count)
        self.letter_values = {}

        for index in range(len(self.alphabet)):
            self.letter_values[self.alphabet[index]] = letter_freq[index]

    def update_word_values(self):
        self.word_values = {}
        for word in self.words:
            word_score = 0
            used_letters = []
            for letter in word:
                if letter not in used_letters:
                    word_score += self.letter_values[letter]
                    used_letters.append(letter)
            self.word_values[word] = word_score
        print(len(self.words), "words")

    def get_best_word(self):
        best_word = None
        best_word_score = 0
        for word, score in self.word_values.items():
            if score > best_word_score:
                best_word = word
                best_word_score = score
        return best_word, best_word_score

    def eliminate_letters(self, bad_letters):
        for letter in bad_letters:
            self.alphabet.remove(letter)

    def eliminate_words(self):
        removed_words = []
        for word in self.words:
            letters_not_contained = len(word)
            for index in range(len(word)):
                letter = word[index]
                if letter not in self.alphabet:
                    removed_words.append(word)  # contains a letter that was eliminated
                    break
                if self.known_letters[index] is not None and self.known_letters[index] != letter:
                    removed_words.append(word)  # different letter in the position of a known letter
                    break
                if letter in self.position_eliminated_letters[index]:
                    removed_words.append(word)  # letter in a position where it is known to not be
                    break
                if len(self.contained_letters) and letter in self.contained_letters:
                    letters_not_contained -= 1
            if len(self.contained_letters) and letters_not_contained == len(word):
                removed_words.append(word)
        for word in removed_words:
            if word in self.words:
                self.words.remove(word)

    def update_belief(self, previous_word, new_information):
        removed_letters = []
        self.words.remove(previous_word)
        for index in range(len(previous_word)):
            info = new_information[index]
            if info == ".":
                removed_letters.append(previous_word[index])
            if info.islower():
                print("position eliminated", (info, index))
                self.position_eliminated_letters[index].append(info)
                self.contained_letters.append(info)
            if info.isupper():
                self.known_letters[index] = info.lower()
        self.eliminate_letters(removed_letters)
        print(self.alphabet)
        self.eliminate_words()
        self.update_word_values()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    solver = WordleSolver()

    while not solver.solved:
        word, score = solver.get_best_word()
        print(word, score)
        new_info = input("Update: ")
        solver.update_belief(word, new_info)



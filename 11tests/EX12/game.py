# # # # # # #  EX12 # # # # # # # # # # # # # #
# ID        : 316138007         && 313471153  #
# NAME      : Michael Sichenko  && Or Katz    #
# LOGIN     : m_sich            && orkatz     #
# COMMENTS  : Isn't it the best game ever?    #
# # # # # # # # # # # # # # # # # # # # # # # #

import boggle_board_randomizer
from Cube import *
from GUI import *

FILENAME        = 'boggle_dict.txt'   # dictionary
MATRIX_SIZE     = 4                   # game matrix size
INITIAL_SCORE   = 0                   # player starting score
GAME_TIME       = 3                   # game length (in minutes)


class Game:
    """ Game object (manager) of the game HUJI Boggle! """
    def __init__(self):
        self.matrix = boggle_board_randomizer.randomize_board()
        self.score = INITIAL_SCORE
        self.all_words = {}
        self.set_all_words()

        self.correct_words = []
        self.old_location = []
        self.potential_new_location = []
        self.letters_list = []
        self.visited_cubes = []

    def get_score(self):
        """ returns the current score of the player """
        return self.score

    def was_word_checked(self, word):
        """ returns True if word appears in previous found words list """
        if word in self.correct_words:
            return True
        return False

    def is_word_in_dict(self, word):
        """ Checks if given word is in the word dictionary """
        word = word.upper()
        try:
            if word[0] in self.all_words.keys():
                if word in self.all_words[word[0]]:
                    return True
            return False
        except IndexError:
            return False

    def check_potential_position(self, location):
        """ returns True if move is valid, false otherwise """
        if location in self.visited_cubes:
            return False
        self.potential_new_location = location
        return self.create_word()

    def create_word(self):
        """ Checks user's selection and appends letter to letter list """
        if self.check_letter():
            new_letter = self.matrix[self.potential_new_location[0]][self.potential_new_location[1]]
            self.letters_list.append(new_letter)
            self.old_location = self.potential_new_location
            self.visited_cubes.append(self.potential_new_location)
            return True
        return False

    def check_letter(self):
        """ Checks if selected letter is valid according to rules"""
        # case first letter
        if not self.old_location:
            return True
        elif self.check_neighbours():
            return True
        return False

    def check_neighbours(self):
        """ Returns true if the location of the cube is close to old location"""
        if self.old_location[0] in range(self.potential_new_location[0] - 1,
                                         self.potential_new_location[0] + 2):
            if self.old_location[1] in range(self.potential_new_location[1] - 1,
                                             self.potential_new_location[1] + 2):
                return True
        return False

    def letters_to_cubes(self):
        """ Converts the letters matrix into cubes matrix"""
        matrix = []
        for row in self.matrix:
            cubes_row = []
            for letter in row:
                cube = Cube.Cube(letter)
                cubes_row.append(cube)
            matrix.append(cubes_row)
        return matrix

    def check_word(self, gui):
        """ creates word from current letters and checks it for scoring"""
        word = ''.join(self.letters_list)

        # check if word already found
        if not self.was_word_checked(word):
            # check if word from dict
            if self.is_word_in_dict(word):
                self.correct_words.append(word)
                self.update_score(word, gui)
                gui.add_word_to_box(word + '\n')
        self.reset_variables()

    def reset_variables(self):
        """ resets locations on board after word completion"""
        self.old_location.clear()
        self.potential_new_location.clear()
        self.visited_cubes.clear()
        self.letters_list.clear()

    def reset_game(self):
        """ called at the end of a game to reset the game """
        self.reset_variables()
        self.score = INITIAL_SCORE
        self.correct_words.clear()
        self.matrix = boggle_board_randomizer.randomize_board()
        cube_matrix = self.letters_to_cubes()
        return cube_matrix

    def update_score(self, word, gui):
        """Updates the player's score and sets it accordingly"""
        length = len(word)
        self.score += length ** 2
        gui.set_score(str(self.score))


    def set_all_words(self):
        """reads the dict file and creates a list of lists of chars for the game"""
        file = open(FILENAME, 'r')
        words_dict = {}
        for word in file:
            word = word.replace('\n', '')
            if word[0] not in words_dict:
                words_dict[word[0]] = [word]
            else:
                words_dict[word[0]].append(word)
        self.all_words = words_dict


if __name__ == '__main__':
    game = Game()
    matrix = game.letters_to_cubes()
    gui = Graphics(matrix, game)


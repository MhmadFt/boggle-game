#################################################################
# FILE : game.py
# WRITER : mohammad,ahmad , mohammad.ftemi,ahmad.ftemi , 213620115,213621279
# EXERCISE : intro2cse ex11 2023
# DESCRIPTION: A program that contains a code to the boggle game
# STUDENTS I DISCUSSED THE EXERCISE WITH: ahmad.ftemi.
# WEB PAGES I USED: www.stackoverflow.com/www.w3schools.com
# NOTES: ...
#################################################################
import tkinter as tk
from boggle_board_randomizer import *
import ex11_utils
from tkinter import messagebox

font_tuple = ("Comic Sans MS", 15, "bold")# Define a font style for labels and buttons


class GameWindow:
    """this class represents the main game window"""
    def __init__(self, root):

        # Initialize game state variables
        self.words = set()
        self.words = self.build_word_lst()
        self.root = root
        self.root.configure(bg="gray")
        self.root.title("Boggle Game")

        # Create game board canvas
        self.game_board = tk.Canvas(root, width=400, height=400, background="gray")
        self.game_board.pack()

        # Create Submit button
        self.submit_button = tk.Button(root, text="Submit", cursor='hand1', border=5, command=self.submit_word,
                                       font=font_tuple)
        self.submit_button.pack()

        # Create Score label
        self.score_label = tk.Label(root, text="Score: 0", font=font_tuple, background="gray")
        self.score_label.pack()

        # Initialize letters grid and labels
        self.letters_labels = []
        self.randomize_board()

        # Create Found Words label and listbox
        self.found_words_label = tk.Label(root, text="Found Words:", font=font_tuple, background="gray")
        self.found_words_label.pack()
        self.found_words_list = tk.Listbox(root, font=font_tuple)
        self.found_words_list.pack()
        # Create label for the typed word
        self.typed_word_label = tk.Label(root, text="", font=font_tuple, background='gray')
        self.typed_word_label.pack()

        # Initialize game parameters
        self.letters_board = []
        self.letters_row = []
        self.path = []

        self.build_game()

    def build_word_lst(self):
        """here it reads the words file and put the words in a set"""
        words = set()
        # Open the "boggle_dict.txt" file for reading
        with open("boggle_dict.txt", "r") as file:
            for line in file:
                word = line.strip()
                words.add(word)
        return words


    def game_over(self):
        """this function runs when the player lose the game and ask
                him if he wants to play again"""
        msg_str = f"Game over! you've scored {self.score} points " \
                  f"Press 'yes'! to try again"
        msg_box = messagebox.askquestion("Oh.. come on!", msg_str,
                                         icon='warning')
        if msg_box == 'yes':
            self.new_game()
        else:
            self.root.destroy()

    def update_timer(self):
        """this function presents the timer in label and update it"""
        sec = self.timer % 60
        mins = int(self.timer / 60) % 60
        self.timer_label.config(text=f"Time : {mins:02}:{sec:02}", background="gray")

    def submit_word(self):
        """this function runs when the player press the submit button"""
        word = self.typed_word_label.cget("text").strip()# Get the typed word from the label
        if self.is_valid_word(self.path) is not None:#Check if the word is valid
            self.words.remove(word) #Remove the word from the list of available words
            self.found_words_list.insert(tk.END, word)#Add the word to the found words list
            self.score += self.calculate_score(self.path)#updating the score
            self.score_label.config(text=f"Score: {self.score}")

        # Reset the typed word label and path
        self.typed_word_label.config(text="")
        self.path = []

    def calculate_score(self,path):
        """this function calculate the score"""
        return len(path) ** 2
    def build_game(self):
        # Initialize game variables
        self.timer = 10# Initial timer value in seconds
        self.score = 0
        self.timer_label = tk.Label(self.root, font=font_tuple)
        self.update_timer()
        self.timer_label.pack()
        self.found_words_list.delete(0, tk.END)
        self.update_timer()
        self.randomize_board()
        self.draw_board()
        self.root.after(1000, self.start_timer)

    def update_typed_word(self, text, i, j):
        # Update the typed word label and path
        current_typed_word = self.typed_word_label.cget("text")
        new_typed_word = current_typed_word + text
        self.typed_word_label.config(text=new_typed_word)
        self.path.append((i, j)) # Add the selected letter's coordinates to the path

    def is_valid_word(self, cords):
        """this function check if the current path forms a valid word"""
        return ex11_utils.is_valid_path(self.board, cords, self.words)

    def new_game(self):
        """this function reset the game and destroy the GUI elements"""
        if hasattr(self, 'timer_id'):  # Check if the timer_id attribute exists
            self.root.after_cancel(self.timer_id)  # Cancel the timer

        # Destroy various GUI elements
        self.game_board.destroy()
        self.typed_word_label.destroy()
        self.timer_label.destroy()
        self.score_label.destroy()
        self.found_words_label.destroy()
        self.root.destroy()
        self.main()#starting a new game

    def randomize_board(self):
        """this function shuffle the letters on the game board to create a random board"""
        random.shuffle(LETTERS)
        for i in range(BOARD_SIZE):
            random.shuffle(LETTERS[i])
        self.board = [row[:] for row in LETTERS[:BOARD_SIZE]]# Create a copy of the randomized board

    def max_score(self):
        """this function calculate the maximum achievable score based on all possible valid words"""
        max = 0
        all_words = ex11_utils.max_score_paths(self.board, self.words)
        for i in range(len(all_words)):
            max += len(all_words[i]) ** 2
        return max

    def draw_board(self):
        """this function draw the game board with letter buttons"""
        self.game_board.delete(tk.ALL)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                letter = self.board[i][j]

                # Create a button for each letter on the board
                self.letters_row.append(self.board[i][j])
                button = tk.Button(
                    self.game_board,
                    text=letter,
                    font=font_tuple,
                    command=lambda txt=letter, i=i, j=j: self.update_typed_word(txt, i, j),
                    height=1,
                    width=5,
                    border=0,
                    cursor='hand1',
                    highlightcolor='WHITE',
                    activebackground="#020f12"
                )
                button.grid(row=i, column=j, padx=10, pady=10)
                self.letters_labels.append(button)
            self.letters_board.append(self.letters_row)

    def start_timer(self):
        """this function start the game timer countdown"""
        if self.timer > 0:
            self.timer -= 1
            self.update_timer()
            self.root.after(1000, self.start_timer)# Continue the timer countdown
        else:
            self.game_over()#Call the game over method when the timer reaches 0

    def main(self):
        """this function create a tkinter window and start the game"""
        root = tk.Tk()
        GameWindow(root)
        root.mainloop()

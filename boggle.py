#################################################################
# FILE : boggle.py
# WRITER : mohammad,ahmad , mohammad.ftemi,ahmad.ftemi , 213620115,213621279
# EXERCISE : intro2cse ex11 2023
# DESCRIPTION: A program that contains a code to the boggle game
# STUDENTS I DISCUSSED THE EXERCISE WITH: ahmad.ftemi.
# WEB PAGES I USED: www.stackoverflow.com/www.w3schools.com
# NOTES: ...
#################################################################
import game
import tkinter as tk
from PIL import ImageTk
from tkinter import messagebox


class BoggleGame:
    """This is the main class that represent the Boggle game."""
    def __init__(self):
        """This is the constructor method that initializes the game,It creates a tkinter main window (self.root),
        sets the window title, dimensions, and creates a canvas for displaying an image."""
        self.root = tk.Tk()
        self.root.title("Boggle Game")
        self.root.geometry("420x250")
        # Create a canvas and display a logo on it.
        canvas = tk.Canvas(width=420, height=250)
        canvas.pack()
        logo = ImageTk.PhotoImage(file=r"C:\Users\MohammedF\OneDrive\Desktop\ex11\OIP.jpeg")
        canvas.create_image(0, 0, image=logo, anchor='nw')

        # Create a "Start!" button to begin the game.
        start_btn = tk.Button(self.root, text='Start!', height=2, width=10, command=self.start_game, background='green',
                              cursor='hand1')
        start_btn.pack()
        start_btn.place(relx=.5, rely=.5, anchor="center")

        # Create a "Quit!" button to exit the game.
        quit_btn = tk.Button(self.root, text='Quit!', height=2, width=10, command=self.quit_mass, background='red',
                             cursor='hand1')
        quit_btn.pack()
        quit_btn.place(relx=.5, rely=.7, anchor="center")

        self.root.mainloop()
    def start_game(self):
        """Starting the Boggle game """
        messagebox.showinfo("Let's Go !", "The game will start now you have 3 minutes\n Enjoy !")
        self.root.destroy()  # Close the intro window
        game.GameWindow.main(self.root) #opinning the game window (starting the game)

    def quit_mass(self):
        """Quit the game with a confirmation dialog."""
        msg_str = "Do you want to quit the game ? "
        msg_box = messagebox.askquestion("Oh.. come on!", msg_str,
                                         icon='warning')
        if msg_box == 'yes':
            self.root.destroy()#exit the game if he choose yes


if __name__ == "__main__":
    BoggleGame()

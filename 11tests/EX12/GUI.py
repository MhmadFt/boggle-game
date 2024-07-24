from tkinter import *
from tkinter import messagebox
import Cube
import boggle
import time

# window properties
WIDTH       = 685      # window width in pixels
HEIGHT      = 500      # window height in pixels

# font settings
H1_FONT     = ("arial", 16, "bold")
BUTTON_FONT = ("comic sans ms", 14, "bold")
MAIN_FONT   = ("comic sans ms", 12, "bold")
CUBE_FONT   = ("david", 36, "bold")
TXT_BOX_FONT= ("david", 13)

# images
LOGO        = "logo.png"

# styles
BTN_WIDTH   = 30
BTN_HEIGHT  = 1
BG_COLOR = "#142752"

class Graphics:
    """GUI of game buggle"""
    def __init__(self, letters, manager):
        self.__manager = manager
        self.__letters = letters
        self.__root = self.init_main_window()
        self.frames = {}

        # game elements
        self.__game_cubes = []    # all cubes of game
        self.__elements = {
            "canvas"    : "",
            "textbox"   : "",
            "time"      : "",
            "score"     : "",
            "pics"      : []
        }

        # create frames
        self.create_game_frame()
        self.create_main_frame()

        self.__curr_time = boggle.GAME_TIME*60
        self.__root.mainloop()

    def init_main_window(self):
        """ Creates and returns instance of Tk"""
        gui_main = Tk()
        gui_main.geometry(f"{WIDTH}x{HEIGHT}")
        gui_main.resizable(width=False, height=False)
        gui_main.title("HUJI Boggle!")
        gui_main.configure(background=BG_COLOR)
        return gui_main

    def create_main_frame(self):
        main_frame = Frame(self.__root)
        self.frames["main"] = main_frame

        # logo
        logo_img = PhotoImage(file=LOGO)
        logo = Label(main_frame, image=logo_img)
        logo.image = logo_img

        # labels
        main_menu_instruction = Label(main_frame, pady=25,
                                  text="Welcome!\nPress 'start!' to get your daily dose of boggle",
                                  font=H1_FONT)
        # buttons
        start_button = Button(main_frame, text="Start!", pady=15,
                              height=BTN_HEIGHT, width=BTN_WIDTH,
                              bg="green", fg="white", relief="solid",
                              font=BUTTON_FONT,
                              command=self.__on_start_click_event)
        start_button.flash()
        quit_button = Button(main_frame, text="Quit!", pady=15,
                             height=BTN_HEIGHT, width=BTN_WIDTH,
                             bg="dark red", fg="white", relief="solid",
                             font=BUTTON_FONT,
                             command=self.__on_quit_click_event)

        space1 = Label(main_frame, text="")
        space2 = Label(main_frame, text="")

        # pack all objects
        main_frame.grid(row=0, column=0, rowspan=50 ,sticky='news', ipadx=100)
        space1.pack()
        logo.pack()
        main_menu_instruction.pack()
        start_button.pack()
        space2.pack()
        quit_button.pack()

    def create_game_frame(self):
        """Creates the frame of the game"""

        debug_style = {"highlightbackground":"black",
                    "highlightcolor":"black",
                    "highlightthickness":1,
                    "bd": 0}

        game_frame = Frame(self.__root, **debug_style)
        self.frames["game"] = game_frame
        left_frame = Frame(game_frame, **debug_style)
        self.frames["left frame"] = left_frame
        right_frame = Frame(game_frame, **debug_style)

        # board
        self.__create_game_board(left_frame)

        # time
        time_frame = Frame(right_frame, **debug_style,)
        time_label = Label(time_frame, text="00:00", font=MAIN_FONT)
        self.__elements["time"] = time_label

        # score
        score_frame = Frame(right_frame, **debug_style)
        score_label = Label(score_frame, text="Score:\t0", font=MAIN_FONT)
        self.__elements["score"] = score_label

        # textbox
        words_frame = Frame(right_frame, **debug_style)
        words_box   = Text(words_frame, state="disabled", cursor="pirate",
                           relief="groove", bg='light grey', spacing1=10,
                           width=20, height=14, padx=10, font=TXT_BOX_FONT)
        self.__elements["textbox"] = words_box

        # quit button
        quit_button = Button(right_frame, text="Quit",
                             bg="dark red", fg="white", relief="solid",
                             font=BUTTON_FONT,
                             command=self.__on_quit_click_event)

        # packing objects
        game_frame.grid(row=0, column=0, rowspan=3, sticky='news')
        left_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nse')
        right_frame.grid(row=0, column=2, padx=10, pady=10, sticky='nsw')
        time_frame.pack(fill=X)
        time_label.pack()
        score_frame.pack(fill=X)
        score_label.pack(side=LEFT)
        words_frame.pack(fill=Y)
        words_box.pack()
        quit_button.pack(fill=X)

    def __create_game_board(self, frame):
        """ Creates a canvas with cubes in the given frame """
        # create image objects for canvas
        bg_img = self.__letters[0][0].get_background()
        img = PhotoImage(file=bg_img)

        # create a canvas
        canvas = Canvas(frame, height=475, width=450, bg="dark blue")
        canvas.config(scrollregion=canvas.bbox(ALL))

        # fill cubes ( pic + letter )
        for row in range(len(self.__letters)):
            curr_letters = self.__letters[row]
            for col in range(len(curr_letters)):
                pos_x = row*115+65
                pos_y = col*110+62

                # create cube
                image = canvas.create_image(pos_y, pos_x, image=img)
                canvas.image = img  # reference to img(tk garbage collector)
                cube_letter = canvas.create_text(pos_y, pos_x,
                                                 font=CUBE_FONT,
                                                 text=curr_letters[col].get_letter())
                self.__game_cubes.append(image)

                # bind to event handler - mouse one
                canvas.tag_bind(image, '<ButtonPress-1>',
                                lambda event, arg=image:
                                self.__on_cube_click_event(event, arg))
                canvas.tag_bind(cube_letter, '<ButtonPress-1>',
                                lambda event,
                                arg=image: self.__on_cube_click_event(event, arg))

                # bind to event - finished word
                canvas.tag_bind(image, '<ButtonPress-3>',
                                lambda event, arg=image:
                                self.__on_finished_word_event(event, arg))
                canvas.tag_bind(cube_letter, '<ButtonPress-3>',
                                lambda event,
                                arg=image: self.__on_finished_word_event(event, arg))

        self.__elements["canvas"] = canvas
        canvas.pack()

    # region EVENTS
    def __on_start_click_event(self):
        """Event handler for start button click - raises game frame"""
        self.frames["game"].tkraise()
        self.__update_time()

        instructions = "Welcome!\nLeft click to select a letter,\n" \
                       "Right click on a cube to finish word\nGood luck!"
        self.show_message(instructions)


    def __on_quit_click_event(self):
        """Event handler for quit button click - closes window"""
        msg_str = "If you quit now, your'e a loser!"
        msg_box = messagebox.askokcancel("Oh.. Please don't!", msg_str,
                                         icon='warning')

        if msg_box:
            self.__root.destroy()

    def __on_cube_click_event(self, event, index):
        """Changes status and bg pic of clicked item"""
        index_row = index // 8
        index_col = ((index - 8*index_row) - 1) // 2

        # check if location is valid
        if self.__manager.check_potential_position([index_row,index_col]):
            self.__select_cube(index_row, index_col)
            self.__change_bg(index_row, index_col, index)

    def __on_finished_word_event(self, event, index):
        """event handler for Mouse2 click - finished word"""
        self.__manager.check_word(self)
        # Unselect all cubes
        for row in range(len(self.__letters)):
            for col in range(len(self.__letters[row])):
                self.__unselect_cube(row,col)
        self.__elements["canvas"].destroy()
        self.__create_game_board(self.frames["left frame"] )

    # endregion EVENTS


    # region SETTERS
    def add_word_to_box(self, word):
        """ Gets a word and adds it to the game's text box """
        self.__elements["textbox"].config(state=NORMAL)
        self.__elements["textbox"].insert(0.0, word)
        self.__elements["textbox"].config(state=DISABLED)

    def set_time(self, new_time):
        """ updates the game time """
        self.__elements["time"].config(text=new_time)

    def set_score(self, new_score):
        """ updates the game time """
        self.__elements["score"].config(text="score:\t"+new_score)

    def show_message(self, message):
        messagebox.showinfo("Important message!", message)

    # endregion SETTERS

    # region INNER METHODS
    def __select_cube(self, row, col):
        """changes cube's bg to selected, returns True upon success, False otherwise"""
        self.__letters[row][col].set_background(True)

    def __unselect_cube(self, row, col):
        """changes cube's bg to normal"""
        self.__letters[row][col].set_background(False)

    def __change_bg(self, row, col, index):
        """ changes the canvas' item at (index) to cube's background """
        bg_img = self.__letters[row][col].get_background()
        img = PhotoImage(file=bg_img)
        self.__elements["canvas"].itemconfig(index, image=img)
        self.__elements["pics"].append(img)

    def __check_if_valid_selection(self, row, col):
        """ checks if selection is valid- returns boolean """
        # check if already selected
        if self.__letters[row][col].is_selected():
            return False
        # check if game approves move
        elif Game.Game.set_potential_new_location([row, col]):
            return True
        return False

    def __endgame(self):
        """ finish the game """
        from tkinter import messagebox
        score = self.__manager.get_score()

        msg_str = f"Game over! you've scored {score}.\n" \
                  f"The previous player scored {score+1},\nPress 'yes'! to try again"
        msg_box = messagebox.askquestion("Oh.. come on!", msg_str,
                                         icon='warning')
        if msg_box == 'yes':
            self.__reset_game()
        else:
            self.__root.destroy()

    def __reset_game(self):
        """ starts a new game """
        self.__letters = self.__manager.reset_game()

        self.frames["game"].destroy()
        self.create_game_frame()

        self.__curr_time = boggle.GAME_TIME * 60
        self.__update_time()

    def __update_time(self):
        """updates game timer and sets it in the time label"""
        if self.__curr_time > 0:
            now = time.strftime("%M:%S", time.gmtime(self.__curr_time))
            self.__curr_time -= 1
            self.set_time(now)
            self.__root.after(1000, self.__update_time)
        else:
            self.__endgame()

    # endregion INNER METHODS


DEFAULT_BG = 'letter_bg2.png'     # path to normal background pic
SELECTED_BG = 'selected_bg2.png'  # path to selected background pic


class Cube:
    """
    Cube instance of the game Boggle
    each cube has a letter
    """
    def __init__(self, letter):
        """ Construct a Cube instance """
        self.__letter = letter
        self.__selected = False
        self.__background = DEFAULT_BG

    def get_letter(self):
        """ returns te cube's letter """
        return self.__letter

    def get_background(self):
        """ returns the path to the current background of the cube """
        return self.__background

    def set_background(self, selected=False):
        """ sets cube background to selected/normal according to param"""
        if selected:
            self.__background = SELECTED_BG
        else:
            self.__background = DEFAULT_BG
        self.__set_selected(selected)
        return None

    def is_selected(self):
        """ returns True if cube selected, False otherwise"""
        return self.__selected

    def __set_selected(self, selected):
        """ Changes cube selected sts according to received param """
        self.__selected = selected

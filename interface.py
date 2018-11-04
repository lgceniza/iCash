import pygame, engine

# Initializes the font module of pygame
pygame.font.init()

# Title of the game
GAME_TITLE = "ICA$H"

# Dimensions of the game screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

# File path to the .ttf file
# Source of font: https://www.1001fonts.com/press-start-font.html
FONT_FILE_PATH = "lib\\press_start_regular.ttf"

# Colors used in the game
BLACK = (0, 0, 0)
GREEN = (30, 197, 3)
RED = (204, 0, 0)

# (Font) sizes of game elements
SMALL_SIZE = 20
INPUT_SIZE = 35
MEDIUM_SIZE = 50
LARGE_SIZE = 80
TITLE_SIZE = 100
GAME_OVER_SIZE = 70
FINAL_SCORE_SIZE = 40

# Offset used in positioning
POS_OFFSET = 50
INPUT_OFFSET = 30

# Scenes or stages of the game
START = "START"
MODES = "MODES"
SET_TIMER = "SET_TIMER"
PLAY = "PLAY"
GAME_OVER = "GAME_OVER"
SAVE = "SAVE"

# Modes of the play scene
RANDOM_WORDS = "RANDOM_WORDS"
ANAGRAMS = "ANAGRAMS"

# Positions of each game element
TITLE_POS = "UPPER_HALF"
START_BTN_POS = "LOWER_HALF"
RND_WRDS_BTN_POS = "UPPER_HALF"
ANAGRAM_BTN_POS = "LOWER_HALF"
DIVIDER_POS = "CENTER"
HELP_POS_1 = "UPPER_MIDDLE"
SET_TIMER_SELECT_POS = "CENTER"
HELP_POS_2 = "LOWER_MIDDLE"
CHAR_SEQ_DISPLAY_POS = "UPPER_HALF"
PLAYER_INPUT_POS = "LOWER_HALF"
SCORE_DISPLAY_POS = "LOWER_MIDDLE"
RETRIES_DISPLAY_POS = "UPPER_RIGHT"
TIME_DISPLAY_POS = "UPPER_MIDDLE"
NEW_GAME_POS = "UPPER_MIDDLE"
GAME_OVER_DISPLAY_POS = "UPPER_HALF"
FINAL_SCORE_POS = "LOWER_HALF"
EXIT_GAME_POS = "LOWER_MIDDLE"
SAVE_STATE_POS = "CENTER"
YES_BTN_POS = "LOWER_LEFT"
NO_BTN_POS = "LOWER_RIGHT"

# Text of game elements used in game
START_BTN_TXT = "START"
MODES_HELP_TXT = "SELECT A GAME MODE."
RND_WRDS_BTN_TXT = "RANDOM WORDS"
DIVIDER_TXT = "---------------"
ANAGRAM_BTN_TXT = "ANAGRAMS"
SET_TIMER_HELP_TXT_1 = "CLICK TO CHANGE."
SET_TIMER_SELECT_TXT = ["NO TIME", "1 MIN.", "3 MIN.", "5 MIN.", "7 MIN.", "10 MIN."]
SET_TIMER_HELP_TXT_2 = "PRESS [ENTER] TO CONFIRM."
NEW_GAME_TXT = "PRESS [N] FOR NEW GAME."
GAME_OVER_DISPLAY_TXT = "GAME OVER"
FINAL_SCORE_TXT = "YOU SCORED "
NO_MONEY_TXT = "YOU GOT NOTHING!"
EXIT_GAME_TXT = "CLICK TO EXIT GAME."
SAVE_STATE_TXT = "SAVE STATE?"
YES_BTN_TXT = "YES"
NO_BTN_TXT = "NO"

class Display:
    """
    A class used to represent a game object that displays text
    ...
    Attributes
    ----------
    text : str
        text to be printed on the game screen
    size : int
        size of the text
    pos: str
        general area where the text will be displayed on-screen
    color : tuple
        RGB values of the color that the text will be displayed in
    Methods
    -------
    get_font()
        Returns the font to be used in displaying the text
    
    printable()
        Returns the Surface with the text to be displayed
    
    get_position(position : str)
        Returns the size and offset of the rendered text based on the specified position
    """    

    def __init__(self, text, size, pos, color=GREEN):
        self.text = text
        self.size = size
        self.pos = pos
        self.color = color
    
    def get_font(self):
        return pygame.font.Font(FONT_FILE_PATH, self.size)

    def printable(self):
        return self.get_font().render(self.text, True, self.color)
    
    def get_coordinates(self, offset=POS_OFFSET):
        btn_rect = self.printable().get_rect()
        if self.pos == "UPPER_LEFT":
            btn_rect.topleft = (offset, offset)
        elif self.pos == "UPPER_MIDDLE":
            btn_rect.midtop = (SCREEN_WIDTH / 2, offset)
        elif self.pos == "UPPER_RIGHT":
            btn_rect.topright = (SCREEN_WIDTH - offset, offset)
        elif self.pos == "UPPER_HALF":
            btn_rect.center = (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - (offset * 2))
        elif self.pos == "CENTER":
            btn_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        elif self.pos ==  "LOWER_HALF":
            btn_rect.center = (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + (offset * 2))
        elif self.pos == "LOWER_LEFT":
            btn_rect.bottomleft = (offset, SCREEN_HEIGHT - offset)
        elif self.pos == "LOWER_MIDDLE":
            btn_rect.midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - offset)
        elif self.pos == "LOWER_RIGHT":
            btn_rect.bottomright = (SCREEN_WIDTH - offset, SCREEN_HEIGHT - offset)
        return btn_rect

class Button(Display):
    """
    A class inherited from Display that supports text rendering and a hover state
    ...
    Attributes
    ----------
    HOVER_STATE_INCREMENT : int
        increment used in increasing the size of Button when hovered over
    text : str
        text to be printed on the game screen
    size : int
        size of the text
    color : list
        RGB values of the color that the text will be displayed in
    hover : boolean
        truth value of whether cursor is hovering over it or not
    Methods
    -------
    get_font()
        Returns the font to be used in displaying the text, which takes into account the hover state of the button
    
    printable()
        Returns the Surface with the text to be displayed
    
    get_position(position : str)
        Returns the size and offset of the rendered text based on the specified position
    """

    HOVER_STATE_INCREMENT = 5

    def __init__(self, text, size, pos, color=GREEN, hover=False):
        super().__init__(text, size, pos, color)
        self.hover = hover

    def get_font(self):
        if self.hover:
            return pygame.font.Font(FONT_FILE_PATH, self.size + self.HOVER_STATE_INCREMENT)
        return pygame.font.Font(FONT_FILE_PATH, self.size)

    def is_colliding(self, obj_pos):
        return self.get_coordinates().collidepoint(obj_pos)

class Select(Button):
    def __init__(self, choices, size, pos, color=GREEN, hover=False):
        self.choices = choices
        self.index = 0
        self.text = self.choices[self.index]
        super().__init__(self.text, size, pos, color)

    def change_text(self):
        if self.index < len(self.choices) - 1:
            self.index += 1
        else:
            self.index = 0
        self.text = self.choices[self.index]

    def printable(self):
        return self.get_font().render(self.text, True, self.color)

class Input(Display):
    def __init__(self, size, pos, text="", color=GREEN):
        super().__init__(text, size, pos, color)
    
    def add_input(self, char):
        self.text += char
    
    def backspace(self):
        if self.text != "":
            self.text = self.text[:-1]

    def reset_input(self):
        self.text = ""

# Elements of the game used in the interface

## Used in Scene "START"
TITLE = Display(GAME_TITLE, TITLE_SIZE, TITLE_POS)
START_BTN = Button(START_BTN_TXT, MEDIUM_SIZE, START_BTN_POS)

## Used in Scene "MODES"
MODES_HELP = Display(MODES_HELP_TXT, SMALL_SIZE, HELP_POS_1)
RND_WRDS_BTN = Button(RND_WRDS_BTN_TXT, MEDIUM_SIZE, RND_WRDS_BTN_POS)
DIVIDER = Display(DIVIDER_TXT, MEDIUM_SIZE, DIVIDER_POS)
ANAGRAMS_BTN = Button(ANAGRAM_BTN_TXT, MEDIUM_SIZE, ANAGRAM_BTN_POS)

## Used in Scene "SET_TIMER"
SET_TIMER_HELP_1 = Display(SET_TIMER_HELP_TXT_1, SMALL_SIZE, HELP_POS_1)
SET_TIMER_SELECT = Select(SET_TIMER_SELECT_TXT, LARGE_SIZE, SET_TIMER_SELECT_POS)
SET_TIMER_HELP_2 = Display(SET_TIMER_HELP_TXT_2, SMALL_SIZE, HELP_POS_2)

## Used in Scene "PLAY"
def display_char_seq(char_seq, game_screen):
    char_seq_display = Display(char_seq, MEDIUM_SIZE, CHAR_SEQ_DISPLAY_POS)
    game_screen.blit(char_seq_display.printable(), char_seq_display.get_coordinates())

def display_score(score, game_screen):
    score_display = Display("$" + str(score), MEDIUM_SIZE, SCORE_DISPLAY_POS)
    game_screen.blit(score_display.printable(), score_display.get_coordinates())

def display_retries(retries, game_screen):
    retries_display = Display(str(retries) + "X", MEDIUM_SIZE, RETRIES_DISPLAY_POS)
    game_screen.blit(retries_display.printable(), retries_display.get_coordinates())

def display_time(time, game_screen):
    time_display = Display(time, MEDIUM_SIZE, TIME_DISPLAY_POS)
    game_screen.blit(time_display.printable(), time_display.get_coordinates())

PLAYER_INPUT = Input(INPUT_SIZE, PLAYER_INPUT_POS)

## Used in Scene "GAME_OVER"
GAME_OVER_DISPLAY = Display(GAME_OVER_DISPLAY_TXT, GAME_OVER_SIZE, GAME_OVER_DISPLAY_POS)

def display_final_score(final_score, game_screen):
    if not final_score:
        final_score_display = Display(NO_MONEY_TXT, FINAL_SCORE_SIZE, FINAL_SCORE_POS)
    else:
        final_score_display = Display(FINAL_SCORE_TXT + "$" + str(final_score) + ".", FINAL_SCORE_SIZE, FINAL_SCORE_POS)
    game_screen.blit(final_score_display.printable(), final_score_display.get_coordinates())

NEW_GAME = Display(NEW_GAME_TXT, SMALL_SIZE, NEW_GAME_POS)
EXIT_GAME = Display(EXIT_GAME_TXT, SMALL_SIZE, EXIT_GAME_POS)

## Used in Scene "SAVE"
SAVE_STATE = Display(SAVE_STATE_TXT, MEDIUM_SIZE, SAVE_STATE_POS)
YES_BTN = Button(YES_BTN_TXT, MEDIUM_SIZE, YES_BTN_POS)
NO_BTN = Button(NO_BTN_TXT, MEDIUM_SIZE, NO_BTN_POS)
import pygame, engine

pygame.font.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Source: https://www.1001fonts.com/press-start-font.html
FONT_FILE_PATH = "press-start.regular.ttf"

# Colors
BLACK = (0, 0, 0)
GREEN = (30, 197, 3)

# Game Element Sizes
SMALL_SIZE = 25
MEDIUM_SIZE = 50
LARGE_SIZE = 80

# Offset used for positioning
OFFSET = 50

class Display:
    def __init__(self, text, size, color=GREEN):
        self.text = text
        self.size = size
        self.color = color
    
    def get_font(self):
        return pygame.font.Font(FONT_FILE_PATH, self.size)

    def printable(self):
        return self.get_font().render(self.text, True, self.color)
    
    def get_position(self, position):
        btn_rect = self.printable().get_rect()
        if position == "UPPER_LEFT":
            btn_rect.topleft = (OFFSET, OFFSET)
        elif position == "UPPER_MIDDLE":
            btn_rect.midtop = (SCREEN_WIDTH / 2, OFFSET)
        elif position == "UPPER_RIGHT":
            btn_rect.topright = (SCREEN_WIDTH - OFFSET, OFFSET)
        elif position == "UPPER_HALF":
            btn_rect.center = (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - (OFFSET * 2))
        elif position ==  "LOWER_HALF":
            btn_rect.center = (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + (OFFSET * 2))
        elif position == "LOWER_LEFT":
            btn_rect.bottomleft = (OFFSET, SCREEN_HEIGHT - OFFSET)
        elif position == "LOWER_MIDDLE":
            btn_rect.midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - OFFSET)
        elif position == "LOWER_RIGHT":
            btn_rect.bottomright = (SCREEN_WIDTH - OFFSET, SCREEN_HEIGHT - OFFSET)
        return btn_rect

class Button(Display):
    HOVER_STATE_INCREMENT = 5

    def __init__(self, text, size, color=GREEN, hover=False):
        super().__init__(text, size, color)
        self.hover = hover

    def get_font(self):
        if self.hover:
            return pygame.font.Font(FONT_FILE_PATH, self.size + self.HOVER_STATE_INCREMENT)
        return pygame.font.Font(FONT_FILE_PATH, self.size)
import pygame, engine

pygame.font.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

MEDIUM_FONT = pygame.font.Font("press-start.k.ttf", 50)

BLACK = (0, 0, 0)
MATRIX_GREEN = (30, 197, 3)

def print_score(score, game_screen):
    score_width, score_height = MEDIUM_FONT.size("$" + str(score))
    position = [(SCREEN_WIDTH / 2) - (score_width / 2), (SCREEN_HEIGHT - score_height) - 25]
    score = MEDIUM_FONT.render("$" + str(score), True, MATRIX_GREEN)
    game_screen.blit(score, position)
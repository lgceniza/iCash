import pygame, sys, engine, interface

pygame.init()

game_screen = pygame.display.set_mode(interface.SCREEN_RESOLUTION)

game_has_ended = False
while not game_has_ended:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_has_ended = True
    
    interface.print_score(0, game_screen)

    pygame.display.update()

pygame.quit()

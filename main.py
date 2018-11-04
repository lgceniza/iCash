import pygame, sys, engine, interface

pygame.init()

game_screen = pygame.display.set_mode(interface.SCREEN_RESOLUTION)
pygame.display.set_caption(interface.GAME_TITLE)
clock = pygame.time.Clock()
game_state = engine.create_or_load_save_file()

passed_time = 0
timer_started = False

game_has_ended = False
while not game_has_ended:
    game_screen.fill(interface.BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if game_state["scene"] == interface.PLAY:
                game_state["scene"] = interface.SAVE
            else:
                engine.save_to_file(engine.SAVE_STATE)
                game_has_ended = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if game_state["scene"] == interface.START:
                if interface.START_BTN.is_colliding(event.pos):
                    game_state["scene"] = interface.MODES
            elif game_state["scene"] == interface.MODES:
                if interface.RND_WRDS_BTN.is_colliding(event.pos):
                    game_state["mode"] = interface.RANDOM_WORDS
                    game_state["scene"] = interface.SET_TIMER
                elif interface.ANAGRAMS_BTN.is_colliding(event.pos):
                    game_state["mode"] = interface.ANAGRAMS
                    game_state["scene"] = interface.SET_TIMER
            elif game_state["scene"] == interface.SET_TIMER:
                if interface.SET_TIMER_SELECT.is_colliding(event.pos):
                    interface.SET_TIMER_SELECT.change_text()
            elif game_state["scene"] == interface.GAME_OVER:
                game_has_ended = True
            elif game_state["scene"] == interface.SAVE:
                if interface.YES_BTN.is_colliding(event.pos):
                    engine.save_to_file(game_state)
                elif interface.NO_BTN.is_colliding(event.pos):
                    engine.save_to_file(engine.SAVE_STATE)
                game_has_ended = True
        elif event.type == pygame.KEYUP:
            if game_state["scene"] == interface.SET_TIMER:
                if event.key == pygame.K_RETURN:
                    set_timer_txt = interface.SET_TIMER_SELECT.text
                    if set_timer_txt == "NO TIME":
                        game_state["with_timer"] = False
                    else:
                        game_state["with_timer"] = True
                        game_state["time_left"] = 60*int(interface.SET_TIMER_SELECT.text[:2])
                    if game_state["mode"] == interface.RANDOM_WORDS:
                        game_state["char_seq"] = engine.combine_words(engine.pick_set_of_words())
                        game_state["valid_words"] = engine.get_valid_words_from_seq(game_state["char_seq"])
                    elif game_state["mode"] == interface.ANAGRAMS:
                        game_state["char_seq"] = engine.pick_word(game_state)
                        game_state["valid_words"] = engine.get_anagrams_for_word(game_state["char_seq"])
                    game_state["scene"] = interface.PLAY
            elif game_state["scene"] == interface.PLAY:
                char = pygame.key.name(event.key).lower()
                if char in interface.ALPHABET:
                    interface.PLAYER_INPUT.add_input(char)
                elif char == "backspace":
                    interface.PLAYER_INPUT.backspace()
                elif char == "return":
                    input_txt = interface.PLAYER_INPUT.text
                    if input_txt in game_state["valid_words"]:
                        game_state["score"] += engine.get_score_equivalent_of_word(input_txt)
                        game_state["valid_words"].remove(input_txt)
                        game_state["used_words"].append(input_txt)
                        if game_state["valid_words"] == []:
                            if game_state["mode"] == interface.RANDOM_WORDS:
                                game_state["char_seq"] = engine.combine_words(engine.pick_set_of_words())
                                game_state["valid_words"] = engine.get_valid_words_from_seq(game_state["char_seq"])
                            else:
                                game_state["char_seq"] = engine.pick_word(game_state)
                                game_state["valid_words"] = engine.get_anagrams_for_word(game_state["char_seq"])
                    else:
                        game_state["retries"] -= 1
                    interface.PLAYER_INPUT.reset_input()
                    if not game_state["retries"]:
                        game_state["scene"] = interface.GAME_OVER
            elif game_state["scene"] == interface.GAME_OVER:
                if event.key == pygame.K_n:
                    game_state["scene"] = interface.MODES

    if game_state["scene"] == interface.START:
        game_screen.blit(interface.TITLE.printable(), interface.TITLE.get_coordinates())
        interface.START_BTN.hover = interface.START_BTN.is_colliding(pygame.mouse.get_pos())
        start_btn_pos = interface.START_BTN.get_coordinates()
        game_screen.blit(interface.START_BTN.printable(), start_btn_pos)
    elif game_state["scene"] == interface.MODES:
        game_screen.blit(interface.MODES_HELP.printable(), interface.MODES_HELP.get_coordinates())
        game_screen.blit(interface.DIVIDER.printable(), interface.DIVIDER.get_coordinates())
        interface.RND_WRDS_BTN.hover = interface.RND_WRDS_BTN.is_colliding(pygame.mouse.get_pos())
        interface.ANAGRAMS_BTN.hover = interface.ANAGRAMS_BTN.is_colliding(pygame.mouse.get_pos())
        rnd_words_btn_pos = interface.RND_WRDS_BTN.get_coordinates()
        anagrams_btn_pos = interface.ANAGRAMS_BTN.get_coordinates()
        game_screen.blit(interface.RND_WRDS_BTN.printable(), rnd_words_btn_pos)
        game_screen.blit(interface.ANAGRAMS_BTN.printable(), anagrams_btn_pos)
    elif game_state["scene"] == interface.SET_TIMER:
        game_screen.blit(interface.SET_TIMER_HELP_1.printable(), interface.SET_TIMER_HELP_1.get_coordinates())
        interface.SET_TIMER_SELECT.hover = interface.SET_TIMER_SELECT.is_colliding(pygame.mouse.get_pos())
        set_timer_select_pos = interface.SET_TIMER_SELECT.get_coordinates()
        game_screen.blit(interface.SET_TIMER_SELECT.printable(), set_timer_select_pos)
        game_screen.blit(interface.SET_TIMER_HELP_2.printable(), interface.SET_TIMER_HELP_2.get_coordinates())
    elif game_state["scene"] == interface.PLAY:
        if game_state["with_timer"]:
            interface.display_time(engine.get_time(game_state["time_left"]), game_screen)
            if not timer_started:
                timer_started = not timer_started
                start_time = pygame.time.get_ticks()
            if pygame.time.get_ticks() - start_time >= 1000:
                game_state["time_left"] -= 1
                interface.display_time(engine.get_time(game_state["time_left"]), game_screen)
                start_time = pygame.time.get_ticks()
                if not game_state["time_left"]:
                    game_state["scene"] = interface.GAME_OVER
        interface.display_char_seq(game_state["char_seq"], game_screen)
        game_screen.blit(interface.PLAYER_INPUT.printable(), interface.PLAYER_INPUT.get_coordinates(interface.INPUT_OFFSET))
        interface.display_score(game_state["score"], game_screen)
        interface.display_retries(game_state["retries"], game_screen)
    elif game_state["scene"] == interface.GAME_OVER:
        game_screen.blit(interface.NEW_GAME.printable(), interface.NEW_GAME.get_coordinates())
        game_screen.blit(interface.GAME_OVER_DISPLAY.printable(), interface.GAME_OVER_DISPLAY.get_coordinates())
        interface.display_final_score(game_state["score"], game_screen)
        game_screen.blit(interface.EXIT_GAME.printable(), interface.EXIT_GAME.get_coordinates())
    elif game_state["scene"] == interface.SAVE:
        game_screen.blit(interface.SAVE_STATE.printable(), interface.SAVE_STATE.get_coordinates())
        interface.YES_BTN.hover = interface.YES_BTN.is_colliding(pygame.mouse.get_pos())
        interface.NO_BTN.hover = interface.NO_BTN.is_colliding(pygame.mouse.get_pos())
        yes_btn_pos = interface.YES_BTN.get_coordinates()
        no_btn_pos = interface.NO_BTN.get_coordinates()
        game_screen.blit(interface.YES_BTN.printable(), yes_btn_pos)
        game_screen.blit(interface.NO_BTN.printable(), no_btn_pos)

    pygame.display.update()
    clock.tick(30)

pygame.quit()

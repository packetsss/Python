# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
environ['SDL_VIDEO_WINDOW_POS'] = "1500, 200"

import numpy as np
import pygame

import collisions
import event
import gamestate
import graphics
import config

was_closed = False
while not was_closed:
    game = gamestate.GameState()
    button_pressed = graphics.draw_main_menu(game)

    if button_pressed == config.play_game_button:
        game.start_pool()
        events = event.events()
        while not (events["closed"] or game.is_game_over or events["quit_to_main_menu"]):
            events = event.events()
            collisions.resolve_all_collisions(game.balls, game.holes, game.table_sides)
            game.redraw_all()

            if game.all_not_moving():
                game.turned_over = False
                game.check_pool_rules()
                if not game.turned_over:
                    print("Good hit!")
                game.cue.make_visible(game.current_player)
                while not (
                    (events["closed"] or events["quit_to_main_menu"]) or game.is_game_over) and game.all_not_moving():
                    game.redraw_all()
                    events = event.events()
                    # operate cue
                    if game.cue.is_clicked(events):
                        game.cue.cue_is_active(game, events)
                    # move cue ball on foul
                    elif game.can_move_white_ball and game.white_ball.is_clicked(events):
                        game.white_ball.is_active(game, game.is_behind_line_break())
            if config.resolution[0] < game.white_ball.rect.center[0] or game.white_ball.rect.center[0] < 0\
                or config.resolution[1] < game.white_ball.rect.center[1] or game.white_ball.rect.center[1] < 0:
                game.check_potted(ball_outside_table=True)

        was_closed = events["closed"]

    if button_pressed == config.exit_button:
        was_closed = True

pygame.quit()

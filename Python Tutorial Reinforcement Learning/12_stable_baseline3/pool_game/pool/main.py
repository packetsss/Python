from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
environ['SDL_VIDEO_WINDOW_POS'] = "1500, 200"

import cv2
import numpy as np
import pygame

import ball
import collisions
import event
import gamestate
import graphics
import config

was_closed = False
game = gamestate.GameState()
while not was_closed:
    # button_pressed = graphics.draw_main_menu(game)

    if 1: #button_pressed == config.play_game_button:
        game.start_pool()
        events = event.events()
        while not (events["closed"] or game.is_game_over or events["quit_to_main_menu"]):
            events = event.events()
            collisions.resolve_all_collisions(game.balls, game.holes, game.table_sides)
            game.redraw_all()



            if game.all_not_moving():
                game.turned_over = False
                game.check_pool_rules()
                if game.current_player != gamestate.Player.Player1:
                    game.current_player = gamestate.Player.Player1

                if not game.turned_over:
                    print("Good hit!")
                else:
                    print("Updating color...")
                    game.redraw_all(update_type=True)
                
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
            im = cv2.rotate(game.image, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
            im = cv2.flip(im, 0)
            im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)[35:-35, 35:-35]
            # print(im.shape)
            # dim = int((1120 - 620) / 2)
            # repeated = np.repeat(im[0, :], dim, 0).reshape(dim, -1)
            # im = np.vstack((repeated, im, repeated))
            size = 80
            im = cv2.resize(im, (int(size * (1120 / 620)), size)).reshape(size, -1, 1)
            # print(im.shape)
            cv2.imshow("im", im)
            cv2.waitKey(1)


        was_closed = events["closed"]

    # if button_pressed == config.exit_button:
    #     was_closed = True

pygame.quit()

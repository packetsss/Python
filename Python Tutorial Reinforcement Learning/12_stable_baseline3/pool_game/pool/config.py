# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import math
import random
import numpy as np
import pygame

pygame.font.init()
# fonts need to be initialised before using
def get_default_font(size):
    font_defualt = pygame.font.get_default_font()
    return pygame.font.Font(font_defualt, size)


def set_max_resolution():
    infoObject = pygame.display.Info()
    global resolution
    global white_ball_initial_pos
    resolution = np.array([infoObject.current_w, infoObject.current_h])
    ball_x = random.choice([random.uniform(0.13, 0.25), random.uniform(0.75, 0.87)])
    white_ball_initial_pos = (resolution + [table_margin + hole_radius, 0]) * [0.25, ball_x]

# window settings
fullscreen = False
# fullscreen resolution can only be known after initializing the screen
if not fullscreen:
    resolution = np.array([1120, 620])
window_caption = "The pool game of loaf?!!"
fps_limit = 1000

# table settings
table_margin = 55
table_side_color = (200, 200, 0)
table_color = (0, 100, 0)
separation_line_color = (200, 200, 200)
hole_radius = 22
middle_hole_offset = np.array([[-hole_radius * 1.35, hole_radius], [-hole_radius, 0],
                               [hole_radius, 0], [hole_radius * 1.35, hole_radius]])
side_hole_offset = np.array([
    [- 2 * math.cos(math.radians(45)) * hole_radius - hole_radius, hole_radius * 0.5],
    [- math.cos(math.radians(45)) * hole_radius, -
    math.cos(math.radians(45)) * hole_radius],
    [math.cos(math.radians(45)) * hole_radius,
     math.cos(math.radians(45)) * hole_radius],
    [- hole_radius * 0.7, 2 * math.cos(math.radians(45)) * hole_radius * 0.9 + hole_radius]
])

# convert each ball to solid, strips, 8-ball, and cue-ball
ball_unassigned_dict = {
    0: 3,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 2,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: 0
}

ball_solids_dict = {
    0: 3,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 2,
    9: 1,
    10: 1,
    11: 1,
    12: 1,
    13: 1,
    14: 1,
    15: 1
}

ball_strips_dict = {
    0: 3,
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 1,
    6: 1,
    7: 1,
    8: 2,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: 0
}

# cue settings
player1_cue_color = (250, 130, 0)
player2_cue_color = (0, 110, 220)
cue_hit_power = 8
cue_length = 250
cue_thickness = 12
cue_max_displacement = 130
# safe displacement is the length the cue stick can be pulled before
# causing the ball to move
cue_safe_displacement = 1
aiming_line_length = 14

# ball settings
total_ball_num = 16
ball_radius = 14
ball_mass = 20
speed_angle_threshold = 0.09
visible_angle_threshold = 0.05
ball_colors = [
    (255, 255, 255),
    player1_cue_color,
    player1_cue_color,
    player1_cue_color,
    player1_cue_color,
    player1_cue_color,
    player1_cue_color,
    player1_cue_color,
    (0, 0, 0),
    player2_cue_color,
    player2_cue_color,
    player2_cue_color,
    player2_cue_color,
    player2_cue_color,
    player2_cue_color,
    player2_cue_color,
]
ball_stripe_thickness = 5
ball_stripe_point_num = 25
# where the balls will be placed at the start
# relative to screen resolution
ball_starting_place_ratio = [0.75, 0.5]
# in fullscreen mode the resolution is only available after initialising the screen
# and if the screen wasn't initialised the resolution variable won't exist
if 'resolution' in locals():
    ball_x = random.choice([random.uniform(0.13, 0.25), random.uniform(0.75, 0.87)])
    white_ball_initial_pos = (resolution + [table_margin + hole_radius, 0]) * [0.25, ball_x]
ball_label_text_size = 10

# physics
# if the velocity of the ball is less then
# friction threshold then it is stopped
friction_threshold = 0.22
friction_coeff = 0.985
# 1 - perfectly elastic ball collisions
# 0 - perfectly inelastic collisions
ball_coeff_of_restitution = 0.9
table_coeff_of_restitution = 0.9

# menu
menu_text_color = (255, 255, 255)
menu_text_selected_color = (0, 0, 255)
menu_title_text = "Pool"
menu_buttons = ["Play Pool", "Exit"]
menu_margin = 20
menu_spacing = 10
menu_title_font_size = 40
menu_option_font_size = 20
exit_button = 2
play_game_button = 1

# in-game ball target variables
player1_target_text = 'P1 balls - '
player2_target_text = 'P2 balls - '
target_ball_spacing = 3
player1_turn_label = "Player 1 turn"
player2_turn_label = "Player 2 turn"
penalty_indication_text = " (on foul)"
game_over_label_font_size = 40

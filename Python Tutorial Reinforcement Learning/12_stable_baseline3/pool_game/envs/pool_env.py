# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from os import environ
environ['SDL_VIDEO_WINDOW_POS'] = "1500, 200"
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import sys
sys.path.append('pool_game/pool')

import event
from ball import BallType
from collisions import resolve_all_collisions
from gamestate import GameState, Player
from graphics import draw_main_menu
from config import *

import cv2
import gym
import numpy as np
import pygame as pg
from gym import error, spaces
from gym.utils import seeding

class PoolEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.game = GameState()
        self.game.start_pool()
        self.game.redraw_all()
        super(PoolEnv, self).__init__()
        
        self.reward = 0
        self.game.steps = 0
        self.game.reward = 0

        self.foul_countdown = []
        self.score_countdown = []
        self.balls_potted = []
        self.steps = 0
        self.max_episode_steps = 100
        self.w, self.h = resolution
        self.number_of_balls = 16
        self.image_h = 100

        # velocity_x, velocity_y
        v_limit = 500
        self.action_space = spaces.Box(low=np.array([-v_limit, -v_limit]), high=np.array([v_limit, v_limit]))

        # image
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(self.image_h, int(self.image_h * (1120 / 620)), 1), dtype=np.uint8
            )

    def pre_process_observation(self):
        im = cv2.rotate(self.game.image, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        im = cv2.flip(im, 0)
        im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)[35:-35, 35:-35]
        im = cv2.resize(im, (int(self.image_h * (1120 / 620)), self.image_h)).reshape(self.image_h, -1, 1)
        return im
        
    def step(self, action):
        # print(action)
        self.game.cue.ball_hit(new_velocity=action*250)

        # render
        _ = pg.event.get() # must get the env?
        resolve_all_collisions(self.game.balls, self.game.holes, self.game.table_sides)
        self.game.redraw_all()

        done = False
        info = {}

        # initialize some consitions for self.reward evaluation
        self.game.hit_a_ball = False
        self.game.turned_over = False

        # wait for ball to stop
        while not self.game.all_not_moving():
            resolve_all_collisions(self.game.balls, self.game.holes, self.game.table_sides)
            self.game.balls.update(update_ball=True)

        self.game.balls.update(update_sprite=True)
        self.game.redraw_all()
        # check game rules
        self.game.check_pool_rules()

        # make sure always player 1 play solids
        if self.game.current_player != Player.Player1:
            self.game.current_player = Player.Player1

        # flip ball colors/types
        if self.game.turn_over:
            self.game.redraw_all(update_type=True)

        # pot a ball
        if not self.game.turned_over:
            self.score_countdown.append(0)
            self.balls_potted.append(0)
            self.foul_countdown = []
            self.reward += 50
            
        # contact with correct ball type
        elif not self.game.can_move_white_ball:
            self.score_countdown.append(0)
            self.foul_countdown = []
            # self.reward += 5 * (len(self.score_countdown))
        # foul penalize
        else:
            self.foul_countdown.append(0)
            self.score_countdown = []
            # self.reward -= int(5 * (len(self.foul_countdown) ** 1.6))

        self.reward += int(3 * (len(self.score_countdown) ** 1.2) - 3 * (len(self.foul_countdown) ** 1.3))
            
        
        # if not touching any balls multiple times, reset env
        if self.reward < -50:
            self.game.is_game_over = True
            self.game.winner = None

        # when game is over
        if self.game.is_game_over:
            done = True
            # check who wins
            if self.game.current_player == self.game.winner and self.game.potting_8ball[self.game.current_player]:
                self.reward += 400
            else:
                self.reward = min(80 * len(self.balls_potted) - 500, -50)

        observation = self.pre_process_observation()
        
        self.steps += 1
        self.game.steps = self.steps
        self.game.reward = self.reward
        pg.display.set_caption(f"step {self.steps} -- reward {self.reward}")
        return observation, self.reward, done, info
                
    def reset(self):
        self.reward = 0
        self.score_countdown = []
        self.foul_countdown = []
        self.balls_potted = []

        self.game.start_pool()
        self.game.redraw_all()
        return self.pre_process_observation()

    def render(self, mode='human'):
        self.game.redraw_all()

    def close(self):
        pg.quit()
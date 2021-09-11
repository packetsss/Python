# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from os import environ
environ['SDL_VIDEO_WINDOW_POS'] = "1500, 200"
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import sys
sys.path.append('pool_game/pool')

import pygame as pg
from ball import BallType
from collisions import resolve_all_collisions
import event
from gamestate import GameState, Player
from graphics import draw_main_menu
from config import *

import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding

class PoolEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.game = GameState()
        self.game.start_pool()
        super(PoolEnv, self).__init__()

        self.game.steps = 0
        self.game.reward = 0

        self.not_touching_countdown = []
        self.steps = 0
        self.max_episode_steps = 60
        self.w, self.h = resolution
        self.number_of_balls = 16

        # velocity_x, velocity_y
        v_limit = 550
        self.action_space = spaces.Box(low=np.array([-v_limit, -v_limit]), high=np.array([v_limit, v_limit]))

        # ball_x, ball_y, ball_type(solid, strips, 8-ball, cue-ball) x 16 balls
        self.observation_space = spaces.Box(
            low=np.repeat(np.array([0, 0, 0]), self.number_of_balls, axis=0).reshape(self.number_of_balls, 3), high=np.repeat(np.array([self.w, self.h, 3]), self.number_of_balls, axis=0).reshape(self.number_of_balls, 3)
            )

    def pre_process_observation(self):
        if self.game.ball_assignment is None:
            ball_dict = ball_unassigned_dict
        elif self.game.ball_assignment[self.game.current_player] == BallType.Solid:
            ball_dict = ball_solids_dict
        else:
            ball_dict = ball_strips_dict
        observation = np.array([np.array([*x.rect.center, ball_dict[x.number]]) for x in self.game.balls.sprites()])
        balls_to_fill = self.number_of_balls - observation.shape[0]
        if balls_to_fill > 0:
            # 1 is opposite color
            return np.vstack((observation, np.repeat(np.array([0, 0, 1]), balls_to_fill, axis=0).reshape(balls_to_fill, 3)))
        else:
            return observation
        
    def step(self, action):
        self.game.cue.ball_hit(new_velocity=action)

        # render
        _ = pg.event.get() # must get the env?
        resolve_all_collisions(self.game.balls, self.game.holes, self.game.table_sides)
        self.game.redraw_all()

        reward = 0
        done = False
        info = {}

        # initialize some consitions for reward evaluation
        self.game.hit_a_ball = False
        self.game.turned_over = False

        # wait for ball to stop
        while not self.game.all_not_moving():
            resolve_all_collisions(self.game.balls, self.game.holes, self.game.table_sides)
            self.game.redraw_all()

        # check game rules
        self.game.check_pool_rules()

        # check cue ball outside the table
        # if resolution[0] < self.game.white_ball.rect.center[0] or self.game.white_ball.rect.center[0] < 0\
        #     or resolution[1] < self.game.white_ball.rect.center[1] or self.game.white_ball.rect.center[1] < 0:
        #         print("cue ball is outside")
        #         self.game.check_potted(ball_outside_table=True)

        # pot a ball
        if not self.game.turned_over:
            reward += 40
        # contact with correct ball type
        elif not self.game.can_move_white_ball:
            reward += 5
        # foul penalize
        else:
            reward -= 10
        
        # reward by hitting a ball (avoid horizontal/vertical hit by multiplying times)
        if not self.game.hit_a_ball:
            self.not_touching_countdown.append(0)
            reward -= 5 * len(self.not_touching_countdown)
        else:
            self.not_touching_countdown = []
        
        # if not touching any balls multiple times, reset env
        if len(self.not_touching_countdown) > 4:
            self.not_touching_countdown = []
            self.game.is_game_over = True
            self.game.winner = None

        # when game is over
        if self.game.is_game_over:
            done = True
            # check who wins
            if self.game.current_player == self.game.winner and self.game.potting_8ball[self.game.current_player]:
                reward += 500
            else:
                reward -= 300

        observation = self.pre_process_observation()

        # a ball is outside the env
        if observation.shape[0] > 16:
            print(observation)
            observation = observation[:16, :]

        
        self.steps += 1
        self.game.steps = self.steps
        self.game.reward = reward
        return observation, reward, done, info
                
    def reset(self):
        self.game.start_pool()
        return self.pre_process_observation()

    def render(self, mode='human'):
        self.game.redraw_all()

    def close(self):
        pg.quit()
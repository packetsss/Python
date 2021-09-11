from .utils import *
from .abstract_game import AbstractGame

import os
import gym
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["SDL_VIDEO_WINDOW_POS"] = "50, 200"
gym.logger.set_level(40)

import cv2
import time
import torch
import random
import datetime
import numpy as np
import pymunk as pm
import pygame as pg
from gym import spaces
from gym.utils import seeding
import pymunk.pygame_util as pygame_util

class MuZeroConfig:
    def __init__(self):
        # More information is available here: https://github.com/werner-duvaud/muzero-general/wiki/Hyperparameter-Optimization

        self.seed = 0  # Seed for numpy, torch and the game
        self.max_num_gpus = None  # Fix the maximum number of GPUs to use. It's usually faster to use a single GPU (set it to 1) if it has enough memory. None will use every GPUs available



        ### Game
        self.observation_shape = (3, IMAGE_HEIGHT, IMAGE_WIDTH)  # Dimensions of the game observation, must be 3D (channel, height, width). For a 1D array, please reshape it to (1, 1, length of array)
        self.action_space = list(range(2))  # Fixed list of all possible actions. You should only edit the length
        self.players = list(range(1))  # List of players. You should only edit the length
        self.stacked_observations = 0  # Number of previous observations and previous actions to add to the current observation

        # Evaluate
        self.muzero_player = 0  # Turn Muzero begins to play (0: MuZero plays first, 1: MuZero plays second)
        self.opponent = None  # Hard coded agent that MuZero faces to assess his progress in multiplayer games. It doesn't influence training. None, "random" or "expert" if implemented in the Game class



        ### Self-Play
        self.num_workers = 8  # Number of simultaneous threads/workers self-playing to feed the replay buffer
        self.selfplay_on_gpu = True
        self.max_moves = 27000  # Maximum number of moves if game is not finished before
        self.num_simulations = 50  # Number of future moves self-simulated
        self.discount = 0.997  # Chronological discount of the reward
        self.temperature_threshold = None  # Number of moves before dropping the temperature given by visit_softmax_temperature_fn to 0 (ie selecting the best action). If None, visit_softmax_temperature_fn is used every time

        # Root prior exploration noise
        self.root_dirichlet_alpha = 0.25
        self.root_exploration_fraction = 0.25

        # UCB formula
        self.pb_c_base = 19652
        self.pb_c_init = 1.25



        ### Network
        self.network = "resnet"  # "resnet" / "fullyconnected"
        self.support_size = 1  # Value and reward are scaled (with almost sqrt) and encoded on a vector with a range of -support_size to support_size. Choose it so that support_size <= sqrt(max(abs(discounted reward)))

        # Residual Network
        self.downsample = "resnet"  # Downsample observations before representation network, False / "CNN" (lighter) / "resnet" (See paper appendix Network Architecture)
        self.blocks = 16  # Number of blocks in the ResNet
        self.channels = 256  # Number of channels in the ResNet
        self.reduced_channels_reward = 256  # Number of channels in reward head
        self.reduced_channels_value = 256  # Number of channels in value head
        self.reduced_channels_policy = 256  # Number of channels in policy head
        self.resnet_fc_reward_layers = [256, 256]  # Define the hidden layers in the reward head of the dynamic network
        self.resnet_fc_value_layers = [256, 256]  # Define the hidden layers in the value head of the prediction network
        self.resnet_fc_policy_layers = [256, 256]  # Define the hidden layers in the policy head of the prediction network

        # Fully Connected Network
        self.encoding_size = 10
        self.fc_representation_layers = []  # Define the hidden layers in the representation network
        self.fc_dynamics_layers = [16]  # Define the hidden layers in the dynamics network
        self.fc_reward_layers = [16]  # Define the hidden layers in the reward network
        self.fc_value_layers = []  # Define the hidden layers in the value network
        self.fc_policy_layers = []  # Define the hidden layers in the policy network



        ### Training
        self.results_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../results", os.path.basename(__file__)[:-3], datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S"))  # Path to store the model weights and TensorBoard logs
        self.save_model = True  # Save the checkpoint in results_path as model.checkpoint
        self.training_steps = int(1000e3)  # Total number of training steps (ie weights update according to a batch)
        self.batch_size = 1024  # Number of parts of games to train on at each training step
        self.checkpoint_interval = int(1e3)  # Number of training steps before using the model for self-playing
        self.value_loss_weight = 0.25  # Scale the value loss to avoid overfitting of the value function, paper recommends 0.25 (See paper appendix Reanalyze)
        self.train_on_gpu = torch.cuda.is_available()  # Train on GPU if available

        self.optimizer = "SGD"  # "Adam" or "SGD". Paper uses SGD
        self.weight_decay = 1e-4  # L2 weights regularization
        self.momentum = 0.9  # Used only if optimizer is SGD

        # Exponential learning rate schedule
        self.lr_init = 0.05  # Initial learning rate
        self.lr_decay_rate = 0.1  # Set it to 1 to use a constant learning rate
        self.lr_decay_steps = 350e3



        ### Replay Buffer
        self.replay_buffer_size = int(4e5)  # Number of self-play games to keep in the replay buffer
        self.num_unroll_steps = 5  # Number of game moves to keep for every batch element
        self.td_steps = 10  # Number of steps in the future to take into account for calculating the target value
        self.PER = True  # Prioritized Replay (See paper appendix Training), select in priority the elements in the replay buffer which are unexpected for the network
        self.PER_alpha = 1  # How much prioritization is used, 0 corresponding to the uniform case, paper suggests 1

        # Reanalyze (See paper appendix Reanalyse)
        self.use_last_model_value = True  # Use the last model to provide a fresher, stable n-step value (See paper appendix Reanalyze)
        self.reanalyse_on_gpu = False



        ### Adjust the self play / training ratio to avoid over/underfitting
        self.self_play_delay = 0  # Number of seconds to wait after each played game
        self.training_delay = 0  # Number of seconds to wait after each training step
        self.ratio = None  # Desired training steps per self played step ratio. Equivalent to a synchronous version, training can take much longer. Set it to None to disable it


    def visit_softmax_temperature_fn(self, trained_steps):
        """
        Parameter to alter the visit count distribution to ensure that the action selection becomes greedier as training progresses.
        The smaller it is, the more likely the best action (ie with the highest visit count) is chosen.

        Returns:
            Positive float.
        """
        if trained_steps < 500e3:
            return 1.0
        elif trained_steps < 750e3:
            return 0.5
        else:
            return 0.25


class Game(AbstractGame):
    metadata = {"render.modes": ["human", "rgb_array"], "video.frames_per_second": 500}
    def __init__(
        self,
        training=TRAINING,
        num_balls=NUM_BALLS,
        draw_screen=DRAW_SCREEN,
        reward_by_steps=REWARD_BY_STEPS,
        total_foul_times=TOTAL_FOUL_TIMES,
        use_image_observation=USE_IMAGE_OBSERVATION,
        ):
        # initialize some constants
        self.episodes = 0
        self.total_steps = 0
        self.running = True
        
        self.training = training
        self.num_balls = num_balls
        self.draw_screen = draw_screen
        self.reward_by_steps = reward_by_steps
        self.total_foul_times = total_foul_times
        self.use_image_observation = use_image_observation

        # initialize space
        self.space = pm.Space()
        self.space.gravity = (0, 0)
        self.space.damping = 0.8
        self.space.collision_slop = 0.5
        self.space.idle_speed_threshold = 5
        self.space.sleep_time_threshold = 1e-8

        # gym environment
        self.spec = None
        self.reward_range = np.array([-1, 1])
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,))
        if self.use_image_observation:
            self.observation_space = spaces.Box(
                low=0,
                high=255,
                shape=(3, IMAGE_HEIGHT, IMAGE_WIDTH),
                dtype=np.uint8,
                )
        else:
            # ball_x, ball_y, ball_type(pocketed, solid, strips, 8-ball, cue-ball) x 16 balls
            self.table_info = np.concatenate([np.array(RAIL_POLY).flatten(), POCKET_LOCATION.flatten()])
            self.table_info = self.table_info / self.table_info.max()
            low = np.concatenate([np.array([0, 0, 0] * self.num_balls), [0] * len(self.table_info)])
            high = np.concatenate([np.array([1, 1, 1] * self.num_balls), [1] * len(self.table_info)])
            self.observation_space = spaces.Box(
                low=low,
                high=high,
                dtype=np.float32,
                )
        
        # speed of the env
        self.dt = 7
        self.step_size = 0.2
        if not TRAINING:
            self.step_size = 0.15

        # initialize pygame
        pg.init()
        self.screen = pg.display.set_mode((int(WIDTH * ZOOM_MULTIPLIER), int(HEIGHT * ZOOM_MULTIPLIER)))
        self.clock = pg.time.Clock()

        # render the game
        self.draw_options = pygame_util.DrawOptions(self.screen)

        # 1 --> ball, 2 --> pocket, 3 --> rail
        self.ball_collision_handler = self.space.add_collision_handler(1, 1)
        self.ball_collision_handler.begin = self.ball_contacted
        self.pocket_collision_handler = self.space.add_collision_handler(1, 2)
        self.pocket_collision_handler.begin = self.ball_pocketed
        self.rail_collision_handler = self.space.add_collision_handler(1, 3)
        self.rail_collision_handler.begin = self.rail_contacted
        self.reset()

    @property
    def unwrapped(self):
        return self

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def legal_actions(self):
        """
        Should return the legal actions at each turn, if it is not available, it can return
        the whole action space. At each turn, the game have to be able to handle one of returned actions.
        
        For complex game where calculating legal moves is too long, the idea is to define the legal actions
        equal to the action space but to return a negative reward if the action is illegal.        

        Returns:
            An array of integers, subset of the action space.
        """
        return list(range(2))

    def add_table(self):
        """
        filter: unassigned, solids, cue-ball, pocket, rail
        --> 0b      0         0        0         0      0
        if change 0 to 1, means filter out the 1's
        e.g. 0b00111 means only account for unassigned and solids

        this is very complex and you won't understand hahaha
        """
        static_body = self.space.static_body
        self.rails = []
        for rail_poly in RAIL_POLY:
            rail = pm.Poly(static_body, rail_poly)
            rail.color = pg.Color(TABLE_SIDE_COLOR)
            rail.collision_type = 3
            rail.elasticity = RAIL_ELASTICITY
            rail.friction = RAIL_FRICTION
            rail.filter = pm.ShapeFilter(categories=0b00001)
            self.rails.append(rail)
        
        self.pockets = []
        for pocket_loc in POCKET_LOCATION:
            pocket = pm.Circle(static_body, POCKET_RADIUS, pocket_loc.tolist())
            pocket.color = pg.Color(BLACK)
            pocket.collision_type = 2
            pocket.elasticity = 0
            pocket.friction = 0
            pocket.filter = pm.ShapeFilter(categories=0b00010)
            self.pockets.append(pocket)
                    
        self.space.add(*self.rails, *self.pockets)
    
    def add_balls(self):
        # 0 -> cue-ball, 1-7 --> solids, 8 --> 8-ball, 9-15 -- strips
        self.balls = []
        positions = []
        for i in range(self.num_balls):
            intertia = pm.moment_for_circle(BALL_MASS, 0, BALL_RADIUS, offset=(0, 0))
            ball_body = pm.Body(BALL_MASS, intertia)
            
            # initialize ball at random position
            if self.num_balls < 9:
                ball_body.position = random.choice(HANGING_BALL_LOCATION).tolist()
            else:
                ball_body.position = random.randint(RAIL_DISTANCE * 2, WIDTH * ZOOM_MULTIPLIER - RAIL_DISTANCE * 2), random.randint(RAIL_DISTANCE * 2, HEIGHT * ZOOM_MULTIPLIER - RAIL_DISTANCE * 2)

            # if overlap with another ball, choose a different location
            while 1:
                for pos in positions:
                    if distance_between_two_points(ball_body.position, pos) < BALL_RADIUS * 2:
                        break
                else:
                    break
                if self.num_balls < 9:
                    ball_body.position = random.choice(HANGING_BALL_LOCATION).tolist()
                else:
                    ball_body.position = random.randint(RAIL_DISTANCE * 2, WIDTH * ZOOM_MULTIPLIER - RAIL_DISTANCE * 2), random.randint(RAIL_DISTANCE * 2, HEIGHT * ZOOM_MULTIPLIER - RAIL_DISTANCE * 2)

            ball = pm.Circle(ball_body, BALL_RADIUS, offset=(0, 0))
            ball.elasticity = BALL_ELASTICITY
            ball.friction = BALL_FRICTION
            ball.collision_type = 1
            ball.number = i
            ball.filter = pm.ShapeFilter(categories=0b00100)

            # separate ball types
            # observation_number: pocketed 0, solid 1, strips 2, 8-ball 3, cue-ball 4
            if i == 0:
                ball.color = pg.Color(WHITE)
                ball.observation_number = 4
                self.cue_ball = ball
            elif i < 8:
                ball.color = pg.Color(SOLIDS_COLOR)
                ball.observation_number = 1
                ball.filter = pm.ShapeFilter(categories=0b01000)
            elif i == 8:
                ball.color = pg.Color(BLACK)
                ball.observation_number = 3
            else:
                ball.color = pg.Color(STRIPS_COLOR)
                ball.observation_number = 2
            
            positions.append(ball_body.position)
            self.balls.append(ball)
            self.space.add(ball, ball_body)

    @staticmethod
    def ball_contacted(arbiter, space, data):
        cb, bs = {data["cue_ball"]}, set(arbiter.shapes)

        if bs.issuperset(cb):
            if data["pocket_tracking"]["cue_ball_first_contact"] is None:
                data["pocket_tracking"]["cue_ball_first_contact"] = 1

            other_ball = bs.difference(cb).pop()
            if data["pocket_tracking"]["first_contacted_ball"] is None:
                data["pocket_tracking"]["first_contacted_ball"] = other_ball
        return True
    
    @staticmethod
    def ball_pocketed(arbiter, space, data):
        # arbiter: [ball, pocket]
        ball, pocket = arbiter.shapes
        data["potted_balls"].append(ball.number)

        if ball.number == 0:
            if data["pocket_tracking"]["cue_ball_first_contact"] is None:
                data["pocket_tracking"]["cue_ball_first_contact"] = 2
            data["pocket_tracking"]["cue_ball_pocketed"] = True
        elif ball.number == 8:
            # check for solids winning
            data["pocket_tracking"]["black_ball_pocketed"] = True
            if any([b.number >= 1 and b.number <= 7 for b in data["balls"]]):
                data["pocket_tracking"]["is_won"] = False
            else:
                data["pocket_tracking"]["is_won"] = True
        elif 1 <= ball.number <= 7:
            data["pocket_tracking"]["total_potted_balls"] += 1

        data["balls"].remove(ball)
        space.remove(ball, ball.body)
        return False

    @staticmethod
    def rail_contacted(arbiter, space, data):
        ball, rail = arbiter.shapes

        if ball.number == 0 and data["pocket_tracking"]["cue_ball_first_contact"] is None:
            data["pocket_tracking"]["cue_ball_first_contact"] = 3
        
        return True

    def redraw_screen(self):
        self.screen.fill(pg.Color(TABLE_COLOR))
        self.space.debug_draw(self.draw_options)

        pg.display.flip()
        self.clock.tick(FPS)

    def process_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_q:
                self.running = False
    
    def process_action(self, action):
        return (np.array(action) * VELOCITY_LIMIT).tolist()

    def process_observation(self):
        if self.use_image_observation:
            img = pg.surfarray.array3d(self.screen)
            img = cv2.resize(img, (IMAGE_WIDTH, IMAGE_HEIGHT))
            img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
            img = cv2.flip(img, 0)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #cv2.imshow("", img)
            #cv2.waitKey(1)
            return img.reshape(3, IMAGE_HEIGHT, IMAGE_WIDTH) / 255
        else:
            # observation_number: pocketed 0, solid 1, strips 2, 8-ball 3, cue-ball 4
            width_multiplier = (IMAGE_WIDTH / (WIDTH * ZOOM_MULTIPLIER)) / IMAGE_WIDTH
            height_multiplier = (IMAGE_HEIGHT / (HEIGHT * ZOOM_MULTIPLIER)) / IMAGE_HEIGHT
            obs = np.array([
                np.array([x.body.position[0] * width_multiplier, 
                x.body.position[1] * height_multiplier, 
                x.observation_number / 4]) 
                for x in self.balls])

            balls_to_fill = self.num_balls - len(self.balls)
            if len(self.balls) == 0:
                # if no balls on table
                obs = np.repeat(np.array([0, 0, 0]), balls_to_fill, axis=0).reshape(balls_to_fill, 3).flatten()
            if balls_to_fill > 0:
                # if some balls are pocketed
                obs = np.vstack((obs, np.repeat(np.array([0, 0, 0]), balls_to_fill, axis=0).reshape(balls_to_fill, 3))).flatten()
            else:
                obs = obs.flatten()
            obs = np.concatenate([obs, self.table_info])
            return obs
    
    def process_reward(self, reward=None):
        # normalizing the reward to range(-1, 1)
        if reward is None:
            reward = self.reward
        if self.reward_by_steps:
            return np.clip((reward / 50) * 2 - 1, -1, 1)
        else:
            return np.clip((reward / 500) * 2 - 1, -1, 1)
    
    def render(self):
        pass

    def step(self, action, *args, **kwargs):
        # waiting for all balls to stop
        action = self.process_action(action)
        self.cue_ball.body.activate()
        pm.Body.update_velocity(self.cue_ball.body, action, damping=0, dt=1)

        # reset some constants
        done = False
        info = {}
        if self.reward_by_steps:
            self.reward = 7
        self.potted_balls.clear()
        closest_ball_dist = 1e6
        closest_pocket_dist = 1e6
        self.pocket_tracking["cue_ball_pocketed"] = False
        self.pocket_tracking["first_contacted_ball"] = None
        self.pocket_tracking["cue_ball_first_contact"] = None
        while self.running:
            # check if all balls stopped
            for ball in self.balls:
                if not ball.body.is_sleeping:
                    break
            else:
                break

            # reward for how close cue_ball to ball and ball to pocket
            fcb = self.pocket_tracking["first_contacted_ball"]
            if fcb is None:
                # filter out everything but balls
                bl = self.space.point_query_nearest(tuple(self.cue_ball.body.position), 1e3, pm.ShapeFilter(mask=pm.ShapeFilter.ALL_MASKS() ^ 0b10111))
                if bl is not None:
                    closest_ball_dist = min(bl.distance, closest_ball_dist)
            elif 1 <= fcb.number <= 7:
                # filter out everything but pockets
                poc = self.space.point_query_nearest(tuple(fcb.body.position), 1e3, pm.ShapeFilter(mask=pm.ShapeFilter.ALL_MASKS() ^ 0b11101))
                if poc is not None:
                    closest_pocket_dist = min(poc.distance, closest_pocket_dist)

            # step through
            if not self.training:
                self.process_events()
                if self.draw_screen:
                    self.redraw_screen()
                self.space.step(self.step_size / self.dt)
            else:
                for _ in range(self.dt):
                    self.space.step(self.step_size / self.dt)
        
        # rewarding
        fcb = self.pocket_tracking["first_contacted_ball"]
        if fcb is not None and 1 <= fcb.number <= 7:
            pck_arr = np.array(self.potted_balls)
            if any(pck_arr[(pck_arr >= 1) & (pck_arr <= 7)]):
                # potted the correct ball
                self.score_tracking["foul_count"] = 0
                self.score_tracking["touch_count"] += 1
                self.score_tracking["pot_count"] += 1
                if self.reward_by_steps:
                    self.reward += 35
                else:
                    self.reward += 40
            else:
                # touched the correct ball
                # although didn't pot ball, still reward by how close ball gets to the pocket
                self.score_tracking["foul_count"] = 0
                self.score_tracking["touch_count"] += 1
                self.reward += 5 + 55 / np.sqrt(closest_pocket_dist)
        else:
            # touched the wrong ball or not touching anything at all
            # although fouled, still reward by how close it gets to the ball
            self.score_tracking["foul_count"] += 1
            self.score_tracking["total_foul"] += 1
            self.score_tracking["touch_count"] = 0
            self.reward += -5 + 25 / np.sqrt(closest_ball_dist)
        
        # if cue ball touch the rail first, subtract the reward
        if self.pocket_tracking["cue_ball_first_contact"] == 3:
            self.reward -= 2

        # total episode reward
        if self.reward_by_steps:
            self.episode_reward.append(self.process_reward())

        # only cue ball left
        if self.num_balls < 9 and len(self.balls) < 2 and self.cue_ball in self.balls:
            self.pocket_tracking["black_ball_pocketed"] = True
            self.pocket_tracking["is_won"] = True
        
        # check endgame condition
        if self.pocket_tracking["black_ball_pocketed"] or self.score_tracking["total_foul"] > self.total_foul_times:
            self.episodes += 1
            done = True
            if self.pocket_tracking["is_won"] and not self.pocket_tracking["cue_ball_pocketed"]:
                if self.reward_by_steps:
                    self.reward = 50
                    self.episode_reward.append(self.process_reward())
                else:
                    self.reward = 500
                
            if not self.reward_by_steps:
                pg.display.set_caption(f"FPS: {self.clock.get_fps():.0f}   REWARD: {self.process_reward():.3f}   POTTED_BALLS: {self.pocket_tracking['total_potted_balls']}   STEPS: {self.episode_steps}   TOTAL_STEPS: {self.total_steps}   EPISODES: {self.episodes}   ACTION: {np.array(action, dtype=int)}")
            else:
                pg.display.set_caption(f"FPS: {self.clock.get_fps():.0f}   TOT_REWARD: {np.sum(self.episode_reward):.2f}   POTTED_BALLS: {self.pocket_tracking['total_potted_balls']}   STEPS: {self.episode_steps}   TOTAL_STEPS: {self.total_steps}   EPISODES: {self.episodes}   ACTION: {np.array(action, dtype=int)}")

        if not self.training:
            pg.display.set_caption(f"FPS: {self.clock.get_fps():.0f}   REWARD: {self.process_reward():.3f}   POTTED_BALLS: {self.pocket_tracking['total_potted_balls']}   STEPS: {self.episode_steps}   TOTAL_STEPS: {self.total_steps}   EPISODES: {self.episodes}   ACTION: {np.array(action, dtype=int).tolist()}")

        # end the game if too many steps
        if self.episode_steps > 100:
            done = True
            self.reward = 0

        # prepare observation
        self.process_events()
        if self.draw_screen:
            self.redraw_screen()
        
        self.episode_steps += 1
        self.total_steps += 1

        # adding cue ball back to table if potted
        if self.pocket_tracking["cue_ball_pocketed"]:
            self.space.add(self.cue_ball.body, self.cue_ball)
            self.balls.append(self.cue_ball)

            pm.Body.update_velocity(self.cue_ball.body, (0, 0), damping=0, dt=1)
            self.cue_ball.body.position = random.randint(RAIL_DISTANCE * 2, WIDTH * ZOOM_MULTIPLIER - RAIL_DISTANCE * 2), random.randint(RAIL_DISTANCE * 2, HEIGHT * ZOOM_MULTIPLIER - RAIL_DISTANCE * 2)
            self.cue_ball.body.activate()

        return self.process_observation(), self.process_reward(), done, info


    def reset(self, *args, **kwargs):
        for x in self.space.shapes:
            try:
                self.space.remove(x)
                self.space.remove(x.body)
            except AssertionError:
                pass

        self.add_table()
        self.add_balls()

        self.reward = self.total_foul_times * 5
        self.episode_reward = []
        self.potted_balls = []
        self.episode_steps = 0
        self.starting_time = time.time()
        self.score_tracking = {
            "foul_count": 0,
            "touch_count": 0,
            "pot_count": 0,
            "total_foul": 0
        }
        self.pocket_tracking = {
            "cue_ball_pocketed": False,
            "black_ball_pocketed": False,
            "is_won": None,
            "cue_ball_first_contact": None, # 1 --> ball, 2 --> pocket, 3 --> rail
            "first_contacted_ball": None,
            "total_potted_balls": 0,
        }

        self.ball_collision_handler.data["cue_ball"] = self.cue_ball
        self.ball_collision_handler.data["pocket_tracking"] = self.pocket_tracking

        self.pocket_collision_handler.data["balls"] = self.balls
        self.pocket_collision_handler.data["potted_balls"] = self.potted_balls
        self.pocket_collision_handler.data["pocket_tracking"] = self.pocket_tracking

        self.rail_collision_handler.data["pocket_tracking"] = self.pocket_tracking

        self.process_events()
        if self.draw_screen:
            self.redraw_screen()
        return self.process_observation()

    def run(self, model=None):
        observation = self.reset()
        while self.running:
            if model is not None:
                velocity = model.predict(observation)[0].tolist()
            else:
                velocity = (random.uniform(0, 1), random.uniform(0, 1))
            observation, reward, done, info = self.step(velocity)
            # whether use space to move through each step
            """ while 1:
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                        break
                else:
                    continue
                break"""
            if done:
                if self.pocket_tracking["is_won"] and not self.pocket_tracking["cue_ball_pocketed"]:
                    print("WIN !!")
                else:
                    print("LOSE!!")
                self.reset()

    def close(self):
        pg.quit()

def main():
    pool = PoolEnv()
    pool.run()

if __name__ == '__main__':
    main()
# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from __future__ import division
import cv2
import gym
import numpy as np
from collections import deque
from gym.wrappers import TimeLimit

from pool_game.envs.pool_env import PoolEnv


def create_env(env_id, args):
    # env = gym.make(env_id)
    env = PoolEnv()
    env = TimeLimit(env, env.max_episode_steps)
    env = frame_stack(env, args)
    return env


def process_frame(frame):
    # image_h = 100
    frame = frame.astype(np.float32)
    frame = frame / 255

    # frame = frame.reshape(1, int(image_h * (1120  /620)), image_h)

    return frame

class frame_stack(gym.Wrapper):
    def __init__(self, env, args):
        super(frame_stack, self).__init__(env)
        self.stack_frames = args.stack_frames
        self.frames = deque([], maxlen=self.stack_frames)
        self.obs_norm = process_frame #NormalizedEnv() alternative or can just not normalize observations as environment is already kinda normalized

    def reset(self):
        ob = self.env.reset()
        ob = np.float32(ob)
        ob = self.obs_norm(ob)
        for _ in range(self.stack_frames):
            self.frames.append(ob)
        return self.observation()

    def step(self, action):
        ob, rew, done, info = self.env.step(action)
        ob = np.float32(ob)
        ob = self.obs_norm(ob)
        self.frames.append(ob)
        return self.observation(), rew, done, info

    def observation(self):
        assert len(self.frames) == self.stack_frames
        # print(np.stack(self.frames, axis=0).shape)
        return np.stack(self.frames, axis=0)


class MaxMinFilter():
    def __init__(self):
        self.mx_d = 3.15
        self.mn_d = -3.15
        self.new_maxd = 10.0
        self.new_mind = -10.0

    def __call__(self, x):
        print(x)
        obs = x.clip(self.mn_d, self.mx_d)
        new_obs = (((obs - self.mn_d) * (self.new_maxd - self.new_mind)
                    ) / (self.mx_d - self.mn_d)) + self.new_mind
        return new_obs


class NormalizedEnv():
    def __init__(self):
        self.state_mean = 0
        self.state_std = 0
        self.alpha = 0.9999
        self.num_steps = 0

    def __call__(self, observation):
        
        self.num_steps += 1
        self.state_mean = self.state_mean * self.alpha + \
            observation.mean() * (1 - self.alpha)
        self.state_std = self.state_std * self.alpha + \
            observation.std() * (1 - self.alpha)

        unbiased_mean = self.state_mean / (1 - pow(self.alpha, self.num_steps))
        unbiased_std = self.state_std / (1 - pow(self.alpha, self.num_steps))

        return (observation - unbiased_mean) / (unbiased_std + 1e-8)

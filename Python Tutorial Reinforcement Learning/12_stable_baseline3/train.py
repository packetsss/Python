#%%
from pool_game.envs.pool_env import PoolEnv

import os
import gym
import numpy as np
import pygame as pg
from gym.wrappers import TimeLimit

from stable_baselines3 import DDPG, DQN, PPO, SAC, TD3
from stable_baselines3.common.callbacks import BaseCallback, CheckpointCallback
#%%
# env = gym.make("BipedalWalker-v3")
env = PoolEnv()
env = TimeLimit(env, env.max_episode_steps)
#%%
model = PPO("MlpPolicy", env, verbose=1, device="cuda")
# checkpoint_callback = CheckpointCallback(save_freq=2000, save_path='models/', name_prefix='rl_model')
#%%
# model = SAC.load("models/pool_model", env=env)
# model.learning_starts = 10
# model.device = "cuda"
# env.reset()
#%%
for x in range(50):
    model.learn(total_timesteps=2000, log_interval=8)
    model.save(f"models/pool_model_{x}")

#%%
# obs = env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs, deterministic=True)
#     obs, reward, done, info = env.step(action)
#     env.render()
#     if done:
#         obs = env.reset()

# env.close()
#%%
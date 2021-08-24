#%%
from pool_game.envs.pool_env import PoolEnv

import pygame as pg
import os
import gym
import numpy as np

from stable_baselines3 import PPO, SAC, TD3
from stable_baselines3.common.callbacks import BaseCallback, CheckpointCallback
from stable_baselines3.common.results_plotter import load_results, ts2xy
#%%
# env = gym.make("BipedalWalker-v3")
env = PoolEnv()
#%%
model = SAC("MlpPolicy", env, verbose=1, learning_rate=0.0006)
checkpoint_callback = CheckpointCallback(save_freq=2000, save_path='models/', name_prefix='rl_model')
#%%
model.learn(total_timesteps=50000, callback=checkpoint_callback)

#%%
obs = env.reset()
for i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()

env.close()
#%%
# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from pool_game.envs.pool_env import PoolEnv

import pygame as pg
import os
import gym
import numpy as np

game = PoolEnv()
game.reset()

while 1:
    vx, vy = float(input("vx: ")), float(input("vy: "))
    game.step(np.array([vx, vy]))
    
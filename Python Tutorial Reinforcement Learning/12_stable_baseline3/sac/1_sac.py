#%%
import gym
import time
import numpy as np
from stable_baselines3 import SAC

#%%
env = gym.make("BipedalWalker-v3")

model = SAC(
    env=env,
    policy="MlpPolicy",
    device="cuda",
    buffer_size=500000,
    learning_starts=10000,
    batch_size=1000,
    optimize_memory_usage=True,
    verbose=2,
)

#%%
model.learn(total_timesteps=100000)

#%%
obs = env.reset()
for i in range(2000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()
    time.sleep(0.01)
# %%
model.save("sac")

# %%

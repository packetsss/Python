#%%
import os
import gym
import pybullet as p
import numpy as np
import pybullet_envs
from gym import wrappers
from models import Agent
from utils import plot_learning_curve


env = gym.make('InvertedPendulumBulletEnv-v0')
agent = Agent(input_dims=env.observation_space.shape, env=env,
        n_actions=env.action_space.shape[0])

# uncomment this line and do a mkdir tmp && mkdir tmp/video if you want to
# record video of the agent playing the game.
# env = wrappers.Monitor(env, os.path.join(os.path.dirname(os.path.realpath(__file__)), 'videos/'), video_callable=lambda episode_id: True, force=True)
filename = 'inverted_pendulum.png'
figure_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'plots/' + filename)

best_score = env.reward_range[0]
score_history = []
#%%
n_games = 5

load_checkpoint = True
if load_checkpoint:
    agent.load_models()
    env.render(mode='human')
#%%
for i in range(n_games):
    observation = env.reset()
    done = False
    score = 0
    while not done:
        action = agent.choose_action(observation)
        observation_, reward, done, info = env.step(action)
        score += reward
        agent.remember(observation, action, reward, observation_, done)
        agent.learn()
        observation = observation_
        
        # p.stepSimulation()
        physicsClient = p.connect(p.DIRECT)
        env.render(mode='human')
        p.disconnect(physicsClient)
        
        
    score_history.append(score)
    avg_score = np.mean(score_history[-100:])

    if avg_score > best_score:
        best_score = avg_score
        agent.save_models()

    print('episode ', i, 'score %.1f' % score, 'avg_score %.1f' % avg_score)

if not load_checkpoint:
    x = [i+1 for i in range(n_games)]
    plot_learning_curve(x, score_history, figure_file)

# %%

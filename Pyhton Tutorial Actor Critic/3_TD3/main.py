#%%
import os
import gym
import numpy as np
from models import Agent
from utils import plot_learning_curve

#env = gym.make('LunarLanderContinuous-v2')
#env = gym.make('Pendulum-v0')
env = gym.make('BipedalWalker-v3')

agent = Agent(alpha=0.001, beta=0.001,
    input_dims=env.observation_space.shape, tau=0.005,
    env=env, batch_size=100, layer1_size=400, layer2_size=300,
    n_actions=env.action_space.shape[0])

#%%
n_games = 1000
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'plots/' + 'walker_' + str(n_games) + '_games.png')

best_score = env.reward_range[0]
score_history = []

#%%
agent.load_models()

#%%
for i in range(n_games):
    observation = env.reset()
    done = False
    score = 0
    ct = 0
    while not done:
        action = agent.choose_action(observation)
        observation_, reward, done, info = env.step(action)
        agent.remember(observation, action, reward, observation_, done)
        agent.learn()
        score += reward
        observation = observation_
        env.render()
        ct += 1
        if ct % 50 == 0:
            print(f"score: {score:04f}")
        if -60 < score < -30:
            score -= 100
            break

    print(f"score: {score:04f}")
    score_history.append(score)
    avg_score = np.mean(score_history[-10:])

    if avg_score > best_score:
        best_score = avg_score
        agent.save_models()

    print('episode ', i, 'score %.1f' % score, 'average score %.1f' % avg_score)

x = [i+1 for i in range(n_games)]
plot_learning_curve(x, score_history, filename)

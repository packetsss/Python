#%%
import os
import gym
import numpy as np
from models import Agent
from utils import plot_learning_curve

env = gym.make('CartPole-v0')
N = 20
batch_size = 5
n_epochs = 4
alpha = 0.0003
agent = Agent(n_actions=env.action_space.n, input_dims=env.observation_space.shape, batch_size=batch_size, alpha=alpha, n_epochs=n_epochs)

figure_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'plots/cartpole.png')

best_score = env.reward_range[0]
score_history = []
#%%
agent.load_models()

#%%
n_games = 300
learn_iters = 0
avg_score = 0
n_steps = 0

for i in range(n_games):
    observation = env.reset()
    done = False
    score = 0
    while not done:
        action, prob, val = agent.choose_action(observation)
        observation_, reward, done, info = env.step(action)
        n_steps += 1
        score += reward
        agent.remember(observation, action, prob, val, reward, done)
        if n_steps % N == 0:
            agent.learn()
            learn_iters += 1
        observation = observation_
        env.render()
        
    score_history.append(score)
    avg_score = np.mean(score_history[-100:])

    if avg_score > best_score:
        best_score = avg_score
        agent.save_models()

    print('episode', i, 'score %.1f' % score, 'avg score %.1f' % avg_score,
            'time_steps', n_steps, 'learning_steps', learn_iters)
x = [i+1 for i in range(len(score_history))]
plot_learning_curve(x, score_history, figure_file)

# %%

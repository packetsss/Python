"""
create a ppo algorithm using pytorch and comment on everything
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import gym
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import time
import os
import torch.distributions as D
from torch.distributions import Categorical
from torch.utils.data.sampler import BatchSampler, SubsetRandomSampler

# hyperparameters
gamma = 0.99
learning_rate = 0.0005
lmbda = 0.95
eps_clip = 0.1
K_epoch = 3
T_horizon = 20

# parameters for the policy and baseline models
hidden_size = 256

# make model
class MLP(nn.Module):
    def __init__(self, input_dim, hidden_size, output_dim):
        super(MLP, self).__init__()

        self.fc1 = nn.Linear(input_dim, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_dim)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class Policy(nn.Module):
    def __init__(self, input_dim, hidden_size, output_dim):
        super(Policy, self).__init__()

        self.fc1 = nn.Linear(input_dim, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_dim)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.softmax(self.fc3(x), dim=1)
        return x

class Baseline(nn.Module):
    def __init__(self, input_dim, hidden_size, output_dim):
        super(Baseline, self).__init__()

        self.fc1 = nn.Linear(input_dim, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_dim)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class Agent():
    def __init__(self, input_dim, hidden_size, output_dim, lr, gamma, K_epoch, eps_clip):
        self.lr = lr
        self.input_dim = input_dim
        self.hidden_size = hidden_size
        self.output_dim = output_dim
        self.gamma = gamma
        self.eps_clip = eps_clip
        self.K_epoch = K_epoch

        self.policy = Policy(input_dim, hidden_size, output_dim)
        self.policy_optimizer = optim.Adam(self.policy.parameters(), lr=lr)

        self.baseline = Baseline(input_dim, hidden_size, 1)
        self.baseline_optimizer = optim.Adam(self.baseline.parameters(), lr=lr)

    def select_action(self, state):
        state = torch.from_numpy(state).float().unsqueeze(0)
        probs = self.policy(state)
        m = Categorical(probs)
        action = m.sample()
        log_prob = m.log_prob(action)
        return action.item(), log_prob

    def update(self, rewards, log_probs, state_values):
        discounted_rewards = []

        for t in range(len(rewards)):
            Gt = 0
            pw = 0
            for r in rewards[t:]:
                Gt = Gt + self.gamma**pw * r
                pw = pw + 1
            discounted_rewards.append(Gt)

        discounted_rewards = torch.tensor(discounted_rewards)
        discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / (discounted_rewards.std() + 1e-9) # normalize discounted rewards

        policy_loss = []
        for log_prob, Gt in zip(log_probs, discounted_rewards):
            policy_loss.append(-log_prob * Gt)

        policy_loss = torch.cat(policy_loss).sum()

        self.policy_optimizer.zero_grad()
        policy_loss.backward()
        self.policy_optimizer.step()

        baseline_loss = []
        for log_prob, Gt, Vt in zip(log_probs, discounted_rewards, state_values):
            baseline_loss.append((Gt - Vt)**2)

        baseline_loss = torch.cat(baseline_loss).sum()

        self.baseline_optimizer.zero_grad()
        baseline_loss.backward()
        self.baseline_optimizer.step()

    def train(self, env, episodes):
        total_rewards = []

        for episode in range(episodes):
            state = env.reset()
            log_probs = []
            rewards = []
            state_values = []

            for steps in range(T_horizon):
                action, log_prob = self.select_action(state)
                new_state, reward, done, _ = env.step(action)

                log_probs.append(log_prob)
                rewards.append(reward)
                state_values.append(self.baseline(torch.from_numpy(state).float()).squeeze(0))

                if done:
                    break

                state = new_state

            total_rewards.append(np.sum(rewards))
            self.update(rewards, log_probs, state_values)

            if episode % 10 == 0:
                print('Episode: {}/{} || Reward: {}  Steps: {}'.format(episode, episodes, total_rewards[-1], steps))

        return total_rewards

if __name__ == '__main__':
    env = gym.make('CartPole-v1')
    agent = Agent(env.observation_space.shape[0], hidden_size, env.action_space.n, learning_rate, gamma, K_epoch, eps_clip)
    rewards = agent.train(env, episodes=200)

    plt.plot(rewards)
    plt.show()
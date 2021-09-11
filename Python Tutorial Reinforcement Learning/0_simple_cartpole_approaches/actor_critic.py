# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited


import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import gym

class Actor(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(Actor, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, output_dim)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.softmax(x, dim=1)

class Critic(nn.Module):
    def __init__(self, input_dim):
        super(Critic, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

class A2C:
    def __init__(self, env):
        self.env = env
        self.actor = Actor(env.observation_space.shape[0], env.action_space.n)
        self.critic = Critic(env.observation_space.shape[0])
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=1e-3)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=1e-3)

    def get_action(self, state):
        state = torch.from_numpy(state).float().unsqueeze(0)
        probs = self.actor(state)
        dist = torch.distributions.Categorical(probs)
        action = dist.sample()
        return action.item()

    def compute_loss(self, trajectory):
        states = torch.FloatTensor([sars[0] for sars in trajectory])
        actions = torch.LongTensor([sars[1] for sars in trajectory]).view(-1, 1)
        rewards = torch.FloatTensor([sars[2] for sars in trajectory])
        next_states = torch.FloatTensor([sars[3] for sars in trajectory])
        dones = torch.FloatTensor([sars[4] for sars in trajectory]).view(-1, 1)

        # compute critic loss
        Qvals = self.critic(states)
        next_Qvals = self.critic(next_states)
        Qprime = rewards + (1 - dones) * 0.99 * next_Qvals
        critic_loss = F.mse_loss(Qvals, Qprime)

        # compute actor loss
        log_probs = torch.log(self.actor(states))
        actor_loss = -1 * torch.sum(torch.gather(log_probs, 1, actions))

        return actor_loss, critic_loss

    def update(self, trajectory):
        actor_loss, critic_loss = self.compute_loss(trajectory)

        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

    def train(self, max_episodes=1000):
        avg_reward = 0
        for episode in range(max_episodes):
            state = self.env.reset()
            trajectory = []
            episode_reward = 0
            while True:
                action = self.get_action(state)
                next_state, reward, done, _ = self.env.step(action)
                trajectory.append((state, action, reward, next_state, done))
                episode_reward += reward
                if done:
                    break
                state = next_state
                self.env.render()
            self.update(trajectory)
            avg_reward += episode_reward
            if episode % 50 == 0:
                avg_reward = avg_reward / 50
                print("Episode: {} | Avg reward: {}".format(episode, avg_reward))
                avg_reward = 0

if __name__ == "__main__":
    env = gym.make("CartPole-v0")
    a2c = A2C(env)
    a2c.train()
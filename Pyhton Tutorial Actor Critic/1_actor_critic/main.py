#%%
import os
import gym
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import tensorflow.keras as keras
import tensorflow_probability as tfp
from utils import plot_learning_curve
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

#%%
class ActorCriticNetwork(keras.Model):
    def __init__(self, n_actions, fc1_dims=1024, fc2_dims=512, fc3_dims=256, name="actor_critic", ckpt_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "actor_critic")):
        super(ActorCriticNetwork, self).__init__()
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims
        self.fc3_dims = fc3_dims
        self.n_actions = n_actions
        self.model_name = name
        self.ckpt_dir = ckpt_dir
        self.ckpt_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.join(self.ckpt_dir, name + "_ac"))

        self.fc1 = Dense(self.fc1_dims, activation="relu")
        self.fc2 = Dense(self.fc2_dims, activation="relu")
        self.fc3 = Dense(self.fc3_dims, activation="relu")
        self.value = Dense(1, activation=None)

        # Probabilities to action
        self.pi = Dense(n_actions, activation="softmax")

    def call(self, state):
        value = self.fc1(state)
        value = self.fc2(value)
        value = self.fc3(value)

        v = self.value(value)
        pi = self.pi(value)

        return v, pi
# %%
class Agent:
    def __init__(self, alpha=0.0003, gamma=0.99, n_actions=2):
        self.gamma = gamma
        self.n_actions = n_actions
        self.action = None
        self.action_space = [i for i in range(self.n_actions)]

        self.actor_critic = ActorCriticNetwork(n_actions=n_actions)

        self.actor_critic.compile(optimizer=Adam(learning_rate=alpha))

    def choose_action(self, observation):
        # add an extra dimention
        state = tf.convert_to_tensor([observation])
        _, probs = self.actor_critic(state)

        action_probabilities = tfp.distributions.Categorical(probs=probs)
        action = action_probabilities.sample()
        self.action = action

        return action.numpy()[0]
    
    def save_models(self):
        print("Saving models...")
        self.actor_critic.save_weights(self.actor_critic.ckpt_file)

    def load_models(self):
        print("Loading models...")
        self.actor_critic.load_weights(self.actor_critic.ckpt_file)
    
    def learn(self, state, reward, state_, done):
        state = tf.convert_to_tensor([state], dtype=tf.float32)
        state_ = tf.convert_to_tensor([state_], dtype=tf.float32)
        reward = tf.convert_to_tensor(reward, dtype=tf.float32) # not fed to NN
        with tf.GradientTape() as tape:
            state_value, probs = self.actor_critic(state)
            state_value_, _ = self.actor_critic(state_)
            state_value = tf.squeeze(state_value)
            state_value_ = tf.squeeze(state_value_)

            action_probs = tfp.distributions.Categorical(probs=probs)
            log_prob = action_probs.log_prob(self.action)

            delta = reward + self.gamma * state_value_ * (1 - int(done)) - state_value
            actor_loss = -log_prob * delta
            critic_loss = delta ** 2
            total_loss = actor_loss + critic_loss

        gradient = tape.gradient(total_loss, self.actor_critic.trainable_variables)
        self.actor_critic.optimizer.apply_gradients(zip(
            gradient, self.actor_critic.trainable_variables))
# %%
def main():
    env = gym.make("CartPole-v0")
    agent = Agent(alpha=1e-5, n_actions=env.action_space.n)
    n_games = 1800

    filename = "cartpole.png"
    figure_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"plots/{filename}")

    best_score = env.reward_range[0]
    score_history = []
    load_ckpt = True

    if load_ckpt:
        agent.load_models()
    load_ckpt = False
    
    for i in range(n_games):
        done_arr = []
        observation = env.reset()
        done = False
        score = 0
        while len(done_arr) < 10:
            env.render()
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            if not load_ckpt:
                agent.learn(observation, reward, observation_, done)
            observation = observation_
            if done:
                done_arr.append(done)
        score_history.append(score)
        avg_score = np.mean(score_history[-250:])
        if avg_score > best_score:
            best_score = avg_score
            if not load_ckpt:
                agent.save_models()
        print(f"episode {i} score {score:1f}, average_score {avg_score:1f}")
        
    x = [i + 1 for i in range(n_games)]
    plot_learning_curve(x, score_history, figure_file)

# %%
if __name__ == '__main__':
    main()
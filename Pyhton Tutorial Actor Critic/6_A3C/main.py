# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import os
import gym
import torch as T
import numpy as np
import torch.multiprocessing as mp
from models import Agent, ActorCritic, SharedAdam
def run():
    env = gym.make("CartPole-v0")
    epochs = 10
    model = ActorCritic([4], 2)
    model.load_state_dict(T.load(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'a3c'), "model" +'_a3c')))
    score_history = []

    for x in range(epochs):
        done = False
        score, best_score = 0, 0
        observation = env.reset()
        model.clear_memory()
        while not done:
            action = model.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            model.remember(observation, action, reward)
            score += reward
            observation = observation_

        score_history.append(score)
        avg_score = np.mean(score_history[-100:])

        if avg_score > best_score:
            best_score = avg_score

            env.render()
    print('episode ', x, 'reward %.1f' % score, f"avg_reward {avg_score:.1f}")

def main():
    lr = 1e-4
    env_id = ['LunarLanderContinuous-v2', 'CartPole-v0', 'BipedalWalker-v3'][1]
    n_actions = 2
    input_dims = [4]
    global_actor_critic = ActorCritic(input_dims, n_actions)
    global_actor_critic.share_memory()
    optim = SharedAdam(global_actor_critic.parameters(), lr=lr, 
                        betas=(0.92, 0.999))
    global_ep = mp.Value('i', 0)

    workers = [Agent(global_actor_critic,
                    optim,
                    input_dims,
                    n_actions,
                    gamma=0.99,
                    lr=lr,
                    name=i,
                    global_ep_idx=global_ep,
                    env_id=env_id) for i in range(mp.cpu_count())]
    [w.start() for w in workers]
    [w.join() for w in workers]

if __name__ == '__main__':
    main()
    # run()
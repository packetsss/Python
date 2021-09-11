# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from sb3_contrib import QRDQN, TQC
from stable_baselines3 import A2C, DDPG, DQN, PPO, SAC, TD3

ALGOS = {
    "a2c": A2C,
    "ddpg": DDPG,
    "dqn": DQN,
    "ppo": PPO,
    "sac": SAC,
    "td3": TD3,
    # SB3 Contrib
    "qrdqn": QRDQN,
    "tqc": TQC,
}

HYPERPARAM = {
    "td3": {'policy': "CnnPolicy", 'verbose': 2, 'device': "cuda", 'optimize_memory_usage': True, 'learning_rate': 0.0003757135947910733, 'gamma': 0.9999, 'batch_size': 10000, 'buffer_size': 200000, 'learning_starts': 20000, 'tau': 0.01, 'train_freq': 16, 'action_noise': None, 'policy_kwargs': dict(net_arch=[512, 512])},

    "sac": {'policy': "CnnPolicy", 'verbose': 2, 'device': "cuda", 'optimize_memory_usage': True, 'learning_rate': 0.00073, 'gamma': 0.98, 'batch_size': 10000, 'buffer_size': 200000, 'learning_starts': 20000, 'use_sde': False, 'use_sde_at_warmup': False, 'ent_coef': "auto", 'action_noise': None},

    "ppo": {'policy': "MlpPolicy", 'verbose': 2, 'device': "cuda", 'learning_rate': 0.0002, 'gamma': 0.99, 'batch_size': 20000, 'n_steps': 2048, 'n_epochs': 10, 'ent_coef': 0.001, 'gae_lambda': 0.95, 'use_sde': True},
}
from pool import PoolEnv
from utils.config import *

import os
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv

def make_vec_env(
    n_envs=1,
    seed=None,
    start_index=0,
    monitor_dir=None,
    wrapper_class=None,
    env_kwargs=None,
    vec_env_cls=None,
    vec_env_kwargs=None,
    monitor_kwargs=None,
    wrapper_kwargs=None,
):
    env_kwargs = {} if env_kwargs is None else env_kwargs
    vec_env_kwargs = {} if vec_env_kwargs is None else vec_env_kwargs
    monitor_kwargs = {} if monitor_kwargs is None else monitor_kwargs
    wrapper_kwargs = {} if wrapper_kwargs is None else wrapper_kwargs

    def make_env(rank):
        def _init():
            env = PoolEnv(num_balls=NUM_BALLS)
            if seed is not None:
                env.seed(seed + rank)
                env.action_space.seed(seed + rank)
            monitor_path = os.path.join(monitor_dir, str(rank)) if monitor_dir is not None else None
            if monitor_path is not None:
                os.makedirs(monitor_dir, exist_ok=True)
            env = Monitor(env, filename=monitor_path, **monitor_kwargs)
            if wrapper_class is not None:
                env = wrapper_class(env, **wrapper_kwargs)
            return env

        return _init

    if vec_env_cls is None:
        vec_env_cls = DummyVecEnv

    return vec_env_cls([make_env(i + start_index) for i in range(n_envs)], **vec_env_kwargs)
from gym.envs.registration import register

register(
    id='PoolGame-v0',
    entry_point='gym_foo.envs:FooEnv',
)
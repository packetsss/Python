# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from gym.envs.registration import register

register(
    id='PoolGame-v0',
    entry_point='gym_foo.envs:FooEnv',
)
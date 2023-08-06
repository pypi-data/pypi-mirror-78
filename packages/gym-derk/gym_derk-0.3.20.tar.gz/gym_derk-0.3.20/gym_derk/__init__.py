from gym.envs.registration import register

register(
    id='derk-v0',
    entry_point='gym_derk.envs:DerkEnv',
)
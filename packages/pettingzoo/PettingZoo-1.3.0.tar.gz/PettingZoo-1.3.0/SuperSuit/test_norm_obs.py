from supersuit.aec_wrappers import frame_skip
import pettingzoo
from pettingzoo.mpe import simple_push_v0
import numpy as np

env = simple_push_v0.raw_env()
env = frame_skip(env,(2,4))
env.reset()

game_len = 0
for x in range(20000):
    #env.render()
    while True:
        reward, done, info = env.last()

        game_len += 1
        if done:

            print("finished!!!\n\n\n")

            orig_obs = env.reset()

            break

        action = env.action_spaces[env.agent_selection].sample()

        next_obs = env.step(action)
        print(env.env.steps)

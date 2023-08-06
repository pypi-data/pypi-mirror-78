from pettingzoo.atari import boxing_v0
import time
import random
#from supersuit import frame_stack
import numpy as np
import supersuit.aec_wrappers

from pettingzoo import AECEnv
from gym.spaces import Box, Discrete
import copy
from pettingzoo.utils.agent_selector import agent_selector
from pettingzoo.utils.to_parallel import ParallelEnv

# class DummyParEnv(ParallelEnv):
#     def __init__(self,observations,observation_spaces,action_spaces):
#         super().__init__()
#         self._observations = observations
#         self.observation_spaces = observation_spaces
#
#         self.agents = [x for x in observation_spaces.keys()]
#         self.num_agents = len(self.agents)
#         self._agent_selector = agent_selector(self.agents)
#         self.agent_selection = self._agent_selector.reset()
#         self.action_spaces = action_spaces
#
#         self.rewards = {a:1 for a in self.agents}
#         self.dones = {a:False for a in self.agents}
#         self.infos = {a:{} for a in self.agents}
#
#     def step(self, actions):
#         for agent,action in actions.items():
#             assert action in self.action_spaces[agent]
#         return self._observations, self.rewards, self.dones, self.infos
#
#     def reset(self):
#         return self._observations
#
#     def close(self):
#         pass
#
# base_obs = {"a{}".format(idx): np.zeros([8,8,3],dtype=np.float32) + np.arange(3) + idx for idx in range(2)}
# base_obs_space = {"a{}".format(idx): Box(low=np.float32(0.),high=np.float32(10.),shape=[8,8,3]) for idx in range(2)}
# base_act_spaces = {"a{}".format(idx): Discrete(5) for idx in range(2)}
#
#
# env = boxing_v0.parallel_env()#obs_type="rgb_image")#obs_type="grayscale_image")
# #print(env.aec_env)
# #env = supersuit.aec_wrappers.dtype(env,np.float32)
# env = supersuit.resize(env, 84, 84, False)
# env = supersuit.frame_stack(env, 4)
# env = supersuit.frame_stack(env, 4)
# env = supersuit.frame_skip(env, 4)
# env = supersuit.delay_observations(env, 5)
# #env = supersuit.aec_wrappers.dtype(env,np.uint8)
# orig_obs = env.reset()
# for i in range(10):
#     action = {agent:env.action_spaces[agent].sample() for agent in env.agents}
#
#     #action = (np.nan*np.ones(4))
#
#     next_obs,rew,done,info = env.step(action)
#     agent = env.agents[0]
    # print(next_obs[agent].shape)
    # print(np.max(next_obs[env.agents[-1]]))
# exit(0)
#print(env.observation_spaces)
#print(env.ale.getRAM().shape)
# print(env.hanabi_env.vectorized_observation_shape())
# print(env.action_spaces)
env = boxing_v0.raw_env()#obs_type="rgb_image")#obs_type="grayscale_image")
#print(env.aec_env)
#env = supersuit.aec_wrappers.dtype(env,np.float32)
env = supersuit.resize(env, 84, 84, False)
env.reset()
start = time.time()
game_len = 0
for x in range(20000):
    #env.render()
    while True:
        reward, done, info = env.last()
        # if reward != 0:
        #     print(env.rewards)
        #print(env.agent_selection+"  "+str(reward))
        #print(agent,reward)
        # if reward != 0:
        #     print("rew:",reward)
        game_len += 1
        if done:
            # for reward in env.rewards.values():
            #     if reward != 0:
            #         print("rew:",reward)
            #print("finished!!!\n\n\n")
            # print(reward)
            #print(env.rewards)
            #val = env.render()
            #print(val.shape)
            orig_obs = env.reset()
            # print(env.observe(env.agent_selection).squeeze())
            # print(env.rewards)
            break
            #game_len = 0

        # print(agent)
        # print(env.agent_selection)
        #assert agent == env.agent_selection
        # print(np.min(env.observe(env.agent_selection)))
        # print(np.max(env.observe(env.agent_selection)))
        #action = random.choice(env.infos[env.agent_selection]['legal_moves'])
        action = env.action_spaces[env.agent_selection].sample()
        env.observe(env.agent_selection)
        #action = (np.nan*np.ones(4))

        next_obs = env.step(action)
        # print(env.agent_selection)
        # print(next_obs)#s[50,50,:])
        # time.sleep(0.3)
        if game_len % 1000 == 0:
            duration = time.time() - start
            avg_time = duration / game_len
            print(avg_time)
        # if game_len % 1 == 0:
        #     env.render()
        #     time.sleep(0.2)
        #print(env.rewards)
        # assert np.all(np.less(np.sum(next_obs,axis=0),1))
        # print(next_obs)
        # print(env.observation_spaces[env.agent_selection])
        #env.render()
        #print("stepped")
        #print(next_obs)
        #print(np.transpose(next_obs,(2,0,1)))

from supersuit import pad_observations, normalize_obs, argvar
import gym
e = gym.make("Acrobot-v1")
e = normalize_obs(e)
e = normalize_obs(e)
e = pad_observations(e)

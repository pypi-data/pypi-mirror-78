class ArgVar:
    meta = "bob"
    def __init__(self):
        pass

class VarArg(ArgVar):
    meta = "bob"
    def __init__(self):
        self.meta = "joe"

print(VarArg().meta)

exit(0)
import gym
from supersuit.gym_wrappers import color_reduction, frame_stack
from supersuit.vector.gym_rollout import RolloutBuilder,transpose_rollout,split_rollouts_on_dones
from supersuit.vector.gym_rollout import RandomPolicy
from stable_baselines.common.vec_env import DummyVecEnv
def make_gym_env():
    env = gym.make('SpaceInvaders-v0')

    env = frame_stack(color_reduction(env, 'full'), 4)
    return env

num_envs = 4
envs = DummyVecEnv([make_gym_env]*num_envs)
policy = RandomPolicy(envs.action_space, num_envs)
rolloutbuilder = RolloutBuilder(envs)
rolloutbuilder.restart(policy)
n_steps = 5
obs,rew,done,infos = rolloutbuilder.rollout(policy,n_steps)
assert obs.shape[:2] == (n_steps,num_envs)
assert rew.shape == (n_steps,num_envs)
assert done.shape == (n_steps,num_envs)
tobs,trew,tdone,tinfos = transpose_rollout(obs,rew,done,infos)
assert tobs.shape[:2] == (num_envs,n_steps)
assert trew.shape == (num_envs,n_steps)
assert tdone.shape == (num_envs,n_steps)
tobs,trew,tinfos = split_rollouts_on_dones(tobs,trew,tdone,tinfos)
assert len(tobs) == num_envs
# exit(0)
# import pettingzoo.gamma
# from supersuit.aec_wrappers import color_reduction, frame_stack
#
# def make_env():
#     env = pettingzoo.gamma.pistonball_v0.env()
#
#     env = frame_stack(color_reduction(env, 'full'), 4)
#     return env
#
# envs = gym.vector.SyncVectorEnv([make_env]*4)

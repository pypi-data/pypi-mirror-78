import gym
import numpy as np
import pickle

def vec_env_args(env, num_envs):
    '''
    Returns: (list of env creator fns, observation space, action space)

    Usage:
    SyncVecEnv(*vec_env_args(env))
    '''
    def env_fn():
        return pickle.loads(pickle.dumps(env))
    return [env_fn]*num_envs, env.observation_space, env.action_space

def gym_vec_env(env, num_envs, use_multiprocessing=False):
    args = vec_env_args(env, num_envs)
    constructor = gym.vector.AsyncVectorEnv if use_multiprocessing else gym.vector.SyncVectorEnv
    return constructor(*args)

def stable_baselines_vec_env(env, num_envs, use_multiprocessing=False):
    import stable_baselines
    args = vec_env_args(env, num_envs)[:1]
    constructor = stable_baselines.common.vec_env.SubprocVecEnv if use_multiprocessing else stable_baselines.common.vec_env.DummyVecEnv
    return constructor(*args)

def stable_baselines3_vec_env(env, num_envs, use_multiprocessing=False):
    import stable_baselines3
    args = vec_env_args(env, num_envs)[:1]
    constructor = stable_baselines3.common.vec_env.SubprocVecEnv if use_multiprocessing else stable_baselines3.common.vec_env.DummyVecEnv
    return constructor(*args)

def test_vec_env_args():
    env = gym.make("Acrobot-v1")
    num_envs = 8
    vec_env = gym_vec_env(env, num_envs)
    vec_env.reset()
    obs, rew, dones, infos = vec_env.step([0]+[1]*(vec_env.num_envs-1))
    assert not np.any(np.equal(obs[0], obs[1]))

def test_all_vec_env_fns():
    num_envs = 8
    env = gym.make("Acrobot-v1")
    vec_env = gym_vec_env(env, num_envs, False)
    vec_env = gym_vec_env(env, num_envs, True)
    vec_env = stable_baselines_vec_env(env, num_envs, False)
    vec_env = stable_baselines_vec_env(env, num_envs, True)
    vec_env = stable_baselines3_vec_env(env, num_envs, False)
    vec_env = stable_baselines3_vec_env(env, num_envs, True)


if __name__ == "__main__":
    test_vec_env_args()
    test_all_vec_env_fns()

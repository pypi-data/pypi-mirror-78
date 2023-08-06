from supersuit.aec_wrappers import RewardWrapper
from collections import deque

class queuesum:
    def __init__(self):
        self.queue = deque()
        self.sum = 0
        self.size = 0
    def add(self, item):
        self.queue.append(item)
        self.sum += item
        if len(self.queue) > self.size:
            self.sum -= self.queue[0]
            self.queue.popleft()
            #assert self.sum == sum(self.queue)
        return self.sum / len(self.queue)
    def resize(self, new_size):
        assert new_size >= self.size
        self.size = new_size

class cyclic_reward_wrapper(RewardWrapper):
    def __init__(self, env, curriculum):
        '''
        The curriculum is a sorted list of tuples:
        (schedual_step, reward_steps_to_sum)
        '''
        assert curriculum == list(sorted(curriculum))
        self.curriculum = curriculum
        self.env_step = 0
        self.curriculum_step = 0
        super().__init__(env)

    def reset(self, observe=True):
        self.reward_queues = {agent:queuesum() for agent in self.agents}
        for qs in self.reward_queues.values():
            qs.resize(self.curriculum[0][1])

        return super().reset(observe)

    def _update_step(self, agent, obs):
        if self.curriculum_step < len(self.curriculum)-1 and self.env_step >= self.curriculum[self.curriculum_step+1][1]:
            self.curriculum_step += 1
            num_cycles_keep = self.curriculum[self.curriculum_step][1]
            for qs in self.reward_queues.values():
                qs.resize(num_cycles_keep)

        self.rewards = {agent: self.reward_queues[agent].add(reward) for agent,reward in self.rewards.items()}
        self.env_step += 1


from pettingzoo.sisl import pursuit_v0
def CyclicLearnerTest():
    env = pursuit_v0.env()
    env = cyclic_reward_wrapper(env, [(0,1), (10,2), (100,3), (1000,8)])
    env.reset()
    for i in range(100):
        reward, done, info = env.last()
        print(list(sorted(list(env.rewards.items()))))
        if done:
            env.reset()
        action = env.action_spaces[env.agent_selection].sample()
        next_obs = env.step(action)

if __name__ == "__main__":
    CyclicLearnerTest()

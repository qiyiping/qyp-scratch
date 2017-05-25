from __future__ import print_function
import gym
import numpy as np

class Solution(object):
    def __init__(self, env, state_size=[10, 10, 10, 10], max_episode_steps=200):
        self.env = env
        self.learning_rate = 0.1
        self.discount = 1.0
        self.epsilon = 0.5
        self.epsilon_decay = 0.99

        self.state_size = state_size
        lower_bound = [ -2.4, -3.0, -0.5, -2.0 ]
        higher_bound = [ 2.4, 3.0, 0.5, 2.0 ]
        self.state_bins = [
            np.linspace(lower_bound[i], higher_bound[i], state_size[i]-1)
            for i in range(4)
        ]

        self.strides = np.ones((4,)).astype(int)
        for i in range(1, 4):
            self.strides[i] = self.strides[i-1] * state_size[i-1]

        self.action_size = 2
        self.q_table = np.zeros((self.strides[3] * state_size[3], self.action_size,))
        self.max_episode_steps = max_episode_steps

    def discrete_state(self, state):
        "state: [cart position, cart velocity, pole angle, pole velocity in angle]"
        return sum([ np.digitize(v, self.state_bins[i]) * self.strides[i]
                     for i, v in enumerate(state) ])

    def select_action(self, state):
        v = self.q_table[state, :]
        if (np.random.rand() < self.epsilon) or (v[0] == v[1]):
            a = np.random.randint(self.action_size)
        else:
            a = np.argmax(v)
        return a

    def begin_episode(self):
        self.current_state = self.discrete_state(self.env.reset())
        self.episode = 0
        self.episode_done = False
        self.epsilon *= self.epsilon_decay

    def act(self, trainable=True):
        self.episode += 1
        action = self.select_action(self.current_state)
        s, _, done, _ = self.env.step(action)
        next_state = self.discrete_state(s)
        if trainable:
            reward = 0
            if done and self.episode < (self.max_episode_steps - 5):
                reward = -1.0
            self.q_table[self.current_state, action] += self.learning_rate * (reward + np.max(self.q_table[next_state,:]) - self.q_table[self.current_state, action])
        self.current_state = next_state
        self.episode_done = done

    def simulate(self, steps):
        self.begin_episode()
        for t in range(steps):
            self.env.render()
            self.act(trainable=False)
            # if self.episode_done:
            #     break
        return t

    def learn(self, epochs):
        print_every = 100
        steps = 0.0

        for e in range(1, epochs+1):
            self.begin_episode()
            for t in range(self.max_episode_steps+1):
                self.act(trainable=True)
                if self.episode_done:
                    break

            steps += t
            if e % print_every == 0:
                none_zero_cnt = np.sum(self.q_table != 0)
                print("epoch: {}, number of steps: {}, none zero count: {}".format(e, steps/print_every, none_zero_cnt))
                steps = 0.0

    def save(self, path):
        np.save(path, self.q_table)

    def load(self, path):
        self.q_table = np.load(path)

if __name__ == '__main__':
    import time
    env = gym.make("CartPole-v0")
    max_episode_steps = env._max_episode_steps
    env.seed(int(time.time()))
    # env = gym.wrappers.Monitor(env, "/tmp/cart-pole-experiment", force=True)

    solution = Solution(env, max_episode_steps=max_episode_steps)
    solution.learn(epochs=2000)
    solution.save("./model")
    print(solution.simulate(1000))

from __future__ import print_function
import numpy as np
from matplotlib import pyplot as plt
import gym
env = gym.make('CartPole-v0')
####################
# Observation:
#     Type: Box(4)
#     Num     Observation               Min                     Max
#     0       Cart Position             -4.8                    4.8
#     1       Cart Velocity             -Inf                    Inf
#     2       Pole Angle                -0.418 rad (-24 deg)    0.418 rad (24 deg)
#     3       Pole Angular Velocity     -Inf                    Inf
# Actions:
#     Type: Discrete(2)
#     Num   Action
#     0     Push cart to the left
#     1     Push cart to the right
#     Note: The amount the velocity that is reduced or increased is not
#     fixed; it depends on the angle the pole is pointing. This is because
#     the center of gravity of the pole increases the amount of energy needed
#     to move the cart underneath it
# Reward:
#     Reward is 1 for every step taken, including the termination step
# Starting State:
#     All observations are assigned a uniform random value in [-0.05..0.05]
# Episode Termination:
#     Pole Angle is more than 12 degrees.
#     Cart Position is more than 2.4 (center of the cart reaches the edge of
#     the display).
#     Episode length is greater than 200.
#     Solved Requirements:
#     Considered solved when the average return is greater than or equal to
#     195.0 over 100 consecutive trials.
####################

# Q learning
# position, velocity, angle, angle velocity
state_size = np.array([20, 20, 20, 20])
lower_bound = np.array([-0.5, -2, -0.1, -2])
upper_bound = np.array([0.5, 2, 0.1, 2])

def to_state(observation):
    s = (observation - lower_bound) / (upper_bound - lower_bound) * state_size
    return s.astype(np.int).clip(0, (state_size)-1)

def epsilon(episode):
    n = episode/100
    return 0.5 * (0.98**n)

q = np.zeros([*state_size, 2])
alpha = 0.3

rounds = []
for episode in range(50000):
    observation = env.reset()
    for t in range(200):
        state = to_state(observation)
        action = 0 if q[(*state,0)] > q[(*state,1)] else 1
        if np.random.random() < epsilon(episode):
            action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        next_state = to_state(observation)
        q[(*state,action)] += alpha * (reward + max(q[(*next_state,)]) - q[(*state,action)])
        if done:
            rounds.append(t)
            break
    if episode % 500 == 1:
        last_mean = np.array(rounds[-500:-1]).mean()
        print("Episode finished after {} timesteps".format(last_mean))
        if last_mean > 195.0:
            break

# Plot the learning process
cum_rounds = np.cumsum(rounds)
moving_average = (cum_rounds[100:] - cum_rounds[:-100])/100
plt.plot(moving_average)
plt.show()

# Test
test_rounds = []
for episode in range(100):
    observation = env.reset()
    for t in range(200):
        # env.render()
        # print(observation)
        state = to_state(observation)
        action = 0 if q[(*state,0)] > q[(*state,1)] else 1
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            test_rounds.append(t)
            break

print("Average test result: {}".format(np.array(test_rounds).mean()))

env.close()

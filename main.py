from torch import mode
from envorinment import RingEnvorinment  # Import the environment
import agent as a
import gym
import numpy as np
import copy

# Initialize the environment and agent
#env = RingEnvorinment()
#env.step([0,1])
# Flattened state space (3 pegs x 3 slots)
#action_size = env.action_space.n
#agent = a.DQNAgent(state_size, action_size)
# Hyperparameters

rings = 3

#state space - all the different possible states one can have
#    pins
# 123 - 0 - 0 
# action space - all the possible actions the things can take

#Q-Table: Q-learning maintains a table (or function) mapping state-action pairs to their Q-values,
#  which estimate the expected future reward for taking a specific action in a specific state.

env = RingEnvorinment(rings)

# Initialize the agent
agent = a.agent(lrRate=0.1, disc=0.95, epsi=100.0, env=env)

# Training loop
for episode in range(1000):
    state =  copy.deepcopy(env.reset())  # Initialize environment
    done = False
    agent.reset_episode()

    while not done:
        action = agent.makeAction(state, range(env.action_space.n))
        next_state, reward, done, info = env.step(action)
        agent.update_q_value(state, action, reward, next_state, range(env.action_space.n))
        state = copy.deepcopy(next_state)  # Move to the next state
        #env.render()
    agent.update_epsilon()  # Decay exploration rate

# Print Q-table after training
print(agent.q_table)

agent.epsi = 1
for episode in range(3):
    print("TRIAL NUMBER:",episode , "------------------")
    done = False
    env.reset()
    while not done:
            action = agent.makeAction(state, range(env.action_space.n))
            next_state, reward, done, info = env.step(action)
            #agent.update_q_value(state, action, reward, next_state, range(env.action_space.n))
            state = copy.deepcopy(next_state)  # Move to the next state
            env.render()
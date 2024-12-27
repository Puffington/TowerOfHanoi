import torch
import torch.nn as nn
import random
import numpy as np




class agent:
    def __init__(self,lrRate,disc,epsi,env): # first values
        self.env = env #the link to the environment class
        self.lrRate = lrRate #learning rate
        self.disc = disc # discount factor
        self.epsi = epsi #epsilon randdomnes chance
        self.epsi_loss =0.9 #multiplier of decay 0.9 etc
        self.epsi_minimum = 0 #epsilon wont get lower than this
        self.q_table = {} # links states to actions 

        #qtable function ??
        self.episode =0

        self.totRewards = 0
        self.episodes =0
         

    def makeAction(self,state,actionsPossible):
        #with the current state, make a choice
        # if, epsilon random or from qtable
        #test = tuple(self.env.state)
        tuppel = self.tupleTransform(self.env.state)
        if tuppel not in self.q_table: #probably error here
        # If the state is new, initialize it with Q-values for each action
            self.q_table[tuppel] = {action: 0 for action in range(self.env.action_space.n)}

        if self.epsi > np.random.uniform(0, 100):
            return self.env.action_space.sample()
            #return [np.random.randint(0, 3),np.random.randint(0, 3)]
        else:           
            # Exploit: Choose the action with the highest Q-value
            return max(self.q_table[self.tupleTransform(self.env.state)],
                        key=self.q_table[self.tupleTransform(self.env.state)].get)

    def tupleTransform(self,state):
        if isinstance(state, list):
        #an array to tuple
            leTuple =[]
            pin =[]

            for a in state: #remove zeroes ------------------
                if type(a) == int:
                    leTuple.append(tuple(a))
                else:
                    for b in a:
                        if b != 0:
                            pin.append(b)
                    leTuple.append(tuple(pin))
                    pin = []

            leTuple = tuple(leTuple)
            return leTuple
        
        else:
            temp = []
            for a in state:
                print(type(a))
                if type(a) == tuple:
                    temp.append(list(a))
                else: 
                    temp.append([a])
            return temp

#fix dis ---------
    def update_q_value(self, state, action, reward, next_state, actions):
        """Update the Q-value using the Bellman equation."""
        nextState = 0
        nextmem = next_state
        statmem = state
        next_state = self.tupleTransform(next_state)
        state = self.tupleTransform(state)

        max_next_q = max(self.q_table[next_state].values()) if next_state in self.q_table else 0
        current_q = self.q_table[state][action]
        # Bellman equation
        
        if next_state not in self.q_table:
        # Initialize Q-values for the new state
            self.q_table[next_state] = {action: 0 for action in range(self.env.action_space.n)}

        new_q = current_q + self.lrRate * (reward + self.disc * max_next_q - current_q)
        self.q_table[state][action] = new_q

    def update_epsilon(self):
        #"""Decay the epsilon value to reduce exploration over time."""
        self.epsi = max(self.epsi_minimum, self.epsi * self.epsi_loss)
        #print(self.epsi)

    def reset_episode(self):
        #resets for each episode
        self.total_rewards = 0
        self.episode += 1



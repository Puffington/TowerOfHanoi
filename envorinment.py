import gym
from gym import spaces
import numpy as np
import copy


class RingEnvorinment(gym.Env):
    def __init__(self,rings):
        super().__init__()
        # Define the state: three pins, each can hold a stack of up to three rings
        self.state = [[3,1], [2], []] #current state

        self.max_rings = rings
        self.pins = 3
        self.action = -1
        self.maxsteps = 1000
        self.stepcount = 1000

        self.pyramid = []
        for i in reversed(range(self.max_rings)):
            self.pyramid.append(i+1) 

        self.goal = [[copy.deepcopy(self.pyramid),[],[]],
                     [[],copy.deepcopy(self.pyramid),[]],
                     [[],[],copy.deepcopy(self.pyramid)]
                     ]
        self.done = False

        
        self.actions_map = [(i, j) for i in range(self.pins) for j in range(self.pins) if i != j] #wow that's neat (all possible actions)


        # Observation space: A tuple of three lists, each representing a pin
        # Each ring is represented by an integer (e.g., 1 = smallest, 3 = largest)

        arr = []
        for i in range(self.max_rings):
            arr.append(self.max_rings+1)

        self.observation_space = spaces.Tuple([
            spaces.MultiDiscrete(arr),  # Each pin can hold up to 3 rings (0 means empty)
            spaces.MultiDiscrete(arr), #4 is because of the size of maximum possible ring
            spaces.MultiDiscrete(arr), #array length is because maximum stacks on each pin
        ])
        
        # Action space: Discrete actions to move a ring from one pin to another
        self.action_space = spaces.Discrete(6)  # 6 possible moves (3 pins, 2 directions)

        # Initial state
        self.randomise()

    def randomise(self):
        # Randomly distribute rings on the pins
        self.state = [[], [], []]
        rings = copy.deepcopy(self.pyramid)   # Rings of sizes 3, 2, and 1
        np.random.shuffle(rings)
        for ring in rings:
            rand = np.random.randint(0, self.pins)
            self.state[rand].append(ring)
        return self.state  # i changed here ------------------------


    def step(self, action):
        """Perform the given action and return the result."""
        # Decode action (move from one pin to another)
        #action mapping

        self.action = action
        source, target = self.actions_map[action] #action[0],action[1] #divmod(action, 2)
        
        if not self.state[source]:
            # Invalid move: No ring to move or trying to place a larger ring on a smaller one #
            return self.state, -1, False, {} #changed -----------

        # Valid move: Transfer the top ring from source to target
        ring = self.state[source].pop()
        self.state[target].append(ring)

        # Check if the goal is achieved
        done = self._is_goal_state()

        # Reward for reaching the goal state #change rewards value
        reward = -1
        #reward += self.reward() #10 if done else 0
        reward += 20 if done else 0

        #return self._get_observation(), reward, done, {}


        if done or self.stepcount == 0:
            self.stepcount = copy.deepcopy(self.maxsteps)
            done = 1
        else:
            self.stepcount -=1

        return self.state,reward,done,{}

    def reward(self):
        #else go through each part and add one reward for each stack
        reward =0

        elements =0
        for p in self.state:
            elements=0
            for s in p:
                if(s == (elements -1)):
                    reward += 1
                elements = s

        return reward

    def render(self):
        print("\n")
        #print("action:", self.action)
        #print("Pins:")
        for i, pin in enumerate(self.state):
            print(f" Pin {i+1}: {pin}")

    def _get_observation(self):
        """Return the current state as a tuple."""
        obs = []
        for pin in self.state:
            obs.append(pin + [0] * (self.max_rings - len(pin)))  # Pad with zeros for uniformity
        return tuple(obs)

    def _is_goal_state(self):
        """Check if the rings are stacked in order on one pin."""

        for a in self.goal:
            if self.state == a:
                return 1

        return 0 #any(pin == goal for pin in self.state)
    
    def reset(self):
        """Reset the environment to a random initial state."""
        self.randomise()
        self.done = False
        return self.state #channged here too -----
    
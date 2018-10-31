import numpy as np

class Vehicle():
    def __init__(self):
        position = np.zeros((1,3),dtype=float)
        velocity = np.zeros((1,3),dtype=float)
        self.states = np.vstack((position,velocity))
        self.state_history = []

    def prop_state():
        pass
    

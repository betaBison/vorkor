from Vehicles import Vehicle
import numpy as np
import random
import param
from math import atan2

class Intruder(Vehicle):
    def __init__(self,type,initial_position):
        Vehicle.__init__(self,type)
        self.states[0:3] = initial_position
        self.states[3:6] = self.rand_velocity()
        self.states[6:9] = self.rand_angle()
        self.states[9:12] = [0.,0.,0.]
        self.encounter = True
        for ii in range(len(self.states)):
            self.state_history[ii][0:0] = [self.states[ii]]

    def rand_velocity(self):
        # creates randomized intruder velocity
        # p118 [39,250]kn = [20,129]m/s
        speed = random.uniform(20.,129.)
        # p109 climb rate, [-500,500]ft/min = [-2.6,2.6]m/s
        climb = random.uniform(-2.6,2.6)
        return [speed,0.,climb]

    def rand_angle(self):
        angle = atan2(self.states[1],self.states[0])
        # must point inside the circle
        theta_min = angle+np.pi-param.intruder_spectrum/2.0
        theta_max = angle+np.pi+param.intruder_spectrum/2.0
        theta = random.uniform(theta_min,theta_max)
        initial_angle = [0.,0.,theta]
        return initial_angle

    def prop_state(self):
        vel = self.states[3]
        ang = self.states[8]
        self.states[0] += param.dt*vel*np.cos(ang)
        self.states[1] += param.dt*vel*np.sin(ang)
        self.states[2] += param.dt*self.states[5]
        new_index = len(self.state_history[0])
        for ii in range(len(self.states)):
            self.state_history[ii][new_index:new_index] = [self.states[ii]]
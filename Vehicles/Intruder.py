from Vehicles import Vehicle
import numpy as np
import random
import param
from math import atan2

class Intruder(Vehicle):
    def __init__(self,type,initial_position):
        Vehicle.__init__(self,type)
        self.states[0:3] = initial_position
        self.states[3:6] = self.rand_initial_velocity()
        print(self.states)

    def rand_vel(self):
        # creates randomized intruder velocity
        # p118 [39,250]kn = [20,129]m/s
        speed = random.randint(20,129)
        # p109 climb rate, [-500,500]ft/min = [-2.6,2.6]m/s
        climb = random.uniform(-2.6,2.6)
        return speed,climb

    def rand_initial_velocity(self):
        angle = atan2(self.states[1],self.states[0])
        #velocity = np.zeros((0,3),dtype=float)
        speed,climb = self.rand_vel()
        # must point inside the circle
        theta_min = angle+np.pi-param.intruder_spectrum/2.0
        theta_max = angle+np.pi+param.intruder_spectrum/2.0
        theta = random.uniform(theta_min,theta_max)
        velocity = [speed*np.cos(theta),speed*np.sin(theta),climb]
        return velocity

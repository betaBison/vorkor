from Vehicle import Vehicle
import numpy as np
import random
import param
from math import atan2

class Intruder(Vehicle):
    """
    Class for intruder objects around the perimeter
    """
    def __init__(self,type,initial_position):
        Vehicle.__init__(self,type)
        self.states[0:3] = initial_position # initial position [north, east, down]
        self.states[3:6] = self.rand_velocity() # initial velocity [u, v, w]
        self.states[6:9] = self.rand_angle() # initial angle [phi, theta, psi]
        self.states[9:12] = [0.,0.,0.]  # initial roll rates [p, q, r]
        self.encounter = True # flag of if it's inside the encounter circle
        self.colision = False # flag for if it's collided with the ownship
        self.separation = False # flag for loss of separation boundary
        self.threshold = False # flag for loss of threshold boundary
        self.state_history[0][0:0] = [self.time]
        for ii in range(len(self.states)):
            self.state_history[ii+1][0:0] = [self.states[ii]]

    def rand_velocity(self):
        """
        randomized intruder velocity
        """
        # p118 [39,250]kn = [20,129]m/s
        speed = random.uniform(20.,129.)
        # p109 climb rate, [-500,500]ft/min = [-2.6,2.6]m/s
        #climb = random.uniform(-2.6,2.6)
        climb = 0.0
        return [speed,0.,climb]

    def rand_angle(self):
        """
        randomized intruder angle pointing inside the circle
        """
        angle = atan2(self.states[1],self.states[0])
        # must point inside the circle
        theta_min = angle+np.pi-param.intruder_spectrum/2.0
        theta_max = angle+np.pi+param.intruder_spectrum/2.0
        theta = random.uniform(theta_min,theta_max)
        initial_angle = [0.,0.,theta]
        return initial_angle

    def prop_state(self,ownship_states):
        """
        propagate the state of the intruder
        """
        self.time += param.dt # increment the time step
        vel = self.states[3]
        ang = self.states[8]
        self.states[0] += param.dt*vel*np.cos(ang)
        self.states[1] += param.dt*vel*np.sin(ang)
        self.states[2] += param.dt*self.states[5]
        new_index = len(self.state_history[0])
        self.state_history[0][new_index:new_index] = [self.time]
        for ii in range(len(self.states)):
            self.state_history[ii+1][new_index:new_index] = [self.states[ii]]
        self.colision = self.boundary(self.states[0:3],ownship_states[0:3],self.dcol,self.hcol)
        if self.separation == False:
            # check if there's been a loss of the separation boundary
            self.separation = self.boundary(self.states[0:3],ownship_states[0:3],self.dsep,self.hsep)
        if self.threshold == False:
            # check if there's been a loss of the threshold boundary
            self.threshold = self.boundary(self.states[0:3],ownship_states[0:3],self.dth,self.hth)

    def boundary(self,point1,point2,radius,height):
        """
        helper function for checking if it's inside a boundary
        """
        if ((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2) <= radius**2:
            if abs(point1[2]-point2[2]) <= height:
                return True
            else:
                return False
        else:
            return False

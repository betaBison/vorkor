from Vehicle import Vehicle
import param
import numpy as np
from tools.vmd import *
from math import atan2

class Ownship(Vehicle):
    def __init__(self,type):
        """
        Class for the ownship object
        """
        Vehicle.__init__(self,type)
        self.states[0:3] = [0.,0.,0.] # initial position [north, east, down]
        # initial airspeed set to 80kn p.118
        #self.states[3:6] = [41.1556,0.,0.] # initial velocity [u, v, w]
        self.states[3:6] = [150.0,0.,0.] # too fast (for testing)
        self.states[6:9] = [0.,0.,0.] # initial angle [phi, theta, psi]
        self.states[9:12] = [0.,0.,0.]  # initial roll rates [p, q, r]
        self.state_history[0][0:0] = [self.time]
        for ii in range(len(self.states)):
            self.state_history[ii+1][0:0] = [self.states[ii]]

    def intruder_pos_places(self):
        """
        creates inital intruder starting spaces
        """
        num_spots = param.intruder_pos_places # possible number of spots
        angles = np.linspace(-np.pi,np.pi-2.0*np.pi/num_spots,num_spots) # angles between each spot
        for ii in range(num_spots):
            new_spot = self.dr*Rz_I2B(angles[ii])[0,:] + np.array([[0.0,0.0,param.intruder_height]])
            if ii == 0:
                self.intruder_spots = new_spot
            else:
                self.intruder_spots = np.vstack((self.intruder_spots,new_spot))

    def encounter_circle(self,intruder_state):
        """
        checks whether the intruder is still inside the encounter circle
        """
        combined = [a_i - b_i for a_i, b_i in zip(self.states[0:2], intruder_state[0:2])]
        dist = np.linalg.norm(combined)
        if dist > self.dr:
            return False
        else:
            return True

    def prop_state(self,own_waypoint):
        """
        propagate the state of the ownship
        """
        self.time += param.dt # increment the time
        vel = self.states[3]
        if any(own_waypoint):
            psi_des = atan2(own_waypoint[1]-self.states[1],own_waypoint[0]-self.states[0])
            self.states[8] = rad_wrap_2pi(psi_des)
        ang = self.states[8]
        self.states[0] += param.dt*vel*np.cos(ang)
        self.states[1] += param.dt*vel*np.sin(ang)
        new_index = len(self.state_history[0])
        self.state_history[0][new_index:new_index] = [self.time]
        for ii in range(len(self.states)):
            self.state_history[ii+1][new_index:new_index] = [self.states[ii]]

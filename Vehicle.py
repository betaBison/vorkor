import numpy as np
import param
import random

class Vehicle():
    def __init__(self,type):
        position = np.zeros((1,3),dtype=float)
        velocity = np.zeros((1,3),dtype=float)
        self.states = np.hstack((position,velocity))
        self.state_history = np.empty((6,1))
        self.size = 0.0
        if type == 'short':
            self.dr = param.dr_short
            self.dth = param.dth_short
            self.hth = param.hth_short
            self.dsep = param.dsep_short
            self.hsep = param.hsep_short
            self.dcol = param.dcol_short
            self.hcol = param.hcol_short
        elif type == 'long':
            self.dr = param.dr_long
            self.dth = param.dth_long
            self.hth = param.hth_long
            self.dsep = param.dsep_long
            self.hsep = param.hsep_long
            self.dcol = param.dcol_long
            self.hcol = param.hcol_long
        else:
            error_codes.error1()

    def rand_vel():
        # creates randomized intruder velocity
        # p118 [39,250]kn = [20,129]m/s
        speed = random.randint(20,129)
        # p109 climb rate, [-500,500]ft/min = [-2.6,2.6]m/s
        climb = random.uniform(-2.6,2.6)
        return speed,climb

    def rand_initial(self):
        position = np.zeros((1,3),dtype=float)
        angle = random.randrange(0,360,18)
        angle = angle*np.pi/180.0
        position = [self.dr*np.cos(angle),self.dr*np.sin(angle),400]

        velocity = np.zeros((1,3),dtype=float)
        speed,climb = Vehicle.rand_vel()
        # must point inside the circle
        theta_min = angle+np.pi-param.intruder_spectrum/2.0
        theta_max = angle+np.pi+param.intruder_spectrum/2.0
        theta = random.uniform(theta_min,theta_max)
        velocity = [speed*np.cos(theta),speed*np.sin(theta),climb]
        self.states = np.hstack((position,velocity))

    def prop_state(self):
        pass

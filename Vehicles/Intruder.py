from Vehicles import Vehicle
import numpy as np
import random
import param
import error_codes

class Intruder(Vehicle):
    def __init__(self,type,initial_position):
        Vehicle.__init__(self,type)
        #self.intruder_list = intruder_list
        duplicate_flag = True
        '''
        while duplicate_flag == True:
            duplicate_flag = False
            self.rand_initial()
            #print(np.size(self.intruder_list,0))
            for ii in range(np.size(self.intruder_list,0)):
                if np.all(self.states[0,0:2] == self.intruder_list[ii,0:2]):
                    #print("duplicate found")
                    duplicate_flag = True
                    break
        '''

    def rand_vel(self):
        # creates randomized intruder velocity
        # p118 [39,250]kn = [20,129]m/s
        speed = random.randint(20,129)
        # p109 climb rate, [-500,500]ft/min = [-2.6,2.6]m/s
        climb = random.uniform(-2.6,2.6)
        return speed,climb
    '''
    def rand_initial(self):
        position = np.zeros((1,3),dtype=float)
        angle = random.randrange(0,360,18)
        angle = angle*np.pi/180.0
        position = np.array([self.dr*np.cos(angle),self.dr*np.sin(angle),400])
        velocity = np.zeros((1,3),dtype=float)
        speed,climb = self.rand_vel()
        # must point inside the circle
        theta_min = angle+np.pi-param.intruder_spectrum/2.0
        theta_max = angle+np.pi+param.intruder_spectrum/2.0
        theta = random.uniform(theta_min,theta_max)
        velocity = [speed*np.cos(theta),speed*np.sin(theta),climb]
        self.states[0,0:3] = position
        self.states[0,3:6] = velocity
    '''

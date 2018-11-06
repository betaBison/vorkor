from Vehicle import Vehicle
import numpy as np
import random
import param

class Intruder(Vehicle):
    def __init__(self,type,intruder_list):
        Vehicle.__init__(self,type)
        self.intruder_list = intruder_list
        duplicate_flag = True
        while duplicate_flag == True:
            duplicate_flag = False
            self.rand_initial()
            print(len(self.intruder_list))
            '''
            for ii in range(len(self.intruder_list)):
                if self.states[0] == self.intruder_list[ii][0] and self.states[1] == self.intruder_list[ii][1]:
                    print("duplicate found")
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

    def rand_initial(self):
        position = np.zeros((1,3),dtype=float)
        angle = random.randrange(0,360,18)
        angle = angle*np.pi/180.0
        position = [self.dr*np.cos(angle),self.dr*np.sin(angle),400]

        velocity = np.zeros((1,3),dtype=float)
        speed,climb = self.rand_vel()
        # must point inside the circle
        theta_min = angle+np.pi-param.intruder_spectrum/2.0
        theta_max = angle+np.pi+param.intruder_spectrum/2.0
        theta = random.uniform(theta_min,theta_max)
        velocity = [speed*np.cos(theta),speed*np.sin(theta),climb]
        self.states = np.hstack((position,velocity))

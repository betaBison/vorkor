from Vehicles import Vehicle
import param
import numpy as np
from vmd import *

class Ownship(Vehicle):
    def __init__(self,type):
        Vehicle.__init__(self,type)

    def intruder_pos_places(self):
        num_spots = param.intruder_pos_places
        angles = np.linspace(-np.pi,np.pi-2.0*np.pi/num_spots,num_spots)
        for ii in range(num_spots):
            new_spot = self.dr*Rz_I2B(angles[ii])[0,:] + np.array([[0.0,0.0,param.intruder_height]])
            if ii == 0:
                self.intruder_spots = new_spot
            else:
                self.intruder_spots = np.vstack((self.intruder_spots,new_spot))

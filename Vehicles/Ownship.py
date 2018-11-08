from Vehicles import Vehicle
import param
import numpy as np

class Ownship(Vehicle):
    def __init__(self,type):
        Vehicle.__init__(self,type)
        self.intruder_spots = np.array([[]])


    def intruder_pos_places(self):
        num_spots = param.intruder_pos_places
        angles = np.linspace(0.0,2.0*pi,num_spots)
        for ii in range(num_spots):
            new_spot = self.dr*Rz(angles[ii])[0,:] + np.array([0.0,0.0,param.intruder_height])
            np.hstack((self.intruder_spots,new_spot.T))

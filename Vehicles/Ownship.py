from Vehicles import Vehicle
import param
import numpy as np

class Ownship(Vehicle):
    def __init__(self,type):
        Vehicle.__init__(self,type)

    def intruder_pos_places(self):
        num_spots = param.intruder_pos_places
        angles = np.linspace(-np.pi,np.pi-2.0*np.pi/num_spots,num_spots)
        for ii in range(num_spots):
            ''' Brady's big_ben option
            new_spot = self.dr*self.Rz(angles[ii])[0,:] + np.array([[0.0,0.0,param.intruder_height]])
            if ii == 0:
                self.intruder_spots = new_spot.T
            else:
                self.intruder_spots = np.hstack((self.intruder_spots,new_spot.T))
            '''
            new_spot = self.dr*self.Rz(angles[ii])[0,:] + np.array([[0.0,0.0,param.intruder_height]])
            if ii == 0:
                self.intruder_spots = new_spot
            else:
                self.intruder_spots = np.vstack((self.intruder_spots,new_spot))


    def Rz(self,input):
        output = np.matrix([[np.cos(input),np.sin(input),0.],
                            [-np.sin(input),np.cos(input),0.],
                            [0.,0.,1.]])
        return output

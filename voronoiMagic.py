import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import vmd

class VoronoiMagic():
    def __init__(self,ownship,intruders):
        self.ownship_states = np.array(ownship.state_history)
        self.intruders = np.array(intruders)
        self.intruder_num = len(self.intruders)
        self.total_steps = len(ownship.state_history[0])
        self.intruder_states = np.zeros((3,self.total_steps,self.intruder_num),dtype=float)
        for ii in range(self.intruder_num):
            self.intruder_states[:,:,ii] = np.matmul(vmd.enu2ned_mat,np.array(self.intruders[ii].state_history[1:4]))
        #print(self.ownship_states[:,0])
        #print(self.intruder_states[:,0,:])

    def graph(self):
        time = 350
        points = np.transpose(self.intruder_states[0:2,time,:])
        vor = Voronoi(points)
        voronoi_plot_2d(vor)
        x,y = np.transpose(self.ownship_states[1:3,time])
        plt.plot(x,y,'ro')
        plt.show()

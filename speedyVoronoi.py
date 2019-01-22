import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import vmd
import math
import time
import voronoiTools as VT

class SpeedyVoronoi():
    def __init__(self,ownship,intruders):
        self.ownship = ownship
        self.intruders = np.array(intruders)
        self.intruder_num = len(self.intruders)
        self.intruder_states = np.zeros((self.intruder_num,2),dtype=float)
        self.num_closest_points = 3
        self.end = np.array([[1.2*self.ownship.dr,0]])

    def graph(self,ownship_states,intruders):
        time0 = time.time()
        self.intruders = intruders
        self.ownship_states = ownship_states[0:2]
        for ii in range(self.intruder_num):
            self.intruder_states[ii,:] = self.intruders[ii].states[0:2]

        vor = Voronoi(self.intruder_states)
        if len(vor.vertices) < 3:
            return [None, None]
        start = np.array([self.ownship_states])

        self.V = np.concatenate((vor.vertices,start,self.end),axis=0)
        #voronoi_plot_2d(vor,line_colors='black',show_vertices=True)
        self.ridge = vor.ridge_vertices
        self.ridge = list(filter(lambda x: x[0] >= 0, self.ridge))

        closest = np.ones((self.num_closest_points,2),dtype=float)
        closest*=self.ownship.dr*1e90
        for ii in range(len(vor.vertices)):
            distance = VT.calcDistance(vor.vertices[ii],start[0])
            if distance < np.amax(closest[:,0]):
                closest[np.argmax(closest[:,0]),1] = ii
                closest[np.argmax(closest[:,0]),0] = distance
        for ii in range(self.num_closest_points):
            start_index = len(vor.vertices)
            closest_index = int(closest[ii,1])
            self.ridge.append([closest_index,start_index])
        closest = np.ones((self.num_closest_points,2),dtype=float)
        closest*=self.ownship.dr*1e9
        for ii in range(len(vor.vertices)):
            distance = VT.calcDistance(vor.vertices[ii],self.end[0])
            if distance < np.amax(closest[:,0]):
                closest[np.argmax(closest[:,0]),1] = ii
                closest[np.argmax(closest[:,0]),0] = distance
        for ii in range(self.num_closest_points):
            end_index = len(vor.vertices)+1
            closest_index = int(closest[ii,1])
            self.ridge.append([closest_index,end_index])


        # assign weight
        weight = np.zeros((len(self.ridge),1))
        for ii in range(len(self.ridge)):
            D_prime = np.zeros((self.intruder_states.shape[0],1))
            for jj in range(self.intruder_states.shape[0]):
                sigma_star = VT.calcSigmaStar(self.intruder_states[jj],self.V[self.ridge[ii][0]],self.V[self.ridge[ii][1]])
                if sigma_star < 0.0:
                    D_prime[jj] = np.linalg.norm(self.intruder_states[jj]-self.V[self.ridge[ii][0]])
                elif sigma_star > 1.0:
                    D_prime[jj] = np.linalg.norm(self.intruder_states[jj]-self.V[self.ridge[ii][1]])
                else:
                    D_prime[jj] = VT.calcWeight(self.intruder_states[jj],self.V[self.ridge[ii][0]],self.V[self.ridge[ii][1]])
            weight[ii] = VT.calcCost(self.V[self.ridge[ii][0]],self.V[self.ridge[ii][1]],np.amin(D_prime))


        time1 = time.time()
        path = VT.dijkstraSearch(self.V,self.ridge,weight)
        time2 = time.time()


        self.next = self.V[path[1]]
        return self.next

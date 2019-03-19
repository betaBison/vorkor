import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import tools.vmd as vmd
import math
import time
import tools.voronoiTools as VT
import param as P

class SpeedyVoronoi():
    def __init__(self,ownship,intruders):
        self.ownship = ownship
        self.intruders = np.array(intruders)
        self.intruder_num = len(self.intruders)
        self.intruder_states = np.zeros((self.intruder_num,2),dtype=float)
        self.num_closest_points = 3
        self.end = P.end


    def compute(self,ownship_states,intruders):
        time0 = time.time()
        self.intruders = intruders
        self.ownship_states = ownship_states[0:2]
        for ii in range(self.intruder_num):
            self.intruder_states[ii,:] = self.intruders[ii].states[0:2]


        start = np.array([self.ownship_states])
        if self.intruder_num > 2:
            vor = Voronoi(self.intruder_states)
            self.ridge = vor.ridge_vertices
            self.V = np.concatenate((vor.vertices,start,self.end),axis=0)
            num_vertices = len(vor.vertices)
        else:
            self.ridge = []
            self.V = np.concatenate((start,self.end),axis=0)
            num_vertices = 0
        '''
        if len(vor.vertices) < 3:
            return [None, None]
        '''



        #voronoi_plot_2d(vor,line_colors='black',show_vertices=True)

        self.ridge = list(filter(lambda x: x[0] >= 0, self.ridge))

        if num_vertices < self.num_closest_points:
            self.num_closest_points = num_vertices
        closest = np.ones((self.num_closest_points,2),dtype=float)
        closest*=self.ownship.dr*1e90
        for ii in range(num_vertices):
            distance = VT.calcDistance(vor.vertices[ii],start[0])
            if distance < np.amax(closest[:,0]):
                closest[np.argmax(closest[:,0]),1] = ii
                closest[np.argmax(closest[:,0]),0] = distance
        start_index = num_vertices
        for ii in range(self.num_closest_points):
            closest_index = int(closest[ii,1])
            self.ridge.append([closest_index,start_index])
        closest = np.ones((self.num_closest_points,2),dtype=float)
        closest*=self.ownship.dr*1e9
        for ii in range(num_vertices):
            distance = VT.calcDistance(vor.vertices[ii],self.end[0])
            if distance < np.amax(closest[:,0]):
                closest[np.argmax(closest[:,0]),1] = ii
                closest[np.argmax(closest[:,0]),0] = distance
        end_index = num_vertices+1
        for ii in range(self.num_closest_points):
            closest_index = int(closest[ii,1])
            self.ridge.append([closest_index,end_index])
        self.ridge.append([start_index,end_index])

        # assign weight
        weight = np.zeros((len(self.ridge),1))
        self.ridge = list(filter(lambda x: x[0] >= 0, self.ridge))
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
        return self.next#,np.amax(weight)

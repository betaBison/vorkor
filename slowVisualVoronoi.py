import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import vmd
import math
import time
import voronoiTools as VT

class slowVisualVoronoi():
    def __init__(self,ownship,intruders):
        self.ownship = ownship
        self.ownship_states = np.array(self.ownship.state_history)
        self.intruders = np.array(intruders)
        self.intruder_num = len(self.intruders)
        self.total_steps = len(ownship.state_history[0])
        self.intruder_states = np.zeros((3,self.total_steps,self.intruder_num),dtype=float)
        self.num_closest_points = 3
        for ii in range(self.intruder_num):
            self.intruder_states[:,:,ii] = np.matmul(vmd.enu2ned_mat,np.array(self.intruders[ii].state_history[1:4]))
        self.end = np.array([[0,1.2*self.ownship.dr]])
        #print(self.ownship_states[:,0])
        #print(self.intruder_states[:,0,:])

    def graph(self,step):
        time0 = time.time()
        self.E = []
        self.points = np.transpose(self.intruder_states[0:2,step,:])
        vor = Voronoi(self.points)
        start = np.array([np.transpose(self.ownship_states[1:3,step])])
        start = np.array([np.transpose([start[0,1],start[0,0]])])

        self.V = np.concatenate((vor.vertices,start,self.end),axis=0)
        #voronoi_plot_2d(vor,line_colors='white',show_vertices=False)

        self.ridge = vor.ridge_vertices

        for vpair in vor.ridge_vertices:
            if vpair[0] >= 0 and vpair[1] >= 0:
                v0 = vor.vertices[vpair[0]]
                v1 = vor.vertices[vpair[1]]
                self.E.append([[v0[0], v0[1]], [v1[0], v1[1]]])
                # Draw a line from v0 to v1.
                #plt.plot([v0[0], v1[0]], [v0[1], v1[1]], 'g')


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
            self.E.append([[vor.vertices[int(closest[ii,1]),0], vor.vertices[int(closest[ii,1]),1]],[start[0][0],start[0][1]]])
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
            self.E.append([[vor.vertices[int(closest[ii,1]),0], vor.vertices[int(closest[ii,1]),1]],[self.end[0][0],self.end[0][1]]])
        self.ridge.append([start_index,end_index])
        self.E.append([[start[0][0],start[0][1]],[self.end[0][0],self.end[0][1]]])
        self.E = np.asarray(self.E)


        self.E_inf = []
        center = self.points.mean(axis=0)
        for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
            simplex = np.asarray(simplex)
            if np.any(simplex < 0):
                i = simplex[simplex >= 0][0] # finite end Voronoi vertex
                t = self.points[pointidx[1]] - self.points[pointidx[0]]  # tangent
                t = t / np.linalg.norm(t)
                n = np.array([-t[1], t[0]]) # normal
                midpoint = self.points[pointidx].mean(axis=0)
                far_point = vor.vertices[i] + np.sign(np.dot(midpoint - center, n)) * n * self.ownship.dr*10.0
                self.E_inf.append([[vor.vertices[i,0], vor.vertices[i,1]],[far_point[0], far_point[1]]])
                #plt.plot([vor.vertices[i,0], far_point[0]],[vor.vertices[i,1], far_point[1]], 'g--')
        self.E_inf = np.asarray(self.E_inf)

        # assign weight
        weight = np.zeros((self.E.shape[0],1))
        self.ridge = list(filter(lambda x: x[0] >= 0, self.ridge))
        for ii in range(len(self.ridge)):
            D_prime = np.zeros((self.points.shape[0],1))
            for jj in range(self.points.shape[0]):
                sigma_star = VT.calcSigmaStar(self.points[jj],self.E[ii,0,:],self.E[ii,1,:])
                if sigma_star < 0.0:
                    D_prime[jj] = np.linalg.norm(self.points[jj]-self.E[ii,0,:])
                elif sigma_star > 1.0:
                    D_prime[jj] = np.linalg.norm(self.points[jj]-self.E[ii,1,:])
                else:
                    D_prime[jj] = VT.calcWeight(self.points[jj],self.E[ii,0,:],self.E[ii,1,:])
            weight[ii] = VT.calcCost(self.E[ii,0,:],self.E[ii,1,:],np.amin(D_prime))
            if np.amin(D_prime) < 0:
                print(np.amin(D_prime))

        time1 = time.time()
        path = VT.dijkstraSearch(self.V,self.ridge,weight)
        '''
        path_weight = np.zeros((len(path),1))
        for mm in range(len(path)):
            path_weight[mm] = weight[mm]
        print(path_weight)
        '''


        time2 = time.time()

        self.path_pts = []
        for ii in range(len(path)-1):
            for jj in range(len(self.ridge)):
                if path[ii] < path[ii+1]:
                    a = path[ii]
                    b = path[ii+1]
                else:
                    a = path[ii+1]
                    b = path[ii]
                if [a,b] == self.ridge[jj]:
                    self.path_pts.append(self.E[jj,:,:])
                    break
        self.path_pts = np.asarray(self.path_pts)

        time3 = time.time()
        #print("VM total =",time3-time0,time1-time0,time2-time1,time3-time2)

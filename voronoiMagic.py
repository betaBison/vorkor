import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import vmd

class VoronoiMagic():
    def __init__(self,ownship,intruders):
        self.ownship = ownship
        self.ownship_states = np.array(self.ownship.state_history)
        self.intruders = np.array(intruders)
        self.intruder_num = len(self.intruders)
        self.total_steps = len(ownship.state_history[0])
        self.intruder_states = np.zeros((3,self.total_steps,self.intruder_num),dtype=float)
        for ii in range(self.intruder_num):
            self.intruder_states[:,:,ii] = np.matmul(vmd.enu2ned_mat,np.array(self.intruders[ii].state_history[1:4]))
        self.end = np.array([[0,1.2*self.ownship.dr]])
        #print(self.ownship_states[:,0])
        #print(self.intruder_states[:,0,:])

    def graph(self):
        time = 250
        points = np.transpose(self.intruder_states[0:2,time,:])
        vor = Voronoi(points)
        start = np.array([np.transpose(self.ownship_states[1:3,time])])

        V = np.concatenate((vor.vertices,start,self.end),axis=0)
        E = []
        voronoi_plot_2d(vor,line_colors='white',show_vertices=False)


        for vpair in vor.ridge_vertices:
            if vpair[0] >= 0 and vpair[1] >= 0:
                v0 = vor.vertices[vpair[0]]
                v1 = vor.vertices[vpair[1]]
                E.append([[v0[0], v0[1]], [v1[0], v1[1]]])
                # Draw a line from v0 to v1.
                #plt.plot([v0[0], v1[0]], [v0[1], v1[1]], 'g')
        '''
        center = points.mean(axis=0)
        for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
            simplex = np.asarray(simplex)
            if np.any(simplex < 0):
                i = simplex[simplex >= 0][0] # finite end Voronoi vertex
                t = points[pointidx[1]] - points[pointidx[0]]  # tangent
                t = t / np.linalg.norm(t)
                n = np.array([-t[1], t[0]]) # normal
                midpoint = points[pointidx].mean(axis=0)
                far_point = vor.vertices[i] + np.sign(np.dot(midpoint - center, n)) * n * self.ownship.dr*10.0
                E.append([[vor.vertices[i,0], vor.vertices[i,1]],[far_point[0], far_point[1]]])
                #plt.plot([vor.vertices[i,0], far_point[0]],[vor.vertices[i,1], far_point[1]], 'g--')
        '''
        
        closest = np.ones((3,2),dtype=float)
        closest*=self.ownship.dr*1e9
        for ii in range(len(vor.vertices)):
            distance = self.calcDistance(vor.vertices[ii],start[0])
            if distance < np.amax(closest[:,0]):
                closest[np.argmax(closest[:,0]),1] = ii
                closest[np.argmax(closest[:,0]),0] = distance
        for ii in range(3):
            E.append([[vor.vertices[int(closest[ii,1]),0], vor.vertices[int(closest[ii,1]),1]],[start[0][0],start[0][1]]])
        closest = np.ones((3,2),dtype=float)
        closest*=self.ownship.dr*1e9
        for ii in range(len(vor.vertices)):
            distance = self.calcDistance(vor.vertices[ii],self.end[0])
            if distance < np.amax(closest[:,0]):
                closest[np.argmax(closest[:,0]),1] = ii
                closest[np.argmax(closest[:,0]),0] = distance
        for ii in range(3):
            E.append([[vor.vertices[int(closest[ii,1]),0], vor.vertices[int(closest[ii,1]),1]],[self.end[0][0],self.end[0][1]]])

        E = np.asarray(E)
        for ii in range(E.shape[0]):
            plt.plot([E[ii,0,0],E[ii,1,0]],[E[ii,0,1],E[ii,1,1]],'m--')

        plt.plot(start[0,0],start[0,1],'go')
        plt.plot(self.end[0,0],self.end[0,1],'ro')
        plt.xlim([-1.5*self.ownship.dr,1.5*self.ownship.dr])
        plt.ylim([-1.5*self.ownship.dr,1.5*self.ownship.dr])
        plt.show()

    def calcDistance(self,pt1,pt2):
        distance = np.linalg.norm(pt1-pt2)
        return distance

import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import vmd
import math
from pqueue import PqueueHeap
import time

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
            distance = self.calcDistance(vor.vertices[ii],start[0])
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
            distance = self.calcDistance(vor.vertices[ii],self.end[0])
            if distance < np.amax(closest[:,0]):
                closest[np.argmax(closest[:,0]),1] = ii
                closest[np.argmax(closest[:,0]),0] = distance
        for ii in range(self.num_closest_points):
            end_index = len(vor.vertices)+1
            closest_index = int(closest[ii,1])
            self.ridge.append([closest_index,end_index])


        # assign weight
        weight = np.zeros((len(self.ridge),5))
        weight[:,0] += self.ownship.dr*1e9
        # 0 = closest distance to edge
        # 1 = index of closest point
        # 2 = weight
        # 3 = d_prime
        # 4 = cost

        for ii in range(len(self.ridge)):
            avg_point = (self.V[self.ridge[ii][0]] + self.V[self.ridge[ii][1]])/2.0
            for jj in range(self.intruder_states.shape[0]):
                new_distance = self.calcDistance(avg_point,self.intruder_states[jj])
                if new_distance < weight[ii,0]:
                    weight[ii,0] = new_distance
                    weight[ii,1] = jj
            sigma_star = self.calcSigmaStar(self.intruder_states[int(weight[ii,1])],self.V[self.ridge[ii][0]],self.V[self.ridge[ii][1]])
            if sigma_star < 0.0:
                weight[ii,3] = np.linalg.norm(self.intruder_states[int(weight[ii,1])]-self.V[self.ridge[ii][0]])
            elif sigma_star > 1.0:
                weight[ii,3] = np.linalg.norm(self.intruder_states[int(weight[ii,1])]-self.V[self.ridge[ii][1]])
            else:
                weight[ii,3] = self.calcWeight(self.intruder_states[int(weight[ii,1])],self.V[self.ridge[ii][0]],self.V[self.ridge[ii][1]])
            weight[ii,4] = self.calcCost(self.V[self.ridge[ii][0]],self.V[self.ridge[ii][1]],weight[ii,3])

        #print(weight)
        time1 = time.time()
        path = self.dijkstraSearch(self.V,self.ridge,weight[:,4])
        time2 = time.time()

        #print(path)
        self.next = self.V[path[1]]
        return self.next
        '''
        self.path_pts = []
        print(self.ridge)
        print(self.V)
        for ii in range(len(path)-1):
            for jj in range(len(self.ridge)):
                if path[ii] < path[ii+1]:
                    a = path[ii]
                    b = path[ii+1]
                else:
                    a = path[ii+1]
                    b = path[ii]
                if [a,b] == self.ridge[jj]:
                    self.path_pts.append([self.V[a],self.V[b]])
                    break
        self.path_pts = np.asarray(self.path_pts)
        print(self.path_pts)

        time3 = time.time()
        #print("VM total =",time3-time0,time1-time0,time2-time1,time3-time2)
        '''

        '''
        # Graphing for debugging purposes
        for ii in range(self.E.shape[0]):
            plt.plot([self.E[ii,0,0],self.E[ii,1,0]],[self.E[ii,0,1],self.E[ii,1,1]],'k--')
        '''
        '''
        for ii in range(len(path)-1):
            plt.plot([self.V[path[ii],0],self.V[path[ii+1],0]],[self.V[path[ii],1],self.V[path[ii+1],1]],'b')

        plt.plot(start[0,0],start[0,1],'go')
        plt.plot(self.end[0,0],self.end[0,1],'ro')
        plt.xlim([-1.5*self.ownship.dr,1.5*self.ownship.dr])
        plt.ylim([-1.5*self.ownship.dr,1.5*self.ownship.dr])
        plt.show()
        '''





    def calcDistance(self,pt1,pt2):
        distance = np.linalg.norm(pt1-pt2)
        return distance

    def calcSigmaStar(self,p,v1,v2):
        A = np.reshape((v1-p),(1,2))
        B = np.reshape((v1-v2),(2,1))
        ans = (np.matmul(A,B)/(np.linalg.norm(v1-v2))**2).item(0)
        return ans

    def calcWeight(self,p,v1,v2):
        A = np.reshape((v1-p),(1,2))
        B = np.reshape((v1-v2),(2,1))
        ans = np.sqrt((np.linalg.norm(p-v1))**2 - ((np.matmul(A,B)**2)/(np.linalg.norm(v1-v2))**2).item(0))
        return ans

    def calcCost(self,v1,v2,D):
        k1 = 0.1
        k2 = 0.9
        cost = k1*np.linalg.norm(v1-v2)+k2/D
        return cost

    def dijkstraSearch(self,V,E,J):
        nodes = [[] for _ in V]

        for i in range(len(E)):
            src = E[i][0]
            dest = E[i][1]
            weight = J[i]
            nodes[src].append((dest, weight))
            nodes[dest].append((src, weight))

        dist = [math.inf for _ in V]
        prevNode = [None for _ in nodes]

        start = len(nodes) - 2

        queue = PqueueHeap()
        for i in range(len(nodes)):
            queue.insert(i, math.inf)

        dist[start] = 0
        queue.decreaseKey(start, 0)

        cur = queue.deleteMin()
        while cur != None:
            curDist = dist[cur]
            edges = nodes[cur]
            for (dest, weight) in edges:
                newDist = curDist + weight
                if newDist < dist[dest]:
                    prevNode[dest] = cur
                    dist[dest] = newDist
                    queue.decreaseKey(dest, newDist)
            cur = queue.deleteMin()


        if dist[-1] == math.inf:
            print('Impossible!')
            return None

        path = [len(nodes) - 1]
        prev = prevNode[len(nodes) - 1]
        while prev != None:
            path.insert(0, prev)
            prev = prevNode[prev]

        return(path)

import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import vmd
import math
from pqueue import PqueueHeap
import time

class VoronoiMagic():
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

        self.ridge = vor.ridge_vertices.copy()

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
            distance = self.calcDistance(vor.vertices[ii],start[0])
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
            distance = self.calcDistance(vor.vertices[ii],self.end[0])
            if distance < np.amax(closest[:,0]):
                closest[np.argmax(closest[:,0]),1] = ii
                closest[np.argmax(closest[:,0]),0] = distance
        for ii in range(self.num_closest_points):
            end_index = len(vor.vertices)+1
            closest_index = int(closest[ii,1])
            self.ridge.append([closest_index,end_index])
            self.E.append([[vor.vertices[int(closest[ii,1]),0], vor.vertices[int(closest[ii,1]),1]],[self.end[0][0],self.end[0][1]]])

        self.ridge = list(filter(lambda x: x[0] >= 0, self.ridge))


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
        self.E = np.asarray(self.E)

        # assign weight
        weight = np.zeros((self.E.shape[0],5))
        weight[:,0] += self.ownship.dr*1e9
        # 0 = closest distance to edge
        # 1 = index of closest point
        # 2 = weight
        # 3 = d_prime
        # 4 = cost
        for ii in range(self.E.shape[0]):
            avg_point = (self.E[ii,0,:] + self.E[ii,1,:])/2.0
            for jj in range(self.points.shape[0]):
                new_distance = self.calcDistance(avg_point,self.points[jj])
                if new_distance < weight[ii,0]:
                    weight[ii,0] = new_distance
                    weight[ii,1] = jj
                weight[ii,2] = self.calcWeight(self.points[int(weight[ii,1])],self.E[ii,0,:],self.E[ii,1,:])
                sigma_star = self.calcSigmaStar(self.points[int(weight[ii,1])],self.E[ii,0,:],self.E[ii,1,:])
                if sigma_star < 0.0:
                    weight[ii,3] = np.linalg.norm(self.points[int(weight[ii,1])]-self.E[ii,0,:])
                elif sigma_star > 1.0:
                    weight[ii,3] = np.linalg.norm(self.points[int(weight[ii,1])]-self.E[ii,1,:])
                else:
                    weight[ii,3] = weight[ii,2]
                weight[ii,4] = self.calcCost(self.E[ii,0,:],self.E[ii,1,:],weight[ii,3])

        time1 = time.time()
        path = self.dijkstraSearch(self.V,self.ridge,weight[:,4])
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
        print("VM total =",time3-time0,time1-time0,time2-time1,time3-time2)

        # Graphing for debugging purposes
        '''
        for ii in range(self.E.shape[0]):
            plt.plot([self.E[ii,0,0],self.E[ii,1,0]],[self.E[ii,0,1],self.E[ii,1,1]],'k--')

        print(self.V)
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
        k2 = -5.9
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
    '''
    def dijkstraSearch(self,V,E,J):
        unvisited = [[ii,float('inf')] for ii in range(V.shape[0])]
        visited = [unvisited.pop(0)]
        visited[0][1] = 0.0
        while unvisited[-1][1] > visited[0][1]:
            pos_edges = []
            for ii in range(E.shape[0]):
                if all(E[ii,0,:] == V[visited[-1][0]]) or all(E[ii,1,:] == V[visited[-1][0]]):
                    print("yep")
            break

        print(unvisited)
        print(visited)


        result = 0
        return result
    '''

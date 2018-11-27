import numpy as np
import matplotlib.pyplot as plt
import random

def drawCircle(x0,y0,z0,radius):
    # creates points for a circle of specified position and radius
    N = 1000 # number of points for circle
    pts = np.empty((N,3))
    pts[0:int(N/2),0] = np.linspace(-radius,radius,N/2)
    pts[int(N/2):N+1,0] = np.linspace(radius,-radius,N/2)
    pts[0:int(N/2),1] = y0 + np.sqrt(radius**2 - (pts[0:int(N/2),0]-x0)**2)
    pts[int(N/2):N+1,1] = y0 - np.sqrt(radius**2 - (pts[int(N/2):N+1,0]-x0)**2)
    pts[:,2] = z0
    return pts

def circle_mesh(x0,y0,z0,radius):
    # creates points for a circle of specified position and radius
    N = 1000 # number of points for circle
    pts = np.ones((N,3))
    pts[0:int(N/2),0] = np.linspace(-radius,radius,N/2)
    pts[int(N/2):N+1,0] = np.linspace(radius,-radius,N/2)
    pts[0:int(N/2),1] = y0 + np.sqrt(radius**2 - (pts[0:int(N/2),0]-x0)**2)
    pts[int(N/2):N+1,1] = y0 - np.sqrt(radius**2 - (pts[int(N/2):N+1,0]-x0)**2)
    pts[:,2] = z0
    verts = np.delete(pts,[N-1,int(N/2)],0)
    #print(verts.shape[0])
    #verts = np.vstack(([x0,y0,z0],pts))
    faces = np.zeros((verts.shape[0]-2,3),dtype=int)
    for i in range(verts.shape[0]-2):
        faces[i,:] = [0,i+1,i+2]
    return verts, faces



#print(rand_pos())
#print(rand_vel())
#print(rand_initial())
#result1,result2 = circle_mesh(0,0,0,10.0)
#print(result1)

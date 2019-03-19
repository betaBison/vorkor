import numpy as np
import matplotlib.pyplot as plt
import random

"""
Helper functions for visualization graphing
"""

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
    # creates circle mesh of a specified position and radius
    N = 1000 # number of points for circle
    pts = np.ones((N,3))
    pts[0:int(N/2),0] = np.linspace(-radius,radius,N/2)
    pts[int(N/2):N+1,0] = np.linspace(radius,-radius,N/2)
    pts[0:int(N/2),1] = y0 + np.sqrt(radius**2 - (pts[0:int(N/2),0]-x0)**2)
    pts[int(N/2):N+1,1] = y0 - np.sqrt(radius**2 - (pts[int(N/2):N+1,0]-x0)**2)
    pts[:,2] = z0
    verts = np.delete(pts,[N-1,int(N/2)],0)
    faces = np.zeros((verts.shape[0]-2,3),dtype=int)
    for i in range(verts.shape[0]-2):
        faces[i,:] = [0,i+1,i+2]
    return verts, faces

import numpy as np
import matplotlib.pyplot as plt


def drawCircle(x0,y0,z0,radius):
    N = 1000 # number of points for circle
    pts = np.empty((N,3))
    pts[0:N/2,0] = np.linspace(-radius,radius,N/2)
    pts[N/2:N+1,0] = np.linspace(radius,-radius,N/2)
    pts[0:N/2,1] = y0 + np.sqrt(radius**2 - (pts[0:N/2,0]-x0)**2)
    pts[N/2:N+1,1] = y0 - np.sqrt(radius**2 - (pts[N/2:N+1,0]-x0)**2)    
    pts[:,2] = z0
    return pts

'''
something = drawCircle(0,0,0,4)
print(something)
plt.plot(something[:,0],something[:,1])
plt.show()
'''
# Waypoints file for visualization

import numpy as np

data = np.empty((100,3))
data[:,0] = np.linspace(0,9.9,100)
data[:,1] = 3*np.sin(data[:,0])
#data[:,2] = 5*np.cos(data[:,0])
data[:,2] = 0
print(data)




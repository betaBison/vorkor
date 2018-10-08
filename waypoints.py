# Waypoints file for visualization

import numpy as np
import flags as flag

N = int(flag.total_time/flag.dt)

data = np.empty((N,3))
data[:,0] = np.linspace(0,990,N)
data[:,1] = 300*np.sin(data[:,0]/65)
#data[:,2] = 5*np.cos(data[:,0])
data[:,2] = 400
#print(data)




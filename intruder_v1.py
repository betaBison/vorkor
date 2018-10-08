import numpy as np
import flags as flag


class intruder(object):
    def __init__(self,position,velocity):
        # position in the form of [x,y,z]
        self.position = position
        # velocity in the form of [Vx,Vy,Vz]
        self.velocity = velocity

    def waypoints(self):
        N = int(flag.total_time/flag.dt) # number of points to create
        pts = np.empty((N,3))
        pts[0] = self.position
        for i in range(0,N):
            pts[i] = [pts[i-1,0]+flag.dt*self.velocity[0],
            pts[i-1,1]+flag.dt*self.velocity[1],
            pts[i-1,2]+flag.dt*self.velocity[2]]
            #print(pts[i])
        return pts

'''
example = intruder([0,0,0],[100,0,0])
new_points = example.waypoints()
print(new_points)
'''
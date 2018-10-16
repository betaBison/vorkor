import numpy as np
import flags as flag


class ownship(object):
    def __init__(self):
        # position in the form of [x,y,z]
        self.position = [0.0,0.0,400.0]
        # velocity in the form of [Vx,Vy,Vz]
        # initial airspeed set to 80kn p.118
        self.velocity = [41.1556,0,0]

    def waypoints(self):
        N = flag.N
        pts = np.empty((N,3))
        pts[0] = self.position
        for i in range(1,N):
            pts[i,:] = [pts[i-1,0]+flag.dt*self.velocity[0],
                            pts[i-1,1]+flag.dt*self.velocity[1],
                            pts[i-1,2]+flag.dt*self.velocity[2]]
                #print(pts[i])
        return pts

'''
example = intruder([1,1,1],[1,1,1])
new_points = example.waypoints()
print(new_points)
'''
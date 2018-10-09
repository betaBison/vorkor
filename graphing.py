import numpy as np
import matplotlib.pyplot as plt
import flags as flag
import random


def drawCircle(x0,y0,z0,radius):
    # creates points for a circle of specified position and radius
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

def rand_pos():
    # creates a randomized position around the circle
    # p118 "one of twenty possible positions"
    angle = random.randrange(0,360,18)
    angle = angle*np.pi/180.0
    pos = flag.dr*np.cos(angle),flag.dr*np.sin(angle),400
    return pos

def rand_vel():
    # creates randomized velocity
    # p118 [39,250]kn = [20,129]m/s
    speed = random.randint(20,129)
    # p109 climb rate, [-500,500]ft/min = [-2.6,2.6]m/s
    climb = random.uniform(-2.6,2.6)
    return speed,climb

def rand_initial():
    # position
    angle = random.randrange(0,360,18)
    angle = angle*np.pi/180.0
    pos = flag.dr*np.cos(angle),flag.dr*np.sin(angle),400
    # speed
    speed,climb = rand_vel()
    # must point inside the circle
    theta_min = np.pi/2+angle+np.pi/4
    theta_max = theta_min + np.pi/2
    theta = random.uniform(theta_min,theta_max)
    velocity = speed*np.cos(theta),speed*np.sin(theta),climb
    initial = np.empty((2,3))
    initial[0,:] = pos
    initial[1,:] = velocity
    return initial

#print(rand_pos())
#print(rand_vel())
#print(rand_initial())
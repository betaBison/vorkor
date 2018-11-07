from Vehicles import Vehicle
import param
from math import pi
import random

class Ownship(Vehicle):
    def __init__(self,type):
        Vehicle.__init__(self,type)
        self.intruder_spots = []


    def intruder_rand_initial(self):
        angles = []
        angles = list(range(param.intruder_pos_places))
        angles = [x*2.0*pi/param.intruder_pos_places for x in angles]
        random.shuffle(angles)
        self.intruder_spots = angles

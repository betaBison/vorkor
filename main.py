from Vehicles import Intruder
from Vehicles import Ownship
import numpy as np
import random

### Debugging
import matplotlib.pyplot as plt
###


def main():
    draw = True
    intruder_num = 19
    type = 'short'          #options are 'short' or 'long'


    o1 = Ownship(type)
    o1.intruder_pos_places()

    np.random.shuffle(o1.intruder_spots)
    intruder_list = []
    for ii in range(intruder_num):
        new_intruder = Intruder(type,o1.intruder_spots[ii,:])
        intruder_list.append(new_intruder)
        '''
        for kk 2:number:
            o1.prop.state()
            for number intruders:
                int_list[i].prop.state()
        if draw:
            graph.update() # try not sending information
            graph = vis(o1,int_list,body inertial frame)
        '''

    #plt.plot(,'bo')
    #plt.show()
    plt.plot(o1.intruder_spots[:,0],o1.intruder_spots[:,1],'bo')
    for ii in range(intruder_num):
        n0 = intruder_list[ii].states[0]
        e0 = intruder_list[ii].states[1]
        plt.plot(n0,e0,'ro')
        plt.plot(n0,e0,'k')
    plt.show()

if __name__ == '__main__':
    main()

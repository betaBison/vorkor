from Vehicles import Intruder
from Vehicles import Ownship
import numpy as np
import random

### Debugging
import matplotlib.pyplot as plt
###

''''
TODO:


propagate dynamics correctly
add time to state history
'''


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

    encounter = [True]
    jj = 0
    while any(encounter):

        o1.prop_state()
        encounter = []
        for ii in range(intruder_num):
            intruder_list[ii].prop_state()
            encounter.append(o1.encounter_circle(intruder_list[ii].states))

        print(encounter)
        jj += 1
        print(jj)
    '''
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
    plt.figure()
    plt.plot(o1.state_history[0],o1.state_history[1],'go')
    for ii in range(intruder_num):
        plt.plot(intruder_list[ii].state_history[0],intruder_list[ii].state_history[1],'ro')
        plt.plot(intruder_list[ii].state_history[0][0],intruder_list[ii].state_history[1][0],'bo')
    plt.show()

if __name__ == '__main__':
    main()

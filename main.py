from Intruder import Intruder
from Ownship import Ownship
import numpy as np
import random

### Debugging
import matplotlib.pyplot as plt
###

''''
TODO:
change reload
    move vehicle functions into differenct functions
    add reload syntax for each library
fix how the results are passed to numpy arrays
propagate dynamics correctly
compute chord if there is a collision
show the initial state history for the ownship that colided

'''



def main():
    result = []
    for ii in range(10):
        result.append((ii,simulation()))
        print(result)

def simulation():
    draw = False
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
    colision = [False]
    jj = 0
    #while jj < 10:
    while any(encounter) and not any(colision):
        o1.prop_state()
        encounter = []
        colision = []
        for ii in range(intruder_num):
            colision.append(intruder_list[ii].prop_state(o1.states))
            encounter.append(o1.encounter_circle(intruder_list[ii].states))
            #colision = detectColision()
        jj += 1

    '''
        if draw:
            graph = vis(o1,int_list,body inertial frame)
            graph.update() # try not sending information
    '''
    if draw == True:
        #plt.plot(,'bo')
        #plt.show()
        plt.plot(o1.intruder_spots[:,0],o1.intruder_spots[:,1],'bo')
        for ii in range(intruder_num):
            n0 = intruder_list[ii].states[0]
            e0 = intruder_list[ii].states[1]
            plt.plot(n0,e0,'ro')
            plt.plot(n0,e0,'k')
        plt.figure()
        plt.plot(o1.state_history[1],o1.state_history[2],'go')
        for ii in range(intruder_num):
            plt.plot(intruder_list[ii].state_history[1],intruder_list[ii].state_history[2],'ro')
            plt.plot(intruder_list[ii].state_history[1][0],intruder_list[ii].state_history[2][0],'bo')
        plt.show()

    result = o1.state_history[0][-1],any(colision)

    return result

if __name__ == '__main__':
    main()

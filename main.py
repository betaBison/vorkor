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
    add reload syntax for each library
propagate dynamics correctly
compute chord if there is a collision
show the initial state history for the ownship that colided
'''





def main():
    draw = False
    intruder_num = 19
    type = 'short'          #options are 'short' or 'long'
    simulations = 10


    o1 = Ownship(type)
    o1.intruder_pos_places()

    results = []
    print("Simulation #, End Time, Colision, Separation")
    for kk in range(simulations):
        o1.__init__(type)
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
            separation = []
            for ii in range(intruder_num):
                intruder_list[ii].prop_state(o1.states)
                colision.append(intruder_list[ii].colision)
                encounter.append(o1.encounter_circle(intruder_list[ii].states))
                separation.append(intruder_list[ii].separation)
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

        if any(colision) == True:
            #col_i = [i for i, x in enumerate(colision) if x]
            print(kk,o1.state_history[0][-1],any(colision),sum(separation))
            #for ll in range(1,7):
            #print(intruder_list[col_i].state_history[ll][0])
        if any(colision) == False:
            print(kk,o1.state_history[0][-1],any(colision),sum(separation))
        results.append((kk,o1.state_history[0][-1],any(colision),sum(separation)))

    #print(results)


if __name__ == '__main__':
    main()

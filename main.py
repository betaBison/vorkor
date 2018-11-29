from Intruder import Intruder
from Ownship import Ownship
import numpy as np
import random
from Visualization import Visualization as vis

### Debugging
import matplotlib.pyplot as plt
###

''''
TODO:
change from inertial to body reference_frame
change to NED from xyz

add colision coloring to cylinders
test turning angles with the ownship

change reload
    add reload syntax for each library

propagate dynamics correctly

compute chord if there is a collision
'''





def main():
    draw = True
    intruder_num = 18
    type = 'short'                  #options are 'short' or 'long'
    simulations = 1
    reference_frame = 'inertial'    # options are 'inertial' or 'body'

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

        if draw == True:
            graph = vis(o1,intruder_list,reference_frame)

        encounter = [True]
        colision = [False]
        while any(encounter) and not any(colision):
            o1.prop_state()
            encounter = []
            colision = []
            for ii in range(intruder_num):
                intruder_list[ii].prop_state(o1.states)
                colision.append(intruder_list[ii].colision)
                encounter.append(o1.encounter_circle(intruder_list[ii].states))
            if draw == True:
                graph.update(o1,intruder_list)
        separation = []
        for ii in range(intruder_num):
            separation.append(intruder_list[ii].separation)

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
        '''


        if any(colision) == True:
            for ll in range(intruder_num):
                if intruder_list[ll].colision == True:
                    print(kk,o1.state_history[0][-1],any(colision),sum(separation))
                    history = np.array(intruder_list[ll].state_history)
                    print(history[1:7,0])
                    break
        else:
            print(kk,o1.state_history[0][-1],any(colision),sum(separation))
        #results.append((kk,o1.state_history[0][-1],any(colision),sum(separation)))
    #print(results)


if __name__ == '__main__':
    main()

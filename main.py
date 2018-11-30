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

fix bug where cylinders only turn white on the first run
test turning angles with the ownship
Go through thesis again

change reload
    add reload syntax for each library

propagate dynamics correctly

compute chord if there is a collision
'''





def main():
    draw = True
    intruder_num = 20
    type = 'long'                  #options are 'short' or 'long'
    simulations = 1
    reference_frame = 'body'    # options are 'inertial' or 'body'

    o1 = Ownship(type)
    o1.intruder_pos_places()

    results = []
    print("Simulation #, End Time, Colision, Separation, Threshold")
    for kk in range(simulations):
        o1.__init__(type)
        np.random.shuffle(o1.intruder_spots)
        intruder_list = []
        for ii in range(intruder_num):
            new_intruder = Intruder(type,o1.intruder_spots[ii,:])
            intruder_list.append(new_intruder)

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

        threshold = []
        separation = []
        for ii in range(intruder_num):
            threshold.append(intruder_list[ii].threshold)
            separation.append(intruder_list[ii].separation)

        if any(colision) == True:
            for ll in range(intruder_num):
                if intruder_list[ll].colision == True:
                    print(kk,o1.state_history[0][-1],any(colision),sum(separation),sum(threshold))
                    history = np.array(intruder_list[ll].state_history)
                    print(history[1:7,0])
                    break
        else:
            print(kk,o1.state_history[0][-1],any(colision),sum(separation),sum(threshold))
        #results.append((kk,o1.state_history[0][-1],any(colision),sum(separation)))
    #print(results)

    if draw == True:# and any(colision)==True:
        graph = vis(o1,intruder_list,reference_frame)
        while(True):
            graph.update()

if __name__ == '__main__':
    main()

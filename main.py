from IPython.core.debugger import set_trace

from importlib import reload

import Intruder
import Ownship
import Visualization
import slowVisualVoronoi
import speedyVoronoi
reload(Intruder)
reload(Ownship)
reload(Visualization)
reload(slowVisualVoronoi)
reload(speedyVoronoi)
from Intruder import Intruder
from Ownship import Ownship
from Visualization import Visualization as vis
from slowVisualVoronoi import slowVisualVoronoi as Voronoi
from speedyVoronoi import SpeedyVoronoi as sVoronoi

import numpy as np
# import random


### Debugging
import matplotlib.pyplot as plt
###

''''
TODO:

** Most Urgent **
Add 1 obstaccle compatiblity tp slowVisualVoronoi
Fix body frame rotation errors in voronoi display

Fix rotation of voronoi in body frame

fix bug where cylinders only turn white on the first run

Go through thesis again
    What are acutal height/diamter dimensions
    What is the goal point?
    Do the intruders climb?
    Will we climb?
propagate dynamics correctly (radius turns)

compute chord if there is a collision


'''





def main():
    draw = True
    intruder_num = 20
    type = 'short'                  #options are 'short' or 'long'
    simulations = 1
    reference_frame = 'inertial'    # options are 'inertial' or 'body'

    o1 = Ownship(type)
    o1.intruder_pos_places()



    results = []
    print("Simulation #, End Time, Colision, Separation, Threshold")
    for kk in range(simulations):
        o1.__init__(type)
        np.random.shuffle(o1.intruder_spots)
        # intruder_list = []
        intruder_list = [ Intruder(type, o1.intruder_spots[ii,:]) for ii in range(intruder_num) ]
        # for ii in range(intruder_num):
        #     new_intruder = Intruder(type,o1.intruder_spots[ii,:])
        #     intruder_list.append(new_intruder)
        # #enu2ned_mat
        # set_trace()

        svoronoi = sVoronoi(o1,intruder_list)

        encounter = [True]
        colision = [False]
        arrived = False
        mm = 0
        #while mm <= 1000:
        while any(encounter) and not any(colision) and not(arrived):
            mm += 1
            if mm %100 == 0:
                print(mm)
            own_waypoint = svoronoi.graph(o1.states,intruder_list)
            o1.prop_state(own_waypoint)
            encounter = []
            colision = []
            for ii in range(intruder_num):
                intruder_list[ii].prop_state(o1.states)
                colision.append(intruder_list[ii].colision)
                encounter.append(o1.encounter_circle(intruder_list[ii].states))
            if np.linalg.norm(o1.states[0:2] - svoronoi.end) < 15.0:
                arrived = True

            #
        #
        threshold = []
        separation = []
        for ii in range(intruder_num):
            threshold.append(intruder_list[ii].threshold)
            separation.append(intruder_list[ii].separation)


        #
        if any(colision) == True:
            for ll in range(intruder_num):
                if intruder_list[ll].colision == True:
                    print(kk,o1.state_history[0][-1],any(colision),sum(separation),sum(threshold))
                    history = np.array(intruder_list[ll].state_history)
                    print(history[1:7,0])
                    break
                #
            #
        else:
            print(kk,o1.state_history[0][-1],any(colision),sum(separation),sum(threshold))
        #
        #results.append((kk,o1.state_history[0][-1],any(colision),sum(separation)))
    #
    #print(results)

    if draw == True:# and any(colision)==True:
        '''
        voronoi = Voronoi(o1,intruder_list)
        voronoi.graph(250)
        '''


        graph = vis(o1,intruder_list,reference_frame)
        while(True):
            graph.update()

        #
    #
if __name__ == '__main__':
    main()
#

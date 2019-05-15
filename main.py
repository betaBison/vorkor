"""
Author:     D. Knowles
Purpose:    Voronoi graph path planning and dynamic object avoidance
Help:       contact knowles <dot> derek <AT> gmail <dot> com with any questions
"""



from IPython.core.debugger import set_trace

from importlib import reload

import Intruder
import Ownship
import Visualization
import slowVisualVoronoi
import speedyVoronoi
import bline
reload(Intruder)
reload(Ownship)
reload(Visualization)
reload(slowVisualVoronoi)
reload(speedyVoronoi)
reload(bline)
from Intruder import Intruder
from Ownship import Ownship
from Visualization import Visualization as vis
from slowVisualVoronoi import slowVisualVoronoi as Voronoi
from speedyVoronoi import SpeedyVoronoi as sVoronoi
import tools.error_codes
from bline import NewPlanner
import param as P
import numpy as np


'''
TODO:

** Most Urgent **
Fix issue in voronoi difference between fast and slow
Calculate a better constant for weight given the colision volume

Add body frame rotation in voronoi display
Add 1 obstaccle compatiblity tp slowVisualVoronoi

Go through thesis again
    What are acutal height/diamter dimensions
    What is the goal point?
    Do the intruders climb?
    Will we climb?
propagate dynamics correctly (radius turns)

compute chord if there is a collision
'''





def main():
    draw = True                    # whether it displays the graph afterwards or not
    intruder_num = 20               # number of intruder ships
    type = 'short'                  # simulation sizes options are 'short' or 'long'
    simulations = 1                 # number of simulations to calculate in a row
    reference_frame = 'inertial'    # the refrence frame of the graph options are 'inertial' or 'body'
    method = 'voronoi'              # path planning method options are 'voronoi' or 'bline'

    o1 = Ownship(type)              # creates instance of ownship class
    o1.intruder_pos_places()        # creates possible places of intruder initial states



    results = []                    # results array
    print("Simulation #, End Time, Colision, Separation, Threshold") # titles for printed columns
    for kk in range(simulations):
        o1.__init__(type)                       # reinitialize the ownship class to initial state
        np.random.shuffle(o1.intruder_spots)    # shuffle the order of the starting spots

        intruder_list = [ Intruder(type, o1.intruder_spots[ii,:]) for ii in range(intruder_num) ] # create array of intruder classes

        if method == 'voronoi':
            svoronoi = sVoronoi(o1,intruder_list)   # initialize voronoi path planning
        elif method == 'bline':
            planner = NewPlanner()                  # initialize the b-line path planning
        else:
            error_codes.error4()                    # send an error if you didn't enter one of the two options

        encounter = [True]      # array of if any intruder is in the encounter circle
        colision = [False]      # array if there is any collision
        arrived = False         # flag if the ownship has reached its end point
        mm = 0                  # path planning loop iteration
        #own_waypoints = []
        #while mm <= 1000:

        # continue to path plan and move if there is still any intruder in the encounter circle
        # and if the ownship has not arrived, but stop if there is a collision
        while any(encounter) and not(arrived) and not any(colision):
            mm += 1 # increment loop iteration counter
            if mm %100 == 0: # print loop count every 100 for user feedback
                print(mm)
            if method == 'voronoi':
                own_waypoint = svoronoi.compute(o1.states,intruder_list) # next waypoint according to voronoi method
            else:
                own_waypoint = planner.compute() # next waypoint according to b-line method

            o1.prop_state(own_waypoint)     # propagate the state of the ownship towards next waypoint
            encounter = []                  # empty encounter array
            colision = []                   # empty colision array
            for ii in range(intruder_num):
                intruder_list[ii].prop_state(o1.states)         # propagate the state of each intruder
                colision.append(intruder_list[ii].colision)     # check whether there's been a collision
                encounter.append(o1.encounter_circle(intruder_list[ii].states)) # check whether the intruder is still in the encounter circle
            if np.linalg.norm(o1.states[0:2] - P.end) < 15.0: # check whether the ownship is within 15.0 meters of end point
                arrived = True

            #
        #
        threshold = []  # empty the threshold array
        separation = [] # empty the separation array
        for ii in range(intruder_num):
            threshold.append(intruder_list[ii].threshold)   # check if inside the threshold boundary
            separation.append(intruder_list[ii].separation) # check if inside the separation boundary


        #
        # print Simulation #, End Time, Colision Flag, Total loss of Separation, Total loss of Threshold
        print(kk,o1.state_history[0][-1],any(colision),sum(separation),sum(threshold))

        if any(colision) == True:
            for ll in range(intruder_num):
                if intruder_list[ll].colision == True: # runs when it finds which intruder collided
                    history = np.array(intruder_list[ll].state_history)
                    # print initial state of the intruder that collided
                    print(history[1:7,0])
                    break
                #
            #
        #results.append((kk,o1.state_history[0][-1],any(colision),sum(separation)))
    #
    #print(results)

    if draw == True:
        graph = vis(o1,intruder_list,reference_frame) # visualize the simulation
        while(True):
            graph.update() # update for each time step

        #
    #
if __name__ == '__main__':
    main()
#

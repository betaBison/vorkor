from Vehicles import Intruder
from Vehicles import Ownship
import numpy as np

### Debugging
import matplotlib.pyplot as plt
import param
###


def main():
    draw = True
    intruder_num = 20
    type = 'short'          #options are 'short' or 'long'


    o1 = Ownship(type)
    o1.intruder_rand_initial()
    print(o1.intruder_spots)
    intruder_list = []
    for ii in range(intruder_num):
        new_intruder = Intruder(type,intruder_list)
        if ii == 0:
            intruder_list = new_intruder.states
        else:
            intruder_list = np.vstack((intruder_list,new_intruder.states))

        '''
        for kk 2:number:
            o1.prop.state()
            for number intruders:
                int_list[i].prop.state()
        if draw:
            graph.update() # try not sending information
            graph = vis(o1,int_list,body inertial frame)
        '''
    #print(intruder_list)
    plt.plot(list(range(param.intruder_pos_places)),o1.intruder_spots,'bo')
    plt.show()

if __name__ == '__main__':
    main()

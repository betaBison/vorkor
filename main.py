from Vehicles import Intruder
from Vehicles import Ownship
import numpy as np

def main():
    draw = True
    intruder_num = 20
    type = 'short'          #options are 'short' or 'long'


    o1 = Ownship(type)
    intruder_list = np.array([])
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
    print(intruder_list)

if __name__ == '__main__':
    main()

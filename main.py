from Ownship import Ownship
from Intruder import Intruder
import numpy as np


def main():
    draw = True
    intruder_num = 5
    type = 'short'          #options are 'short' or 'long'


    o1 = Ownship(type)

    intruder_list = np.array([])
    for ii in range(intruder_num):
        np.append(intruder_list,Intruder(intruder_list))
        print('hello')
        '''
        for kk 2:number:
            o1.prop.state()
            for number intruders:
                int_list[i].prop.state()
        if draw:
            graph.update() # try not sending information
            graph = vis(o1,int_list,body inertial frame)
        '''


if __name__ == '__main__':
    main()

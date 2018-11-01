from Vehicle import Vehicle
import error_codes

class Intruder(Vehicle):
    def __init__(self,type,intruder_list):
        Vehicle.__init__(self,type)
        self.intruder_list = intruder_list
        Vehicle.rand_initial(self)
        

        '''
        for ii in range(self.intruder_list.shape()):
            print(ii)
        '''

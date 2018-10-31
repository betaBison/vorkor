# This version runs through the simulation as fast as possible w/o visualizaiton
# Author: D. Knowles
# Date: 10/22/18

class zippy(object):
    def __init__(self,type,num_intruders):
        self.type = type
        self.num_intruders = num_intruders
        self.time0 = time.time()
            if self.num_intruders > 20:
                print("Warning: number of intruders exceeds limit")
                print("Must be <= 20 intruders")
            if type == "long":
                self.dr = flag.dr_long
                self.dth = flag.dth_long
                self.hth = flag.hth_long
                self.dsep = flag.dsep_long
                self.hsep = flag.hsep_long
                self.dcol = flag.dcol_long
                self.hcol = flag.hcol_long
            elif type == "short":
                self.dr = flag.dr_short
                self.dth = flag.dth_short
                self.hth = flag.hth_short
                self.dsep = flag.dsep_short
                self.hsep = flag.hsep_short
                self.dcol = flag.dcol_short
                self.hcol = flag.hcol_short
            else:
                print("invalid simulation type")
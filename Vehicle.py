import numpy as np
import param
import error_codes

class Vehicle():
    def __init__(self,type):
        self.state_history = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.states = []
        self.size = 0.0
        self.time = 0.0
        if type == 'short':
            self.dr = param.dr_short
            self.dth = param.dth_short
            self.hth = param.hth_short
            self.dsep = param.dsep_short
            self.hsep = param.hsep_short
            self.dcol = param.dcol_short
            self.hcol = param.hcol_short
        elif type == 'long':
            self.dr = param.dr_long
            self.dth = param.dth_long
            self.hth = param.hth_long
            self.dsep = param.dsep_long
            self.hsep = param.hsep_long
            self.dcol = param.dcol_long
            self.hcol = param.hcol_long
        else:
            error_codes.error1()

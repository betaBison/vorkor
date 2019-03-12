import param as P
import numpy as np

class NewPlanner():
    def __init__(self):
        self.end = P.end

    def compute(self):
        end_n = self.end.item(0)
        end_e = self.end.item(1)
        next = np.array([end_n,end_e])
        return next

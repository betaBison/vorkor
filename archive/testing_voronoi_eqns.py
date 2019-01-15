import numpy as np

def calcCost(v1,v2,D):
    k1 = 0.1
    k2 = 1000000.9
    cost = k1*np.linalg.norm(v1-v2)+k2/D
    return cost

def calcSigmaStar(p,v1,v2):
    ans = (np.matmul((v1-p),np.transpose(v1-v2))/(np.linalg.norm(v1-v2))**2)
    return ans

def calcWeight(p,v1,v2):
    ans = np.sqrt((np.linalg.norm(p-v1))**2 - ((np.matmul((v1-p),np.transpose(v1-v2))**2)/(np.linalg.norm(v1-v2))**2))
    return ans

v1 = np.array([0.0,0.0])
v2 = np.array([10.0,0.0])
p = np.array([7.0,18.0])
d = 0.05
print(calcSigmaStar(p,v1,v2))
print(calcWeight(p,v1,v2))
print(calcCost(v1,v2,d))

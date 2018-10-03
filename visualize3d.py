



from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets
# added Modules
import flags as flag
import waypoints as wp
# Variables
global current_waypoint, pos1, sp1
current_waypoint = 0

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.opts['distance'] = 20
w.show()
w.setWindowTitle('pyqtgraph example: GLScatterPlotItem')

g = gl.GLGridItem()
w.addItem(g)


##
##  First example is a set of points with pxMode=False
##  These demonstrate the ability to have points with real size down to a very small scale 
## 
pos1 = wp.data[current_waypoint]
size1 = 0.5   
color1 = (1.0, 0.0, 0.0, 0.5)


sp1 = gl.GLScatterPlotItem(pos=(1,4,3), size=size1, color=color1, pxMode=False)
w.addItem(sp1)

def update():
    global current_waypoint
    global pos1, sp1
    if current_waypoint < (len(wp.data)-1):
        current_waypoint += 1
    else:
        current_waypoint = 0
    print(wp.data[current_waypoint])
    #pos1 = wp.data[current_waypoint]
    #sp1.setData(pos=pos1)
    
    '''
    global phase, sp2, d2
    s = -np.cos(d2*2+phase)
    color = np.empty((len(d2),4), dtype=np.float32)
    color[:,3] = np.clip(s * 0.1, 0, 1)
    color[:,0] = np.clip(s * 3.0, 0, 1)
    color[:,1] = np.clip(s * 1.0, 0, 1)
    color[:,2] = np.clip(s ** 3, 0, 1)
    sp2.setData(color=color)
    phase -= 0.1
    
    ## update surface positions and colors
    global sp3, d3, pos3
    z = -np.cos(d3*2+phase)
    pos3[:,2] = z
    color = np.empty((len(d3),4), dtype=np.float32)
    color[:,3] = 0.3
    color[:,0] = np.clip(z * 3.0, 0, 1)
    color[:,1] = np.clip(z * 1.0, 0, 1)
    color[:,2] = np.clip(z ** 3, 0, 1)
    sp3.setData(pos=pos3, color=color)
    '''
t = QtCore.QTimer()
t.timeout.connect(update)
t.start(500)


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

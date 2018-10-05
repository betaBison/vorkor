# Visualization in 3 dimensions


from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets
from graphing import drawCircle
# added Modules
import flags as flag
import waypoints as wp
# Variables
global current_waypoint, pos1, sp1
current_waypoint = 0


pg.setConfigOptions(antialias=True)
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
w.opts['distance'] = 20
w.show()
w.setBackgroundColor('k')

# add xygrid
xygrid = gl.GLGridItem(color = 'k')
w.addItem(xygrid)

# add circle radius
for i in range(10):
    circle_pts = drawCircle(0,0,0,i)
    color2 = np.array([[0.0,1.0,0.0,1.0]])
    new_circle = gl.GLLinePlotItem(pos=circle_pts, color=color2, width=5.0, antialias=True,mode='line_strip')
    w.addItem(new_circle)

##
##  First example is a set of points with pxMode=False
##  These demonstrate the ability to have points with real size down to a very small scale 
## 
pos1 = np.array([wp.data[current_waypoint]])
size1 = np.array([[0.5]])   
color1 = np.array([[1.0, 0.1, 0.1, 1.0]])
sp1 = gl.GLScatterPlotItem(pos=pos1, size=size1, color=color1, pxMode=False)
w.addItem(sp1)

def update():
    global current_waypoint
    global pos1, sp1
    if current_waypoint < (len(wp.data)-1):
        current_waypoint += 1
    else:
        current_waypoint = 0
    print(wp.data[current_waypoint])
    pos1 = np.array([wp.data[current_waypoint]])
    sp1.setData(pos=pos1)
t = QtCore.QTimer()
t.timeout.connect(update)
t.start(50)


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

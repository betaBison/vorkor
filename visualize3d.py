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
#xygrid = gl.GLGridItem(color = 'k')
#w.addItem(xygrid)

# add circle radii
for i in range(1,11):
    circle_pts = drawCircle(0,0,0,i)
    color2 = pg.glColor('w')
    new_circle = gl.GLLinePlotItem(pos=circle_pts, color=color2, width=0.5, antialias=True,mode='line_strip')
    w.addItem(new_circle)

# add all three axis
xaxis_pts = np.array([[0.0,0.0,0.0],
                 [11.0,0.0,0.0]])
xaxis = gl.GLLinePlotItem(pos=xaxis_pts,color=pg.glColor('r'),width=0.5)
w.addItem(xaxis)
xaxis_pts = np.array([[0.0,0.0,0.0],
                 [11.0,0.0,0.0]])
xaxis = gl.GLLinePlotItem(pos=xaxis_pts,color=pg.glColor('r'),width=0.5)
w.addItem(xaxis)
yaxis_pts = np.array([[0.0,0.0,0.0],
                 [0.0,11.0,0.0]])
yaxis = gl.GLLinePlotItem(pos=yaxis_pts,color=pg.glColor('g'),width=0.5)
w.addItem(yaxis)
zaxis_pts = np.array([[0.0,0.0,0.0],
                 [0.0,0.0,11.0]])
zaxis = gl.GLLinePlotItem(pos=zaxis_pts,color=pg.glColor('b'),width=0.5)
w.addItem(zaxis)

# Ownship
pos1 = np.array([wp.data[current_waypoint]])
size1 = np.array([[0.5]])   
color1 = pg.glColor('r')
sp1 = gl.GLScatterPlotItem(pos=pos1, size=size1, color=(1,0,0,1), pxMode=False)
w.addItem(sp1)

# sphere mesh
md = gl.MeshData.sphere(rows=100, cols=100, radius=0.5)
body = gl.GLMeshItem(meshdata=md, smooth=False, drawFaces=True, drawEdges=True, edgeColor=(0,0,1,1), color=(0,0,1,1) )
w.addItem(body)
body.translate(10,0,4)

def update():
    global current_waypoint
    global pos1, sp1
    if current_waypoint < (len(wp.data)-1):
        current_waypoint += 1
        body.translate(-0.1,0,0)
    else:
        current_waypoint = 0
        body.translate(10,0,0)
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

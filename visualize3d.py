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
from intruder_v1 import intruder
# Variables
global current_waypoint, pos1, sp1
step = 0


pg.setConfigOptions(antialias=True)
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
w.opts['distance'] = 2000
w.show()
w.setBackgroundColor('k')

# add xygrid
#xygrid = gl.GLGridItem(color = 'k')
#w.addItem(xygrid)

# add circle radii
for i in range(1,6):
    circle_pts = drawCircle(0,0,0,i*flag.dr/5)
    color2 = pg.glColor('w')
    new_circle = gl.GLLinePlotItem(pos=circle_pts, color=color2, width=0.5, antialias=True,mode='line_strip')
    w.addItem(new_circle)

# add all three axis
xaxis_pts = np.array([[0.0,0.0,0.0],
                 [1.1*flag.dr,0.0,0.0]])
xaxis = gl.GLLinePlotItem(pos=xaxis_pts,color=pg.glColor('r'),width=0.5)
w.addItem(xaxis)
yaxis_pts = np.array([[0.0,0.0,0.0],
                 [0.0,1.1*flag.dr,0.0]])
yaxis = gl.GLLinePlotItem(pos=yaxis_pts,color=pg.glColor('g'),width=0.5)
w.addItem(yaxis)
zaxis_pts = np.array([[0.0,0.0,0.0],
                 [0.0,0.0,1.1*flag.dr]])
zaxis = gl.GLLinePlotItem(pos=zaxis_pts,color=pg.glColor('b'),width=0.5)
w.addItem(zaxis)

# add radial lines
for j in range(0,24):
    angle = j*2*np.pi/24.0
    rad_line_pts = xaxis_pts = np.array([[0.0,0.0,0.0],
                                         [1.1*flag.dr*np.cos(angle),1.1*flag.dr*np.sin(angle),0.0]])
    rad_line = gl.GLLinePlotItem(pos=rad_line_pts,color=pg.glColor('w'),width=.5)
    w.addItem(rad_line)


# Initialize and import paths of intruder aircraft
intruder_1 = intruder([300,800,500],[-100,-300,-200])
intruder_1_pts = intruder_1.waypoints()
md = gl.MeshData.sphere(rows=100, cols=100, radius=50)
intruder_1_3d = gl.GLMeshItem(meshdata=md, smooth=False, drawFaces=True, drawEdges=True, edgeColor=(0,1,1,1), color=(0,1,1,1) )
w.addItem(intruder_1_3d)
intruder_1_p0 = intruder_1.position
intruder_1_3d.translate(intruder_1_p0[0],intruder_1_p0[1],intruder_1_p0[2])





# sphere mesh
md = gl.MeshData.sphere(rows=100, cols=100, radius=50)
body = gl.GLMeshItem(meshdata=md, smooth=False, drawFaces=True, drawEdges=True, edgeColor=(0,0,1,1), color=(0,0,1,1) )
w.addItem(body)
body.translate(1000,0,400)

# Ownship
pos1 = np.array([wp.data[step]])
size1 = np.array([[50]])   
color1 = pg.glColor('r')
sp1 = gl.GLScatterPlotItem(pos=pos1, size=size1, color=(1,0,0,1), pxMode=False)
w.addItem(sp1)



def update():
    global step
    global pos1, sp1
    global intruder_1_pts, intruder_1_3d
    if step < (len(wp.data)-1):
        step += 1
        body.translate(-10,0,0)
        intruder_1_3d.translate(intruder_1_pts[step,0]-intruder_1_pts[step-1,0],
                                intruder_1_pts[step,1]-intruder_1_pts[step-1,1],
                                intruder_1_pts[step,2]-intruder_1_pts[step-1,2])
    else:
        body.translate(2000,0,0)
        intruder_1_3d.translate(intruder_1_pts[0,0]-intruder_1_pts[step,0],
                                intruder_1_pts[0,1]-intruder_1_pts[step,1],
                                intruder_1_pts[0,2]-intruder_1_pts[step,2])
        step = 0
    print(step)
    #print(wp.data[current_waypoint])
    pos1 = np.array([wp.data[step]])
    sp1.setData(pos=pos1)
t = QtCore.QTimer()
t.timeout.connect(update)
t.start(flag.dt*1000)


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

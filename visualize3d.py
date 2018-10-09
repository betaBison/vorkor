# Visualization in 3 dimensions
# Author: Derek Knowles
# Date: 10/2/18


from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets
from graphing import drawCircle
from graphing import rand_pos
from graphing import rand_vel
from graphing import rand_initial
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
    new_circle = gl.GLLinePlotItem(pos=circle_pts, color=color2, width=0.1, antialias=True)
    w.addItem(new_circle)

# add radial lines
for j in range(0,20):
    angle = j*2*np.pi/20.0
    rad_line_pts = xaxis_pts = np.array([[0.0,0.0,0.0],
                                         [1.1*flag.dr*np.cos(angle),1.1*flag.dr*np.sin(angle),0.0]])
    rad_line = gl.GLLinePlotItem(pos=rad_line_pts,color=pg.glColor('w'),width=0.1,antialias=True)
    w.addItem(rad_line)

# add all three axis
xaxis_pts = np.array([[0.0,0.0,0.0],
                 [1.1*flag.dr,0.0,0.0]])
xaxis = gl.GLLinePlotItem(pos=xaxis_pts,color=pg.glColor('r'),width=3.0)
w.addItem(xaxis)
yaxis_pts = np.array([[0.0,0.0,0.0],
                 [0.0,-1.1*flag.dr,0.0]])
yaxis = gl.GLLinePlotItem(pos=yaxis_pts,color=pg.glColor('g'),width=3.0)
w.addItem(yaxis)
zaxis_pts = np.array([[0.0,0.0,0.0],
                 [0.0,0.0,-1.1*flag.dr]])
zaxis = gl.GLLinePlotItem(pos=zaxis_pts,color=pg.glColor('b'),width=3.0)
w.addItem(zaxis)


# Initialize and import paths of intruder 
itr_3d = np.empty((flag.itr_num),dtype=object)
itr_pts = np.empty((flag.N,3,flag.itr_num)) 
for k in range(flag.itr_num):
    initial = rand_initial()
    itr_object = intruder(initial[0,:],initial[1,:])
    itr_pts[:,:,k] = itr_object.waypoints()
    sphere_object = gl.MeshData.sphere(rows=100, cols=100, radius=50)    
    itr_3d[k] = gl.GLMeshItem(meshdata=sphere_object, smooth=False, drawFaces=True, drawEdges=False, color=(0,1.0-float(k)/flag.itr_num,float(k)/flag.itr_num,1) )
    w.addItem(itr_3d[k])
    # Translate to initial position
    itr_3d[k].translate(initial[0,0],initial[0,1],initial[0,2])

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
    if step < (len(wp.data)-1):
        step += 1
        body.translate(-10,0,0)
        for k in range(flag.itr_num):
            itr_3d[k].translate(itr_pts[step,0,k]-itr_pts[step-1,0,k],
                                itr_pts[step,1,k]-itr_pts[step-1,1,k],
                                itr_pts[step,2,k]-itr_pts[step-1,2,k],)
    else:
        body.translate(2000,0,0)
        for k in range(flag.itr_num):
            itr_3d[k].translate(itr_pts[0,0,k]-itr_pts[step,0,k],
                                itr_pts[0,1,k]-itr_pts[step,1,k],
                                itr_pts[0,2,k]-itr_pts[step,2,k],)
        step = 0
    #print(step)
    #print(wp.data[current_waypoint])
    pos1 = np.array([wp.data[step]])
    sp1.setData(pos=pos1)
    #print(rand_pos())
t = QtCore.QTimer()
t.timeout.connect(update)
t.start(flag.dt*1000)



## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

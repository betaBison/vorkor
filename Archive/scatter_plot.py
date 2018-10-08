from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np

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
pos = np.empty((53, 3))
size = np.empty((53))
color = np.empty((53, 4))
pos[0] = (1,0,0); size[0] = 0.5;   color[0] = (1.0, 0.0, 0.0, 0.5)
pos[1] = (0,1,0); size[1] = 0.2;   color[1] = (0.0, 0.0, 1.0, 0.5)
pos[2] = (0,0,1); size[2] = 2./3.; color[2] = (0.0, 1.0, 0.0, 0.5)
pos[3] = (1,2,3); size[3] = 3.0;    color[3] = (1.0, 0.0, 1.0, 0.80)

z = 0.5
d = 6.0
for i in range(4,53):
    pos[i] = (0,0,z)
    size[i] = 2./d
    color[i] = (0.0, 1.0, 0.0, 0.5)
    z *= 0.5
    d *= 2.0
    
sp1 = gl.GLScatterPlotItem(pos=pos, size=size, color=color, pxMode=False)
#sp1.translate(5,5,0)
#pos2 = np.empty((1,3))
size2 = np.empty((1))
color2 = np.empty((1,4))
pos2 = np.array([[0,0,5]]) 
size2[0] = 2.5  
color2[0] = (1.0, 1.0, 0.0, 0.9)
sp2 = gl.GLScatterPlotItem(pos=pos2,size=size2,color=color2,pxMode=False)
w.addItem(sp2)
w.addItem(sp1)
print(pos2,size2,color2)





## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
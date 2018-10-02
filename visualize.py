# Visualization 

# import modules
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets




# Setting up screen size
getscreen = QtWidgets.QApplication(sys.argv) # you have to have this to set app before widgets
screen = getscreen.primaryScreen()
#print('Screen: %s' % screen.name())
size = screen.size() # Get main screen size
#print('Size: %d x %d' % (size.width(), size.height()))
rect = screen.availableGeometry()
#print('Available: %d x %d' % (rect.width(), rect.height()))
top_left_x = rect.width()/10.0
top_left_y = rect.height()/10.0
width = rect.width()*0.8
height = rect.height()*0.8 


pg.setConfigOptions(antialias=True) # Enable antialiasing for prettier plots
view = pg.GraphicsView()
app = QtGui.QApplication([])
view.setBackground('w')
pg.setConfigOption('foreground', 'k')
win = pg.GraphicsLayout()
view.setGeometry(top_left_x,top_left_y,width,height)
win.setWindowTitle("Basic Plotting")
view.setCentralItem(win)
view.show()




p6 = win.addPlot(title="Updating plot")
curve = p6.plot(pen='g')
data = np.random.normal(size=(10,1000))
ptr = 0
def update():
    global curve, data, ptr, p6
    curve.setData(data[ptr%10])
    if ptr == 0:
        p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
    ptr += 1
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        


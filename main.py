from visualize3d import visualization
from pyqtgraph.Qt import QtCore, QtGui
import flags as flag
import time


def main():
    #visualization("short"or"long",#intruders)
    graph = visualization("short",12)
    #graph.timing()
    
    ''' 
    t = QtCore.QTimer(graph)
    t.timeout.connect(lambda: graph.update_graph())
    t.start(flag.dt*5000)
    '''


    for i in range(1000):
        x = time.clock()
        graph.update_graph()
        y = time.clock()
        elapsed = y-x
        if elapsed < flag.dt:
            time.sleep(flag.dt-elapsed)
        z = time.clock()
        print(z-x)
        #time.sleep(flag.dt)

if __name__ == '__main__':
    main()
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
         QtGui.QApplication.instance().exec_()
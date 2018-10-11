from visualize3d import visualization
from pyqtgraph.Qt import QtCore, QtGui


#visualization("short"or"long",#intruders)
new = visualization("short",12)


if __name__ == '__main__':
    # import sys
    graph = visualization("short",12)
    for i in range(1000):
        graph.update()
    # if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    #     QtGui.QApplication.instance().exec_()
from visualize3d import visualization
from pyqtgraph.Qt import QtCore, QtGui

def main():
    #visualization("short"or"long",#intruders)
    graph = visualization("short",12)
    for i in range(1000):
        graph.update()

if __name__ == '__main__':
    main()
    

    # import sys
    # if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    #     QtGui.QApplication.instance().exec_()
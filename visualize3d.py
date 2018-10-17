# Visualization in 3 dimensions
# Author: Derek Knowles
# Date: 10/2/18


from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets
from math import *
# added Modules
from graphing import *
import flags as flag
#import waypoints as wp
from intruder_v1 import intruder
from ownship import ownship
import time

class visualization(QtCore.QThread):
    def __init__(self,type,num_intruders):
        QtCore.QThread.__init__(self)
        self.type = type
        self.num_intruders = num_intruders
        if self.num_intruders > 20:
            print("Warning: number of intruders exceeds limit")
            print("Must be <= 20 intruders")
        if type == "long":
            self.dr = flag.dr_long
            self.dth = flag.dth_long
            self.hth = flag.hth_long
            self.dsep = flag.dsep_long
            self.hsep = flag.hsep_long
            self.dcol = flag.dcol_long
            self.hcol = flag.hcol_long
        elif type == "short":
            self.dr = flag.dr_short
            self.dth = flag.dth_short
            self.hth = flag.hth_short
            self.dsep = flag.dsep_short
            self.hsep = flag.hsep_short
            self.dcol = flag.dcol_short
            self.hcol = flag.hcol_short
        else:
            print("invalid simulation type")
        self.step = 0
        self.own_rotate = np.array([0.0,0.0,0.0])       #initial orientation
        #QtCore.QThread.__init__(self)

        pg.setConfigOptions(antialias=True)
        self.app = QtGui.QApplication([])        
        self.w = gl.GLViewWidget()
        self.w.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
        self.w.opts['distance'] = 2*self.dr
        self.w.show()
        self.w.setBackgroundColor('k')


        # add circle radii
        for i in range(1,int(self.dr/1000.0)+1):
            circle_pts = drawCircle(0,0,0,i*1000.0)
            color2 = pg.glColor('w')
            new_circle = gl.GLLinePlotItem(pos=circle_pts, color=color2, width=0.1, antialias=True)
            self.w.addItem(new_circle)

        # add radial lines
        for j in range(0,20):
            angle = j*2*np.pi/20.0
            rad_line_pts = xaxis_pts = np.array([[0.0,0.0,0.0],
                                                [1.1*self.dr*np.cos(angle),1.1*self.dr*np.sin(angle),0.0]])
            rad_line = gl.GLLinePlotItem(pos=rad_line_pts,color=pg.glColor('w'),width=0.1,antialias=True)
            self.w.addItem(rad_line)

        # add all three axis
        xaxis_pts = np.array([[0.0,0.0,0.0],
                        [1.1*self.dr,0.0,0.0]])
        xaxis = gl.GLLinePlotItem(pos=xaxis_pts,color=pg.glColor('r'),width=3.0)
        self.w.addItem(xaxis)
        yaxis_pts = np.array([[0.0,0.0,0.0],
                        [0.0,-1.1*self.dr,0.0]])
        yaxis = gl.GLLinePlotItem(pos=yaxis_pts,color=pg.glColor('g'),width=3.0)
        self.w.addItem(yaxis)
        zaxis_pts = np.array([[0.0,0.0,0.0],
                        [0.0,0.0,-1.1*self.dr]])
        zaxis = gl.GLLinePlotItem(pos=zaxis_pts,color=pg.glColor('b'),width=3.0)
        self.w.addItem(zaxis)


        # Initialize and import paths of intruder 
        self.itr_3d = np.empty((self.num_intruders),dtype=object)
        self.itr_pts = np.empty((flag.N,3,self.num_intruders)) 
        for k in range(self.num_intruders):
            duplicate_flag = True
            while duplicate_flag == True:
                duplicate_flag = False
                initial = rand_initial(self)
                for m in range(k,-1,-1):
                    if np.all(initial[0,:] == self.itr_pts[0,:,m]):
                        #print("duplicate found")
                        #print(initial[0,:],self.itr_pts[0,:,m])
                        duplicate_flag = True
                        break
            itr_object = intruder(initial[0,:],initial[1,:])
            self.itr_pts[:,:,k] = itr_object.waypoints()
            sphere_object = gl.MeshData.sphere(rows=100, cols=100, radius=50)    
            self.itr_3d[k] = gl.GLMeshItem(meshdata=sphere_object, smooth=False, drawFaces=True, drawEdges=False, color=(0,1.0-float(k)/self.num_intruders,float(k)/self.num_intruders,1) )
            self.w.addItem(self.itr_3d[k])
            # Translate to initial position
            self.itr_3d[k].translate(initial[0,0],initial[0,1],initial[0,2])

        # Ownship
        ownship1 = ownship()
        self.own_items = 18 # number of meshes that make up ownship
        self.own_pts = ownship1.waypoints()
        self.own_3d = np.empty(self.own_items,dtype=object)
        sphere_object = gl.MeshData.sphere(rows=100, cols=100, radius=10.0)
        small_sphere = gl.MeshData.sphere(rows=100, cols=100, radius=5.0)
        cyl_length = 20.0
        cyl_object = gl.MeshData.cylinder(rows=100,cols=100,radius=[5.0,5.0],length=20.0)
        rotate_angle = 45
        for l in range(9):
            if l == 0:
                self.own_3d[l] = gl.GLMeshItem(meshdata=sphere_object, smooth=True, drawFaces=True, drawEdges=False, color=(1,0,0,1))
            elif l < 5:
                if l <= 2:
                    cyl_color = pg.glColor('r') # front of quad
                else:
                    cyl_color = pg.glColor('g') # back of quad
                self.own_3d[l] = gl.GLMeshItem(meshdata=cyl_object, smooth=True, drawFaces=True, drawEdges=False, color=cyl_color)
                self.own_3d[l].rotate(90,1,0,0)
                self.own_3d[l].rotate(rotate_angle,0,0,1)
                rotate_angle += 90
            else:
                if l <= 6:
                    cyl_color = pg.glColor('r') # front of quad
                else:
                    cyl_color = pg.glColor('g') # back of quad
                self.own_3d[l] = gl.GLMeshItem(meshdata=small_sphere, smooth=True, drawFaces=True, drawEdges=False, color=cyl_color)
                self.own_3d[l].translate(0,0,20.0)
                self.own_3d[l].rotate(90,1,0,0)
                self.own_3d[l].rotate(rotate_angle,0,0,1)
                rotate_angle += 90
            self.w.addItem(self.own_3d[l])
            self.own_3d[l].translate(self.own_pts[0,0],self.own_pts[0,1],self.own_pts[0,2])
        for l in range(9,(self.own_items)):
            if l == 9:
                radius = self.dcol
                height = 2.0*self.hcol
                cyl_color = np.ones((cyl_object.faceCount(), 4), dtype=float)
                cyl_color[:,3] = 0.4
                cyl_color[:,0] = 0.0
            elif l == 12:
                radius = self.dsep
                height = 2.0*self.hsep
                cyl_color = np.ones((cyl_object.faceCount(), 4), dtype=float)
                cyl_color[:,3] = 0.4
                cyl_color[:,1] = 0.0
            elif l == 15:
                radius = self.dth
                height = 2.0*self.hth
                cyl_color = np.ones((cyl_object.faceCount(), 4), dtype=float)
                cyl_color[:,3] = 0.4
                cyl_color[:,2] = 0.0
            

            if l == 9 or l == 12 or l == 15:
                cyl_object = gl.MeshData.cylinder(rows=100,cols=100,radius=[radius,radius],length=height)
                cyl_object.setFaceColors(cyl_color)
                self.own_3d[l] = gl.GLMeshItem(meshdata=cyl_object, smooth=True, drawFaces=True,drawEdges=False)
                top_circle_verts,top_circle_faces = circle_mesh(0,0,height,radius)
                bot_circle_verts,bot_circle_faces = circle_mesh(0,0,0,radius)
                cir_color = np.ones((cyl_object.faceCount(), 4), dtype=float)
                cir_color[:,3] = 0.1 # transperancy
                cir_color[:,0] = cyl_color[0,0]
                cir_color[:,1] = cyl_color[0,1]
                cir_color[:,2] = cyl_color[0,2]
                self.own_3d[l+1] = gl.GLMeshItem(vertexes=top_circle_verts, faces=top_circle_faces, faceColors=cir_color, smooth=True)
                self.own_3d[l+2] = gl.GLMeshItem(vertexes=bot_circle_verts, faces=bot_circle_faces, faceColors=cir_color, smooth=True)

                for i in range(3):                  
                    self.own_3d[l+i].setGLOptions('additive')
                    self.w.addItem(self.own_3d[l+i])
                    #print(cyl_color)
                    #print("added %d" %l)
                    self.own_3d[l+i].translate(0.0,0.0,-height/2.0)
                    self.own_3d[l+i].translate(self.own_pts[0,0],self.own_pts[0,1],self.own_pts[0,2])
            
        
        '''
        # timing
        status_update_timer = QtCore.QTimer(self)
        status_update_timer.setSingleShot(False)
        status_update_timer.timeout.connect(lambda: self.update_graph())
        status_update_timer.start(5000)
        '''
        

    def update_graph(self):
        time0 = time.clock()
        if self.step < (flag.N-1):
            self.step += 1
            dx = self.own_pts[self.step,0]-self.own_pts[self.step-1,0]
            dy = self.own_pts[self.step,1]-self.own_pts[self.step-1,1]
            dz = self.own_pts[self.step,2]-self.own_pts[self.step-1,2]
            theta = degrees(atan2(dy,dx))
            phi = degrees(atan2(dz,dy))
            psi = degrees(atan2(dz,dx))
            angle_z = theta - self.own_rotate[0]
            angle_x = phi - self.own_rotate[1]
            angle_y = psi - self.own_rotate[2]
            for k in range(self.own_items):
                # translate object to origin
                self.own_3d[k].translate(-self.own_pts[self.step-1,0],
                                    -self.own_pts[self.step-1,1],
                                    -self.own_pts[self.step-1,2])
                # rotate object in direction of where it came from
                self.own_3d[k].rotate(angle_z,0,0,1)
                #self.own_3d[k].rotate(angle_x,1,0,0)
                #self.own_3d[k].rotate(angle_y,0,1,0)
                # translate object back to its spot
                self.own_3d[k].translate(self.own_pts[self.step,0],
                                    self.own_pts[self.step,1],
                                    self.own_pts[self.step,2])
                #new_u = [dx/sqrt(dx**2+dy**2+dz**2),dy/sqrt(dx**2+dy**2+dz**2),dz/sqrt(dx**2+dy**2+dz**2)]
            self.own_rotate[0] = theta
            self.own_rotate[1] = phi
            self.own_rotate[2] = psi
            for k in range(self.num_intruders):
                self.itr_3d[k].translate(self.itr_pts[self.step,0,k]-self.itr_pts[self.step-1,0,k],
                                    self.itr_pts[self.step,1,k]-self.itr_pts[self.step-1,1,k],
                                    self.itr_pts[self.step,2,k]-self.itr_pts[self.step-1,2,k])
        else:
            for k in range(self.own_items):
                self.own_3d[k].translate(self.own_pts[0,0]-self.own_pts[self.step,0],
                                self.own_pts[0,1]-self.own_pts[self.step,1],
                                self.own_pts[0,2]-self.own_pts[self.step,2])
            for k in range(self.num_intruders):
                self.itr_3d[k].translate(self.itr_pts[0,0,k]-self.itr_pts[self.step,0,k],
                                    self.itr_pts[0,1,k]-self.itr_pts[self.step,1,k],
                                    self.itr_pts[0,2,k]-self.itr_pts[self.step,2,k])
            self.step = 0

        self.app.processEvents()
        time1 = time.clock()
        elapsed_time = time1-time0
        if elapsed_time < flag.dt:
            time.sleep(flag.dt-elapsed_time)
        time2 = time.clock()
        #print(time2-time0)
        



## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
#    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#        QtGui.QApplication.instance().exec_()
# Visualization in 3 dimensions for new simulation
# Author: Derek Knowles
# Date: 11/27/18


from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets
from math import *
from visMods import *
import error_codes
import vmd

####### Debugging
import time
#######


class Visualization(QtCore.QThread):
    def __init__(self,ownship,intruders,reference_frame):
        QtCore.QThread.__init__(self)
        self.ownship = ownship
        self.own_states = np.matmul(vmd.enu2ned_mat,np.array(self.ownship.state_history[1:4]))
        self.intruders = intruders
        self.reference_frame = reference_frame
        self.intruder_num = len(intruders)
        self.total_steps = len(self.ownship.state_history[0])
        self.step = 0
        self.intr_states = np.zeros((3,self.total_steps,self.intruder_num),dtype=float)
        if self.reference_frame != 'body' and self.reference_frame != 'inertial':
            error_codes.error3()

        for ii in range(self.intruder_num):
            self.intr_states[:,:,ii] = np.matmul(vmd.enu2ned_mat,np.array(self.intruders[ii].state_history[1:4]))

        # Colision variables
        self.collision_flag_timer = 0
        self.separation_flag_timer = 0
        self.threshold_flag_timer = 0
        self.intruder_status = np.zeros((self.intruder_num,3),dtype=bool)

        pg.setConfigOptions(antialias=True)
        self.app = QtGui.QApplication([])
        self.w = gl.GLViewWidget()
        self.w.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
        self.w.opts['distance'] = 2.0*self.ownship.dr
        self.w.show()
        self.w.setBackgroundColor('k')


        # add circle radii
        for i in range(1,int(self.ownship.dr/1000.0)+1):
            circle_pts = drawCircle(0,0,0,i*1000.0)
            color2 = pg.glColor('w')
            new_circle = gl.GLLinePlotItem(pos=circle_pts, color=color2, width=0.1, antialias=True)
            self.w.addItem(new_circle)

        # add radial lines
        for j in range(0,20):
            angle = j*2*np.pi/20.0
            rad_line_pts = xaxis_pts = np.array([[0.0,0.0,0.0],
                                                [1.1*self.ownship.dr*np.cos(angle),1.1*self.ownship.dr*np.sin(angle),0.0]])
            rad_line = gl.GLLinePlotItem(pos=rad_line_pts,color=pg.glColor('w'),width=0.1,antialias=True)
            self.w.addItem(rad_line)

        # add all three axis
        xaxis_pts = np.array([[0.0,0.0,0.0],
                        [0.0,1.1*self.ownship.dr,0.0]])
        xaxis = gl.GLLinePlotItem(pos=xaxis_pts,color=pg.glColor('r'),width=3.0)
        self.w.addItem(xaxis)
        yaxis_pts = np.array([[0.0,0.0,0.0],
                        [1.1*self.ownship.dr,0.0,0.0]])
        yaxis = gl.GLLinePlotItem(pos=yaxis_pts,color=pg.glColor('g'),width=3.0)
        self.w.addItem(yaxis)
        zaxis_pts = np.array([[0.0,0.0,0.0],
                        [0.0,0.0,-1.1*self.ownship.dr]])
        zaxis = gl.GLLinePlotItem(pos=zaxis_pts,color=pg.glColor('b'),width=3.0)
        self.w.addItem(zaxis)



        # Ownship
        self.own_items = 21 # number of meshes that make up ownship
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
            self.own_3d[l].translate(self.own_states[0,0],self.own_states[1,0],self.own_states[2,0])
        for l in range(9,(self.own_items)):
            if l == 9:
                radius = self.ownship.dcol
                height = 2.0*self.ownship.hcol
                cyl_color = np.ones((cyl_object.faceCount(), 4), dtype=float)
                cyl_color[:,3] = 0.4
                cyl_color[:,0] = 0.0
            elif l == 13:
                radius = self.ownship.dsep
                height = 2.0*self.ownship.hsep
                cyl_color = np.ones((cyl_object.faceCount(), 4), dtype=float)
                cyl_color[:,3] = 0.4
                cyl_color[:,1] = 0.0
            elif l == 17:
                radius = self.ownship.dth
                height = 2.0*self.ownship.hth
                cyl_color = np.ones((cyl_object.faceCount(), 4), dtype=float)
                cyl_color[:,3] = 0.4
                cyl_color[:,2] = 0.0


            if l == 9 or l == 13 or l == 17:
                cyl_object = gl.MeshData.cylinder(rows=100,cols=100,radius=[radius,radius],length=height)
                cyl_object.setFaceColors(cyl_color)
                self.own_3d[l] = gl.GLMeshItem(meshdata=cyl_object, smooth=True, drawFaces=True,drawEdges=False)
                cyl_object2 = gl.MeshData.cylinder(rows=100,cols=100,radius=[radius,radius],length=height)
                cyl_color2 = np.ones((cyl_object2.faceCount(), 4), dtype=float)
                cyl_color2[:,3] = 0.3
                cyl_object2.setFaceColors(cyl_color2)
                self.own_3d[l+1] = gl.GLMeshItem(meshdata=cyl_object2, smooth=True, drawFaces=True,drawEdges=False)
                top_circle_verts,top_circle_faces = circle_mesh(0,0,height,radius)
                bot_circle_verts,bot_circle_faces = circle_mesh(0,0,0,radius)
                cir_color = np.ones((cyl_object.faceCount(), 4), dtype=float)
                cir_color[:,3] = 0.1 # transperancy
                cir_color[:,0] = cyl_color[0,0]
                cir_color[:,1] = cyl_color[0,1]
                cir_color[:,2] = cyl_color[0,2]
                self.own_3d[l+2] = gl.GLMeshItem(vertexes=top_circle_verts, faces=top_circle_faces, faceColors=cir_color, smooth=True)
                self.own_3d[l+3] = gl.GLMeshItem(vertexes=bot_circle_verts, faces=bot_circle_faces, faceColors=cir_color, smooth=True)

                for i in range(4):
                    self.own_3d[l+i].setGLOptions('additive')
                    self.w.addItem(self.own_3d[l+i])
                    if i == 1:
                        self.own_3d[l+i].setVisible(False)
                    self.own_3d[l+i].translate(0.0,0.0,-height/2.0)
                    self.own_3d[l+i].translate(self.own_states[0,0],self.own_states[1,0],self.own_states[2,0])

        # Initialize and import paths of intruder
        self.itr_3d = np.empty((self.intruder_num),dtype=object)
        for k in range(self.intruder_num):
            sphere_object = gl.MeshData.sphere(rows=100, cols=100, radius=50)
            self.itr_3d[k] = gl.GLMeshItem(meshdata=sphere_object, smooth=False, drawFaces=True, drawEdges=False, color=(0,1.0-float(k)/self.intruder_num,float(k)/self.intruder_num,1) )
            self.w.addItem(self.itr_3d[k])
            # Translate to initial position
            self.itr_3d[k].translate(self.intr_states[0,0,k],self.intr_states[1,0,k],self.intr_states[2,0,k])


    def update(self):
        if self.step < self.total_steps-1:
            self.step += 1
            own_dx = self.own_states[0,self.step] - self.own_states[0,self.step-1]
            own_dy = self.own_states[1,self.step] - self.own_states[1,self.step-1]
            own_dz = self.own_states[2,self.step] - self.own_states[2,self.step-1]
            if self.reference_frame == 'inertial':
                for k in range(self.own_items):
                    self.own_3d[k].translate(own_dx,own_dy,own_dz)

            for k in range(self.intruder_num):
                intr_dx = self.intr_states[0,self.step,k] - self.intr_states[0,self.step-1,k]
                intr_dy = self.intr_states[1,self.step,k] - self.intr_states[1,self.step-1,k]
                intr_dz = self.intr_states[2,self.step,k] - self.intr_states[2,self.step-1,k]
                if self.reference_frame == 'inertial':
                    self.itr_3d[k].translate(intr_dx,intr_dy,intr_dz)
                else:
                    self.itr_3d[k].translate(intr_dx-own_dx,intr_dy-own_dy,intr_dz-own_dz)
                for k in range(self.intruder_num):
                    if ((self.intr_states[0,self.step,k]-self.own_states[0,self.step])**2 + (self.intr_states[1,self.step,k]-self.own_states[1,self.step])**2) <= self.ownship.dcol**2 and abs(self.intr_states[2,self.step,k]-self.own_states[2,self.step]) <= self.ownship.hcol:
                         in_circle = True
                         if in_circle == True and self.intruder_status[k,0] == False:
                            self.collision_flag_timer = 1
                            self.intruder_status[k,0] = True
                            self.own_3d[10].setVisible(True)
                            #print("collision")
                         if in_circle == False and self.intruder_status[k] == True:
                             self.intruder_status[k,0] == False
                    if ((self.intr_states[0,self.step,k]-self.own_states[0,self.step])**2 + (self.intr_states[1,self.step,k]-self.own_states[1,self.step])**2) <= self.ownship.dsep**2 and abs(self.intr_states[2,self.step,k]-self.own_states[2,self.step]) <= self.ownship.hsep:
                         in_circle = True
                         if in_circle == True and self.intruder_status[k,1] == False:
                            self.separation_flag_timer = 1
                            self.intruder_status[k,1] = True
                            self.own_3d[14].setVisible(True)
                            #print("separation")
                         if in_circle == False and self.intruder_status[k,1] == True:
                             self.intruder_status[k,1] == False
                    if ((self.intr_states[0,self.step,k]-self.own_states[0,self.step])**2 + (self.intr_states[1,self.step,k]-self.own_states[1,self.step])**2) <= self.ownship.dth**2 and abs(self.intr_states[2,self.step,k]-self.own_states[2,self.step]) <= self.ownship.hth:
                         in_circle = True
                         if in_circle == True and self.intruder_status[k,2] == False:
                            self.threshold_flag_timer = 1
                            self.intruder_status[k,2] = True
                            self.own_3d[18].setVisible(True)
                            #print("threshold")
                         if in_circle == False and self.intruder_status[k,2] == True:
                             self.intruder_status[k,2] == False
                if self.separation_flag_timer > 0:
                    self.separation_flag_timer += 1
                    if self.separation_flag_timer == 60:
                        self.separation_flag_timer = 0
                        self.own_3d[14].setVisible(False)
                if self.collision_flag_timer > 0:
                    self.collision_flag_timer += 1
                    if self.collision_flag_timer == 60:
                        self.collision_flag_timer = 0
                        self.own_3d[10].setVisible(False)
                if self.threshold_flag_timer > 0:
                    self.threshold_flag_timer += 1
                    if self.threshold_flag_timer == 60:
                        self.threshold_flag_timer = 0
                        self.own_3d[18].setVisible(False)
        else:
            if self.reference_frame == 'inertial':
                for ii in range(self.own_items):
                    self.own_3d[ii].translate(self.own_states[0,0]-self.own_states[0,self.step],
                                              self.own_states[1,0]-self.own_states[1,self.step],
                                              self.own_states[2,0]-self.own_states[2,self.step])
                for ii in range(self.intruder_num):
                    self.itr_3d[ii].translate(self.intr_states[0,0,ii]-self.intr_states[0,self.step,ii],
                                              self.intr_states[1,0,ii]-self.intr_states[1,self.step,ii],
                                              self.intr_states[2,0,ii]-self.intr_states[2,self.step,ii])
            else:
                for ii in range(self.intruder_num):
                    self.itr_3d[ii].translate((self.intr_states[0,0,ii]-self.intr_states[0,self.step,ii])-(self.own_states[0,0]-self.own_states[0,self.step]),
                                              (self.intr_states[1,0,ii]-self.intr_states[1,self.step,ii])-(self.own_states[1,0]-self.own_states[1,self.step]),
                                              (self.intr_states[2,0,ii]-self.intr_states[2,self.step,ii])-(self.own_states[2,0]-self.own_states[2,self.step]))
            self.step = 0

        self.app.processEvents()



## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
#    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#        QtGui.QApplication.instance().exec_()

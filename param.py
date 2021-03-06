from math import pi
import numpy as np

"""
Parameters based off of "Airborne Collision Detection and avoidance
for Small UAS Sense and Avoid Systems"
Dissertation by Laith Rasmi Sahaweh in 2016
"""


# LONG-RANGE PARAMETERS
# short-range radius = 1.62nmi p.118
dr_short = 3000       # m, radius of graphic for collision avoidance
# separation radius = 4000ft p.118
dsep_short = 1219.2
# separation height = 700ft p.118
hsep_short = 213.36
# threshold radius = separation radius, p.118
dth_short = dsep_short
# threshold height = separation height p.118
hth_short = hsep_short
# collision radius = 500ft p.118
dcol_short = 152.4
# collision total height = 200ft p.119
# half of total = 100ft
hcol_short = 30.48


# SHORT-RANGE PARAMETERS
# long-range radius = 10nmi p.118
dr_long = 18520.0       # m, radius of graphic for collision avoidance
# threshold radius = 5nmi, p.118
dth_long = 9260.0
# threshold height = 1000ft p.118
hth_long = 304.8
# separation radius = 4000ft p.118
dsep_long = 1219.2
# separation height = 700ft p.118
hsep_long = 213.36
# collision radius = 500ft p.118
dcol_long = 152.4
# collision total height = 200ft p.119
# half of total = 100ft
hcol_long = 30.48

#INTRUDER PARAMETERS
#angle range that intruder penetrates circle
# pi means could be anywhere inside circle including tangent
intruder_spectrum = pi # radians
# number of places intruders could be placed around the circle
intruder_pos_places = 20
# initial intruder height
intruder_height = 0.0

#OWNSHIP PARAMETERS
# end destination [north position, east position]
#end = np.array([[0,1.2*self.ownship.dr]])
end = np.array([[1.2*dr_short,0.0*dr_short]])

# VISUALIZATION PARAMETERS
dt = 0.050      # sec, time step

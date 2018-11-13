# #!/usr/bin/python3

# Latis MoDules     -->     lmd name space
# TODO:
# add angle wrapping

import numpy as np

# length of Earth's semi-major and minor axes in meters
earth_semi_major = 6378137.0
earth_semi_minor = 6356752.314245

earth_semi_minor_major_sq = np.square(earth_semi_minor / earth_semi_major)
# first numerical eccentricity of an ellipse
ellipse_frst_ecc_sq = 1.0 - earth_semi_minor_major_sq
#


# ======================================
# ======================================

# magic numbers

r2d = 180.0 / np.pi
d2r = np.pi / 180.0

i_vec = np.array( [ 1, 0, 0 ] )
j_vec = np.array( [ 0, 1, 0 ] )
k_vec = np.array( [ 0, 0, 1 ] )

enu2ned_mat = np.array( [ [0,1,0], [1,0,0], [0,0,-1] ] )

unit_mat = np.array( [ [1,0,0], [0,1,0], [0,0,1] ] )



# ======================================
# ======================================


def geodet2ecef( lat, lon, alt ):

    '''geodetic to earth-centered-earth-fixed'''

    c_lat = np.cos( lat )
    s_lat = np.sin( lat )
    c_lon = np.cos( lon )
    s_lon = np.sin( lon )

    N_phi = earth_semi_major / ( np.sqrt( 1.0 - ellipse_frst_ecc_sq * np.square( s_lat ) ) )
    #
    px = ( N_phi + alt ) * c_lat * c_lon
    py = ( N_phi + alt ) * c_lat * s_lon
    pz = ( earth_semi_minor_major_sq * N_phi + alt ) * s_lat

    p_xyz = np.array( [px, py, pz] )

    return p_xyz
    #
#


def ecef2enu( p_xyz, lat, lon ):

    '''earth-centered-earth-fixed to local east-north-up'''

    c_lat = np.cos( lat ) # phi
    s_lat = np.sin( lat )
    c_lon = np.cos( lon ) # lambda
    s_lon = np.sin( lon )

    # earth-centered to east-north matrix
    ecef2enu_mat = np.array( [ [-s_lon,        c_lon,       0],
                               [-s_lat*c_lon, -s_lat*s_lon, c_lat],
                               [ c_lat*c_lon,  c_lat*s_lon, s_lat] ] )
    #

    p_enu = ecef2enu_mat @ p_xyz

    p_ned = lmd.enu2ned_mat @ p_enu

    return p_ned
#


def radar2base( ):
    #
    print('blah printed')
    #
#

# ======================================

def Rx_I2B( phi ):
    '''Rotation matrix about y-axis.
    This is the inertial_2_body rotation'''
    cph = np.cos( phi )
    sph = np.sin( phi )

    Rx_i2b = np.array([[1,0,0],[0,cph,sph],[0,-sph,cph]])

    return Rx_i2b
#

# ======================================

def Ry_I2B( theta ):
    '''Rotation matrix about y-axis.
    This is the inertial_2_body rotation'''
    cth = np.cos( theta )
    sth = np.sin( theta )

    Ry_i2b = np.array([[cth,0,-sth],[0,1,0],[sth,0,cth]])

    return Ry_i2b
#

# ======================================

def Rz_I2B( psi ):
    '''Rotation matrix about z-axis.
    This is the inertial_2_body rotation'''
    cps = np.cos( psi )
    sps = np.sin( psi )

    Rz_i2b = np.array([[cps,sps,0],[-sps,cps,0],[0,0,1]])

    return Rz_i2b
#

# ======================================

def RI2B(attitude):
    # returns the transformation inertial to body frame
    # ======================================
    # first check if attitude was given in quaternion values
    # use appropriate i2b calculation

    if np.size(attitude) == 4:
        # print("size 4")
        return RI2Bq(attitude)
    elif np.size(attitude) == 3:
        # print("size 3")
        return RI2Be(attitude)
    else:
        print("Error. Size not equal to 4 or 3.\nOr possibly a shape error.")
    #
#

# ======================================

def RI2Be(stateEul):
    print("RI2Be")
    # hold current phi, theta, and psi
    phi     = stateEul[0]
    theta   = stateEul[1]
    psi     = stateEul[2]

    # ======================================

    # # trig abbreviations
    cph = np.cos(phi)
    sph = np.sin(phi)
    # tph = tan(phi)

    cth = np.cos(theta)
    sth = np.sin(theta)
    # tth = tan(theta);

    cps = np.cos(psi)
    sps = np.sin(psi)
    # tps = tan(psi);

    ri2bE   = np.array([[cth*cps, cth*sps, -sth],
                        [sph*sth*cps - cph*sps, sph*sth*sps + cph*cps, sph*cth],
                        [cph*sth*cps + sph*sps, cph*sth*sps - sph*cps, cph*cth]])
    #
    return ri2bE
    # # tb2i = rpyI2B'
#

# ======================================

def RI2Bq(stateQuat):
    print("Error. Size equal to 4.")
    # q0 = stateQuat(4, 1)
    # q1 = stateQuat(5, 1)
    # q2 = stateQuat(6, 1)
    # q3 = stateQuat(7, 1)
    #
    # # ======================================
    # ri2bQ   = [ q0^2+q1^2-q2^2-q3^2,    2*(q1*q2+q0*q3),        2*(q1*q3-q0*q2);
    #             2*(q1*q2-q0*q3),        q0^2-q1^2+q2^2-q3^2,    2*(q2*q3+q0*q1);
    #             2*(q1*q3+q0*q2),        2*(q2*q3-q0*q1),        q0^2-q1^2-q2^2+q3^2 ];
    # #
#

#

# if __name__ = '__main__':
#     pass
# #

import sys

"""
These errors are called if the described error exsists
"""

def error1():
    sys.exit("Invalid 'type' variable for simulation type in the main.py \
function. Must be either 'long' or 'short'")

'''
def error2():
    sys.exit("number of intruders must be less than number of available spots")
'''
def error3():
    sys.exit("reference frame variable must be either 'inertial' or 'body' \
    in the main.py function.")

def error4():
    sys.exit("Invalid 'method' variable for propagation method in the main.py \
function. Must be either 'voronoi' or 'bline'")

import sys

def error1():
    sys.exit("Invalid 'type' variable for simulation type in the main.py \
function. Must be either 'long' or 'short'")

def error2():
    sys.exit("number of intruders must be less than number of available spots")

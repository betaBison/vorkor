Questions:
#dynamically resizing arrays
#timestep?
#how to stop???
#how much error handling should I implement?\
#numpy or no?
#cordinate axes use for states?


suggested header information?
#Brady's variable naming guide



TODO:
change to lists instead of numpy arrays
change number of places
convert to a numpy at the end
0.01 seconds for timestep
stop when intruders are fully outside the dr
moderate error handling
frame of reference = _if,_bf
_R = rotation



def main():
    draw = True
    o1 = Ownship(short/long) # possibly vehicle class
    int_list = []
    for range(number intruders):
        int_list.append(Intruders(ID number, size, (state)))

        for kk 2:number:
            o1.prop.state()
            for number intruders:
                int_list[i].prop.state()
        if draw:
            graph = vis(o1,int_list,body inertial frame)
            graph.update() # try not sending information



class ownship(short/long)
    self.collision radius
    self.collison

class vis(o1,int_list,body inertial frame):
    initialize meshes

class Vehicle()
    self.states
    self.ID number
    self. size
    self.state_history

    prop_state function()


class Voronoi_magic():
    intruder_states
    intruder_sizes
    ownship_states
    ownship_size




def main():
    simulation("long" or "short",number of intruders, reference frame, Y/N plotting)



class simulation():

    def __init__("long" or "short",number of intruders, reference frame, T/F plotting):
        # Set variables
        if type == "long":
            set lots of long variables
        if type == "short":
            set lots of short variables
        self.num_intruders = number of intruders

        initialize intruder

        for i in range(number of intruders):
            initial position & velocity = initial()

        if plotting == True:
            start a bunch of pyqtgraph stuff
            use correct reference frame

    def update():
        intruder new state = voronoi_magic()

        for i in range(number of intruders):
            set new intruder states


        if plotting == True:
            translate all objects to the new state
            use correct reference frame
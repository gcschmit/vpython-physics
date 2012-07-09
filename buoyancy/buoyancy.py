### INITIALIZE VPYTHON
# -----------------------------------------------------------------------

from __future__ import division
from visual import *
from physutil import *
from visual.graph import *

### FUNCTIONS
# ------------------------------------------------------------------------

# Calculates the volume of the specified objecdt
def volumeSubmerged(object, fluid):
    topOfFluid = fluid.pos.y + fluid.size.y/2
    topOfObject = object.pos.y + object.size.y/2
    bottomOfObject = object.pos.y - object.size.y/2
    
    if topOfObject <= topOfFluid:
        heightSubmerged = object.size.y
    elif bottomOfObject >= topOfFluid:
        heightSubmerged = 0
    else:
        heightSubmerged = (topOfFluid - bottomOfObject)
        
    return (object.size.x * heightSubmerged * object.size.z)


### SETUP ELEMENTS FOR GRAPHING, SIMULATION, VISUALIZATION, TIMING
# ------------------------------------------------------------------------

# Set window title
scene.title = "Buoyancy"

# Make scene background black
scene.background = color.black

# Define scene objects (units are in meters)
fluid = box(size = (2, 2, .2), color = color.blue, opacity = 0.3)
object = box(color = color.red)

# Set up graph with three plots
graphs = PhysGraph(2)


### SETUP PARAMETERS AND INITIAL CONDITIONS
# ----------------------------------------------------------------------------------------

# Define parameters

dragCoefficient = -5.0

fluid.density = 1000 # density of the fluid in units of kg/m^3

object.density = 500 # density of the object in units of kg/m^3
object.pos = vector(0, 0, 0) # initial position of the mass in (x, y, z) form, units are in meters
object.size = size = (0.4, 0.4, 0.1) # size of the object in (x, y, z) form, units are in meters
object.v = vector(0, 0, 0) # initial velocity of mass in (vx, vy, vz) form, units are m/s

g = -9.8 # acceleration due to gravity; units are m/s/s

# Define time parameters
t = 0 # starting time
deltat = 0.001  # time step units are s


### CALCULATION LOOP; perform physics updates and drawing
# ------------------------------------------------------------------------------------

while t < 20 and object.pos.y > (fluid.pos.y - fluid.size.y/2) :  # run for one second
 
    # Required to make animation visible / refresh smoothly (keeps program from running faster
    #    than 1000 frames/s)
    rate(1000)
    
    # compute the force on the object by the fluid (buoyant force)
    Fbuoyant = fluid.density * (-g) * volumeSubmerged(object, fluid)
    
    # compute the force on the object by the gravitational field
    mass = object.density * object.size.x * object.size.y * object.size.z
    Fgravity = mass * g
    
    # compute the drag force on the object
    Fdrag = dragCoefficient * object.v.y
    
    # Compute Net Force 
    Fnet = vector(0, Fbuoyant + Fgravity + Fdrag, 0)

    # Newton's 2nd Law 
    object.v = object.v + (Fnet/mass * deltat)

    # Position update 
    object.pos = object.pos + object.v * deltat

    # Update graphs
    graphs.plot(t, Fbuoyant, Fgravity) # plot energies

    # Time update 
    t = t + deltat
    

### OUTPUT
# --------------------------------------------------------------------------------------

# Print the final time and the cart's final position
print t

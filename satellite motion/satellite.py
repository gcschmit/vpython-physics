### INITIALIZE VPYTHON
# -----------------------------------------------------------------------

from __future__ import division
from visual import *
from physutil import *
from visual.graph import *


### SETUP ELEMENTS FOR GRAPHING, SIMULATION, VISUALIZATION, TIMING
# ------------------------------------------------------------------------

# Set window title
scene.title = "Satellite Motion"

# Make scene background black
scene.background = color.black

# Define scene objects (units are in meters)
earth = sphere(radius = 6.378e6, color = color.blue)

satellite = sphere(radius = 10, color = color.green)

# Set up trail to mark the satellite's trajectory
trail = curve(color = color.yellow, radius = 1e5) # units are in meters

# Set up motion map for satellite's velocity
vMotionMap = MotionMap(satellite, 100000, # expected end time in seconds
    10, # number of markers to draw
    markerScale = 5e3, # scale the vector so it fits on the screen
    labelMarkerOrder = False)

# Set up motion map for satellite's acceleration
aMotionMap = MotionMap(satellite, 100000, # expected end time in seconds
    10, # number of markers to draw
    markerScale = 5e7, # scale the vector so it fits on the screen
    markerColor = color.orange,
    labelMarkerOrder = False)


### SETUP PARAMETERS AND INITIAL CONDITIONS
# ----------------------------------------------------------------------------------------

# Define parameters

earth.m = 5.972e24 # mass of the earth in kg

satellite.m = 1000 # mass of satellite in kg
satellite.pos = vector(4.23e7, 0, 0) # initial position of the satellite, units are in meters
satellite.v = vector(0, 3.07e3, 0) # initial velocity of the satellite

# Define time parameters
t = 0 # starting time
deltat = 360  # time step units are s


### CALCULATION LOOP; perform physics updates and drawing
# ------------------------------------------------------------------------------------

while t < 100000 :
 
    # Required to make animation visible / refresh smoothly (keeps program from running faster
    #    than 1000 frames/s)
    rate(1000)    

    # computer the force of gravity on the satellite by the earth
    Fg = (6.673e-11) * satellite.m * earth.m / mag(satellite.pos)**2
    
    # Compute Net Force 
    Fnet = vector(0, 0, 0) - satellite.pos # direction of the net force is toward the earth
    Fnet.mag = Fg # magnitude of the net force is the force of gravity

    # Newton's 2nd Law 
    satellite.v = satellite.v + (Fnet/satellite.m * deltat)

    # Position update 
    satellite.pos = satellite.pos + satellite.v * deltat
    
    # Update motion maps and trail
    trail.append(pos = satellite.pos)
    vMotionMap.update(t, satellite.v)
    aMotionMap.update(t, Fnet/satellite.m)

    # Time update 
    t = t + deltat
    

### OUTPUT
# --------------------------------------------------------------------------------------

# Print the final time and the satellite's final position
print t
print satellite.v
print Fnet/satellite.m

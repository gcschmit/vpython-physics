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
earth1 = sphere(radius = 6.378e6, color = color.blue)
earth2 = sphere(radius = 6.378e6, color = color.blue)

satellite = sphere(radius = 6.378e6, color = color.green) # r = 10

# Set up trail to mark the satellite's trajectory
trail = curve(color = color.yellow, radius = 5e5) # units are in meters

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

earth1.m = 1*5.972e24 # mass of the earth in kg
earth2.m = 1 * 5.972e24
earth2.pos = vector(2 * 4.23e7, 0, 0)
satellite.m = 1000 # mass of satellite in kg
satellite.pos = vector(5*4.23e7, 3*4.23e7, 0) # initial position of the satellite, units are in meters
satellite.v = vector(-.0*3.07e3, -.4*3.07e3, 0) # initial velocity of the satellite

# Define time parameters
t = 0 # starting time
deltat = 36  # time step units are s


### CALCULATION LOOP; perform physics updates and drawing
# ------------------------------------------------------------------------------------

while t < 5000000 :
 
    # Required to make animation visible / refresh smoothly (keeps program from running faster
    #    than 1000 frames/s)
    rate(1000)    # 1000

    # Note: This model makes the false assumption that the stars are stationary
    #in space
    
    # Force on satellite by both stars
    Fg1 = (6.673e-11) * satellite.m * earth1.m / ((earth1.pos.x - satellite.pos.x)**2 + (earth1.pos.y - satellite.pos.y)**2)
    Fg2 = (6.673e-11) * satellite.m * earth2.m / ((earth2.pos.x - satellite.pos.x)**2 + (earth2.pos.y - satellite.pos.y)**2)

    
#    Fnet1 = vector(Fg1*(earth1.pos.x - satellite.pos.x),
#                   Fg1*(earth1.pos.y - satellite.pos.y),0) 
#    Fnet2 = vector(Fg2*(earth2.pos.x - satellite.pos.x),
#                   Fg2*(earth2.pos.y - satellite.pos.y),0)

    Fnet1 = vector((earth1.pos.x - satellite.pos.x),
                   (earth1.pos.y - satellite.pos.y),0) 
    Fnet1.mag = Fg1
    
    Fnet2 = vector((earth2.pos.x - satellite.pos.x),
                   (earth2.pos.y - satellite.pos.y),0)
    Fnet2.mag = Fg2

    Fnet = Fnet1 + Fnet2

    # Arctan can be undefined if x = 0,while it's unlickily, it's still possible
#    if Fnet.x == 0:
#        Fnet.mag = Fg1 +Fg2
#    else:
#        Fnet.mag = (Fg1 +Fg2) * math.sin(math.atan(math.fabs(Fnet.y/Fnet.x)))

    
    # Newton's 2nd Law 
    satellite.v = satellite.v + (Fnet/satellite.m * deltat)

    # Position update 
    satellite.pos = satellite.pos + satellite.v * deltat
    
    # Update motion maps and trail
    trail.append(pos = satellite.pos)
    #vMotionMap.update(t, satellite.v)
    #aMotionMap.update(t, Fnet/satellite.m)

    # Time update 
    t = t + deltat
    

### OUTPUT
# --------------------------------------------------------------------------------------

# Print the final time and the satellite's final position
print t
print satellite.v
print Fnet/satellite.m

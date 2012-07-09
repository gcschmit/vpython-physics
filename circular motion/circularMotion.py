### INITIALIZE VPYTHON
# -----------------------------------------------------------------------

from __future__ import division
from visual import *
from physutil import *
from visual.graph import *


### FUNCTIONS
# ------------------------------------------------------------------------

# Calculates the net force vector for an object of mass m moving in uniform circular motion with
#    angular velocity w and linear velocity v
def centripetalForce(m, w, v):
    return m * (cross(w, v))


### SETUP ELEMENTS FOR GRAPHING, SIMULATION, VISUALIZATION, TIMING
# ------------------------------------------------------------------------

# Set window title
scene.title = "Circular Motion Particle Model"

# Make scene background black
scene.background = color.black

# Define scene objects (units are in meters)
string = cylinder(pos = vector(0, 0, 0), axis = (1, 0, 0), length = 1, radius = 0.01,
    color = color.green)

ball = sphere(radius = 0.1, color = color.blue)

# Set up trail to mark the ball's trajectory
trail = curve(color = color.yellow, radius = 0.01) # units are in meters

# Set up motion map for ball's velocity
vMotionMap = MotionMap(ball, 1, # expected end time in seconds
    10, # number of markers to draw
    markerScale = 0.1, # scale the vector so it fits on the screen
    labelMarkerOrder = False)

# Set up motion map for ball's acceleration
aMotionMap = MotionMap(ball, 1, # expected end time in seconds
    10, # number of markers to draw
    markerScale = 0.01, # scale the vector so it fits on the screen
    markerColor = color.orange,
    labelMarkerOrder = False)


### SETUP PARAMETERS AND INITIAL CONDITIONS
# ----------------------------------------------------------------------------------------

# Define parameters

period = 1.0 # units in seconds

ball.m = 0.1 # mass of ball in kg
ball.pos = string.pos + string.axis # initial position of the ball is at the end of the string, units are in meters
ball.w = (0, 0, 2 * pi / period) # angular velocity vector
ball.v = cross(ball.w, string.axis)

# Define time parameters
t = 0 # starting time
deltat = 0.001  # time step units are s


### CALCULATION LOOP; perform physics updates and drawing
# ------------------------------------------------------------------------------------

while t < period :  # run for 10 seconds
 
    # Required to make animation visible / refresh smoothly (keeps program from running faster
    #    than 1000 frames/s)
    rate(1000)    

    # Compute Net Force 
    Fnet = centripetalForce(ball.m, ball.w, ball.v)

    # Newton's 2nd Law 
    ball.v = ball.v + (Fnet/ball.m * deltat)

    # Position update 
    ball.pos = ball.pos + ball.v * deltat
    
    # Update the orientation of the string so it stays connected to the ball :)
    string.axis = rotate(string.axis, angle=(mag(ball.w) * deltat))
    
    # Update motion maps and trail
    trail.append(pos = ball.pos)
    vMotionMap.update(t, ball.v)
    aMotionMap.update(t, Fnet/ball.m)

    # Time update 
    t = t + deltat
    

### OUTPUT
# --------------------------------------------------------------------------------------

# Print the final time and the ball's final position
print t
print Fnet

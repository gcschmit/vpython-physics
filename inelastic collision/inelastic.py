### INITIALIZE VPYTHON
# -----------------------------------------------------------------------

from __future__ import division
from visual import *
from physutil import *
from visual.graph import *

### SETUP ELEMENTS FOR GRAPHING, SIMULATION, VISUALIZATION, TIMING
# ------------------------------------------------------------------------

# Set window title
scene.title = "Conservation of Momentum Model (inelastic collisions)"

# Make scene background black
scene.background = color.black

# Define scene objects (units are in meters)
ball1 = sphere(radius = 0.1, color = color.green)
ball2 = sphere(radius = 0.1, color = color.blue)

# Set up motion map for ball 1
motionMap1 = MotionMap(ball1, 10, # expected end time in seconds
    10, # number of markers to draw
    labelMarkerOrder = False)

# Set up motion map for ball 2
motionMap2 = MotionMap(ball2, 10, # expected end time in seconds
    10, # number of markers to draw
    labelMarkerOrder = False)

# Set timer in top right of screen
timerDisplay = PhysTimer(1, 1) # timer position (units are in meters)


### SETUP PARAMETERS AND INITIAL CONDITIONS
# ----------------------------------------------------------------------------------------

# Define parameters

ball1.m = 0.5 # mass of ball in kg
ball1.pos = vector(-1, 1, 0) # initial position of the ball in(x, y, z) form, units are in meters
ball1.v = vector(0, 0, 0) - ball1.pos # set the direction of the velocity vector toward the origin
ball1.v.mag = 0.5 # set the magnitude of the velocity vector

ball2.m = 2.0 # mass of ball in kg
ball2.pos = vector(-0.7, -0.5, 0) # initial position of the ball in(x, y, z) form, units are in meters
ball2.v = vector(0, 0, 0) - ball2.pos # set the direction of the velocity vector toward the origin
ball2.v.mag = 0.3 # set the magnitude of the velocity vector

# Define time parameters
t = 0 # starting time
deltat = 0.001  # time step units are s


### CALCULATION LOOP; perform physics updates and drawing
# ------------------------------------------------------------------------------------

while mag(ball1.pos) < 2 and mag(ball2.pos) < 2 :  # while the balls are within 2 meters of the origin
 
    # Required to make animation visible / refresh smoothly (keeps program from running faster
    #    than 1000 frames/s)
    rate(1000)    

    # Compute Net Force 
    Fnet = vector(0, 0, 0)

    # Newton's 2nd Law 
    ball1.v = ball1.v + (Fnet/ball1.m * deltat)
    ball2.v = ball2.v + (Fnet/ball2.m * deltat)

    # Position update 
    ball1.pos = ball1.pos + ball1.v * deltat
    ball2.pos = ball2.pos + ball2.v * deltat
    
    # check if the balls collided
    if mag(ball1.pos - ball2.pos) < ((ball1.radius + ball2.radius) / 2):
        # calculate the total momentum
        totalMomentum = (ball1.m * ball1.v) + (ball2.m * ball2.v)
        
        # calculate the velocity of the combined ball
        ball1.v = ball2.v = totalMomentum / (ball1.m + ball2.m)
        

    # Update motion map, timer
    motionMap1.update(t, ball1.m * ball1.v)
    motionMap2.update(t, ball2.m * ball2.v)
    timerDisplay.update(t)

    # Time update 
    t = t + deltat
    
    
### OUTPUT
# --------------------------------------------------------------------------------------

# Print the final time and the ball's final position
print t

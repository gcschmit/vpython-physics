### INITIALIZE VPYTHON
# -----------------------------------------------------------------------

from __future__ import division
from visual import *
from physutil import *
from visual.graph import *

### SETUP ELEMENTS FOR GRAPHING, SIMULATION, VISUALIZATION, TIMING
# ------------------------------------------------------------------------

# Set window title
scene.title = "Projectile Motion Particle Model"

# Make scene background black
scene.background = color.black

# Define scene objects (units are in meters)
field = box(pos = vector(0, 0, 0), size = (300, 10, 100), color = color.green, opacity = 0.3)
ball = sphere(radius = 5, color = color.blue)

# Define axis marks the field with a specified number of tick marks
xaxis = PhysAxis(field, 10) # 10 tick marks
yaxis = PhysAxis(field, 5, # 5 tick marks
    axisType = "y",
    labelOrientation = "left",
    startPos = vector(-150, 0, 0), # start the y axis at the left edge of the scene
    length = 100) # units are in meters

# Set up graph with two plots
posgraph = PhysGraph(2)

# Set up trail to mark the ball's trajectory
trail = curve(color = color.yellow, radius = 1) # units are in meters

# Set up motion map for ball
motionMap = MotionMap(ball, 8.163, # expected end time in seconds
    10, # number of markers to draw
    labelMarkerOffset = vector(0, -20, 0),
    dropTime = False)

# Set timer in top right of screen
timerDisplay = PhysTimer(140, 150) # timer position (units are in meters)


### SETUP PARAMETERS AND INITIAL CONDITIONS
# ----------------------------------------------------------------------------------------

# Define parameters
ball.m = 0.6 # mass of ball in kg
ball.pos = vector(-150, 0, 0) # initial position of the ball in(x, y, z) form, units are in meters
ball.v = vector(30, 40, 0) # initial velocity of car in (vx, vy, vz) form, units are m/s

g = vector(0, -9.8, 0) # acceleration due to gravity; units are m/s/s

# Define time parameters
t = 0 # starting time
deltat = 0.001  # time step units are s


### CALCULATION LOOP; perform physics updates and drawing
# ------------------------------------------------------------------------------------

while ball.pos.y >= 0 :  #while the ball's y-position is greater than 0 (above the ground)
 
    # Required to make animation visible / refresh smoothly (keeps program from running faster
    #    than 1000 frames/s)
    rate(1000)    

    # Compute Net Force 
    Fnet = ball.m * g

    # Newton's 2nd Law 
    ball.v = ball.v + (Fnet/ball.m * deltat)

    # Position update 
    ball.pos = ball.pos + ball.v * deltat

    # Update motion map, graph, timer, and trail
    motionMap.update(t, ball.v)
    posgraph.plot(t, ball.pos.x, ball.pos.y) # plot x and y position vs. time
    trail.append(pos = ball.pos)
    timerDisplay.update(t)

    # Time update 
    t = t + deltat
    
    
### OUTPUT
# --------------------------------------------------------------------------------------

# Print the final time and the ball's final position
print t
print ball.pos

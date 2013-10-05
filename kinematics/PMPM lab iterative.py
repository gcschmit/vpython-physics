### INITIALIZE VPYTHON
# -----------------------------------------------------------------------

from __future__ import division
from visual import *
from physutil import *
from visual.graph import *

### SETUP ELEMENTS FOR GRAPHING, SIMULATION, VISUALIZATION, TIMING
# ------------------------------------------------------------------------

# Set window title
scene.title = "PMPM Lab Model"

# Make scene background black
scene.background = color.black

# Define scene objects (units are in meters)
field = box(pos = vector(1.5, 0, 0), size = (3, .10, 1), color = color.green, opacity = 0.3)
ball = sphere(radius = .05, color = color.blue)

# Define axis marks the field with a specified number of tick marks
xaxis = PhysAxis(field, 10, length = 4.5) # 10 tick marks
yaxis = PhysAxis(field, 5, # 5 tick marks
    axisType = "y",
    labelOrientation = "left",
    startPos = vector(0, 0, 0), # start the y axis at the left edge of the scene
    length = 1) # units are in meters

# Set up graph with two plots
posgraph = PhysGraph(1)

# Set up trail to mark the ball's trajectory
trail = curve(color = color.yellow, radius = .01) # units are in meters

# Set timer in top right of screen
timerDisplay = PhysTimer(2.0, 1.50) # timer position (units are in meters)


### SETUP PARAMETERS AND INITIAL CONDITIONS
# ----------------------------------------------------------------------------------------

# Define parameters
theta = 20; # angle in degrees
v = 4.1; # initial launcher velocity in m/s
targetRange = 1.75;
ball.m = 0.6 # mass of ball in kg

while (ball.pos.x < targetRange - 0.04) or (ball.pos.x > targetRange + 0.04) :

    # Increment the launch angle
    theta += 2;

    # set (reset) the initial position and velocity
    ball.pos = vector(0, 1.17, 0) # initial position of the ball in(x, y, z) form, units are in meters
    ball.v = vector(v*cos(radians(theta)), v*sin(radians(theta)), 0) # initial velocity of car in (vx, vy, vz) form, units are m/s

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
        posgraph.plot(ball.pos.x, ball.pos.y) # plot x and y position vs. time
        trail.append(pos = ball.pos)
        timerDisplay.update(t)

        # Time update 
        t = t + deltat
    
    
    ### OUTPUT
    # --------------------------------------------------------------------------------------

    # Print the final time and the ball's final position
    print t
    print ball.pos

# Print the final time and the ball's final position
print t
print ball.pos
print theta

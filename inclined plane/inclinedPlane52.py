### INITIALIZE VPYTHON
# -----------------------------------------------------------------------

from __future__ import division
from visual import *
from physutil import *
from visual.graph import *

### SETUP ELEMENTS FOR GRAPHING, SIMULATION, VISUALIZATION, TIMING
# ------------------------------------------------------------------------

# Set window title
scene.title = "Incline Plane"

# Make scene background black
scene.background = color.black
scene.center = (5, 1, 0) # location at which the camera looks

# Define scene objects (units are in meters)

# 10-m long inclined plane whose center is at 5 m
inclinedPlane = box(pos = vector(5, 0, 0), size = (10, 0.02, 0.2),
    color = color.green, opacity = 0.3)

# 20-cm long cart on the inclined plane
cart = box(size = (0.2, 0.06, 0.06), color = color.blue)

# Set up graph with two plots
posgraph = PhysGraph()
velgraph = PhysGraph()
accelgraph = PhysGraph()

# Set up trail to mark the cart's trajectory
trail = curve(color = color.yellow, radius = 0.01) # units are in meters

# Set up motion map for cart
motionMap = MotionMap(cart, 3, # expected end time in seconds
    10, # number of markers to draw
    markerType = "breadcrumbs",
    dropTime = False)

# Set timer in top right of screen
timerDisplay = PhysTimer(9, 5) # timer position (units are in meters)


### SETUP PARAMETERS AND INITIAL CONDITIONS
# ----------------------------------------------------------------------------------------

# Define parameters
cart.m = 0.5 # mass of cart in kg

# initial position of the cart in(x, y, z) form, units are in meters
#   cart is positioned on the inclined plane at the far right end
cart.pos = vector(9.1, 0.04, 0.08)

cart.v = vector(0, 0, 0) # initial velocity of car in (vx, vy, vz) form, units are m/s

# angle of inclined plane relative to the horizontal
theta = 22.0 * (pi / 180.0)

# rotate the cart and the inclined plane based on the specified angle (counterclockwise)
inclinedPlane.rotate(angle = theta, origin = (0, 0, 0), axis = (0,0,1))
cart.rotate(angle = theta, origin = (0, 0, 0), axis = (0,0,1))

g = 9.8 # acceleration due to gravity; units are m/s/s

# Define time parameters
t = 0 # starting time
deltat = 0.0005  # time step units are s

print "initial cart position (m): ", cart.pos


### CALCULATION LOOP; perform physics updates and drawing
# ------------------------------------------------------------------------------------

while cart.pos.y > 0.04 :  # while the cart's y-position is greater than 0 (above the ground)
 
    # Required to make animation visible / refresh smoothly (keeps program from running faster
    #    than 1000 frames/s)
    rate(1000)    

    # Compute Net Force 
    # set the direction of the net force along the inclined plane
    Fnet = norm(inclinedPlane.axis)
    # set the magnitude to the component of the gravitational force parallel to the inclined plane
    Fnet.mag = -(cart.m * g * sin(theta))

    # Newton's 2nd Law 
    cart.v = cart.v + (Fnet/cart.m * deltat)

    # Position update 
    cart.pos = cart.pos + cart.v * deltat

    # Update motion map, graph, timer, and trail
    motionMap.update(t)
    posgraph.plot(t, mag(cart.pos)) # plot position (along inclined plane) vs. time
    velgraph.plot(t, mag(cart.v)) # plot velocity (along inclined plane) vs. time
    accelgraph.plot(t, mag(Fnet) / cart.m) # plot acceleration (along inclined plane) vs. time
    trail.append(pos = cart.pos)
    timerDisplay.update(t)

    # Time update 
    t = t + deltat
        
### OUTPUT
# --------------------------------------------------------------------------------------

# Print the final time and the cart's final position
print "final time (s): ", t
print "final cart position (m): ", cart.pos
print "final cart velocity (m/s): ", cart.v
print "final cart speed (m/s): ", mag(cart.v)
print "final cart acceleration (m/s/s): ", (mag(Fnet) / cart.m)


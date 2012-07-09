### INITIALIZE VPYTHON
# -----------------------------------------------------------------------

from __future__ import division
from visual import *
from physutil import *
from visual.graph import *

### SETUP ELEMENTS FOR GRAPHING, SIMULATION, VISUALIZATION, TIMING
# ------------------------------------------------------------------------

# Set window title
scene.title = "Mass on Spring"

# Make scene background black
scene.background = color.black
scene.center = (0, 1, 0)

# Define scene objects (units are in meters)
springLengthInitial = 1.0
spring = helix(axis = (0, 1, 0), length = springLengthInitial, radius = 0.1,
   thickness = 0.05, color = color.green)
mass = sphere(radius = 0.2, color = color.blue)

yaxis = PhysAxis(spring, 10, # 5 tick marks
    axisType = "y",
    labelOrientation = "left",
    startPos = vector(-0.5, 0, 0), # start the y axis at the left edge of the scene
    length = 2) # units are in meters

# Set up graph with three plots
energyGraph = PhysGraph(4)


### SETUP PARAMETERS AND INITIAL CONDITIONS
# ----------------------------------------------------------------------------------------

# Define parameters
mass.m = 0.5 # mass of cart in kg
mass.pos = vector(0, springLengthInitial, 0) # initial position of the mass in(x, y, z) form, units are in meters
mass.v = vector(0, 0, 0) # initial velocity of mass in (vx, vy, vz) form, units are m/s

g = -9.8 # acceleration due to gravity; units are m/s/s

k = 15.0 # spring constant; units are N/m

# Define time parameters
t = 0 # starting time
deltat = 0.001  # time step units are s


### CALCULATION LOOP; perform physics updates and drawing
# ------------------------------------------------------------------------------------

while t < 2 :  # run for one second
 
    # Required to make animation visible / refresh smoothly (keeps program from running faster
    #    than 1000 frames/s)
    rate(1000)
    
    # calculate the spring displacement
    springDisplacement = (spring.length - springLengthInitial)

    # compute the force on the mass by the spring
    Fspring = -k * springDisplacement
    
    # compute the force on the mass by the gravitational field
    Fgravity = mass.m * g
    
    # Compute Net Force 
    Fnet = vector(0, Fspring + Fgravity, 0)

    # Newton's 2nd Law 
    mass.v = mass.v + (Fnet/mass.m * deltat)

    # Position update 
    mass.pos = mass.pos + mass.v * deltat
    spring.length = mass.pos.y

    # Calculate energy
    KE = 0.5 * mass.m * mag(mass.v)**2
    GPE = mass.m * (-g) * mass.pos.y # relative to the ground
    EPE = 0.5 * k * springDisplacement**2
    
    # Update graphs
    energyGraph.plot(t, KE, GPE, EPE, (KE + GPE + EPE)) # plot energies

    # Time update 
    t = t + deltat
    
        
### OUTPUT
# --------------------------------------------------------------------------------------

# Print the final time
print t

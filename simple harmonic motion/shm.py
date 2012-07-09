### INITIALIZE VPYTHON
# -----------------------------------------------------------------------

from __future__ import division
from visual import *
from physutil import *
from visual.graph import *

### SETUP ELEMENTS FOR GRAPHING, SIMULATION, VISUALIZATION, TIMING
# ------------------------------------------------------------------------

# Set window title
scene.title = "Simple Harmonic Motion"

# Make scene background black
scene.background = color.black

# Define scene objects (units are in meters)
springLengthInitial = 1.0
spring = helix(pos = (-springLengthInitial, 0, 0), axis = (1, 0, 0),
   length = springLengthInitial, radius = 0.1,
   thickness = 0.05, color = color.green)
mass = sphere(radius = 0.2, color = color.blue)

axis = PhysAxis(spring, 11, # number of tick marks
    startPos = vector(-springLengthInitial, -0.5, 0), # start the x axis at the left edge of the scene
    length = 2) # units are in meters

# Set up graphs
energyGraph = PhysGraph(3)
motionGraph = PhysGraph(3)


### SETUP PARAMETERS AND INITIAL CONDITIONS
# ----------------------------------------------------------------------------------------

# Define parameters
mass.m = 0.5 # mass in kg
mass.pos = vector(0, 0, 0) # initial position of the mass in(x, y, z) form, units are in meters
mass.v = vector(1.0, 0, 0) # initial velocity of mass in (vx, vy, vz) form, units are m/s

k = 2.0 # spring constant; units are N/m

# Define time parameters
t = 0 # starting time
deltat = 0.001  # time step units are s


### CALCULATION LOOP; perform physics updates and drawing
# ------------------------------------------------------------------------------------

while t < 5 :  # run for one second
 
    # Required to make animation visible / refresh smoothly (keeps program from running faster
    #    than 1000 frames/s)
    rate(1000)
    
    # calculate the spring displacement
    springDisplacement = (spring.length - springLengthInitial)

    # compute the force on the mass by the spring
    Fspring = -k * springDisplacement
    
    # Compute Net Force
    Fnet = vector(Fspring, 0, 0)

    # Newton's 2nd Law 
    mass.v = mass.v + (Fnet/mass.m * deltat)

    # Position update 
    mass.pos = mass.pos + mass.v * deltat
    spring.length = springLengthInitial + mass.pos.x

    # Calculate energy
    KE = 0.5 * mass.m * mag(mass.v)**2
    EPE = 0.5 * k * springDisplacement**2
    
    # Update graphs
    energyGraph.plot(t, KE, EPE, (KE + EPE)) # plot energies
    motionGraph.plot(t, mass.pos.x, mass.v.x, Fnet.x/mass.m) # plot position, velocity, and acceleration vs. time

    # Time update 
    t = t + deltat
    
    
### OUTPUT
# --------------------------------------------------------------------------------------

# Print the final time
print t

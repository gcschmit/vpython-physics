from __future__ import division, print_function  
from visual import *  
from visual.graph import *  
scene.background = color.white  
scene.height = 50  
scene.width = 50  
scene.x = scene.y =0  
## Josh Gates 2012, started with kernel of Ruth Chabay program  
print ("""  
Click anywhere in display window to start.  
Click to stop.  
Momentum and velocity are shown as .6 kg block is pushed with a constant 1,000,000 N force.  
Uncomment gamma line to remove classical p def'n/assumption""")  
  
## CONSTANTS  
delta_t = 0.01  ## for 100 steps  
mblock = 0.06  
c=3e8  
Fnet = vector(1e6,0,0)  
  
## OBJECTS & INITIAL VALUES  
pblock = mblock*vector(0,0,0)  
gamma = 1  
  
# start time at 0  
t = 0  
scene.center = (0,.1,0)  # move camera up  
scene.range = 0.15  
  
## GRAPH STUFF  
gp = gdisplay(background=color.white, foreground=color.black, y=0, x=250, height=300,  
       title='Momentum vs. time: block with constant F', xtitle='Time (s)', ytitle='Position (m)',  
       ymax=3e7,xmax=30)  
blockp = gcurve(color=color.magenta)  
blockp.plot(pos=(t,pblock.x)) ## initial pos.x of block  
  
gv = gdisplay(background=color.white, foreground=color.black, y=300, x=250, height=300,  
       title='Velocity vs. time: block with constant F', xtitle='Time (s)', ytitle='Velocity (m/s)',  
       ymax = 3e8, ymin=0, xmax=30)  
blockv = gcurve(color=color.blue)  
blockv.plot(pos=(t,pblock.x/(gamma*mblock))) #initial velocity  
asymptote=gcurve(color=color.red)  
  
  
scene.mouse.getclick()  
stopper='go'  
  
a=.1  
while a<1000:  
  asymptote.plot(pos=(30/a,3e8))  
  a=a+1  
  
## CALCULATIONS  
while stopper=='go':  
  rate(500)   
  
  pblock = pblock + Fnet*delta_t  
  
  # comment to make classical approximation  
  #gamma = (1-(pblock.x)**2/(mblock**2 * c**2+(pblock.x)**2))**-.5  
    
  # update time  
  t = t + delta_t  
  # plot pos.x, velocity.x of block  
  blockp.plot(pos=(t,pblock.x))  
  blockv.plot(pos=(t,pblock.x/(gamma*mblock)))  
##  print t, block.y  
  if scene.mouse.clicked:  
    stopper='stop'  
   
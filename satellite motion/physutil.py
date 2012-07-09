# physutil.py v1.22
# Copyright (c) 2011-2012 GT Physics Education Research Group
# License: GPL-3.0 (http://opensource.org/licenses/GPL-3.0)

# This module is built to simplify and assist high school physics students
# in the construction of models for lab exercises using VPython.


# Revisions by date

# v1.22 24 January 2011 -- Danny Caballero
# Added labelColor attribute to PhysAxis, MotionMap, and MotionMapN
# controls color of text

# v1.21 5 December 2011 -- Danny Caballero
# Added timerColor attribute to PhysTimer
# controls color of text

# v1.2 19 October 2011 -- Danny Caballero
# Added MotionMapN, a class that allows the placing of breadcrumbs or arrows
# every "n" steps.

# v1.13 26 September 2011 -- Daniel Borrero
# Fixed unit test bug for PhysTimer

# v1.12 30 August 2011 -- Daniel Borrero
# Fixed bug in PhysTimer output
# E.g., 2.00 s is now displayed as 00:00:02.00 instead of 00:00:01:100

# v1.11 29 August 2011 -- Danny Caballero
# Changed License to GNU

# v1.1 15 August 2011 -- Daniel Borrero
# Print statements made compatible with Python 3.1

# v1.01 16 July 2011 -- Danny Caballero
# Added ability to change PhysAxis color using axisColor

# v1.0 29 April 2011 -- CS Build Team
# Heavy Modification

# v0.1 05 January 2011 -- Danny Caballero
# Initial Build

from __future__ import division
import unittest

"""
#
#
# UNIT TESTING / IMPORT SETUP CODE ------------------------------------------------------------
#
#
"""

# Determine whether we are being used as a module or just running unittests (for mock purposes this is important)
if __name__ == "__main__":
    # If we are unit testing, set up mock objects (must be done before classes are defined below!)
    from visual import vector
    class Mock:
        def __init__(self, name, *args, **kwargs):
            self.name = name
            self.called = 0
            
        def __call__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            for name in kwargs:
                setattr(self, name, kwargs[name])
            self.called += 1
            return self

        def reset(self):
            self.called = 0
                
    color = Mock("color")
    color.red = "red"
    color.green = "green"
    color.blue = "blue"
    color.yellow = "yellow"
    color.orange = "orange"
    color.cyan = "cyan"
    color.magenta = "magenta"
    color.white = "white"

    arrow = Mock("arrow")
    label = Mock("label")
    points = Mock("points")
    curve = Mock("curve")
    gdisplay = Mock("gdisplay")
    gcurve = Mock("gcurve")
    gcurve.plots = []
    def mockPlot(pos):
        gcurve.plots.append(pos)
    gcurve.plot = mockPlot

    """
    vector = Mock("vector")
    def call(x, y, z):
        vector.x = x
        vector.y = y
        vector.z = z
    vector.__call__ = call
    """

else:
    # These are the actual imports for the utility
    from visual import *
    from visual.graph import *


"""
#
#
# ACTUAL PHYSUTIL CODE FOLLOWS --------------------------------------------------
#
#
"""

# Initialize window positions for students (if we aren't unit testing)
if __name__ != "__main__":
    scene.x = 50
    scene.y = 50

# Helper function for returning proper size of something
def obj_size(obj):
    if type(obj) == box or type(obj) == pyramid:
        return obj.size
    elif type(obj) == sphere:
        return vector(obj.radius, obj.radius, obj.radius)

class MotionMap:
    """
    This class assists students in constructing motion maps 
    using either arrows (measuring a quantity) or "breadcrumbs" 
    (with timestamps).
    """
    
    def __init__(self, obj, tf, numMarkers, markerType="arrow", 
                markerScale=1, markerColor=color.red, 
                labelMarkerOrder=True, labelMarkerOffset=vector(0,0,0),
                dropTime=False, timeOffset=vector(0,0,0), arrowOffset=vector(0,0,0), labelColor=color.white):
        # MotionMap
        # obj - object to track in mapping / placing markers
        # tf - expected tFinal, used to space marker placement over time
        # numMarkers - number of markers to place
        # markerType - determines type of motionmap; options are "arrow" or "breadcrumbs"
        # markerScale - replaces pSize / quantscale from motionmodule.py depending on type
        # markerColor - color of markers
        # labelMarkerOrder - drop numbers of markers?
        # labelMarkerOffset - amount to offset numbering by
        # dropTime - boolean determining whether a timestamp should be placed along with the marker
        # timeOffset - if dropTime is True, determines the offset, if any, of the label from the marker
        # arrowOffset - shift an arrow by an amount (x,y,z), useful for two arrows views

        self.obj = obj
        self.tf = tf
        self.numMarkers = numMarkers
        self.markerType = markerType
        self.markerScale = markerScale
        self.markerColor = markerColor
        self.labelMarkerOrder = labelMarkerOrder
        self.labelMarkerOffset = labelMarkerOffset
        self.timeOffset = timeOffset
        self.dropTime = dropTime
        self.arrowOffset = arrowOffset
        self.labelColor = labelColor

        # Calculate size of interval for each step, set initial step index
        try:
            self.interval = self.tf / self.numMarkers
        except TypeError as err:
            print("**********TYPE ERROR**********")
            print("Please check that you are not passing in a variable of the wrong type (e.g. a scalar as a vector, or vice-versa)!")
            print("******************************")
            print(err)
            raise err
        self.curMarker = 0


    def update(self, t, quantity=1):
        try:
            # Display new arrow if t has broken next threshold
            if t > (self.interval * self.curMarker):
                # Increment threshold
                self.curMarker += 1
                
                # Display marker!
                if self.markerType == "arrow":
                    arrow(pos=self.obj.pos+self.arrowOffset, 
                        axis=self.markerScale*quantity, color=self.markerColor)
                elif self.markerType == "breadcrumbs":
                    points(pos=self.obj.pos, 
                        size=10*self.markerScale*quantity, color=self.markerColor)

                #Also display timestamp if requested
                if self.dropTime is not False:
                    epsilon = vector(0,self.markerScale*.5,0)+self.timeOffset
                    droptimeText = label(pos=self.obj.pos+epsilon, text='t='+str(t)+'s', height=10, box=False, color=self.labelColor)

                # Same with order label
                if self.labelMarkerOrder is not False:
                    label(pos=self.obj.pos-vector(0,self.markerScale*.5,0)+self.labelMarkerOffset, text=str(self.curMarker), height=10, box=False, color=self.labelColor)
        except TypeError as err:
            print("**********TYPE ERROR**********")
            print("Please check that you are not passing in a variable of the wrong type (e.g. a scalar as a vector, or vice-versa)!")
            print("******************************")
            print(err)
            raise err

class MotionMapN:
    """
    This class assists students in constructing motion maps 
    using either arrows (measuring a quantity) or "breadcrumbs" 
    (with timestamps).
    """
    
    def __init__(self, obj, dt, numSteps, markerType="arrow", 
                markerScale=1, markerColor=color.red, 
                labelMarkerOrder=True, labelMarkerOffset=vector(0,0,0),
                dropTime=False, timeOffset=vector(0,0,0), arrowOffset=vector(0,0,0), labelColor=color.white):
        # MotionMapN
        # obj - object to track in mapping / placing markers
        # dt - time between steps
        # numSteps - number of steps between markers
        # markerType - determines type of motionmap; options are "arrow" or "breadcrumbs"
        # markerScale - replaces pSize / quantscale from motionmodule.py depending on type
        # markerColor - color of markers
        # labelMarkerOrder - drop numbers of markers?
        # labelMarkerOffset - amount to offset numbering by
        # dropTime - boolean determining whether a timestamp should be placed along with the marker
        # timeOffset - if dropTime is True, determines the offset, if any, of the label from the markers
        # arrowOffset - shift an arrow by an amount (x,y,z), useful for two arrows views
        
        self.obj = obj
        self.dt = dt
        self.numSteps = numSteps
        self.markerType = markerType
        self.markerScale = markerScale
        self.markerColor = markerColor
        self.labelMarkerOrder = labelMarkerOrder
        self.labelMarkerOffset = labelMarkerOffset
        self.timeOffset = timeOffset
        self.dropTime = dropTime
        self.arrowOffset = arrowOffset
        self.labelColor = labelColor
        
        # Calculate size of interval for each step, set initial step index
        try:
            self.interval = self.dt * self.numSteps
        except TypeError as err:
            print("**********TYPE ERROR**********")
            print("Please check that you are not passing in a variable of the wrong type (e.g. a scalar as a vector, or vice-versa)!")
            print("******************************")
            print(err)
            raise err
        self.curMarker = 0


    def update(self, t, quantity=1):
        try:

            threshold = self.interval * self.curMarker
            # Display new arrow if t has broken new threshold
            if t >= threshold:

                # Increment marker count
                self.curMarker += 1
                
                # Display marker!
                if self.markerType == "arrow":
                    arrow(pos=self.obj.pos+self.arrowOffset, 
                        axis=self.markerScale*quantity, color=self.markerColor)
                elif self.markerType == "breadcrumbs":
                    points(pos=self.obj.pos, 
                        size=10*self.markerScale*quantity, color=self.markerColor)

                #Also display timestamp if requested
                if self.dropTime is not False:
                    epsilon = vector(0,self.markerScale*.5,0)+self.timeOffset
                    droptimeText = label(pos=self.obj.pos+epsilon, text='t='+str(t)+'s', height=10, box=False, color=self.labelColor)

                # Same with order label
                if self.labelMarkerOrder is not False:
                    label(pos=self.obj.pos-vector(0,self.markerScale*.5,0)+self.labelMarkerOffset, text=str(self.curMarker), height=10, box=False, color=self.labelColor)
                
        except TypeError as err:
            print("**********TYPE ERROR**********")
            print("Please check that you are not passing in a variable of the wrong type (e.g. a scalar as a vector, or vice-versa)!")
            print("******************************")
            print(err)
            raise err

class PhysAxis:
    """
    This class assists students in creating dynamic axes for their models.
    """
    
    def __init__(self, obj, numLabels, axisType="x", axis=vector(1,0,0), startPos=None, 
                length=None, labels = None, labelOrientation="down", axisColor=color.yellow, labelColor=color.white):
        # PhysAxis
        # obj - Object which axis is oriented based on by default
        # numLabels - number of labels on axis
        # axisType - sets whether this is a default axis of x or y, or an arbitrary axis
        # axis - unit vector defining the orientation of the axis to be created IF axisType = "arbitrary"
        # startPos - start position for the axis - defaults to (-obj_size(obj).x/2,-4*obj_size(obj).y,0)
        # length - length of the axis - defaults to obj_size(obj).x
        # labelOrientation - how labels are placed relative to axis markers - "up", "down", "left", or "right"

        try:
            self.intervalMarkers = []
            self.intervalLabels = []
            self.labelText = labels
            self.obj = obj
            self.lastPos = vector(self.obj.pos.x, self.obj.pos.y, self.obj.pos.z)
            self.numLabels = numLabels
            self.axisType = axisType
            self.axis = axis if axisType != "y" else vector(0,1,0)
            self.length = length if (length is not None) else obj_size(obj).x
            self.startPos = startPos if (startPos is not None) else vector(-obj_size(obj).x/2,-4*obj_size(obj).y,0)
            self.axisColor = axisColor
            self.labelColor = labelColor

            if labelOrientation == "down":
                self.labelShift = vector(0,-0.05*self.length,0)
            elif labelOrientation == "up":
                self.labelShift = vector(0,0.05*self.length,0)
            elif labelOrientation == "left":
                self.labelShift = vector(-0.1*self.length,0,0)
            elif labelOrientation == "right":
                self.labelShift =  vector(0.1*self.length,0,0)  
            
            self.__reorient()
        except TypeError as err:
            print("**********TYPE ERROR**********")
            print("Please check that you are not passing in a variable of the wrong type (e.g. a scalar as a vector, or vice-versa)!")
            print("******************************")
            print(err)
            raise err    

    def update(self):
        try:
            # Determine if reference obj. has shifted since last update, if so shift us too
            if self.obj.pos != self.lastPos:
                diff = self.obj.pos - self.lastPos

                for i in range(len(self.intervalMarkers)):
                    self.intervalMarkers[i].pos += diff
                    self.intervalLabels[i].pos += diff
                self.axisCurve.pos = [x + diff for x in self.axisCurve.pos]

                self.lastPos = vector(self.obj.pos.x, self.obj.pos.y, self.obj.pos.z)
        except TypeError as err:
            print("**********TYPE ERROR**********")
            print("Please check that you are not passing in a variable of the wrong type (e.g. a scalar as a vector, or vice-versa)!")
            print("******************************")
            print(err)
            raise err
    
    def reorient(self, axis=None, startPos=None, length=None, labels=None, labelOrientation=None):
        try:
            # Determine which, if any, parameters are being modified
            self.axis = axis if axis is not None else self.axis
            self.startPos = startPos if startPos is not None else self.startPos
            self.length = length if length is not None else self.length
            self.labelText = labels if labels is not None else self.labels

            # Re-do label orientation as well, if it has been set
            if labelOrientation == "down":
                self.labelShift = vector(0,-0.05*self.length,0)
            elif labelOrientation == "up":
                self.labelShift = vector(0,0.05*self.length,0)
            elif labelOrientation == "left":
                self.labelShift = vector(-0.1*self.length,0,0)
            elif labelOrientation == "right":
                self.labelShift =  vector(0.1*self.length,0,0)

            self.__reorient()
        except TypeError as err:
            print("**********TYPE ERROR**********")
            print("Please check that you are not passing in a variable of the wrong type (e.g. a scalar as a vector, or vice-versa)!")
            print("******************************")
            print(err)
            raise err

    def __reorient(self):
        # Actual internal axis setup code... determines first whether we are creating or updating
        updating = True if len(self.intervalMarkers) > 0 else False

        # Then determines the endpoint of the axis and the interval
        final = self.startPos + (self.length * self.axis)
        interval = (self.length / (self.numLabels-1)) * self.axis

        # Loop for each interval marker, setting up or updating the markers and labels
        i=0
        while i<self.numLabels:      
            intervalPos = self.startPos+(i*interval)

            # Determine text for this label
            if self.labelText is not None:
                labelText = self.labelText[i]
            elif self.axisType == "y":
                labelText = "%.2f" % intervalPos.y 
            else:
                labelText = "%.2f" % intervalPos.x

            if updating:
                self.intervalMarkers[i].pos = intervalPos
                self.intervalLabels[i].pos = intervalPos+self.labelShift
                self.intervalLabels[i].text = str(labelText)
            else:
                self.intervalMarkers.append(
                    points(pos=intervalPos,color=self.axisColor,size = 6) )
                self.intervalLabels.append(
                    label(pos=intervalPos+self.labelShift, text=str(labelText),box=False,height = 8, color=self.labelColor) )
            i=i+1

        # Finally, create / update the line itself!
        if updating:
            self.axisCurve.pos = [self.startPos,final]
        else:
            self.axisCurve = curve(pos=[self.startPos,final],color = self.axisColor)
    
class PhysTimer:
    """
    This class assists students in creating an onscreen timer display.
    """
    
    def __init__(self, x, y, useScientific=False, timerColor=color.white):
        
        # PhysTimer
        # x,y - world coordinates for the timer location
        # useScientific - bool to turn off/on scientific notation for time
        # timerColor - attribute controlling the color of the text
        
        try:
            self.useScientific = useScientific
            self.timerColor = timerColor
            if useScientific is False:
                self.timerLabel = label(pos=vector(x,y,0), text='00:00:00.00', box=False)
            else:
                self.timerLabel = label(pos=vector(x,y,0), text='00E01', box=False)
        except TypeError as err:
            print("**********TYPE ERROR**********")
            print("Please check that you are not passing in a variable of the wrong type (e.g. a scalar as a vector, or vice-versa)!")
            print("******************************")
            print(err)
            raise err

    def update(self, t):
        try:
            # Basically just use sprintf formatting according to either stopwatch or scientific notation
            if self.useScientific:
                self.timerLabel.text = "%.4E" % t
            else:
                hours = int(t / 3600)
                mins = int((t / 60) % 60)
                secs = int(t % 60)
                frac = int(round(100 * (t % 1)))
                if frac == 100:
                    frac = 0
                    secs = secs + 1;
                self.timerLabel.text = "%02d:%02d:%02d.%02d" % (hours, mins, secs, frac)
        except TypeError as err:
            print("**********TYPE ERROR**********")
            print("Please check that you are not passing in a variable of the wrong type (e.g. a scalar as a vector, or vice-versa)!")
            print("******************************")
            print(err)
            raise err

class PhysGraph:
    """
    This class assists students in creating graphs with advanced functionality.
    """ 
    
    # Static, pre-determined list of colors from which each line will be generated
    graphColors = [color.red, color.green, color.blue, color.yellow, 
                    color.orange, color.cyan, color.magenta, color.white]

    def __init__(self, numPlots=1):
        try:
            # Create our specific graph window
            self.graphDisplay = gdisplay(475,350)
            self.numPlots = numPlots

            # Initialize each plot curve
            self.graphs = []
            for i in range(numPlots):
                self.graphs.append(gcurve(color=PhysGraph.graphColors[i%len(PhysGraph.graphColors)]))
        except TypeError as err:
            print("**********TYPE ERROR**********")
            print("Please check that you are not passing in a variable of the wrong type (e.g. a scalar as a vector, or vice-versa)!")
            print("******************************")
            print(err)
            raise err

    def plot(self, independent, *dependents):
        try:
            if len(dependents) != self.numPlots:
                raise Exception("ERROR: Number of dependent parameters given does not match numPlots given at initialization!")

            # Plot each line based on its parameter!
            for i in range(len(dependents)):
                self.graphs[i].plot(pos=(independent,dependents[i]))
        except TypeError as err:
            print("**********TYPE ERROR**********")
            print("Please check that you are not passing in a variable of the wrong type (e.g. a scalar as a vector, or vice-versa)!")
            print("******************************")
            print(err)
            raise err

"""
#
#
# UNIT TESTING BELOW ----------------------------------------------------------------------
#
#
"""

class TestMotionMap(unittest.TestCase):
    def setUp(self):
        self.obj = Mock("obj")
        self.obj.pos = vector(0,0,0)
        self.tf = 10
        self.numMarkers = 5
        self.timeOffset = vector(1,1,1)
        self.markerScale = 2
        self.arrowOffset = vector(1,1,1)

        arrow.reset()
        points.reset()
        label.reset()

        self.map = MotionMap(self.obj, self.tf, self.numMarkers, markerType="arrow", 
                    markerScale=2, markerColor=color.green,
                    dropTime=True, timeOffset=self.timeOffset, arrowOffset=self.arrowOffset)

    def test_init(self):
        self.assertEqual(self.obj, self.map.obj)
        self.assertEqual(self.tf, self.map.tf)
        self.assertEqual(self.numMarkers, self.map.numMarkers)
        self.assertEqual("arrow", self.map.markerType)
        self.assertEqual(self.markerScale, self.map.markerScale)
        self.assertEqual(color.green, self.map.markerColor)
        self.assertEqual(vector(1,1,1), self.map.timeOffset)
        self.assertEqual(True, self.map.dropTime)
        self.assertEqual(self.map.interval, self.tf / self.numMarkers)
        self.assertEqual(self.map.curMarker, 0)
        self.assertEqual(vector(1,1,1), self.map.arrowOffset)
        

    def test_update(self):
        self.map.curMarker = 1

        self.map.update(0)
        self.assertEqual(arrow.called, 0)
        self.assertEqual(points.called, 0)
        self.assertEqual(label.called, 0)

        self.map.update(3, quantity=2)
        self.assertEqual(arrow.called, 1)
        self.assertEqual(points.called, 0)
        self.assertEqual(label.called, 2)
        self.assertEqual(self.map.curMarker, 2)
        self.assertEqual(arrow.pos, self.obj.pos+self.arrowOffset)
        self.assertEqual(arrow.axis, 4)
        self.assertEqual(arrow.color, color.green)
        self.assertEqual(label.text, "2")

class TestMotionMapN(unittest.TestCase):
    def setUp(self):
        self.obj = Mock("obj")
        self.obj.pos = vector(0,0,0)
        self.dt = 1
        self.numSteps = 5
        self.timeOffset = vector(1,1,1)
        self.markerScale = 2
        self.arrowOffset = vector(1,1,1)

        arrow.reset()
        points.reset()
        label.reset()

        self.map = MotionMapN(self.obj, self.dt, self.numSteps, markerType="arrow", 
                    markerScale=2, markerColor=color.green,
                    dropTime=True, timeOffset=self.timeOffset, arrowOffset=self.arrowOffset)

    def test_init(self):
        self.assertEqual(self.obj, self.map.obj)
        self.assertEqual(self.dt, self.map.dt)
        self.assertEqual(self.numSteps, self.map.numSteps)
        self.assertEqual("arrow", self.map.markerType)
        self.assertEqual(self.markerScale, self.map.markerScale)
        self.assertEqual(color.green, self.map.markerColor)
        self.assertEqual(vector(1,1,1), self.map.timeOffset)
        self.assertEqual(True, self.map.dropTime)
        self.assertEqual(self.map.curMarker, 0)
        self.assertEqual(vector(1,1,1), self.map.arrowOffset)

    def test_update(self):
        self.map.curMarker = 1

        self.map.update(0)
        self.assertEqual(arrow.called, 0)
        self.assertEqual(points.called, 0)
        self.assertEqual(label.called, 0)

        self.map.update(3, quantity=2)
        self.assertEqual(arrow.called, 0)
        self.assertEqual(points.called, 0)
        self.assertEqual(label.called, 0)
        self.assertEqual(self.map.curMarker, 1)
        self.assertEqual(arrow.pos, self.obj.pos+self.arrowOffset)
        self.assertEqual(arrow.axis, 4)
        self.assertEqual(arrow.color, color.green)
        self.assertEqual(label.text, "2")

class TestPhysAxis(unittest.TestCase):
    def setUp(self):
        self.obj = Mock("obj")
        self.obj.pos = vector(0,0,0)
        self.numLabels = 5
        self.axis = vector(1,1,1)
        self.startPos = vector(0,1,0)
        self.length = 10
        self.labels = ["a", "b", "c", "d", "e"]
        self.wrongLabels = ["a"]
        self.axisType = "arbitrary"
        self.labelOrientation="left"

        curve.reset()

        self.physAxis = PhysAxis(self.obj, self.numLabels, axisType=self.axisType, axis=self.axis, 
                    startPos=self.startPos, length=self.length, labels = self.labels,
                    labelOrientation=self.labelOrientation)

    
    def test_init(self):
        self.assertEqual(self.physAxis.labelText, self.labels)
        self.assertEqual(self.physAxis.obj, self.obj)
        self.assertEqual(self.physAxis.lastPos, self.obj.pos)
        self.assertEqual(self.physAxis.numLabels, self.numLabels)
        self.assertEqual(self.physAxis.axis, self.axis)
        self.assertEqual(self.physAxis.length, self.length)
        self.assertEqual(self.physAxis.startPos, self.startPos)
        self.assertEqual(self.physAxis.axisType, self.axisType)
        self.assertEqual(self.physAxis.labelShift, vector(-0.1*self.length, 0, 0))
        self.assertEqual(len(self.physAxis.intervalMarkers), self.numLabels)
        self.assertEqual(len(self.physAxis.intervalLabels), self.numLabels)
        
        intervalPos = self.startPos+(self.length * self.axis)
        self.assertEqual(self.physAxis.intervalMarkers[-1].pos, intervalPos)
        self.assertEqual(self.physAxis.intervalLabels[-1].pos, intervalPos+self.physAxis.labelShift)
        self.assertEqual(self.physAxis.intervalLabels[-1].text, "e")

        self.assertEqual(curve.called, 1)

    def test_reorient(self):
        newAxis = vector(0,0,1)
        startPos = vector(1,0,0)
        otherLabels = ["f", "g", "h", "i", "j"]
        self.physAxis.reorient(axis=newAxis, startPos=startPos, length=1, 
            labels=otherLabels, labelOrientation="right")
        self.assertEqual(self.physAxis.axis, newAxis)
        self.assertEqual(self.physAxis.startPos, startPos)
        self.assertEqual(self.physAxis.length, 1)
        self.assertEqual(self.physAxis.labelShift, vector(0.1, 0, 0))

        intervalPos = startPos+newAxis
        self.assertEqual(self.physAxis.intervalMarkers[-1].pos, intervalPos)
        self.assertEqual(self.physAxis.intervalLabels[-1].pos, intervalPos+self.physAxis.labelShift)
        self.assertEqual(self.physAxis.intervalLabels[-1].text, "j")

        self.assertEqual(curve.called, 1)


    def test_update(self):
        startMarkerPos = vector(self.physAxis.intervalMarkers[-1].pos.x, 
                                self.physAxis.intervalMarkers[-1].pos.y, 
                                self.physAxis.intervalMarkers[-1].pos.z)
        startLabelPos = vector(self.physAxis.intervalLabels[-1].pos.x,
                                self.physAxis.intervalLabels[-1].pos.y,
                                self.physAxis.intervalLabels[-1].pos.z)
        startCurvePos = vector(self.physAxis.axisCurve.pos[0].x,
                                self.physAxis.axisCurve.pos[0].y,
                                self.physAxis.axisCurve.pos[0].z)

        self.physAxis.update()

        self.assertEqual(startMarkerPos, self.physAxis.intervalMarkers[-1].pos)
        self.assertEqual(startLabelPos, self.physAxis.intervalLabels[-1].pos)
        self.assertEqual(startCurvePos, self.physAxis.axisCurve.pos[0])

        self.physAxis.obj.pos = self.physAxis.obj.pos + vector(1,1,1)
        self.physAxis.update()

        self.assertNotEqual(startMarkerPos, self.physAxis.intervalMarkers[-1].pos)
        self.assertNotEqual(startLabelPos, self.physAxis.intervalLabels[-1].pos)
        self.assertNotEqual(startCurvePos, self.physAxis.axisCurve.pos[0])

class TestPhysGraph(unittest.TestCase):
    def setUp(self):
        self.physGraph = PhysGraph(numPlots = 5)

    def test_init(self):
        self.assertEqual(self.physGraph.graphDisplay.args, (475, 350))
        self.assertEqual(self.physGraph.numPlots, 5)
        self.assertEqual(len(self.physGraph.graphs), 5)

    def test_plot(self):
        self.assertRaises(Exception, self.physGraph.plot, vector(0,0,0), vector(1,1,1))

        self.physGraph.plot(vector(0,0,0), vector(1,1,1), vector(2,2,2), vector(3,3,3), vector(4,4,4), vector(5,5,5))
        self.assertEqual(len(self.physGraph.graphs[-1].plots), 5)
        self.assertEqual(self.physGraph.graphs[-1].plots[0], (vector(0,0,0), vector(1,1,1)))

class TestPhysTimer(unittest.TestCase):
    def setUp(self):
        self.timer = PhysTimer(1,1)

    def test_init(self):
        self.assertEquals(self.timer.timerLabel.text, "00:00:00.00")
        self.assertEquals(self.timer.timerLabel.pos, vector(1,1,0))

    def test_update(self):
        self.timer.update(3923.65)
        self.assertEquals(self.timer.timerLabel.text, "01:05:23.65")

        self.timer.useScientific=True
        self.timer.update(3923.65)
        self.assertEquals(self.timer.timerLabel.text, "3.9237E+03")


# Now set up unittests to be executed when module is run individually
if __name__ == "__main__":
    print("Beginning unit tests!")
    unittest.main()

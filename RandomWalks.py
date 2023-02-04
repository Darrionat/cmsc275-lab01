# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 13:09:47 2019

@author: Kerri-Ann Norton
"""
import random

"""
Represents a point in the cartesian plane, or equivalently, a point in R2.
"""


class Location(object):
    def __init__(self, x, y):
        """x and y are numbers"""
        self.x, self.y = x, y

    # Moves this current location by dX and dY
    def move(self, deltaX, deltaY):
        """deltaX and deltaY are numbers"""
        return Location(self.x + deltaX, self.y + deltaY)

    # The methods below change the points' coordinates.
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    # Computes the distance between two points with the L2 norm (Euclidean norm).
    def distFrom(self, other):
        ox, oy = other.x, other.y
        xDist, yDist = self.x - ox, self.y - oy
        return (xDist ** 2 + yDist ** 2) ** 0.5

    # Returns a string representation of this point
    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'


"""
Represents a dictionary of drunks that allows one to add, move, but not remove drunks. 
"""


class Field(object):
    def __init__(self):
        self.drunks = {}

    # The following methods allow adding and moving Drunks within the dictionary.
    def addDrunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        else:
            self.drunks[drunk] = loc

    def moveDrunk(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep()
        currentLocation = self.drunks[drunk]
        # use move method of Location to get new location
        self.drunks[drunk] = currentLocation.move(xDist, yDist)

    def getLoc(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        return self.drunks[drunk]


'''
Represents a string.
'''


class Drunk(object):
    def __init__(self, name=None):
        """Assumes name is a str"""
        self.name = name

    def __str__(self):
        if self != None:
            return self.name
        return 'Anonymous'


"""
Represents a drunk that steps only by one unit at a time in a random direction on either the x-axis or y-axis.
This is equivalent to the drunk only moving to other lattice points in R2.
"""


class UsualDrunk(Drunk):
    # Randomly steps the drunk to another lattice points.
    def takeStep(self):
        stepChoices = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return random.choice(stepChoices)


# Walks the drunk for a given number of steps, and then returns the euclidian distance from the starting point to the final.
def walk(f, d, numSteps):
    """Assumes: f a Field, d a Drunk in f, and numSteps an int >= 0.
       Moves d numSteps times; returns the distance between the
       final location and the location at the start of the  walk."""
    start = f.getLoc(d)
    for s in range(numSteps):
        f.moveDrunk(d)
    return start.distFrom(f.getLoc(d))


# Simulates multiple trials of random walks of a given length for a particular kind of drunk.
def simWalks(numSteps, numTrials, dClass):
    """Assumes numSteps an int >= 0, numTrials an int > 0,
         dClass a subclass of Drunk
       Simulates numTrials walks of numSteps steps each.
       Returns a list of the final distances for each trial"""
    Homer = dClass()
    origin = Location(0, 0)
    distances = []
    for t in range(numTrials):
        f = Field()
        f.addDrunk(Homer, origin)
        # distances.append(round(walk(f, Homer, numTrials), 1))
        # next line is the correction made in the text
        distances.append(round(walk(f, Homer, numSteps), 1))
    return distances


# Runs trials for multiple walk lengths for a particular kind of drunk.
def drunkTest(walkLengths, numTrials, dClass):
    """Assumes walkLengths a sequence of ints >= 0
         numTrials an int > 0, dClass a subclass of Drunk
       For each number of steps in walkLengths, runs simWalks with
         numTrials walks and prints results"""
    for numSteps in walkLengths:
        distances = simWalks(numSteps, numTrials, dClass)
        print(dClass.__name__, 'random walk of', numSteps, 'steps')
        print(' Mean =', round(sum(distances) / len(distances), 4))
        print(' Max =', max(distances), 'Min =', min(distances))


"""
Represents a Drunk that moves exactly like a UsualDrunk except when moving in the leftwards direction, 
the ColdDrunk will move by 2 units.
"""


class ColdDrunk(Drunk):
    def takeStep(self):
        stepChoices = [(0.0, 1.0), (0.0, -2.0), (1.0, 0.0), \
                       (-1.0, 0.0)]
        return random.choice(stepChoices)


"""
The EWDrunk behaves the same as the UsualDrunk with the restriction that it can not move vertically (along the y-axis).
"""


class EWDrunk(Drunk):
    def takeStep(self):
        stepChoices = [(1.0, 0.0), (-1.0, 0.0)]
        return random.choice(stepChoices)


"""
Runs simulations of random walks that vary the type of drunk and the length of walks.
"""


def simAll(drunkKinds, walkLengths, numTrials):
    for dClass in drunkKinds:
        drunkTest(walkLengths, numTrials, dClass)

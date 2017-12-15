# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import pylab
import numpy

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        #raise NotImplementedError
        self.width = width
        self.height = height
        self.clean = {}
        for x in range(self.width):
            for y in range(self.height):
                self.clean[(x,y)] = False
        
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = math.floor(pos.getX())
        y = math.floor(pos.getY())
        self.clean[(x, y)]=True
        
        #raise NotImplementedError

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.clean[(m,n)]
        #raise NotImplementedError
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height
        #raise NotImplementedError

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return sum(1 for x in self.clean.values() if x)        
        #raise NotImplementedError

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        randWidth = random.random() * self.width
        randHeight = random.random() * self.height
        return Position(randWidth, randHeight)
        
        #raise NotImplementedError

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return (pos.getX() >= 0 and pos.getX() <= self.width and pos.getY() >= 0 and pos.getY() <= self.height)
        #raise NotImplementedError


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed        
        self.direction = int(random.random()*360)
        self.pos = self.room.getRandomPosition()        
        self.room.cleanTileAtPosition(self.pos)
        #raise NotImplementedError

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos
        #raise NotImplementedError
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction
        #raise NotImplementedError

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.pos = position
        #raise NotImplementedError

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction        
        #raise NotImplementedError

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.pos = self.pos.getNewPosition(self.direction, self.speed)    
        self.room.cleanTileAtPosition(self.pos)
        
        #raise NotImplementedError


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        
        tempPos = self.pos.getNewPosition(self.direction, self.speed)
        #
        #print tempPos.getX(), tempPos.getY()
        if self.room.isPositionInRoom(tempPos):
            #print "the position is valid."            
            self.setRobotPosition(tempPos)
            self.room.cleanTileAtPosition(self.pos)
        else:
            self.direction = int(random.random()*360)
    
        #raise NotImplementedError

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    totalTimeSteps = []    
    for trial in range(num_trials):
        #anim = ps6_visualize.RobotVisualization(num_robots, width, height)        
        # Create new room and reset it for each trial
        trialRoom = RectangularRoom(width, height)

        # Initialize the number of timesteps required in each trial
        timeSteps = 0       
        # Initialize the list of robots
        robots = [] 
        for i in range(num_robots):
            robots.append(robot_type(trialRoom, speed))
            
        # Loop that runs robots through the room.
        # Condition = the loop will run until the number of cleaned tiles exceeds
        # the number of tiles in the room times the minimum coverage specified.
        while trialRoom.getNumCleanedTiles() < (trialRoom.getNumTiles() * min_coverage):
            #anim.update(trialRoom, robots)            
            # Loop through the number of robots and move each one time step.            
            for robot in robots:
                robot.updatePositionAndClean()
            timeSteps += 1
            #print "Timestep: ", timeSteps
        totalTimeSteps.append(timeSteps)
        #anim.done()
    return numpy.mean(totalTimeSteps)
        
            
    
    #raise NotImplementedError


# === Problem 4
#
# 1) How long does it take to clean 80% of a 20×20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20×20, 25×16, 40×10, 50×8, 80×5, and 100×4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """ 
    numRobotsRange = range(1,11)
    times1 = []
    for i in numRobotsRange:
        times1.append(runSimulation(i, 1, 20, 20, 0.8, 30, StandardRobot))
    
    pylab.plot(numRobotsRange, times1)
    pylab.title('Mean Time to Clean 80% of a 20x20 Room, by Number of Robots')
    pylab.xlabel('Number of Robots')
    pylab.ylabel('Mean Time (time steps)')
    pylab.show()    
    #raise NotImplementedError

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    roomSizeRange = [(4,100),(20,20),(25,16),(40,10),(50,8),(80,5),(100,4)]
    roomSizeRatios = []    
    times2 = []
    for i in roomSizeRange:
        times2.append(runSimulation(2, 1, i[0], i[1], 0.8, 30, StandardRobot))
        roomSizeRatios.append(float(i[0])/i[1])
    
    pylab.plot(roomSizeRatios, times2)
    pylab.title('Mean Time for Two Robots to Clean 80% of a 400-Tile Room, by W:H Ratio')
    pylab.xlabel('Width:Height Ratio')
    pylab.ylabel('Mean Time (time steps)')
    pylab.show()    
    
    #raise NotImplementedError

# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    #raise NotImplementedError
    def updatePositionAndClean(self):
        tempPos = self.pos.getNewPosition(self.direction, self.speed)
        
        if self.room.isPositionInRoom(tempPos):
            self.setRobotPosition(tempPos)
            self.room.cleanTileAtPosition(self.pos)
            self.direction = int(random.random()*360)
        else:        
            self.direction = int(random.random()*360)



# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    #numRobotsRange = range(1,11)
    roomSizeRange = range(20, 100, 10)
    roomWidthRange = [x/2 for x in roomSizeRange]    
    standardTimes = []
    randomWalkTimes = []
    #for i in numRobotsRange:
    for i in roomWidthRange:
        standardTimes.append(runSimulation(1, 1, i, 2, 0.8, 40, StandardRobot))
        #standardTimes.append(runSimulation(i, 1, 20, 20, 0.8, 20, StandardRobot))
        randomWalkTimes.append(runSimulation(1, 1, i, 2, 0.8, 40, RandomWalkRobot))
        #randomWalkTimes.append(runSimulation(i, 1, 20, 20, 0.8, 20, RandomWalkRobot))
    
    
    pylab.plot(roomSizeRange, standardTimes)
    pylab.plot(roomSizeRange, randomWalkTimes)
    pylab.title("Mean Time for 1 Robot to Clean 80% of an 'X' x 2 Room, by Room Size (StandardRobot)")
    pylab.xlabel('Room Size')
    pylab.ylabel('Mean Time (time steps)')
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    
    pylab.show()
    #raise NotImplementedError

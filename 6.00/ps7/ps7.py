# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab

random.seed(5)

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """
        # TODO
        if random.random() <= self.clearProb:
            return True
        else: return False
        
    
    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        # TODO
        birthProb = self.maxBirthProb * (1 - popDensity)
        if random.random() <= birthProb:
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            NoChildException()


class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):

        """

        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """

        # TODO
        self.viruses = viruses
        self.maxPop = maxPop

    def getTotalPop(self):

        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """

        # TODO        
        return len(self.viruses)

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO
        survivingViruses = [virus for virus in self.viruses if not virus.doesClear()]
        self.viruses = survivingViruses
        popDensity = float(self.getTotalPop())/self.maxPop
        offspring = []        
        for virus in self.viruses:
            newVirus = virus.reproduce(popDensity)             
            if newVirus != None:
                offspring.append(newVirus)
        self.viruses += offspring
        return self.getTotalPop()



#
# PROBLEM 2
#
def simulationWithoutDrug():

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    patient = SimplePatient([SimpleVirus(0.1, 0.05)] * 100, 1000)
    virusPopulation = [patient.getTotalPop()]    
    for i in range(300):
        virusPopulation.append(patient.update())
    xvals = range(301)
    pylab.plot(xvals, virusPopulation)
    pylab.xlabel("Number of time steps")
    pylab.ylabel("Total virus population in the patient")
    pylab.title("Simple Virus Population with MaxBirthRate = 0.1, ClearRate = 0.05,\
    Initial Pop = 100, Max Pop = 1000")
    pylab.show()
    
    # TODO

def testYahtzee(numrolls):
    yahtzees = 0    
    for i in range(numrolls):
        roll = []
        for i in range(5): 
            roll.append(random.choice(range(1,7)))
        #print roll
        if roll[0] == roll[1] == roll[2] == roll[3] == roll[4]:
            yahtzees += 1
    return float(yahtzees)/numrolls
    
def plotYahtzee():
    yvals = []
    xvals = range(10000, 100000, 10000)    
    for i in xvals:
        yvals.append(testYahtzee(i))
    pylab.plot(xvals, yvals)
    pylab.xlabel("number of rolls")
    pylab.ylabel("Yahtzee probability")    
    pylab.show()
    
'''
Created on Oct 1, 2015

@author: XING
'''

class Environment(object):
    '''
    Environment is a class that contains information about the system being simulated.                
    '''
    DIAG_CLASS = "Environment."


    def __init__(self, startTime = 0, degradation = 0):
        '''
        Constructor
        Creates an instance of Environment                
        '''
        self.time = startTime
        self.degradation = degradation
        self.rotationPeriod = None
        
    def getTime(self):
        """
        Returns the value (in microseconds) of the simulated clock.                
        """
        return self.time
        
    def incrementTime(self, deltaT = None):
        """
        Advances the current time by a specified number of microseconds.                
        """
        diagMethod = "incrementTime:  "        
        if (deltaT == None):
            raise ValueError(Environment.DIAG_CLASS + diagMethod + "You must provide the amount of time to be added to the simulated clock")
        if not (isinstance(deltaT, (int, long))):
            #print deltaT
            raise ValueError(Environment.DIAG_CLASS + diagMethod + "The value you provided must be an integer")
        if (deltaT < 0):
            raise ValueError(Environment.DIAG_CLASS + diagMethod + "The value you provided must be greater than or equal to 0")
        self.time += deltaT
        return self.time
        
    def setRotationalPeriod(self, period = None):
        """
        Defines how much time (in microseconds) is required for the satellite to rotate once along it longitudinal axis.                 
        """
        diagMethod = "setRotationalPeriod:  "
        if (period == None):
            raise ValueError(Environment.DIAG_CLASS + diagMethod + "You must provide the amount of time to be added to the simulated clock")
        if not (isinstance(period, int)):
            raise ValueError(Environment.DIAG_CLASS + diagMethod + "The value you provided must be an integer")
        if (period < 1000000):
            raise ValueError(Environment.DIAG_CLASS + diagMethod + "The value you provided must be greater than or equal to 1,000,000")
        self.rotationPeriod = period
        return self.rotationPeriod
        
    def getRotationalPeriod(self):
        """
        Returns the amount of time required for the satellite to rotate once along its longitudinal axis.                
        """
        diagMethod = "getRotationalPeriod:  "
        if (self.rotationPeriod == None):
            raise ValueError(Environment.DIAG_CLASS + diagMethod + "The rotational period has not previously been set")
        return self.rotationPeriod
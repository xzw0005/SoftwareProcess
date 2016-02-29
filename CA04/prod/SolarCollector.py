'''
Created on Dec 2, 2015

@author: XING
'''
import math
import CA02.prod.Environment as Environment

class SolarCollector(object):
    '''
    classdocs
    '''
    DIAG_CLASS = "SolarCollector."
    FOV_LOW = 0.0
    FOV_HIGH = math.pi / 4
    SENSOR_OFFSET = math.pi / 2
    LATENCY = 40

    def __init__(self):
        '''
        Constructor: create an instance of the solar collector
        Returns: and instance of SolarCollector
        '''
        self.environment = None
        #self.degradation = 0
        #self.controller = None
        
        
    def getDegradation(self):
        if (self.environment != None):
            return self.environment.degradation
        return None

    def configure(self, environment = None):
        """
        Passes information about the simulation environment to the collector.
        Returns: True
        """
        diagMethod = "configure:  "
        if (environment == None):
            raise ValueError(SolarCollector.DIAG_CLASS + diagMethod + "missing environment parameter")
        if not (isinstance(environment, Environment.Environment)):
            raise ValueError(SolarCollector.DIAG_CLASS + diagMethod + "non-environment parameter")
        self.environment = environment
        return True
    
    def serviceRequest(self):
        """
        Returns the amount of solar energy being collected by the solar panels.
        """
        diagMethod = "serviceRequest:  "
        if (self.environment == None):
            raise ValueError(SolarCollector.DIAG_CLASS + diagMethod + "configure() has not yet been called")
        
        ORBITAL_PERIOD = (23 * 3600 + 56 * 60 + 4.1) * 1e6
        currentTime = self.environment.getTime()
        numberOfOrbits = currentTime * 1.0 / ORBITAL_PERIOD
        amountIntoCurrentOrbit = numberOfOrbits - int(numberOfOrbits)
        satelliteRightAscension = amountIntoCurrentOrbit * 360.0 #(2 * math.pi)        
        if (satelliteRightAscension <= 8.6  or satelliteRightAscension >= 351.4):
            ret = "0000"
        else:
            degradation = self.getDegradation()
            energy = int("7fff", 16) * (100 - degradation) / 100
            ret = '{0:04x}'.format(int(energy))
        self.environment.incrementTime(SolarCollector.LATENCY)
        return ret
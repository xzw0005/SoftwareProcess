'''
Created on Oct 1, 2015

@author: XING
'''

import math
import os
#import CA01.prod.StarCatalog as StarCatalog
import CA02.prod.Environment as Environment
#from django.db.models.aggregates import Count

class StarSensor(object):
    '''
    StarSensor represents a device mounted to the exterior of a satellite that detects star light within its field of view.  
    The sensor is positioned so that it is perpendicular to the satellite's rotational axis.  
    It uses the patterns of stars it detects to determine the satellite's position as well as to monitor the speed at which the satellite is spinning.                  
    '''
    DIAG_CLASS = "StarSensor."
    FOV_LOW = 0.0
    FOV_HIGH = math.pi / 4
    SENSOR_OFFSET = math.pi / 2
    LATENCY = 40

    def __init__(self, fov = None):
        '''
        Constructor
        Creates an instance of a star sensor that has a specific field of view of the sky.                
        
        '''
        diagMethod = "__init__:  "
        
        if (fov == None):
            raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "Missing fieldOfView parameter!");
        if not (isinstance(fov, int) or isinstance(fov, float)):
            raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "Non-numeric fieldOfView parameter!")
        if not (fov > 0  and fov <= math.pi / 4):
            raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "invalid fov. The fieldOfView parameter must be in range (0, pi/4]!")
        self.fov = fov
        #self.time = None
        #self.rotationPeriod = None
        self.environment = None
        self.catalog = {}
    
    
    def loadCatalog(self, starFile = None):
        diagMethod = "initializeSensor:  "
        if (starFile == None or type(starFile) != str):
            raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "The file name violates the parameter specifications.")
        if (os.path.isfile(starFile)):
            f = open(starFile, 'r')
        else:
            raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "No file exists by the specified file name.")
        
        for line in f:
            #lineList = line.split("\t")
            lineList = line.split()
            if (len(lineList) != 4):
                raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "A problem arises when parsing the file for star data.")
            try:
                lineList[0] = int(lineList[0])
            except ValueError:
                raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "Invalid star inventory number found: not an integer!")
            try:
                lineList[1] = float(lineList[1])
            except ValueError:
                raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "Invalid star magnitude found: not numeric!")
            try:
                lineList[2] = float(lineList[2])
            except ValueError:
                raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "Invalid star Right Ascention: not numeric!")
            if not ((lineList[2] >= 0) and (lineList[2] < math.pi * 2)):
                raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "Invalid star Right Ascention: must be in range [0, 2*pi)")
            try:
                lineList[3] = float(lineList[3])
            except ValueError:
                raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "Invalid star Declination: not numeric!")
            if ((lineList[3] < -math.pi/2) or (lineList[3] > math.pi/2)):
                raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "Invalid star Declination: must be in range [-pi/2, pi/2]")
                      
            if int(lineList[0]) in self.catalog.keys():
                raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "An attempt is made to add a duplicate star to the catalog.")
            self.catalog[lineList[0]] = [x for x in lineList[1:]]
        f.close()
        return len(self.catalog)   
    
        
    def initializeSensor(self, starFile = None):
        """
        Informs the star sensor about the location and magnitude of stars it should be capable of detecting.                
        """
        #starCatalog = StarCat.StarCatalog()
        #return starCatalog.loadCatalog(starFile)
        diagMethod = "initializeSensor:  "
        if (starFile == None):
            raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "missing filename parameter")
        try:
            #self.catalog = StarCatalog.StarCatalog()
            #numOfStars = self.catalog.loadCatalog(starFile)
            numOfStars = StarSensor.loadCatalog(self, starFile)
            return numOfStars
        except:
            raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "problem when loading catalog")
        
    
    def configure(self, environment = None):
        """
        Passes information (such as the simulated time, rotational speed of the satellite, etc.)  
        about the simulation environment to the star sensor.                
        """
        diagMethod = "configure:  "
        if (environment == None):
            raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "Missing Environment parameter!")
        if not (isinstance(environment, Environment.Environment)):
            raise ValueError(StarSensor.DIAG_CLASS + diagMethod + "Non-Environment parameter!")
        #self.time = env.getTime()
        #self.rotationPeriod = env.getRotationPeriod()
        self.environment = environment
        return True
    
    def hexString(self, mag):
        if (mag == None):
            return None

        intMag = int(mag * 10)
        #if (intMag >= 0):
        #    return '{:04x}'.format(intMag)
        #else:
        #    return hex(abs(mag) ^ ((1<<16)-1))[2:]
        if (intMag < 0):
            intMag = abs(intMag) ^ 0xFFFF
        convertedReading = '{0:04x}'.format(intMag)
        return convertedReading

    def getSensorPosition(self):
        """if (self.environment == None):     
            return [None, None]
        MICROSEC_PER_DAY = (23 * 3600 + 56 * 60 + 4.1) * 1e6
        raSatellite = math.pi * 2 * (self.environment.getTime() % MICROSEC_PER_DAY) / MICROSEC_PER_DAY
        decSensor = math.pi * 2 * (self.environment.getTime() % self.environment.getRotationPeriod()) / self.environment.getRotationPeriod()
        if (decSensor >= math.pi/2) and (decSensor <= math.pi * 3 / 2):
            raSensor = raSatellite - math.pi/2
        else:
            raSensor = raSatellite + math.pi/2
            
        if (raSensor < 0):
            raSensor += math.pi * 2
        if (raSensor > math.pi * 2):
            raSensor -= math.pi * 2
            
        return [raSensor, decSensor]"""
        
        # Calculate satellite Right Ascension by determining the amount into the current orbit
        ORBITAL_PERIOD = (23 * 3600 + 56 * 60 + 4.1) * 1e6
        currentTime = self.environment.getTime()
        numberOfOrbits = currentTime * 1.0 / ORBITAL_PERIOD
        amountIntoCurrentOrbit = numberOfOrbits - int(numberOfOrbits)
        satelliteRightAscension = amountIntoCurrentOrbit * (2 * math.pi)
        
        # Calculate sensor declination by determining how much the satellite has rotated
        rotationPeriod = self.environment.getRotationalPeriod()
        numberOfRotations = currentTime * 1.0 / rotationPeriod
        amountIntoCurrentRotation = numberOfRotations - int(numberOfRotations)
        radiansOfRotation = amountIntoCurrentRotation * (2 * math.pi)
        hemisphereOffset = StarSensor.SENSOR_OFFSET
        if (radiansOfRotation <= math.pi / 2):
            sensorDeclination = radiansOfRotation
        else:
            if (radiansOfRotation <= math.pi * 1.5):
                sensorDeclination = math.pi - radiansOfRotation
                hemisphereOffset = hemisphereOffset + math.pi
            else:
                sensorDeclination = radiansOfRotation - (2 * math.pi)
        sensorRightAscension = math.fmod((satelliteRightAscension + hemisphereOffset), 2 * math.pi)
        return [sensorRightAscension, sensorDeclination]

                
    def serviceRequest(self):
        """
        Returns the magnitude of the brightest star in the star sensor's field of view at the time the request is made.  
        The position of the satellite relative to the celestial sphere is determined by the simulated clock.                
        """
        
        """# If configure() has not been previously invoked, return None
        if (self.environment == None):     
            return None
        if (self.catalog == None):
            return None
        result = None
        sensorPosition = self.getSensorPosition()
        self.environment.incrementTime(StarSensor.LATENCY)
        try:
            mag = self.getMagnitude(rightAscentionCenterPoint = sensorPosition[0], 
                                       declinationCenterPoint= sensorPosition[1], 
                                       fieldOfView = self.fov)
            result = self.hexString(mag)
        except:
            result = None
        return result"""
        # If configure() has not been previously invoked, return None
        if (self.environment == None):     
            return None
        
        sensorPosition = self.getSensorPosition() 
        #print sensorPosition     
        mag = self.getMagnitude(rightAscentionCenterPoint = sensorPosition[0], 
                                       declinationCenterPoint= sensorPosition[1], 
                                       fieldOfView = self.fov)
        self.environment.incrementTime(StarSensor.LATENCY)
        return self.hexString(mag)    

 
    '''        
    def getMagnitude(self, rightAscentionCenterPoint=None, declinationCenterPoint=None, fieldOfView=None):
        """ Returns numeric value of the magnitude of the brightest star within the field of view; 
            returns "None" if no stars are in the field of view.
        """       
        if (rightAscentionCenterPoint==None) or (not isinstance(rightAscentionCenterPoint, (float, int, long))) or (rightAscentionCenterPoint < 0) or (rightAscentionCenterPoint >= math.pi * 2):
            raise ValueError("Invalid input: rightAscensiionCenterPoint violates its specification.")
        if (declinationCenterPoint==None) or (not isinstance(declinationCenterPoint, (float, int, long))) or (declinationCenterPoint < -math.pi/2) or (declinationCenterPoint > math.pi/2):
            raise ValueError("Invalid input: declinationCenterPoint violates its specification.")
        if (fieldOfView==None) or (not isinstance(fieldOfView, (float, int, long))) or (fieldOfView <= 0) or (fieldOfView > math.pi * 2):
            raise ValueError("Invalid input: fieldOfView violates its specification.")
        magnitudeInField = []
        for val in self.catalog.values():
            raFlag = False
            if (rightAscentionCenterPoint - fieldOfView / 2.0 < 0):
                if not ((val[1] < rightAscentionCenterPoint - fieldOfView / 2.0 + math.pi * 2) 
                            and (val[1] > rightAscentionCenterPoint + fieldOfView / 2.0)):
                    raFlag = True
                    
            elif (rightAscentionCenterPoint + fieldOfView / 2.0 > math.pi * 2):
                if not ((val[1] > rightAscentionCenterPoint + fieldOfView / 2.0 - math.pi * 2)
                            and (val[1] < rightAscentionCenterPoint - fieldOfView / 2.0)):
                    raFlag = True
                
            else:
                if ((val[1] >= rightAscentionCenterPoint - fieldOfView / 2.0)
                            and (val[1] <= rightAscentionCenterPoint + fieldOfView / 2.0)):
                    raFlag = True                
            southFlag = False
            northFlag = False        
            if (declinationCenterPoint - fieldOfView / 2.0 < -math.pi / 2):
                southFlag = True
            else:
                if (val[2] >= declinationCenterPoint - fieldOfView / 2.0):
                    southFlag = True
            if (declinationCenterPoint + fieldOfView / 2.0 > math.pi / 2):
                northFlag = True
            else:
                if (val[2] <= declinationCenterPoint + fieldOfView / 2.0):
                    northFlag = True
            
            if (raFlag and northFlag and southFlag):
                magnitudeInField.append(val[0])

        if (len(magnitudeInField) == 0):
            return None
        else:
            return min(magnitudeInField)
    '''
   
    def getMagnitude(self, rightAscentionCenterPoint = None, declinationCenterPoint = None, fieldOfView = None):
        """ Returns numeric value of the magnitude of the brightest star within the field of view; 
            returns "None" if no stars are in the field of view.
        """       
        if (rightAscentionCenterPoint==None) or (not isinstance(rightAscentionCenterPoint, (float, int, long))) or (rightAscentionCenterPoint < 0) or (rightAscentionCenterPoint >= math.pi * 2):
            raise ValueError("Invalid input: rightAscentionCenterPoint violates its specification.")
        if (declinationCenterPoint==None) or (not isinstance(declinationCenterPoint, (float, int, long))) or (declinationCenterPoint < -math.pi/2) or (declinationCenterPoint > math.pi/2):
            raise ValueError("Invalid input: declinationCenterPoint violates its specification.")
        if (fieldOfView==None) or (not isinstance(fieldOfView, (float, int, long))) or (fieldOfView <= 0) or (fieldOfView > math.pi * 2):
            raise ValueError("Invalid input: fieldOfView violates its specification.")
        magnitudeInField = []
        vals = self.catalog.values()
        for val in vals:        
        
            if (rightAscentionCenterPoint - fieldOfView / 2.0 < 0):
                if not ((val[1] == 0) or (rightAscentionCenterPoint + fieldOfView / 2.0 <= val[1] <= 2 * math.pi + rightAscentionCenterPoint - fieldOfView / 2.0)):
                    if (declinationCenterPoint - fieldOfView/2.0 <= val[2] <= declinationCenterPoint + fieldOfView / 2.0):
                        magnitudeInField.append(val[0])

            if (rightAscentionCenterPoint + fieldOfView / 2 > 2 * math.pi):
                if not ((val[1] == 0) or (rightAscentionCenterPoint + fieldOfView / 2.0 - math.pi * 2 <= val[1] <= rightAscentionCenterPoint - fieldOfView / 2.0)):
                    if (declinationCenterPoint - fieldOfView / 2.0 <= val[2] <= declinationCenterPoint + fieldOfView / 2.0):
                        magnitudeInField.append(val[0])
                    
            if (declinationCenterPoint + fieldOfView / 2.0 > math.pi / 2):
                if ((val[1] != 0) and (rightAscentionCenterPoint - fieldOfView/2.0 <= val[1] <=rightAscentionCenterPoint + fieldOfView/2.0)):
                    if (declinationCenterPoint - fieldOfView / 2.0 <= val[2] <= math.pi / 2.0):
                        magnitudeInField.append(val[0])
                if ( (val[1] != 0) and (2 * math.pi - (rightAscentionCenterPoint + fieldOfView / 2.0) <= val[1] <= 2 * math.pi-(rightAscentionCenterPoint - fieldOfView / 2.0) ) ):
                    if ( math.pi - (declinationCenterPoint+fieldOfView/2.0) <= val[2] <= math.pi / 2 ):
                        magnitudeInField.append(val[0])
            elif (declinationCenterPoint-fieldOfView/2.0 < -math.pi/2):
                if (rightAscentionCenterPoint-fieldOfView/2.0 <= val[1] <= rightAscentionCenterPoint+fieldOfView/2.0 ):
                    if (-math.pi/2<= val[2] <= declinationCenterPoint+fieldOfView/2.0):
                        magnitudeInField.append(val[0])

                if ( 2*math.pi-(rightAscentionCenterPoint+fieldOfView/2.0) <= val[1] <= 2*math.pi-(rightAscentionCenterPoint-fieldOfView/2.0) ):
                    if ( -math.pi/2<= val[2] <= -math.pi-(declinationCenterPoint-fieldOfView/2.0) ):
                        magnitudeInField.append(val[0])
            else:
                if ( rightAscentionCenterPoint-fieldOfView/2.0 <= val[1] <= rightAscentionCenterPoint+fieldOfView/2.0 ):
                    if (declinationCenterPoint-fieldOfView/2.0 <= val[2] <=declinationCenterPoint+fieldOfView/2.0 ):
                        magnitudeInField.append(val[0])
             
        if (len(magnitudeInField) == 0):
            return None
        else:
            return min(magnitudeInField)
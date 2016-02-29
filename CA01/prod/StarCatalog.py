'''
Created on Aug 30, 2015

@author: XING WANG (xzw0005@tigermail.auburn.edu)
'''
import os
import math

class StarCatalog(object):
    '''
    StarCatalog is an abstraction that represents an inventory of stars that are visible from earth. 
    Associated with each star is its catalog identifier, the magnitude of its brightness, its right ascension, and its declination.                
    '''
    DIAG_CLASS = "StarCatalog."
    
    def __init__(self):
        '''
        Constructor: Creates an instance of a StarCatalog.
        '''
        self.catalog = {}

    def loadCatalog(self, starFile = None):
        """
        Loads the star catalog from a text file containing star data.
        """
        diagMethod = "loadCatalog:  "
        if (starFile == None or type(starFile) != str):
            raise ValueError(StarCatalog.DIAG_CLASS + diagMethod + "The file name violates the parameter specifications.")
        if (os.path.isfile(starFile)):
            f = open(starFile, 'r')
        else:
            raise ValueError(StarCatalog.DIAG_CLASS + diagMethod + "No file exists by the specified file name.")
        
        for line in f:
            #lineList = line.split("\t")
            lineList = line.split()
            if (len(lineList) != 4):
                raise ValueError(StarCatalog.DIAG_CLASS + diagMethod + "A problem arises when parsing the file for star data.")
            """
            for element in lineList:
                try:
                    element = float(element)
                except ValueError:
                    raise ValueError("A problem arises when parsing the file for star data.")
            if ((lineList[2] < 0) or (lineList[2] >= math.pi * 2) 
                    or (lineList[3] < -math.pi/2) or (lineList[3] > math.pi/2)):
                raise ValueError("A problem arises when parsing the file for star data.")
            """
            try:
                lineList[0] = int(lineList[0])
            except ValueError:
                raise ValueError(StarCatalog.DIAG_CLASS + diagMethod + "Invalid star inventory number found: not an integer!")
            try:
                lineList[1] = float(lineList[1])
            except ValueError:
                raise ValueError(StarCatalog.DIAG_CLASS + diagMethod + "Invalid star magnitude found: not numeric!")
            try:
                lineList[2] = float(lineList[2])
            except ValueError:
                raise ValueError(StarCatalog.DIAG_CLASS + diagMethod + "Invalid star Right Ascention: not numeric!")
            if not ((lineList[2] >= 0) and (lineList[2] < math.pi * 2)):
                raise ValueError(StarCatalog.DIAG_CLASS + diagMethod + "Invalid star Right Ascention: must be in range [0, 2*pi)")
            try:
                lineList[3] = float(lineList[3])
            except ValueError:
                raise ValueError(StarCatalog.DIAG_CLASS + diagMethod + "Invalid star Declination: not numeric!")
            if ((lineList[3] < -math.pi/2) or (lineList[3] > math.pi/2)):
                raise ValueError(StarCatalog.DIAG_CLASS + diagMethod + "Invalid star Declination: must be in range [-pi/2, pi/2]")
                      
            if int(lineList[0]) in self.catalog.keys():
                raise ValueError(StarCatalog.DIAG_CLASS + diagMethod + "An attempt is made to add a duplicate star to the catalog.")
            self.catalog[lineList[0]] = [x for x in lineList[1:]]
        f.close()
        return len(self.catalog)
    
    def emptyCatalog(self):
        """ Deletes all stars from the catalog.
            An integer count of the number of stars deleted from the catalog.
        """
        count = len(self.catalog)
        self.catalog = {}
        return count

    def getStarCount(self, lowerMagnitude = None, upperMagnitude = None):
        """ Returns the number of stars in the star catalog that 
            have a magnitude within the range [lowerMagnitude, upperMagnitude].
        """
        diagMethod = "getStarCount:  "
        if (lowerMagnitude == None):
            lowerMagnitude = min(val[0] for val in self.catalog.values())
        if (upperMagnitude == None):
            upperMagnitude = max(val[0] for val in self.catalog.values())
        if (not isinstance(lowerMagnitude, (float, int, long))):
            raise ValueError(StarCatalog.DIAG_CLASS + diagMethod + "Invalid input: upperMagnitude violates its specfication.")
        if (not isinstance(upperMagnitude, (float, int, long))): #or (upperMagnitude < 0):
            raise ValueError(StarCatalog.DIAG_CLASS + diagMethod + "Invalid input: lowerMagnitude violates its specfication.")
        if (lowerMagnitude > upperMagnitude):
            raise ValueError(StarCatalog.DIAG_CLASS + diagMethod + "Invalid input: lowerMagnitude is greater than upperMagnitude!")
        count = 0
        for val in self.catalog.values():
            if (val[0] >= lowerMagnitude and val[0] <= upperMagnitude):
                count+=1
        return count
    
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
              
            decLo = declinationCenterPoint - fieldOfView / 2.0
            if (decLo < -math.pi / 2):
                southFlag = True
                if (decLo < -math.pi):
                    if (0 <= val[2] <= -decLo - math.pi):
                        northFlag = True
            else: 
                if (val[2] >= declinationCenterPoint - fieldOfView / 2.0):
                    southFlag = True
                    
            decHi = declinationCenterPoint + fieldOfView / 2.0
            if (decHi > math.pi / 2):
                northFlag = True
                if (decHi > math.pi):
                    if (decHi > math.pi):
                        southFlag = True
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
        diagMethod = "getMagnitude:  "
        if (rightAscentionCenterPoint==None) or (not isinstance(rightAscentionCenterPoint, (float, int, long))) or (rightAscentionCenterPoint < 0) or (rightAscentionCenterPoint >= math.pi * 2):
            raise ValueError(StarCatalog.DIAG_CLASS + diagMethod + "Invalid input: rightAscentionCenterPoint violates its specification.")
        if (declinationCenterPoint==None) or (not isinstance(declinationCenterPoint, (float, int, long))) or (declinationCenterPoint < -math.pi/2) or (declinationCenterPoint > math.pi/2):
            raise ValueError(StarCatalog.DIAG_CLASS + diagMethod + "Invalid input: declinationCenterPoint violates its specification.")
        if (fieldOfView==None) or (not isinstance(fieldOfView, (float, int, long))) or (fieldOfView <= 0) or (fieldOfView > math.pi * 2):
            raise ValueError(StarCatalog.DIAG_CLASS + diagMethod + "Invalid input: fieldOfView violates its specification.")
        magnitudeInField = []
        
        for val in self.catalog.values():        
        
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
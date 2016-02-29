import unittest
import gc
import os

try:
    import CA04.prod.Controller as Controller
    print("\nCA04 Controller being used --- minor exception\n")
    
except ImportError:
    import CA03.prod.Controller as Controller


class CA04Test(unittest.TestCase):

    def setUp(self):
        self.className = "Controller"
        self.testController = Controller.Controller()
        self.logFile = "logfile.txt"

    def tearDown(self):
        try:
            os.remove(self.logFile)
        except:
            pass
            
    
# Verify architectureFile
# SolarCollector
    def test_100_010_ShouldDetectSolarCollector(self):
        expectedResult = ["SolarCollector"]
        deviceList = self.testController.initialize("test_100_010_ShouldDetectSolarCollector.xml")
        deviceList.sort()
        self.assertListEqual(expectedResult, deviceList,
                             "Major:  initialize() fails on specifying solar collector")
        
    def test_100_020_ShouldWorkWithMultipleSolarCollectorsInFrame(self):
        expectedResult = ["Device", "SolarCollector", "StarSensor"]
        deviceList = self.testController.initialize("test_100_020_ShouldWorkWithMultipleSolarCollectorsInFrame.xml")
        deviceList.sort()
        self.assertListEqual(expectedResult, deviceList,
                             "Minor:  initialize() fails on multiple solar collectors in frame")
        
    def test_100_025_ShouldDetectMissingSolarCollectorDefinition(self):
        expectedString = self.className + ".initialize:"
        with self.assertRaises(ValueError) as context:
            self.testController.initialize("test_100_025_ShouldDetectMissingSolarCollectorDefinition.xml")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for missing solar collector definition")
        
# degradation
    def test_100_030_ShouldWorkWithMissingDegradation(self):
        expectedResult = ["SolarCollector"]
        deviceList = self.testController.initialize("test_100_030_ShouldWorkWithMissingDegradation.xml")
        deviceList.sort()        
        self.assertListEqual(expectedResult, deviceList,
                             "Minor:  initialize() fails when degradation is omitted")
        
    def test_100_040_ShouldDetectInvalidDegradation(self):
        expectedString = self.className + ".initialize:"
        with self.assertRaises(ValueError) as context:
            self.testController.initialize("test_100_040_ShouldDetectInvalidDegradation.xml")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for invalid degradation value")
 
    def test_100_050_ShouldDetectOutOfRangeDegradation(self):
        expectedString = self.className + ".initialize:"
        with self.assertRaises(ValueError) as context:
            self.testController.initialize("test_100_050_ShouldDetectOutOfRangeDegradation.xml")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for out-of-range degradation value")
        
# startTime
    def test_100_060_ShouldAllowMissingStartTime(self):
        expectedResult = ["SolarCollector"]
        deviceList = self.testController.initialize("test_100_060_ShouldAllowMissingStartTime.xml")
        deviceList.sort()        
        self.assertListEqual(expectedResult, deviceList,
                             "Minor:  initialize() fails when startTime is omitted")
               
    def test_100_070_ShouldDetectInvalidStartTime(self):
        expectedString = self.className + ".initialize:"
        with self.assertRaises(ValueError) as context:
            self.testController.initialize("test_100_070_ShouldDetectInvalidStartTime.xml")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for invalid startTime")            

# ------------------------------------
# Verify startTime Results

# should start at beginning of new frame
#        set frame rate to 1000
#        start at 1000 
#        complete 1 frame
    def test_200_005_ShouldStartAtNonZeroTime(self):
        expectedResults = [
                 [1000, "Controller", "SolarCollector", "serviceRequest"],
                 [1040, "SolarCollector", "Controller", "0000"],
             ] 
        self.testController.initialize("test_200_005_ShouldStartAtNonZeroTime.xml") 
        self.testController.run(40)
         
        del self.testController
        gc.collect()
        self.compare2Log(self.logFile, expectedResults)       
        
# should start in middle of new frame
#        set frame rate to 1000
#        start at 1020; produce simulation results for one frame
#        put 1 device in the frame 
#            controller requests service at time 0
#            device responds at time 40
#            controller requests service at time 1000
#            simulation starts here
#            device responds at time 40
#        complete the remainder of the frame

    def test_200_007_ShouldStartMidFrame(self):
        expectedResults = [
                 [1040, "SolarCollector", "Controller", "0000"],
             ] 
        self.testController.initialize("test_200_007_ShouldStartMidFrame.xml") 
        self.testController.run(500)
         
        del self.testController
        gc.collect()
        self.compare2Log(self.logFile, expectedResults)           


# ------------------------------------
# Verify SolarCollector Results 

# should not detect solar energy.   
#        frame consists of SolarCollector
#        start when the earth is blocking the sun  (startTime = 0)
#        simulate one frame
    def test_200_010_ShouldNotDetectSolarEnergy(self):
        expectedResults = [
                 [0, "Controller", "SolarCollector", "serviceRequest"],
                 [40, "SolarCollector", "Controller", "0000"],
             ] 
        self.testController.initialize("test_200_010_ShouldNotDetectSolarEnergy.xml") 
        self.testController.run(40)
         
        del self.testController
        gc.collect()
        self.compare2Log(self.logFile, expectedResults)
         
# should detect solar energy.  
#        frame consists of SolarCollector
#        start when the sun is fully exposed  (startTime = orbital period/2 floored to beginning of frame)
#        simulate one frame            
    def test_200_020_ShouldDetectSolarEnergy(self):
        expectedResults = [
                 [43082000000, "Controller", "SolarCollector", "serviceRequest"],
                 [43082000040, "SolarCollector", "Controller", "7fff"],
             ] 
        self.testController.initialize("test_200_020_ShouldDetectSolarEnergy.xml") 
        self.testController.run(40)
         
        del self.testController
        gc.collect()
        self.compare2Log(self.logFile, expectedResults)
        
# should not detect, then detect solar energy.   
#        frame consists of SolarCollector
#        set frame rate so that satellite orbits slightly less than 8.6 degrees every frame
#        start at time 0
#        simulate three frames 
#            first frame (RA is 0 degrees) shows sun is blocked by earth
#            second frame (RA is slightly less than 8.6 degrees) shows sun is blocked by earth
#            third frame (RA is > 8.6 degrees) shows sun exposure
    def test_200_030_ShouldDetectSolarEnergyMidOrbit(self):
        expectedResults = [
                 [0, "Controller", "SolarCollector", "serviceRequest"],
                 [40, "SolarCollector", "Controller", "0000"],
                 [2058360000, "Controller", "SolarCollector", "serviceRequest"],
                 [2058360040, "SolarCollector", "Controller", "0000"],
                 [4116720000, "Controller", "SolarCollector", "serviceRequest"],
                 [4116720040, "SolarCollector", "Controller", "7fff"],
             ] 
        self.testController.initialize("test_200_030_ShouldDetectSolarEnergyMidOrbit.xml") 
        self.testController.run(4116720040)
         
        del self.testController
        gc.collect()
        self.compare2Log(self.logFile, expectedResults)
        
# should detect degraded solar energy.   
#        frame consists of SolarCollector
#        degradation is 50%    (50% of 7fff is 3fff)
#        start when the sun is fully exposed  (startTime = orbital period/2 floored to beginning of frame)
#        simulate one frame       
    def test_200_040_ShouldDetectSolarEnergy(self):
        expectedResults = [
                 [43082000000, "Controller", "SolarCollector", "serviceRequest"],
                 [43082000040, "SolarCollector", "Controller", "3fff"],
             ] 
        self.testController.initialize("test_200_040_ShouldDetectDegradedSolarEnergy.xml") 
        self.testController.run(40)
         
        del self.testController
        gc.collect()
        self.compare2Log(self.logFile, expectedResults)
        
        
# should detect sun in star sensor   
#        frame consists of StarSensor and SolarCollector
#        start when star sensor is pointed to the sun
#            satellite is at 1/4 orbit + 1/2 rotation, floored to nearest frame boundary
#        simulate one frame     
    def test_200_050_ShouldDetectSunInStarSensor(self):
        expectedResults = [
                [21546025000, "Controller", "StarSensor", "serviceRequest"],
                [21546025040, "StarSensor", "Controller", "8000"],
             ] 
        self.testController.initialize("test_200_050_ShouldDetectSunInStarSensor.xml") 
        self.testController.run(40)
         
        del self.testController
        gc.collect()
        self.compare2Log(self.logFile, expectedResults)        
        
        
        
        
# ------------------------------------    
# utility methods
    def compare2Log(self, logFile, expectedResults):
        try:
            satLogFile = open(logFile, 'r')
        except:
            self.fail("Major:  no log records found")  
        loggedLines = satLogFile.readlines()
        entryCount = min(len(expectedResults), len(loggedLines))
        self.assertGreater(entryCount, 0, "Major:  no log records found")
        for entry in range(entryCount):
            entryFromLog = loggedLines[entry].split()
            entryFromLog[0] = int(entryFromLog[0])
            expectedEntry = expectedResults[entry]
            for itemNumber in range(len(entryFromLog)):
                if(expectedEntry[itemNumber] == None):
                    break
                else:
                    self.assertEqual(entryFromLog[itemNumber], expectedEntry[itemNumber],
                                     "Major:  log does not match expected results")           
        self.assertEquals(len(expectedResults), len(loggedLines), "Minor:  lines missing from log")
    


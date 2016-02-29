import CA03.prod.Monitor as Monitor
import CA02.prod.Environment as Environment
import unittest
import os
import tempfile
import re


class MonitorTest(unittest.TestCase):

    def setUp(self):
        self.className = "Monitor"
        self.testMonitor = Monitor.Monitor()
        self.temporaryFileName = self.generateTemporaryName()
        self.testEnvironment = Environment.Environment()
        self.testMonitor.configure(self.testEnvironment)

    def tearDown(self):
        self.testMonitor = None
        self.removeTemporaryFile(self.temporaryFileName)

# initialize
    def test_100_010_ShouldInitializeNewFile(self):
        self.assertTrue(self.testMonitor.initialize(self.temporaryFileName),
                        "Minor: initial returned incorrect value")
        
    def test_100_020_ShouldDetectExistingFile(self):
        self.testMonitor.initialize(self.temporaryFileName)
        self.assertFalse(self.testMonitor.initialize(self.temporaryFileName),
                        "Minor: initial returned incorrect value")
        
    def test_100_910_ShouldFailOnMissingFile(self):
        expectedString = self.className + ".initialize:"
        with self.assertRaises(ValueError) as context:
            self.testMonitor.initialize()
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for missing file name") 
        
    def test_100_920_ShouldFailOnInvalidFileName(self):
        expectedString = self.className + ".initialize:"
        with self.assertRaises(ValueError) as context:
            self.testMonitor.initialize('')
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for missing file name") 

# configure
    def test_200_010_ShouldConfigureWithEnvironment(self):
        myEnv = Environment.Environment()
        testMonitor = Monitor.Monitor()
        self.assertTrue(testMonitor.configure(myEnv),
                        "Minor: failure to return correct value on  configure() ")
         
    def test_200_910_ShouldFailIfEnvironmentMissing(self):
        expectedString = self.className + ".configure:  "
        with self.assertRaises(ValueError) as context:
            self.testMonitor.configure()
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for missing environment") 
 
    def test_200_910_ShouldFailIfEnvironmentIsBad(self):
        expectedString = self.className + ".configure:  "
        with self.assertRaises(ValueError) as context:
            self.testMonitor.configure(42)
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Minor:  failure to check for invalid environment") 
 
# serviceRequest
    def test_300_010_ShouldReturnTime(self):
        latency = 10
        self.testMonitor.initialize(self.temporaryFileName)
        for localTime in range(0, 100, latency):
            monitorTime = self.testMonitor.serviceRequest("source", "target")
            self.assertEquals(localTime, monitorTime,
                              "Minor:  incorrect time returned")
            self.testEnvironment.incrementTime(latency)

    def test_300_020_ShouldLogInformation(self):
        latency = 40
        entryToLog = [
                     [0, "source", "target1", "event1"],
                     [0, "target1", "source", "event2"],
                     [0, "source", "target2", "event3"],
                     [0, "target2", "source", "event4"]
                     ] 
        entryTime = 0
        for entry in entryToLog:
            entry[0] = entryTime
            entryTime += latency
                                
        self.testMonitor.initialize(self.temporaryFileName)
        for item in entryToLog:
            self.testMonitor.serviceRequest(item[1], item[2], item[3])
            self.testEnvironment.incrementTime(latency)
   
        with open(self.temporaryFileName, 'r') as temporaryLogFile:
            loggedLines = temporaryLogFile.readlines()
            entryCount = min(len(entryToLog), len(loggedLines))
            self.assertGreater(entryCount, 0,
                               "Major:  no log records found")
            for entry in range(entryCount):
                entryFromLog = loggedLines[entry].split()
                entryFromLog[0] = int(entryFromLog[0])
                self.assertListEqual(entryFromLog, entryToLog[entry],
                                     "Major: log not working")
                
            self.assertEquals(len(entryToLog), len(loggedLines),
                              "Minor:  lines missing from log")
                
    def test_300_910_ShouldRejectMissingSource(self):
        expectedString = self.className + ".serviceRequest:"
        self.testMonitor.initialize(self.temporaryFileName)
        with self.assertRaises(ValueError) as context:
            monitorTime = self.testMonitor.serviceRequest(target="target", event="event")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Minor:  failure to check for missing source") 

    def test_300_910_ShouldRejectMissingTarget(self):
        expectedString = self.className + ".serviceRequest:"
        self.testMonitor.initialize(self.temporaryFileName)
        with self.assertRaises(ValueError) as context:
            monitorTime = self.testMonitor.serviceRequest(source="source", event="event")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Minor:  failure to check for missing target")     
        
# utility methods
    def generateTemporaryName(self):
        foundFileName = False
        while not (foundFileName):
            temporaryFileName = next(tempfile._get_candidate_names()) + ".txt"
            if not (os.path.isfile(temporaryFileName)):
                foundFileName = True
        return temporaryFileName
    
    def removeTemporaryFile(self, fileName):
        try:
            if(os.path.isfile(fileName)):
                os.remove(fileName)
        except:
            pass
        

        

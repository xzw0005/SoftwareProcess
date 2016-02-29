import CA02.prod.Environment as Environment
import CA03.prod.Monitor as Monitor
import unittest

import os

class MonitorTest(unittest.TestCase):
    def setUp(self):
        self.myMonitor = Monitor.Monitor()

# 100 constructor
    def test_100_010_ShouldConstruct(self):
        self.assertIsInstance(self.myMonitor, Monitor.Monitor)
        
    def test_200_010_ShouldInitialize(self):
        logFile = "shabi.txt"
        self.assertIsInstance(self.myMonitor.initialize(logFile), bool)
        
    def test_200_020_shouldHasWrittenFile(self):
        written = os.path.isfile("shabi.txt")
        self.assertEquals(written, True) 

    def test_200_910_shouldRejectMissingParm(self):
        expectedString = "Monitor.initialize:  "
        with self.assertRaises(ValueError) as context:
            self.myMonitor.initialize()                                
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
        
    def test_200_920_shouldRejectNonTxtType(self):
        expectedString = "Monitor.configure:  "
        with self.assertRaises(ValueError) as context:
            self.myMonitor.configure("ca.xml")                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
    def test_200_930_shouldRejectNegativeValues(self):
        expectedString = "Environment.incrementTime:"
        simEnv = Environment.Environment()
        self.myMonitor.configure(simEnv)
        with self.assertRaises(ValueError) as context:
            self.myMonitor.environment.incrementTime(-1)                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 

    def test_300_010_ShouldConfigure(self):
        simEnv = Environment.Environment()
        self.myMonitor.configure(simEnv)
        self.assertIsInstance(self.myMonitor.environment, Environment.Environment)    
        
    def test_300_910_shouldRejectMissingParm(self):
        expectedString = "Monitor.configure:  "
        with self.assertRaises(ValueError) as context:
            self.myMonitor.configure()                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
    def test_300_920_shouldRejectNonEnvironmentType(self):
        expectedString = "Monitor.configure:  "
        with self.assertRaises(ValueError) as context:
            self.myMonitor.configure(123)                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
    def test_300_930_shouldRejectNegativeValues(self):
        expectedString = "Environment.incrementTime:"
        simEnv = Environment.Environment()
        self.myMonitor.configure(simEnv)
        with self.assertRaises(ValueError) as context:
            self.myMonitor.environment.incrementTime(-1)                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 


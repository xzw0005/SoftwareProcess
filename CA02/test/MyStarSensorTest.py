'''
Created on Oct 2, 2015

@author: XING
'''

import unittest
import CA02.prod.StarSensor as Sensor
import math
import os
import CA02.prod.Environment as Env
from CA02.prod.StarSensor import StarSensor


class MySensorTest(unittest.TestCase):

#-----------------------
# 10 StarSensor()
# happy path tests
    def test10_010_ShouldInstantiateStarSensor(self):
        self.assertIsInstance(Sensor.StarSensor(0.1), Sensor.StarSensor)

# sad path tests
    def test10_920_ShouldRequireStringParm(self):        
        expectedString = "StarSensor.__init__: None fov"
        try:
            self.assertRaises(ValueError, Sensor.StarSensor)
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")
             
    def test20_930_ShouldRequireNumeric(self):
        expectedString = "StarSensor.__init__: invalid fov"
        try:
            self.assertRaises(ValueError, Sensor.StarSensor, "string")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")
             
    def test20_940_ShouldRequirePositive(self):
        expectedString = "StarSensor.__init__: invalid fov"
        try:
            self.assertRaises(ValueError, Sensor.StarSensor, 0)
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")
             
    def test20_950_ShouldNoMoreThan(self):
        expectedString = "StarSensor.__init__: invalid fov"
        try:
            self.assertRaises(ValueError, Sensor.StarSensor, math.pi/2)
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")
#-----------------------
# 20 initializeSensor(starFile)
# happy path tests
    def test20_010_ShouldInitializeSensor(self):
        starSensor = Sensor.StarSensor(0.1)
        self.assertEquals(starSensor.initializeSensor("Chart_TwoValidStars.txt"), 2)
        
    def test20_020_ShouldLoadFile(self):
        starSensor = Sensor.StarSensor(0.1)
        self.assertEquals(starSensor.initializeSensor("SaoChart.txt"), 9040)

    def test20_910_ShouldRequireParm(self):
        starSensor = Sensor.StarSensor(0.1)
        expectedString = "StarSensor.initializeSensor:"
        try:
            self.assertRaises(ValueError, starSensor.initializeSensor)
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")
             
# sad path tests
    def test20_920_ShouldRequireStringParm(self):
        starSensor = Sensor.StarSensor(0.1)
        expectedString = "StarSensor.initializeSensor:"
        try:
            self.assertRaises(ValueError, starSensor.initializeSensor, 42)
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")
             
    def test20_930_ShouldRequireFoundFile(self):
        starSensor = Sensor.StarSensor(0.1)
        expectedString = "StarSensor.initializeSensor:"
        try:
            self.assertRaises(ValueError, starSensor.initializeSensor, "missingfile")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")
             
    def test20_940_ShouldRejectInvalidStarData(self):
        starSensor = Sensor.StarSensor(0.1)
        expectedString = "StarSensor.initializeSensor:"
        try:
            self.assertRaises(ValueError, starSensor.initializeSensor, "Chart_InvalidStarData.txt")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString,
            diagnosticString[0:len(expectedString)])
        except:
            self.fail("incorrect exception was raised")

    def test20_950_ShouldRejectDuplicateStarDataInDifferentFiles(self):
        starSensor = Sensor.StarSensor(0.1)
        expectedString = "StarSensor.initializeSensor:" 
        try:
            starSensor.initializeSensor("Chart_TwoValidStars.txt")
            self.assertRaises(ValueError, starSensor.initializeSensor, "Chart_TwoValidStars.txt")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
            self.fail("incorrect exception was raised")  
            
    def test20_960_ShouldRejectDuplicateStarDataInSameFile(self):
        starSensor = Sensor.StarSensor(0.1)
        expectedString = "StarSensor.initializeSensor:" 
        try:
            self.assertRaises(ValueError, starSensor.initializeSensor, "Chart_DupStarData.txt")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString,
            diagnosticString[0:len(expectedString)])
        except:
            self.fail("incorrect exception was raised")
            
#-----------------------
# 30 configure(env):
# happy path tests
    def test30_010_ShouldConfigureEnvironment(self):
        env = Env.Environment()
        env.incrementTime(100)
        env.setRotationPeriod(1000000)
        
        starSensor = Sensor.StarSensor(0.1)
        self.assertEquals(starSensor.configure(env), True)
        

    def test30_910_ShouldRequireParm(self):
        starSensor = Sensor.StarSensor(0.1)
        expectedString = "StarSensor.configure: You must provide an instance of Environment as parameter!"
        try:
            self.assertRaises(ValueError, starSensor.configure)
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")   
                      
#-----------------------
# 35 hexString(mag):
# happy path tests
    def test35_010_ShouldReturnNone(self):
        starSensor = Sensor.StarSensor(0.1)
        mag = None
        self.assertEquals(starSensor.hexString(mag), None)
        
    def test35_020_ShouldReturnHexZero(self):
        starSensor = Sensor.StarSensor(0.1)
        mag = 0
        self.assertEquals(starSensor.hexString(mag), "0000")   
             
    def test35_030_ShouldReturnHexOne(self):
        starSensor = Sensor.StarSensor(0.1)
        mag = 1
        self.assertEquals(starSensor.hexString(mag), "000a")
        
    def test35_040_ShouldReturnHexDecimal(self):
        starSensor = Sensor.StarSensor(0.1)
        mag = 6.55
        self.assertEquals(starSensor.hexString(mag), "0041")
        
    def test35_050_ShouldReturnHexTwenty(self):
        starSensor = Sensor.StarSensor(0.1)
        mag = 20
        self.assertEquals(starSensor.hexString(mag), "00c8")
            
    def test35_060_ShouldReturnHexNegative(self):
        starSensor = Sensor.StarSensor(0.1)
        mag = -20
        self.assertEquals(starSensor.hexString(mag), "ff37")
        
        
        
    def test40_010_ShouldReturnList(self):
        simEnv = Env.Environment()
        #simEnv.incrementTime(100)
        rotationalPeriod = 1000000 * 60 / 6
        simEnv.setRotationPeriod(rotationalPeriod)
        
        fov = (2.0 / 360.0) * (2.0 * math.pi)
        starSensor = Sensor.StarSensor(fov)
        #starSensor.initializeSensor("SaoChart.txt")
        starSensor.configure(simEnv)
        
        starSightings = []
        increment = 10 * 1000000
        for t in range(0, 5 * 60 * 1000000, increment):            
            timeOfNextIncrement = simEnv.getTime() + increment
            starSightings.append(starSensor.serviceRequest())
            print starSensor.getSensorPosition()
            
            simEnv.incrementTime(timeOfNextIncrement - simEnv.getTime())
        print len(starSightings)   
        self.assertEquals(len(starSightings), len(range(0, 5 * 60 * 1000000, increment))) 
       
    def test40_020_ShouldReturnList(self):
        simEnv = Env.Environment()
        #simEnv.incrementTime(100)
        rotationalPeriod = 1000000 * 60 / 6
        simEnv.setRotationPeriod(rotationalPeriod)
        
        fov = (2.0 / 360.0) * (2.0 * math.pi)
        starSensor = Sensor.StarSensor(fov)
        starSensor.initializeSensor("SaoChart.txt")
        starSensor.configure(simEnv)
        
        starSightings = []
        increment = 10 * 1000000
        for t in range(0, 5 * 60 * 1000000, increment):            
            timeOfNextIncrement = simEnv.getTime() + increment
            starSightings.append(starSensor.serviceRequest())
            
            simEnv.incrementTime(timeOfNextIncrement - simEnv.getTime())
        print len(starSightings)   
        self.assertEquals(len(starSightings), len(range(0, 5 * 60 * 1000000, increment))) 
                             
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
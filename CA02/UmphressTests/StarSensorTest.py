import CA02.prod.StarSensor as StarSensor
import CA02.prod.Environment as Environment
import math
import unittest

class StarSensorTest(unittest.TestCase):

    def setUp(self):
        self.className = "StarSensor"
        self.myEnv = Environment.Environment()
        self.myEnv.setRotationalPeriod(int(60 / 6 * 1000000))
        self.myStarSensor = StarSensor.StarSensor((10.0 / 360.0) * 2.0 * math.pi)
        self.myStarSensor.configure(self.myEnv)
        self.starCatalog1 = {'file': 'SaoChart.txt', 'count': 9040}
        self.starCatalog2 = {'file': 'CA02StarTestChart.txt', 'count': 9040}
        self.time2Orbit = int(((23 * 60 * 60) + (56 * 60) + (4.1)) * 1000000)
        
    def tearDown(self):
        pass


# 100 constructor
    def test_100_910_ShouldFailOnConstructWithoutParm(self):
        expectedString = self.className + ".__init__:  "
        with self.assertRaises(ValueError) as context:
            StarSensor.StarSensor()                             
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
    def test_100_920_ShouldFailOnConstructNonIntFov(self):
        expectedString = self.className + ".__init__:  "
        with self.assertRaises(ValueError) as context:
            StarSensor.StarSensor('a')                             
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
    def test_100_930_ShouldFailOnConstructBelowThresholdFov(self):
        expectedString = self.className + ".__init__:  "
        with self.assertRaises(ValueError) as context:
            StarSensor.StarSensor(0)                             
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
    def test_100_940_ShouldFailOnConstructBelowThresholdFov(self):
        expectedString = self.className + ".__init__:  "
        with self.assertRaises(ValueError) as context:
            StarSensor.StarSensor((math.pi / 4.0) + 0.01)                            
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
# 200 initializeSensor
    def test_200_010_ShouldLoadStarCatalog(self):
        self.assertEquals(self.myStarSensor.initializeSensor(self.starCatalog1['file']), self.starCatalog1['count'])
        
    def test_200_910_ShouldFailOnMissingParm(self):
        expectedString = self.className + ".initializeSensor:  "
        with self.assertRaises(ValueError) as context:
            self.myStarSensor.initializeSensor()                          
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
    def test_200_920_ShouldFailOnBadFileName(self):
        expectedString = self.className + ".initializeSensor:  "
        with self.assertRaises(ValueError) as context:
            self.myStarSensor.initializeSensor("nofile")                          
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
        
# 300 configure
    def test_300_010_ShouldConnectSensorWithEnvirojnment(self):
        self.assertTrue(self.myStarSensor.configure(self.myEnv))
        
    def test_300_910_ShouldFailOnMissingParm(self):
        expectedString = self.className + ".configure:  "
        with self.assertRaises(ValueError) as context:
            self.myStarSensor.configure()
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
    def test_300_920_ShouldFailOnNonEnvironmentParm(self):
        expectedString = self.className + ".configure:  "
        with self.assertRaises(ValueError) as context:
            self.myStarSensor.configure(42)
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
# 400 getSensorPosition
    def test_400_010_ShouldGetPositionAtTimeZero(self):
        self.assertListEqual(self.myStarSensor.getSensorPosition(), [math.pi / 2.0, 0.0])
    
        
    def test_400_020_ShouldGetPositionAtNominalOrbit(self):
        self.myEnv.incrementTime(42)
        sensorPosition = [1.57079633, 0.0000263893782901543000000000]
        position = self.myStarSensor.getSensorPosition()
        for item in range(1):
            self.assertAlmostEqual(position[item], sensorPosition[item], 5)
            
    def test_400_030_ShouldGetPositionAtRotationBetween90And180(self):
        amountOfRotation = int(self.myEnv.getRotationalPeriod() / 4.0) + 1
        self.myEnv.incrementTime(amountOfRotation)
        sensorPosition = [4.71257128333396, 1.57079569847637]
        position = self.myStarSensor.getSensorPosition()
        for item in range(1):
            self.assertAlmostEqual(position[item], sensorPosition[item], 5)
            
    def test_400_040_ShouldGetPositionAtRotationBetween180And270(self):
        amountOfRotation = int(self.myEnv.getRotationalPeriod() / 2.0) + 1
        self.myEnv.incrementTime(amountOfRotation)
        sensorPosition = [4.71275358621031, -0.0000006283185306197640000000]
        position = self.myStarSensor.getSensorPosition()
        for item in range(1):
            self.assertAlmostEqual(position[item], sensorPosition[item], 5)
            
    def test_400_050_ShouldGetPositionAtRotationBetween270And360(self):
        amountOfRotation = int(self.myEnv.getRotationalPeriod() * 3.0 / 4.0) + 1
        self.myEnv.incrementTime(amountOfRotation)
        sensorPosition = [1.57134323549686, -1.57079569847637]
        position = self.myStarSensor.getSensorPosition()
        for item in range(1):
            self.assertAlmostEqual(position[item], sensorPosition[item], 5)
            
    def test_400_060_ShouldGetPositionAtMultipleOrbits(self):
        self.myEnv.incrementTime(self.time2Orbit + 42)
        sensorPosition = [4.71238898344738, 0.565460288267873]
        position = self.myStarSensor.getSensorPosition()
        for item in range(1):
            self.assertAlmostEqual(position[item], sensorPosition[item], 5)
            
    def test_400_070_ShouldGetPositionAtMultipleRotations(self):
        amountOfRotation = self.myEnv.getRotationalPeriod() + 1
        self.myEnv.incrementTime(amountOfRotation)
        sensorPosition = [1.57152553837321, 6.28318530717959E-07]
        position = self.myStarSensor.getSensorPosition()
        for item in range(1):
            self.assertAlmostEqual(position[item], sensorPosition[item], 5)
            
# 500 serviceRequest
    def test_500_010_ShouldGetPostiveValue(self):
        self.myStarSensor.initializeSensor(self.starCatalog2['file'])
        rotate15Degrees = int(self.myEnv.getRotationalPeriod() * 15.0 / 360.0)
        self.myEnv.incrementTime(rotate15Degrees)
        self.assertEquals("003e", self.myStarSensor.serviceRequest())
        
    def test_500_020_ShouldGetNegativeValue(self):
        self.myStarSensor.initializeSensor(self.starCatalog2['file'])
        rotate30Degrees = int(self.myEnv.getRotationalPeriod() * 30.0 / 360.0)
        self.myEnv.incrementTime(rotate30Degrees)
        self.assertEquals("fff4", self.myStarSensor.serviceRequest())
        
    def test_500_030_ShouldGetValueWhenStraddlingRightAscensionBoundary(self):
        self.myStarSensor.initializeSensor(self.starCatalog2['file'])
        moveSensorToSmallRightAscension = int(self.time2Orbit * 3.0 / 4.0)
        rotateSensorToNegativeDeclination = int(self.myEnv.getRotationalPeriod() / 2.0)
        time = moveSensorToSmallRightAscension + rotateSensorToNegativeDeclination
        self.myEnv.incrementTime(time)     
        self.assertEquals("002a", self.myStarSensor.serviceRequest())
        
    def test_500_040_ShouldIncrementTime(self):
        serviceRequestLatency = 40
        self.myStarSensor.initializeSensor(self.starCatalog2['file'])
        timeBeforeServiceRequest = self.myEnv.getTime()
        self.myStarSensor.serviceRequest()
        timeAfterServiceRequest = self.myEnv.getTime()
        self.assertEquals(serviceRequestLatency, timeAfterServiceRequest - timeBeforeServiceRequest)
        
    def test_500_050_ShouldReturnNoneIfNotConfigured(self):
        myStarSensor = StarSensor.StarSensor((10.0 / 360.0) * 2.0 * math.pi)
        self.assertEquals(None, myStarSensor.serviceRequest())
        
   
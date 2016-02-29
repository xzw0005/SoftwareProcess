import CA02.prod.Environment as Environment
import CA03.prod.Device as Device
import unittest

class DeviceTest(unittest.TestCase):
    def setUp(self):
        self.myDevice = Device.Device()

# 100 constructor
    def test_100_010_ShouldConstruct(self):
        self.assertIsInstance(self.myDevice, Device.Device)
        
    def test_200_010_ShouldConfigure(self):
        simEnv = Environment.Environment()
        self.myDevice.configure(simEnv)
        self.assertIsInstance(self.myDevice.environment, Environment.Environment)    
        
    def test_200_910_shouldRejectMissingParm(self):
        expectedString = "Device.configure:  "
        with self.assertRaises(ValueError) as context:
            self.myDevice.configure()                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
    def test_200_920_shouldRejectNonEnvironmentType(self):
        expectedString = "Device.configure:  "
        with self.assertRaises(ValueError) as context:
            self.myDevice.configure(123)                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
    def test_200_930_shouldRejectNegativeValues(self):
        expectedString = "Environment.incrementTime:"
        simEnv = Environment.Environment()
        self.myDevice.configure(simEnv)
        with self.assertRaises(ValueError) as context:
            self.myDevice.environment.incrementTime(-1)                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
          
# 400 setRotationalPeriod
    def test_300_010_ShouldIncrementTime(self):
        simEnv = Environment.Environment()
        self.myDevice.configure(simEnv)
        self.myDevice.serviceRequest()
        self.assertEqual(self.myDevice.environment.getTime(), 40)  
        
    def test_300_020_ShouldReturnString(self):
        simEnv = Environment.Environment()
        self.myDevice.configure(simEnv)
        self.assertIsInstance(self.myDevice.serviceRequest(), str)        
        
    def test_300_030_ShouldReturnHexString(self):
        simEnv = Environment.Environment()
        self.myDevice.configure(simEnv)
        ret = self.myDevice.serviceRequest()
        num = int(ret, 16)
        hexString = '{0:04x}'.format(num)       
        self.assertEquals(ret, hexString)
        
    def test_300_910_shouldRejectNoneEnvironment(self):
        expectedString = "Device.serviceRequest:  "
        with self.assertRaises(ValueError) as context:
            self.myDevice.serviceRequest()                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
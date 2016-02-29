import CA02.prod.Environment as Environment
import unittest

class EnvironmentTest(unittest.TestCase):
    def setUp(self):
        self.myEnv = Environment.Environment()

# 100 constructor
    def test_100_010_ShouldConstruct(self):
        self.assertIsInstance(self.myEnv, Environment.Environment)
        
# 200 getTime
    def test_200_010_ShouldGetTimeOfZeroAfterConstruct(self):
        self.assertEquals(self.myEnv.getTime(), 0)
        
# 300 incrementTime
    def test_300_010_ShouldIncrementTime(self):
        #self.assertEquals(self.myEnv.incrementTime(500), 500)
        self.myEnv.incrementTime(500)
        self.assertEquals(self.myEnv.getTime(), 500)
        
    def test_300_910_shouldRejectNonInt(self):
        expectedString = "Environment.incrementTime:"
        with self.assertRaises(ValueError) as context:
            self.myEnv.incrementTime(-1)                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 

    def test_300_920_shouldRejectNegativeValues(self):
        expectedString = "Environment.incrementTime:"
        with self.assertRaises(ValueError) as context:
            self.myEnv.incrementTime(-1)                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 

    def test_300_930_shouldRejectMissingParm(self):
        expectedString = "Environment.incrementTime:"
        with self.assertRaises(ValueError) as context:
            self.myEnv.incrementTime()                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
          
# 400 setRotationalPeriod
    def test_400_010_ShouldSetPeriod(self):
        self.assertEquals(self.myEnv.setRotationalPeriod(1000000), 1000000)
        
    def test_400_910_ShouldRejectMissingParm(self):
        expectedString = "Environment.setRotationalPeriod:"
        with self.assertRaises(ValueError) as context:
            self.myEnv.setRotationalPeriod()                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 

    def test_400_920_ShouldRejectNonInt(self):
        expectedString = "Environment.setRotationalPeriod:"
        with self.assertRaises(ValueError) as context:
            self.myEnv.setRotationalPeriod(1.5)                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
        
    def test_400_930_ShouldRejectLowInt(self):
        expectedString = "Environment.setRotationalPeriod:"
        with self.assertRaises(ValueError) as context:
            self.myEnv.setRotationalPeriod(999999)                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
# 500 getRotationalPeriod
    def test_500_010_ShouldGetPeriod(self):
        self.assertEquals(self.myEnv.setRotationalPeriod(1000000), self.myEnv.getRotationalPeriod())
        
    def test_500_910_ShouldRaiseExceptionIfPeriodNotSet(self):
        expectedString = "Environment.getRotationalPeriod:"
        with self.assertRaises(ValueError) as context:
            self.myEnv.getRotationalPeriod()                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
'''
Created on Oct 2, 2015

@author: XING
'''
import unittest
import CA02.prod.Environment as Env
import math
import os

class MyEnvironmentTest(unittest.TestCase):

#-----------------------
# 10 StarCatalog()
    def test10_010_ShouldInstantiateEnvironment(self):
        self.assertIsInstance(Env.Environment(), Env.Environment)

#-----------------------
# 20 getTime()
# happy path tests
    def test20_010_ShouldGetInitTime(self):
        env = Env.Environment()
        self.assertEquals(env.getTime(), 0)

#-----------------------
# 30 incrementTime(deltaT):
# happy path tests
    def test30_010_ShouldIncrementTime(self):
        env = Env.Environment()
        env.incrementTime(100)
        self.assertEquals(env.getTime(), 100)

    def test30_910_ShouldRequireParm(self):
        env = Env.Environment()
        expectedString = "Environment.incrementTime:"
        try:
            self.assertRaises(ValueError, env.incrementTime)
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")
# sad path tests
    def test30_920_ShouldRequireIntegerParm(self):
        env = Env.Environment()
        expectedString = "Environment.incrementTime:"
        try:
            self.assertRaises(ValueError, env.incrementTime, 66.6)
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")
    def test30_930_ShouldNotBeNegativeParm(self):
        env = Env.Environment()
        expectedString = "Environment.incrementTime:"
        try:
            self.assertRaises(ValueError, env.incrementTime(-1))
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")     
       
#-----------------------
# 40 setRotationPeriod(period):    
# happy path tests
    def test40_010_ShouldSetRotationPeriod(self):
        env = Env.Environment()
        env.setRotationPeriod(1000000)
        self.assertEquals(env.getRotationPeriod(), 1e6)
        
    def test40_910_ShouldRequireParm(self):
        env = Env.Environment()
        expectedString = "Environment.setRotationPeriod:"
        try:
            self.assertRaises(ValueError, env.setRotationPeriod)
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")
# sad path tests
    def test40_920_ShouldRequireIntegerParm(self):
        env = Env.Environment()
        expectedString = "Environment.setRotationPeriod:"
        try:
            self.assertRaises(ValueError, env.setRotationPeriod, 1e7)
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")
             
    def test40_930_ShouldRequireLargeParm(self):
        env = Env.Environment()
        expectedString = "Environment.setRotationPeriod:"
        try:
            self.assertRaises(ValueError, env.setRotationPeriod, 1000)
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")             
         
#-----------------------
# 50 getRotationPeriod(period):    
# happy path tests
    def test50_010_ShouldGetInitialRotationPeriod(self):
        env = Env.Environment()
        expectedString = "Environment.getRotationPeriod: The rotational period has not previously been set"
        try:
            self.assertRaises(ValueError, env.getRotationPeriod())
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")
             
    def test50_020_ShouldGetRotationPeriod(self):
        env = Env.Environment()
        env.setRotationPeriod(1000000)
        self.assertEquals(env.getRotationPeriod(), 1e6)       

             
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
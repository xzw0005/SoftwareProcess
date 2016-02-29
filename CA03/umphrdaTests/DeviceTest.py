import unittest
import random
import CA03.prod.Device as Device
import CA02.prod.Environment as Environment


class DeviceTest(unittest.TestCase):
    
    def setUp(self):
        self.testDevice = Device.Device()
        self.environment = Environment.Environment()
        self.testDevice.configure(self.environment)
        self.className = "Device"
        self.sampleSize = 1000000
        self.xffff = int("ffff", 16)
        self.x7fff = int("7fff", 16)

# constructor
    def test_100_010_ShouldConstructWithNoParm(self):
        self.assertIsInstance(Device.Device(), Device.Device,
                              "Major:  construction failure")
         
# configure
    def test_200_010_ShouldConfigureWithEnvironment(self):
        myEnv = Environment.Environment()
        self.assertTrue(self.testDevice.configure(myEnv),
                        "Major:  configure() failure")
         
    def test_200_910_ShouldFailIfEnvironmentMissing(self):
        expectedString = self.className + ".configure:  "
        with self.assertRaises(ValueError) as context:
            self.testDevice.configure()
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for missing environment") 
 
    def test_200_910_ShouldFailIfEnvironmentIsBad(self):
        expectedString = self.className + ".configure:  "
        with self.assertRaises(ValueError) as context:
            self.testDevice.configure(42)
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Minor:  failure to check for invalid environment") 
 
# serviceRequest   
    def test_300_010_ShouldDistributeZeroPositiveNegativeValues(self):
        numberOfBins = 2 ** 8
        sampleSize = 10000
        #    Elements of bins:
        #        [0]:  [lower range, upper range] of values
        #        [1]:  expected probability
        #        [2]:  expected number of observations of values within range
        #        [3]:  observed number 
        #        [4]:  [histogram of observations within lower range and upper range]
        bins = [
                [[0, 0], 0.25, 0, 0, [0 for _ in range(numberOfBins)]],
                [[1, 0x7fff], 0.50, 0, 0, [0 for _ in range(numberOfBins)]],
                [[0x7fff, 0xffff], 0.25, 0, 0, [0 for _ in range(numberOfBins)]]
                ]   
        for bin in bins:
            bin[2] = sampleSize * bin[1]
            
        # obtain samples, count:
        #    the number of values that fall into each range
        #    the number of values that fall into evenly distributed intervals within each range 
        for sample in range(sampleSize):
            value = int(self.testDevice.serviceRequest(), 16)
            for bin in bins:
                if((value >= bin[0][0]) & (value <= bin[0][1])):
                    bin[3] += 1
                    bin[4][value % numberOfBins] += 1
                    
        #  Determine if negative, zero, and positive values are roughly 25%, 25%, and 50% of observations
        #  Calculate Chi-square of negative-zero-positive distribution,
        #  2 degrees of freedom, alpha = 0.01
        chiSquare = 9.210340372
        observedDifference = 0.0
        for bin in bins:
            observedDifference += ((bin[3] - bin[2]) ** 2) / bin[2]
        self.assertLessEqual(observedDifference, chiSquare,
                             "Major:  negative-zero-positive values do not fit prescribed probabilities")
        
        #  For negative and positive values, determine if the values are distributed uniformly
        #  Calculate Chi-square of negative and positive observations
        #  2**8-1 degrees of freedom, alpha = 0.01
        chiSquare = 310.4573882
        for binNumber in range(1, len(bins)):
            bin = bins[binNumber]
            observedDifference = 0.0
            expectedObservations = bin[3] / numberOfBins
            for observedValues in bin[4]:
                observedDifference += ((observedValues - expectedObservations) ** 2) / expectedObservations
            self.assertLessEqual(observedDifference, chiSquare,
                                 "Major:  values are not uniformly distributed")
            
            
    def test_300_910_ShouldFailServiceRequestIfNotInitialized(self):
        expectedString = self.className + ".serviceRequest:"
        with self.assertRaises(ValueError) as context:
            testDevice = Device.Device()
            testDevice.serviceRequest()
            self.fail("Minor:  failure to check for initialization")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Minor: expected diagnostic not produced  ") 
    

import CA04.prod.Controller as Controller
import unittest
import gc


class ControllerTest(unittest.TestCase):

    def setUp(self):
        self.className = "Controller"
        self.testController = Controller.Controller()

    def tearDown(self):
        pass

# initialize(architecturefile)
    def test_100_010_ShouldReturnListOfDevices(self):
        expectedResult = ["Device", "StarSensor"]
        deviceList = self.testController.initialize("100010ValidFrameDevices.xml")
        deviceList.sort()
        self.assertListEqual(expectedResult, deviceList,
                             "Minor:  initialize() does not return correct devices")

    def test_100_020_ShouldReturnListOfDevicesWithUnorderedDefinition(self):
        expectedResult = ["Device", "StarSensor"]
        deviceList = self.testController.initialize("100020ValidFrameBeforeDefinitions.xml")
        deviceList.sort()
        self.assertListEqual(expectedResult, deviceList,
                             "Minor:  initialize() does not return correct devices")

    def test_100_910_ShouldDetectInvalidComponent(self):
        expectedString = self.className + ".initialize:"
        with self.assertRaises(ValueError) as context:
            self.testController.initialize("100910InvalidComponent.xml")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for invalid component")

    def test_100_920_ShouldDetectMissingComponentAttribute(self):
        expectedString = self.className + ".initialize:"
        with self.assertRaises(ValueError) as context:
            self.testController.initialize("100920MissingComponentAttribute.xml")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for missing component attribute on definition tag")

    def test_100_930_ShouldDetectMissingParm(self):
        expectedString = self.className + ".initialize:"
        with self.assertRaises(ValueError) as context:
            self.testController.initialize("100930MissingParm.xml")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for missing parm tag")

    def test_100_940_ShouldDetectInvalidParmName(self):
        expectedString = self.className + ".initialize:"
        with self.assertRaises(ValueError) as context:
            self.testController.initialize("100940InvalidParmName.xml")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for invalid name attribute on parm tag")

    def test_100_950_ShouldDetectInvalidParmAttribute(self):
        expectedString = self.className + ".initialize:"
        with self.assertRaises(ValueError) as context:
            self.testController.initialize("100950MissingParmName.xml")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for missing name attribute on parm tag")

    def test_100_960_ShouldDetectMissingParmValue(self):
        expectedString = self.className + ".initialize:"
        with self.assertRaises(ValueError) as context:
            self.testController.initialize("100960MissingParmValue.xml")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for missing parm value")

    def test_100_970_ShouldDetectInvalidParmValue(self):
        expectedString = self.className + ".initialize:"
        with self.assertRaises(ValueError) as context:
            self.testController.initialize("100970InvalidParmValue.xml")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for invalid parm value")

    def test_100_980_ShouldDetectInvalidFrameAttribute(self):
        expectedString = self.className + ".initialize:"
        with self.assertRaises(ValueError) as context:
            self.testController.initialize("100980InvalidFrameAttribute.xml")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for invalid frame attribute")

    def test_100_985_ShouldDetectMissingFrameDeviceValue(self):
        expectedString = self.className + ".initialize:"
        with self.assertRaises(ValueError) as context:
            self.testController.initialize("100985MissingFrameDeviceValue.xml")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for missing device value")

    def test_100_990_ShouldDetectInvalidFrameDevice(self):
        expectedString = self.className + ".initialize:"
        with self.assertRaises(ValueError) as context:
            self.testController.initialize("100990InvalidFrameDevice.xml")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)],
                          "Major:  failure to check for invalid device")

# run(microseconds)
    def test_200_010_ShouldCompleteOneFrame(self):
        expectedResults = [
                 [0, "Controller", "StarSensor", "serviceRequest"],
                 [40, "StarSensor", "Controller", "0028"],
             ]
        self.testController.initialize("200010OneFrameOneDevice.xml")
        self.testController.run(40)

        del self.testController
        gc.collect()
        self.compare2Log("200010LogFile.txt", expectedResults)

    def test_200_020_ShouldCompleteMultipleFrames(self):
        expectedResults = [
                 [0, "Controller", "StarSensor", "serviceRequest"],
                 [40, "StarSensor", "Controller", "0028"],
                 [10000000, "Controller", "StarSensor", "serviceRequest"],
                 [10000040, "StarSensor", "Controller", "0028"],
                 [20000000, "Controller", "StarSensor", "serviceRequest"],
                 [20000040, "StarSensor", "Controller", "0028"],
                 [30000000, "Controller", "StarSensor", "serviceRequest"],
                 [30000040, "StarSensor", "Controller", "fff4"],
                 [40000000, "Controller", "StarSensor", "serviceRequest"],
                 [40000040, "StarSensor", "Controller", "fff4"],
             ]
        self.testController.initialize("200020MultipleFramesMultipleDevices.xml")

        self.testController.run(40000040)
        del self.testController
        gc.collect()
        self.compare2Log("200020LogFile.txt", expectedResults)

    def test_200_030_ShouldCompleteMultipleFramesMultipleDevices(self):
        expectedResults = [
                 [None, "Controller", "StarSensor", "serviceRequest"],
                 [None, "StarSensor", "Controller", None],
                 [None, "Controller", "Device", "serviceRequest"],
                 [None, "Device", "Controller", None],
                 [None, "Controller", "StarSensor", "serviceRequest"],
                 [None, "StarSensor", "Controller", None],
                 [None, "Controller", "Device", "serviceRequest"],
                 [None, "Device", "Controller", None],
             ]
        self.testController.initialize("200030MultipleFramesMultipleDevices.xml")
        self.testController.run(150)
        del self.testController
        gc.collect()
        self.compare2Log("200030LogFile.txt", expectedResults)

    def test_200_040_ShouldReturnCompletionTime(self):
        self.testController.initialize("200040ReturnTime.xml")
        runTime = self.testController.run(10)
        self.assertEquals(40, runTime,
                          "Minor:  run() does not return the correct result")


# utility methods
    def compare2Log(self, logFile, expectedResults):
        with open(logFile, 'r') as logFile:
            loggedLines = logFile.readlines()
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

import CA03.prod.Controller as Controller
import unittest

class ControllerTest(unittest.TestCase):
    
    def setUp(self):
        self.controller = Controller.Controller()  
        
    # 100 constructor
    def test_100_010_ShouldConstruct(self):
        self.assertIsInstance(self.controller, Controller.Controller)
        
    # 200 initialize
    def test_200_910_shouldRejectNonExistFile(self):
        expectedString = "Controller.initialize:  "
        with self.assertRaises(ValueError) as context:
            self.controller.initialize('a.xml')                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
    
    def test_200_920_shouldRejectNonXmlFile(self):
        expectedString = "Controller.initialize:  "
        with self.assertRaises(ValueError) as context:
            self.controller.initialize('frameConfiguration.txt')                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
        
    def test_200_930_shouldRejectInvalidXmlFile1(self):
        expectedString = "Controller.initialize:  "
        with self.assertRaises(ValueError) as context:
            self.controller.initialize('wrongComponent.xml')                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])  
    
    def test_200_940_shouldRejectInvalidXmlFile2(self):
        expectedString = "Controller.initialize:"
        with self.assertRaises(ValueError) as context:
            self.controller.initialize('noFieldOfView.xml')                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])  
        
    def test_200_950_shouldRejectInvalidXmlFile3(self):
        expectedString = "Controller.initialize:"
        with self.assertRaises(ValueError) as context:
            self.controller.initialize('noStarSensorAttr.xml')                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
        
    def test_200_960_shouldRejectInvalidXmlFile4(self):
        expectedString = "Controller.initialize:"
        with self.assertRaises(ValueError) as context:
            self.controller.initialize('noMonitorLogFile.xml')                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])   
        
    def test_200_970_shouldRejectInvalidXmlFile5(self):
        expectedString = "Controller.initialize:"
        with self.assertRaises(ValueError) as context:
            self.controller.initialize('wrongRate.xml')                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])  
        
    def test_200_010_ShouldReturnList(self): 
        self.assertEqual(['Device', 'StarSensor'], self.controller.initialize('frameConfiguration.xml'))
        
    def test_200_020_ShouldReturnEmptyList(self):
        self.assertEqual([], self.controller.initialize('emptyFrame.xml'))
        

    # 300 run
    def test_300_910_shouldRejectNonIntegerParameter(self):
        expectedString = "Controller.run:  "
        with self.assertRaises(ValueError) as context:
            self.controller.run('aa')                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
        
    def test_300_920_shouldRejectNegetiveParameter(self):
        expectedString = "Controller.run:"
        with self.assertRaises(ValueError) as context:
            self.controller.run(-1)                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
        
    def test_300_930_shouldRejectInvalidConfigure(self):
        expectedString = "Controller.run:"
        with self.assertRaises(ValueError) as context:
            self.controller.run(10000)                                 
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
        
    def test_300_010_ShouldReturnRunTime1(self):
        self.controller.initialize('frameConfiguration.xml')
        self.assertEqual(1000120, self.controller.run(2000000))
        
    def test_300_020_ShouldReturnRunTime2(self):
        self.controller.initialize('frameConfiguration.xml')
        self.assertEqual(120, self.controller.run(40))
        
    def test_300_030_ShouldReturnRunTime4(self):
        self.controller.initialize('frameConfiguration.xml')
        self.controller.run(2000000)
        self.assertEqual(1000120, self.controller.run(2000000))
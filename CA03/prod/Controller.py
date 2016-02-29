'''
Created on Oct 27, 2015

@author: XING
'''

import os
import re
import math
import CA02.prod.StarSensor as StarSensor
import CA02.prod.Environment as Environment

import CA03.prod.Architecture as Architecture
import CA03.prod.Monitor as Monitor
import CA03.prod.Device as Device

import CA04.prod.SolarCollector as SolarCollector
#from xml.dom.minidom import parse

class Controller(object):
    '''
    Controller represents a supervisory component that oversees the operations of all devicesList on the satellite.
    Our satellite architecture is designed such that devicesList (e.g. StarSensor) respond to requests for information.
    They cannot provide information unless requested to do so.
    The Controller is the brain of the satellite.
    It communicates with each device in a prescribed order within a prescribed timeframe.
    '''
    DIAG_CLASS = "Controller."
    ValidDevices = ["Device", "StarSensor", "Controller", "SolarCollector"]

    def __init__(self):
        '''
        Constructor. Create an instance of Controller.
        Returns: An instance of Controller
        '''
        self.architecture = None
        #self.domTree = None
        self.environment = None #Environment.Environment()
        #self.environment = Environment.Environment()
        self.starSensor = None
        self.monitor = Monitor.Monitor()
        self.device = Device.Device()
        self.devicesList = []
        self.rate = None
        
        #self.degradation = 0
        self.solarCollector = SolarCollector.SolarCollector()
    
    def initialize(self, architectureFile = None):
        """
        Informs the controller about the satellite architecture.
        Returns: a list of unique dev in the architecture file.
        """
        diagMethod = "initialize:  "
        if (architectureFile == None or type(architectureFile) != str):
            raise ValueError(Controller.DIAG_CLASS + diagMethod + "missing filename parameter")
        #if not (len(architectureFile) > 4 and architectureFile[-4:] == ".xml"):
        pattern = re.compile('.+\.xml$')
        if (pattern.match(architectureFile) == None):
            raise ValueError(Controller.DIAG_CLASS + diagMethod + "not a valid xml file")
        if (not (os.path.isfile(architectureFile))):
            raise ValueError(Controller.DIAG_CLASS + diagMethod + "no file exists by the specified file name")
        self.architecture = Architecture.Architecture(architectureFile)
        #f = open(architectureFile)
        #try:
        #    self.domTree = parse(f)
        #except:
        #    raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid XML")
        startTime = 0
        degradation = 0
        
        domTree = self.architecture.domTree
        definitionTags = domTree.getElementsByTagName("definition")
        for defTag in definitionTags:
            if (not (defTag.hasAttribute('component'))):
                raise ValueError(Controller.DIAG_CLASS + diagMethod + "definitionTag tag has no component attribute")            
            c = defTag.getAttribute('component')
            if (c not in ["Environment", "Monitor", "StarSensor", "Device", "SolarCollector"]):
                raise ValueError(Controller.DIAG_CLASS + diagMethod + "no component called " + c + "exists") 
            parmTags = defTag.getElementsByTagName('parm')
            if (c == "Environment"):
                if (not parmTags):
                    raise ValueError(Controller.DIAG_CLASS + diagMethod + "missing parms") 
                for parmTag in parmTags:
                    if (not (parmTag.hasAttribute('name'))):
                        raise ValueError(Controller.DIAG_CLASS + diagMethod +"tag has no name attribute")
                    parmName = parmTag.getAttribute('name')
                    parmValue = self.architecture.parseContent(parmTag.childNodes)
                    if (parmName == "startTime"):
                        if (parmValue == None):
                            continue
                            #raise ValueError(Controller.DIAG_CLASS + diagMethod + "no startTime value")
                        try:
                            startTime = int(parmValue)
                        except ValueError:
                            raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid startTime value")
                        if (startTime < 0):
                            raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid startTime value")
                    elif (parmName == "rotationalPeriod"):
                        if (parmValue == None):
                            raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid rotationalPeriod value")
                        try:
                            rotationalPeriod = int(parmValue)
                        except ValueError:
                            raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid rotationalPeriod value")
                        #self.environment.setRotationalPeriod(rotationalPeriod)
                    elif (parmName == "degradation"):
                        if (parmValue == None):
                            continue
                            #raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid rotationalPeriod value")
                        try:
                            degradation = int(parmValue)
                        except ValueError:
                            raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid rotationalPeriod value")
                        if (degradation < 0 or degradation > 100):
                            raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid rotationalPeriod value")
                    else:
                        raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid environment parm name")
            elif (c == "Monitor"):
                if (not parmTags):
                    raise ValueError(Controller.DIAG_CLASS + diagMethod + "missing parms") 
                for parmTag in parmTags:
                    if (not (parmTag.hasAttribute('name'))):
                        raise ValueError(Controller.DIAG_CLASS + diagMethod +"tag has no name attribute")
                    parmName = parmTag.getAttribute('name')
                    parmValue = self.architecture.parseContent(parmTag.childNodes)
                    if (parmName == "logFile"):
                        if (parmValue == None):
                            raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid parm value")
                        try:
                            logFile = str(parmValue)
                            self.monitor.initialize(logFile)
                        except ValueError:
                            raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid parm value")
                    else:
                        raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid monitor parm name")
            elif (c == "StarSensor"):
                if (not parmTags):
                    raise ValueError(Controller.DIAG_CLASS + diagMethod + "missing parms") 
                for parmTag in parmTags:
                    if (not (parmTag.hasAttribute('name'))):
                        raise ValueError(Controller.DIAG_CLASS + diagMethod +"tag has no name attribute")
                    parmName = parmTag.getAttribute('name')
                    parmValue = self.architecture.parseContent(parmTag.childNodes)
                    if (parmName == "fieldOfView"):
                        if (parmValue == None):
                            raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid fov parm value")
                        try:
                            fov = float(parmValue)
                        except ValueError:
                            raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid fov parm value")
                        if not (fov > 0  and fov <= math.pi / 4):
                            raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid fov parm value")
                        self.starSensor = StarSensor.StarSensor(fov)
                    elif (parmName == "starFile"):
                        if (parmValue == None):
                            raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid starFile parm value")
                        try:
                            starFile = str(parmValue)
                        except ValueError:
                            raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid starFile parm value")
                        self.starSensor.initializeSensor(starFile)                       
                    else:
                        raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid star sensor parm name")
                
        self.environment = Environment.Environment(startTime, degradation)
        self.environment.setRotationalPeriod(rotationalPeriod)
        #self.degradation = degradation
                
        #components = self.architecture.getComponentDefinition()
        #for component in components:
        #    print component
        frameTags = self.architecture.domTree.getElementsByTagName("frame")
        for frame in frameTags:
            #r = frame.getAttribute("rate")
            try:
                rate = int(frame.getAttribute("rate"))
            except:
                raise ValueError(Controller.DIAG_CLASS + diagMethod + "the rate attribute has an invalid value")
            if (rate < 0):
                raise ValueError(Controller.DIAG_CLASS + diagMethod +  "Invalid frame rate")
            self.rate = rate
            
            devicesInFrame = frame.getElementsByTagName("device")
            for dev in devicesInFrame:
                if (not dev.childNodes):
                    raise ValueError(Controller.DIAG_CLASS + diagMethod + "missing frame device value")
                nodes = dev.childNodes
                for node in nodes:
                    if (str(node.data) not in Controller.ValidDevices):
                        raise ValueError(Controller.DIAG_CLASS + diagMethod + "invalid frame device value")
                    self.devicesList.append(str(node.data))
                    
        self.starSensor.configure(self.environment)
        self.monitor.configure(self.environment)
        self.device.configure(self.environment)
        self.solarCollector.configure(self.environment)
        
        #print self.devicesList            
        uniqueDevices = []
        for dev in self.devicesList:
            if dev not in uniqueDevices:
                uniqueDevices.append(dev)       
    
        return uniqueDevices
    
    def run(self, microseconds = None):
        """
        Runs the simulation for the specified number of microseconds.
        microseconds is a nonnegative integer.
        Returns: True
        """
        diagMethod = "run:  "
        if (microseconds == None or not isinstance(microseconds, (int, long))):
            raise ValueError(Controller.DIAG_CLASS + diagMethod + "not a valid microseconds parameter")
        if (microseconds <= 0):
            raise ValueError(Controller.DIAG_CLASS + diagMethod + "microseconds must be positive")
        if (self.environment == None):
            raise ValueError(Controller.DIAG_CLASS + diagMethod + "the controller has not been properly initialized")
        runStartTime = self.environment.getTime()
        while (self.environment.getTime() < microseconds + runStartTime):
            startTime = self.environment.getTime()
            for dev in self.devicesList:
                if (dev == "Device"):
                    self.monitor.serviceRequest("Controller", dev)
                    ret = self.device.serviceRequest()
                    self.monitor.serviceRequest(dev, "Controller", ret)
                elif (dev == "StarSensor"):
                    self.monitor.serviceRequest("Controller", dev)
                    ret = self.starSensor.serviceRequest()
                    self.monitor.serviceRequest(dev, "Controller", ret)
                elif (dev == "SolarCollector"):
                    self.monitor.serviceRequest("Controller", dev)
                    ret = self.solarCollector.serviceRequest()
                    self.monitor.serviceRequest(dev, "Controller", ret)
            elaspedTime = self.environment.getTime() - startTime
            if (self.environment.getTime() + self.rate - elaspedTime >= microseconds + runStartTime):
                break
            if (elaspedTime < self.rate):
                self.environment.incrementTime(self.rate - elaspedTime)
            #print self.environment.getTime()
        return self.environment.getTime() - runStartTime

    
#c = Controller()
#print c.initialize('frameConfiguration.xml')
#print c.run(int(24 * 3600 * 1e6 * 2))
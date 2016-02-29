'''
Created on Oct 27, 2015

@author: XING
'''

import os
import re

import CA02.prod.Environment as Environment

class Monitor(object):
    '''
    Monitor is a device whose purpose is to observe and record the following satellite events:
        1) requests the controller makes for service, and
        2) data returned to the controller in response to a service request
    '''
    DIAG_CLASS = "Monitor."

    def __init__(self):
        '''
        Constructor
        Returns: an instance of Monitor
        '''
        self.fileHandle = None
        self.fileName = None
        self.environment = None
        
    def initialize(self, logFile = None):
        """
        Informs the monitor where to store log information.
        Returns: boolean -- Is 'logFile' is a new file.
        """
        diagMethod = "initialize:  "
        if (logFile == None or type(logFile) != str):
            raise ValueError(Monitor.DIAG_CLASS + diagMethod + "missing filename parameter")
        pat = re.compile('.+\.txt$')
        if not (pat.match(logFile)):
            raise ValueError(Monitor.DIAG_CLASS + diagMethod + "not a valid .txt file")  
        if (self.fileName != None):
            return False
        self.fileName = logFile
        if (os.path.isfile(logFile)):
            return False
        else:
            return True
        
        #self.fileHandle = open(logFile, 'w')
        #if (os.path.isfile(logFile)):
        #    return False
        #else:
        #    return True
        
    def configure(self, environment = None):
        """
        Passes information about the simulation environment to the device.
        Returns: True
        """
        diagMethod = "configure:  "
        if (environment == None):
            raise ValueError(Monitor.DIAG_CLASS + diagMethod + "missing environment parameter")
        if not (isinstance(environment, Environment.Environment)):
            raise ValueError(Monitor.DIAG_CLASS + diagMethod + "non-environment parameter")
        self.environment = environment
        return True
    
    def serviceRequest(self, source = None, target = None, event = "serviceRequest"):
        """
        Logs simulated time, the device which originated the data, and the data itself.
        Returns: the integer time of the simulated clock.
        The information is recorded to the log file,
        or is discarded if no log file has been previously designated.
        """
        diagMethod = "serviceRequest:  "
        if (source == None or type(source) != str):
            raise ValueError(Monitor.DIAG_CLASS + diagMethod + "missing source parameter")
        if (target == None or type(source) != str):
            raise ValueError(Monitor.DIAG_CLASS + diagMethod + "missing target parameter")
        time = self.environment.getTime()
        line = str(time) + '\t' + source + '\t' + target + '\t' + event + '\n'
        #self.fileHandle.write(line)
        if (self.fileName != None):
            f = open(self.fileName, 'a')
            f.write(line)
            f.close()
        return time
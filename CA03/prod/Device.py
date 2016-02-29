'''
Created on Oct 27, 2015

@author: XING
'''

import random

import CA02.prod.Environment as Environment

class Device(object):
    '''
    Device is a generic satellite component that produces simulated results.
    '''
    DIAG_CLASS = "Device."
    LATENCY = 40

    def __init__(self):
        '''
        Constructor: create an instance of the device
        Returns: and instance of Device
        '''
        self.environment = None
        
    def configure(self, environment = None):
        """
        Passes information about the simulation environment to the device.
        Returns: True
        """
        diagMethod = "configure:  "
        if (environment == None):
            raise ValueError(Device.DIAG_CLASS + diagMethod + "missing environment paramiter")
        if not (isinstance(environment, Environment.Environment)):
            raise ValueError(Device.DIAG_CLASS + diagMethod + "non-environment parameter")
        self.environment = environment
        return True
    
    def serviceRequest(self):
        """
        Returns simulated bogus data.
        """
        diagMethod = "serviceRequest:  "
        if (self.environment == None):
            raise ValueError(Device.DIAG_CLASS + diagMethod + "configure() has not yet been called")
        rn1 = random.uniform(0, 1)
        if (rn1 <= 0.25):
            ret = "0000"
        elif (rn1 > .75):
            start = int("fffe", 16)  # 65534
            end = int("8000", 16)  # 32768
            rn2 = random.randint(end, start)
            #rn2 = 2 ** 16 - rn2 - 1
            ret = '{0:04x}'.format(rn2)
        else:
            start = int("0001", 16)  # 1
            end = int("7fff", 16)   # 32767
            rn2 = random.randint(start, end)
            ret = '{0:04x}'.format(rn2)
        self.environment.incrementTime(Device.LATENCY)
        return ret
    
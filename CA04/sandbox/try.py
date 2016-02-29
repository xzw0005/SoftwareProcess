'''
Created on Oct 27, 2015

@author: XING


import re

fname = '..xml'
print len(fname)
print fname[-4:] == ".xml"
pat = re.compile(".+\.xml$")
#print pat
m = pat.match(fname)
#if m:
if pat.match(fname):
    print "nima"
else:
    print "caonima"
    
'''

import CA02.prod.Environment as Environment

startTime = 0
degradation = 0
rotationalPeriod = 1000000000

myenvironment = Environment.Environment(startTime, degradation)
myenvironment.setRotationalPeriod(rotationalPeriod)

print isinstance(myenvironment, Environment.Environment)
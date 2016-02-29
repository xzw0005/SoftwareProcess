'''
Created on Oct 27, 2015

@author: XING
'''

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
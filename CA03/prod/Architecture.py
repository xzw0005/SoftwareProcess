#import xml.etree.ElementTree as ET

from xml.dom.minidom import  parse
class Architecture(object):

    def __init__(self, fileName):
        self.fileName = fileName
        source = open(fileName)
        try:
            self.domTree = parse(source)
        except:
            raise ValueError("Controller.__init__:  invalid XML")
        
    def getComponentDefinition(self):
        components = self.parseDefinitionTags(self.domTree)
        return components
        
    def parseDefinitionTags(self, domTree):
        components = []
        definitionTags = domTree.getElementsByTagName("definition")
        for tag in definitionTags:
            components.append(self.parseDefinitionTag(tag))
        return components
 
    def parseDefinitionTag(self, definitionTag):
        component = {}
        if (not (definitionTag.hasAttribute('component'))):
            raise ValueError("Controller.__init__: definitionTag tag has no component attribute")
        component['component'] = definitionTag.getAttribute('component')
        parmTags = definitionTag.getElementsByTagName('parm')
        component['parms'] = self.parseParmTags(parmTags)
        return component 
        
    def parseParmTags(self, parmTags):
        parameters = []
        for tag in parmTags:
            parameters.append(self.parseParmTag(tag))
        return parameters
    
    def parseParmTag(self, parmTag):
        if (not (parmTag.hasAttribute('name'))):
            raise ValueError("Controller.__init__: tag tag has no name attribute")
        parmName = parmTag.getAttribute('name')
        parmValue = self.parseContent(parmTag.childNodes)
        return({'name': parmName, 'value': parmValue})
        
            
    def parseContent(self, domSubTree):
        for node in domSubTree:
            if node.nodeType == node.TEXT_NODE:
                return node.data
        return None           
          
#==========================================================================================================
#  Usage:    getComponentDefinition returns a dictionary consisting of
#                    key:  component     value:  the value associated with the "component" attribute
#                    key:  parms         value:  a list of key/value pairs, defined as
#                                           key:  name   value:  the value associated with the "name" attribute
#                                           key:  value  value:  the information beteen <parm> and </parm>
"""
myArchitecture = Architecture('frameConfiguration.xml')
components = myArchitecture.getComponentDefinition()
for component in components:
    componentName = component['component']
    print ('Component {0}'.format(component['component']))
    parms = component['parms']
    for parm in parms:
        print('\tParameter name: {0} \t value: {1}'.format(parm['name'], parm['value']))
"""
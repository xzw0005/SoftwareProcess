class aClass():
    
    # pass a function as a parm
    def __init__(self, f):
        self.myFunction = f
        
    # call the function.  Note that it is called 
    # using the name of the variable in which 
    # the function was stored
    def callPassedFunction(self, value):
        return self.myFunction(value)
    

if __name__ == '__main__':
    # define the function to pass as a parm
    def aFunction(z):
        return z + 42
    
    # instantiate the class with the function
    myObject = aClass(aFunction)
    
    for aValue in range(0, 10):
        print(myObject.callPassedFunction(aValue))

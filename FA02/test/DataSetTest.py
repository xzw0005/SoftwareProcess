import unittest
import FA02.prod.DataSet as DataSet
import math


class TCurveTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
# Acceptance Tests
# Analysis
#    inputs
#        t ->   float .GT. 0  mandatory  unvalidated
#        tails  ->  {1,2}  mandatory unvalidated
#        n -> int .GE. 3 mandatory unvalided
#    outputs
#        float .GE. 0 and .LE. 1
#
# Happy path
#    nominal case:  p(1.8946, 7, 2)  -> .9
#    nominal case:  p(1.8946, 7, 1)  -> .95
#    edge case: p(0.2767, 1) -> 0.6
#    edge case: p(0.2767, 2) -> 0.2
#    edge case: p(0.
#    edge case:
# Sad path
#    t
#            non-float t:  p(t=1, n=7, tails=1)
#            out-of-bounds t:  p(t=-1, n=7,  tails=1)
#            missing t: p(n= 7, tails=1)
#    tails
#            invalid tails: p(t=1.8946, n=7, tails= 0)
#            missing tails:  p(t=1.8946, n=7)
#    n
#            non-int n:  p(t=1.8946, n=2.3, tails=1)
#            out-of-bounds n:  p(t=1.8946, n=2, tails=1)
#            missing n:  p(t=1.8946, tails=1)
#
# Design:
#    p -> LHP
#    p -> RHP
#    LHP -> gamma
#    RHP -> integrate
#    integrate -> f



# 100 constructor
# Happy path tests
    def test100_010_ShouldConstruct(self):
        self.assertIsInstance(DataSet.DataSet(), DataSet.DataSet)
        
        
# 200 gamma
# Analysis
#    inputs:
#        x: numeric mandatory validated
# Acceptance tests
# Happy path:
#    gamma(1)  -> 1
#    gamma(1/2)  -> sqrt(pi)
#    gamma(5)  ->  4*3*2*1*1 = 24
#    gamma(5/2) -> 3/2 * 1/2 * sqrt(pi) ~ 1.329
# Sad path:
#    none ... will prevalidate
# Design:  gamma algorithm
    def test200_010_ShouldReturnUpperTerminationCondition(self):
        myT = DataSet.DataSet()
        self.assertEquals(myT.gamma(1), 1)
        
    def test200_020_ShouldReturnLowerTerminationCondition(self):
        myT = DataSet.DataSet()
        self.assertEquals(myT.gamma(1.0 / 2.0), math.sqrt(math.pi))
        
    def test200_030_ShouldWorkOnIntegerX(self):
        myT = DataSet.DataSet()
        self.assertEquals(myT.gamma(5), 24)
        
    def test200_030_ShouldWorkOnHalfX(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.gamma(5.0 / 2.0), 1.329, 3)
        
# 300 LHP
# Analysis
#    inputs
#        n -> numeric  mandatory validated
#    outputs
#        float .GE. 0 
#
# Happy path
#    nominal case:  LHP(5) -> 
# Sad path
#    none ... will prevalidate
# Design:  equation
    def test300_010_ShouldCalculateLHP(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.LHP(5), 0.37960669, 4)
        
# 400 f
# Analysis
#    inputs
#        n -> numeric mandatory validated
#        u -> float mandatory validated
#    outputs
#        float .GE. 0
# Happy path
#    nominal case:  f(1) -> 0.5787
# Sad path
#    none ... will prevalidate
# Design:  equation
    def test400_010_ShouldCalculateFStarterCase(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.f(0, 5), 1, 4)
        
    def test400_020_ShouldCalculateF(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.f(1, 5), 0.578703704)
                
    
# 500 p
# Design:    if tails == 1, then integrate from 0 to t and add .5
#           if tails == 2, integrate from 0 to t and double
# Happy path
    def test500_010ShouldCalculateNominalCaseOneTail(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.p(1.8946, 7, 1), .95, 4)
        
    def test500_020ShouldCalculateNominalCaseTwoTail(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.p(1.8946, 7, 2), .90, 4)

    def test500_030ShouldEdgeLowTLowNOneTail(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.p(0.2767, 3, 1), 0.6, 4)        

    def test500_040ShouldEdgeLowTHighNOneTail(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.p(0.2567, 20, 1), 0.6, 4)    

    def test500_050ShouldEdgeHighTLowNOneTail(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.p(5.8409, 3, 1), .995, 4)
        
    def test500_060ShouldEdgeHighTHighNOneTail(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.p(2.8453, 20, 1), .995, 4)
        
# Sad path
    def test500_910ShouldRaiseExceptionOnMissingT(self):
        myT = DataSet.DataSet()
        with self.assertRaises(ValueError) as context:
            myT.p(n=7, tails=1)
    
    def test500_920ShouldRaiseExceptionOnBadT(self):
        myT = DataSet.DataSet()
        with self.assertRaises(ValueError) as context:
            myT.p(t=1, n=7, tails=1)
            
    def test500_930ShouldRaiseExceptionOnOutOfRangeT(self):
        myT = DataSet.DataSet()
        with self.assertRaises(ValueError) as context:
            myT.p(t=-1, n=7, tails=1)
            
    def test500_930ShouldRaiseExceptionInvalidTails(self):
        myT = DataSet.DataSet()
        with self.assertRaises(ValueError) as context:
            myT.p(t=-1, n=7, tails=0)
            
    def test500_940ShouldRaiseExceptionOnMissingTails(self):
        myT = DataSet.DataSet()
        with self.assertRaises(ValueError) as context:
            myT.p(t=-1, n=7)
            
    def test500_950ShouldRaiseExceptionOnMissingN(self):
        myT = DataSet.DataSet()
        with self.assertRaises(ValueError) as context:
            myT.p(t=-1, tails=1)
            
    def test500_950ShouldRaiseExceptionOnBadN(self):
        myT = DataSet.DataSet()
        with self.assertRaises(ValueError) as context:
            myT.p(t=-1, n=3.5, tails=1)
            
    def test500_960ShouldRaiseExceptionOnOutOfRangeN(self):
        myT = DataSet.DataSet()
        with self.assertRaises(ValueError) as context:
            myT.p(t=-1, n=2, tails=1)
 
 
 
# 600 RHP            
#------------- your tests go here --------------            
# Design:    Integration from 0 to t
# Analysis
#        inputs
#            t -> float mandatory validated
#            n -> numeric mandatory validated
#            f -> a function that implemented for test
# Happy path
#    different f cases: RHP(t, n, f) ->
#    different t cases:
#    different n cases:
#    nominal case:  RHP(t, n, f) -> 
# Sad path
#    DivideByZero exception
#    other ... pre-validated
# Design:  equation
            
# Happy path
    def f1(self, t, n):
        return t

    def test600_510ShouldCalculateEasyIntegration(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.RHP(1.0, 2, self.f1), 1.0 / 2, 4)
        
    def test600_520NShouldNotMatter(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.RHP(1.0, 99, self.f1), 1.0 / 2, 4)
        
        
    def f2(self, t, n):
        return t ** 2
    def test600_530ShouldCalculateEasyIntegration(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.RHP(1.0, 2, self.f2), 1.0 / 3, 4)
        
    def test600_540NShouldNotMatter(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.RHP(1.0, 99, self.f2), 1.0 / 3, 4)  
        
    def f3(self, t, n):
        return t ** 99
    def test600_550ShouldCalculateEasyIntegration(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.RHP(1.0, 99, self.f3), 1.0 / 100, 4)
        
    def f4(self, t, n):
        return math.exp(t)
    def test600_560ShouldCalculateExpIntegration(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.RHP(1.0, 99, self.f4), math.exp(1.0) - 1, 4)     
        
    def f5(self, t, n):
        return math.cos(t)
    def test600_570ShouldCalculateCosIntegration(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.RHP(1.0, 99, self.f5), math.sin(1), 4)     

        
    def test600_010_ShouldCalculateRHPNominalCase(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.RHP(1.0, 5, myT.f), 0.83874, 4)
        
    def test600_020_ShouldCalculateRHPVerySmallT(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.RHP(0.01, 5, myT.f), 0.0099998, 4)
        
    def test600_030_ShouldCalculateRHPSmallT(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.RHP(0.5, 2, myT.f), 0.47141, 4)
        
    def test600_040_ShouldCalculateRHPLargeN(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.RHP(1.0, 99, myT.f), 0.85473, 4)
        
    def test600_050_ShouldCalculateRHPLargeT(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.RHP(99.0, 2, myT.f), 1.41407, 4)
        
    def test600_060_ShouldCalculateRHPLargeNLargeT(self):
        myT = DataSet.DataSet()
        self.assertAlmostEquals(myT.RHP(99.0, 99, myT.f), 1.25648, 4)       
 
# Sad path 
#    DivideByZero exception,
#    which actually is not necessary, could be pre-validated in p
#    Other ... pre-validated      
    def test600_910_ShouldRaiseExceptionOnZeroDivisionError(self):
        myT = DataSet.DataSet()
        with self.assertRaises(ZeroDivisionError) as context:
            myT.RHP(0, 5, myT.f)
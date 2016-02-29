import unittest
import CA01.prod.StarCatalog as StarCat
import math
import os

class StarCatalogTest(unittest.TestCase):

#-----------------------
# 10 StarCatalog()
    def test10_010_ShouldInstantiateStarCatalog(self):
        self.assertIsInstance(StarCat.StarCatalog(), StarCat.StarCatalog)

#-----------------------
# 20 loadCatalog(starFile)
# happy path tests
    def test20_010_ShouldLoadCatalog(self):
        starCatalog = StarCat.StarCatalog()
        self.assertEquals(starCatalog.loadCatalog("Chart_TwoValidStars.txt"), 2)

    def test20_910_ShouldRequireParm(self):
        starCatalog = StarCat.StarCatalog()
        expectedString = "StarCatalog.loadCatalog:"
        try:
            self.assertRaises(ValueError, starCatalog.loadCatalog)
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")

# sad path tests
    def test20_920_ShouldRequireStringParm(self):
        starCatalog = StarCat.StarCatalog()
        expectedString = "StarCatalog.loadCatalog:"
        try:
            self.assertRaises(ValueError, starCatalog.loadCatalog, 42)
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")

    def test20_930_ShouldRequireFoundFile(self):
        starCatalog = StarCat.StarCatalog()
        expectedString = "StarCatalog.loadCatalog:"
        try:
            self.assertRaises(ValueError, starCatalog.loadCatalog, "missingfile")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")

    def test20_940_ShouldRejectInvalidStarData(self):
        starCatalog = StarCat.StarCatalog()
        expectedString = "StarCatalog.loadCatalog:"

        try:
            self.assertRaises(ValueError, starCatalog.loadCatalog,
            "Chart_InvalidStarData.txt")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString,
            diagnosticString[0:len(expectedString)])
        except:
            self.fail("incorrect exception was raised")

    def test20_950_ShouldRejectDuplicateStarDataInDifferentFiles(self):
        starCatalog = StarCat.StarCatalog()
        expectedString = "StarCatalog.loadCatalog:"

        try:
            self.assertRaises(ValueError, starCatalog.loadCatalog,
            "Chart_TwoValidStars.txt")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString,
            diagnosticString[0:len(expectedString)])
        except:
            self.fail("incorrect exception was raised")

    def test20_960_ShouldRejectDuplicateStarDataInSameFile(self):
        starCatalog = StarCat.StarCatalog()
        expectedString = "StarCatalog.loadCatalog:"

        try:
            self.assertRaises(ValueError, starCatalog.loadCatalog,
            "Chart_DupStarData.txt")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString,
            diagnosticString[0:len(expectedString)])
        except:
            self.fail("incorrect exception was raised")

#-----------------------
# 30 emptyCatalog
    def test30_010_ShouldEmptyCatalog(self):
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_TwoValidStars.txt")
        self.assertEqual(starCatalog.emptyCatalog(), 2)

# 40 getStarCount
    def test40_010ShouldReturnTotalCount(self):
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_TwoValidStars.txt")
        self.assertEqual(starCatalog.getStarCount(), 2)

    def test40_020ShouldUseDefaultLowerMagnitude(self):
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_TwoValidStars.txt")
        self.assertEqual(starCatalog.getStarCount(upperMagnitude=6.3), 1)

    def test40_030ShouldUseDefaultUpperMagnitude(self):
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_TwoValidStars.txt")
        self.assertEqual(starCatalog.getStarCount(lowerMagnitude=6.3), 1)

    def test40_040ShouldUseFindSingleMagnitude(self):
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_TwoValidStars.txt")
        self.assertEqual(starCatalog.getStarCount(6.2, 6.2), 1)

    def test40_050ShouldUseFindMagnitudeRange(self):
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_TwoValidStars.txt")
        self.assertEqual(starCatalog.getStarCount(5.0, 7.0), 2)

    def test40_910ShouldRejectBadLowerBound(self):
        starCatalog = StarCat.StarCatalog()
        expectedString = "StarCatalog.getStarCount:"
        try:
            self.assertRaises(ValueError, starCatalog.getStarCount, "a", 0.0)
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")

    def test40_920ShouldRejectBadUpperBound(self):
        starCatalog = StarCat.StarCatalog()
        expectedString = "StarCatalog.getStarCount:"
        try:
            self.assertRaises(ValueError, starCatalog.getStarCount, 0.0, "b")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")

    def test40_930ShouldRejectInvertedBounds(self):
        starCatalog = StarCat.StarCatalog()
        expectedString = "StarCatalog.getStarCount:"
        try:
            self.assertRaises(ValueError, starCatalog.getStarCount, 0.0, -1.0)
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
             self.fail("incorrect exception was raised")

#-----------------------
# 30 getMagnitude

    def test50_005ShouldNotFindStarsInEmptyCatalog(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (10.0 / 360.0) * 2.0 * math.pi
        dec = (45.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), None)

    def test50_007ShouldNotFindStarsInBlankFov(self):
        fov = (1.0 / 360.0) * 2.0 * math.pi
        ra = (20.0 / 360.0) * 2.0 * math.pi
        dec = (45.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_TwoValidStars.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), None)

    def test50_010ShouldFindBrightestStarInGeneralCase(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (20.0 / 360.0) * 2.0 * math.pi
        dec = (45.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_nominal.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), 1)

    def test0_020ShouldFindBrightestStarRaLowDecInLow(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (35.0 / 360.0) * 2.0 * math.pi
        dec = (45.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_nominal.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -1)

    def test50_030ShouldFindBrightestStarRaLowDecLow(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (50.0 / 360.0) * 2.0 * math.pi
        dec = (45.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_nominal.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -3)

    def test50_040ShouldFindBrightestStarRaLowDecInHigh(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (65.0 / 360.0) * 2.0 * math.pi
        dec = (45.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_nominal.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -5)

    def test50_050ShouldFindBrightestStarRaLowDecHi(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (80.0 / 360.0) * 2.0 * math.pi
        dec = (45.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_nominal.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -7)

    def test50_060ShouldFindBrightestStarRaHiDecInLow(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (170.0 / 360.0) * 2.0 * math.pi
        dec = (45.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_nominal.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -9)

    def test50_070ShouldFindBrightestStarRaHiDecLow(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (110.0 / 360.0) * 2.0 * math.pi
        dec = (45.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_nominal.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -11)

    def test50_080ShouldFindBrightestStarRaHiDecInLow(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (125.0 / 360.0) * 2.0 * math.pi
        dec = (45.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_nominal.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -13)

    def test50_090ShouldFindBrightestStarRaHiDecHi(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (140.0 / 360.0) * 2.0 * math.pi
        dec = (45.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_nominal.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -15)

    def test50_100ShouldFindBrightestStarRaBoundaryNegative1Only(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (2.0 / 360.0) * 2.0 * math.pi
        dec = (15.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_raBoundary.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), 1)

    def test50_110ShouldFindBrightestStarRaBoundaryNegative2Only(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (2.0 / 360.0) * 2.0 * math.pi
        dec = (30.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_raBoundary.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -1)

    def test50_120ShouldFindBrightestStarRaBoundaryNegative1And2(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (2.0 / 360.0) * 2.0 * math.pi
        dec = (45.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_raBoundary.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -3)

    def test50_130ShouldFindBrightestStarRaBoundaryNegativeDistractors(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (2.0 / 360.0) * 2.0 * math.pi
        dec = (60.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_raBoundary.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -5)

    def test50_140ShouldFindBrightestStarRaBoundary360Section1Only(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (358.0 / 360.0) * 2.0 * math.pi
        dec = (15.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_raBoundary2.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), 1)

    def test50_150ShouldFindBrightestStarRaBoundary360Section2Only(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (358.0 / 360.0) * 2.0 * math.pi
        dec = (30.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_raBoundary2.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -1)

    def test50_160ShouldFindBrightestStarRaBoundary360Section1And2(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (358.0 / 360.0) * 2.0 * math.pi
        dec = (45.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_raBoundary2.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -3)

    def test50_170ShouldFindBrightestStarRaBoundary360Distractors(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (358.0 / 360.0) * 2.0 * math.pi
        dec = (60.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_raBoundary2.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -5)

    def test50_180ShouldFindBrightestStarDecBoundarySection1(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (10.0 / 360.0) * 2.0 * math.pi
        dec = (89.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_DecBoundary.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), 1)

    def test50_190ShouldFindBrightestStarDecBoundarySection2Only(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (25.0 / 360.0) * 2.0 * math.pi
        dec = (89.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_DecBoundary.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -1)

    def test50_200ShouldFindBrightestStarDecBoundarySection1(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (40.0 / 360.0) * 2.0 * math.pi
        dec = (89.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_DecBoundary.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -3)

    def test50_210ShouldFindBrightestStarDecBoundaryDistractors(self):
        fov = (10.0 / 360.0) * 2.0 * math.pi
        ra = (55.0 / 360.0) * 2.0 * math.pi
        dec = (89.0 / 360.0) * 2.0 * math.pi
        starCatalog = StarCat.StarCatalog()
        starCatalog.loadCatalog("Chart_DecBoundary.txt")
        self.assertEquals(starCatalog.getMagnitude(ra, dec, fov), -5)

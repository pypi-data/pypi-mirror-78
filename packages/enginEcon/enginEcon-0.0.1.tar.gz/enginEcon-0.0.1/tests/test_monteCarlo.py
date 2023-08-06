# -*- coding: utf-8 -*-

from context import enginecon as ie
from numpy import irr,arange
import unittest

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""
    def test_distributions(self):
        pass
    def test_Risk(self):
        risk = ie.mc.risk(lambda x: x , {'x':[1,2,3,4,5]})
        risk.seq = arange(-50,51)
        assert risk.valueAtRisk(5) == 45.0
        assert risk.downsideRisk() == 50/101
        assert risk.upsidePotential() == 51/101
if __name__ == '__main__':
    unittest.main()

import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import numpy as np
from snf3x3.xgcd import xgcd

class TestXgcd(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInstantiate(self):
        vals = self._get_random_vals()
        r, s, t = xgcd(vals)
        print("%d = %d * (%d) + %d * (%d)" %
              (r, vals[0], s, vals[1], t))

    def _get_random_vals(self):
        vals = np.random.randint(100, size=2) + 1
        return vals

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestXgcd)
    unittest.TextTestRunner(verbosity=2).run(suite)

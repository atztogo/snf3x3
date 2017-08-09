import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import numpy as np
from snf3x3 import SNF3x3

class TestCore(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInstantiate(self):
        mat = self._get_random_mat()
        snf = SNF3x3(mat)
        print()
        print(snf.A)
        print(np.linalg.det(snf.A))
        snf.run()
        print(snf.A)
        print(np.linalg.det(snf.A))

        print("P")
        for P in np.array(snf.P):
            print(P)
        print("Q")
        for Q in np.array(snf.Q):
            print(Q)

    def _get_random_mat(self):
        k = 30
        mat = np.random.randint(k, size=(3, 3)) - k // 2
        if np.linalg.det(mat) < 0.5:
            mat = self._get_random_mat()
        return mat

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCore)
    unittest.TextTestRunner(verbosity=2).run(suite)

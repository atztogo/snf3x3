import unittest
import numpy as np
from snf3x3 import SNF3x3


class TestCore(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInstantiate(self):
        for i in range(100):
            mat = self._get_random_mat()
            snf = SNF3x3(mat)
            print()
            print(snf.A)
            detA = np.linalg.det(snf.A)
            print(detA)
            snf.run()

            print("PAQ")
            PAQ = np.dot(snf.P, np.dot(mat, snf.Q))
            print(PAQ)
            detPAQ = np.linalg.det(PAQ)
            print(detPAQ)

            np.testing.assert_almost_equal(np.linalg.det(snf.P), 1)
            np.testing.assert_almost_equal(np.linalg.det(snf.Q), 1)
            np.testing.assert_almost_equal(detPAQ, detA)

    def _get_random_mat(self):
        k = 15
        mat = np.random.randint(k, size=(3, 3)) - k // 2
        if np.linalg.det(mat) < 0.5:
            mat = self._get_random_mat()
        return mat


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCore)
    unittest.TextTestRunner(verbosity=2).run(suite)

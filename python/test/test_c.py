import unittest
import numpy as np
from snf3x3._snf3x3 import snf3x3
from snf3x3 import SNF3x3


def det(m):
    return (m[0, 0] * (m[1, 1] * m[2, 2] - m[1, 2] * m[2, 1])
            + m[0, 1] * (m[1, 2] * m[2, 0] - m[1, 0] * m[2, 2])
            + m[0, 2] * (m[1, 0] * m[2, 1] - m[1, 1] * m[2, 0]))


class TestC(unittest.TestCase):
    def setUp(self):
        self.verbose = False
        pass

    def tearDown(self):
        pass

    def _test_snf3x3(self, m):
        A = np.array(m, dtype='intc', order='C')
        P = np.zeros_like(A)
        Q = np.zeros_like(A)

        snf = SNF3x3(A)
        snf.run()

        _A = np.zeros_like(A)
        _A[:] = A
        snf3x3(_A, P, Q)

        if self.verbose:
            print("Python version")
            print(snf.A)
            print(snf.P)
            print(snf.Q)
            print(np.dot(np.dot(snf.P, A), snf.Q))
            print(det(A), det(snf.A), det(snf.P), det(snf.Q))
            print("C version")
            print(_A)
            print(P)
            print(Q)
            print(det(A), det(_A), det(P), det(Q))

        np.testing.assert_equal(snf.A, _A)
        np.testing.assert_equal(snf.P, P)
        np.testing.assert_equal(snf.Q, Q)
        np.testing.assert_equal(np.dot(np.dot(P, A), Q), _A)

        detA = det(A)
        assert det(_A) == detA * np.sign(detA)
        assert det(P) == 1
        assert det(Q) == np.sign(detA)

    def get_matrix(self):
        while True:
            m = np.random.randint(10, size=(3, 3), dtype='intc')
            if det(m) != 0:
                return m

    def test_c(self):
        for i in range(1000):
            m = self.get_matrix()
            if self.verbose:
                print("***** test %d *****" % (i + 1))
                print(m)
            self._test_snf3x3(m)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestC)
    unittest.TextTestRunner(verbosity=2).run(suite)

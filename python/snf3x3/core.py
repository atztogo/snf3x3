import numpy as np
from snf3x3.xgcd import xgcd


class SNF3x3(object):
    """Smith normal form for 3x3 matrix

    Input 3x3 interger matrix A is transformed to 3x3 diagonal interger
    matrix (D) by two 3x3 interger matrices P and Q, which is written as

        D = PAQ

    The algorithm implemented refers
    https://en.wikipedia.org/wiki/Smith_normal_form.

    Usage
    -----
    snf = SNF3x3(int_mat)
    snf.run()

    Attributes
    ----------
    D, P, Q : ndarray
        These 3x3 interger matrices explained above.
        shape=(3, 3), dtype='intc'

    """

    def __init__(self, A):
        """

        Parameters
        ----------
        A : array_like
            3x3 interger matrix.
            shape=(3, 3)

        """

        self._A_orig = np.array(A, dtype='intc', order='C')
        self._A = np.array(A, dtype='intc', order='C')
        self._Ps = []
        self._Qs = []
        self._L = []
        self._P = None
        self._Q = None
        self._D = None
        self._attempt = 0

    def run(self):
        for i in self:
            pass

    def __iter__(self):
        return self

    def __next__(self):
        self._attempt += 1
        if self._first():
            if self._second():
                self._set_PQ()
                raise StopIteration
        return self._attempt

    def next(self):
        self.__next__()

    @property
    def A(self):
        return self._A

    @property
    def D(self):
        return self._D

    @property
    def P(self):
        return self._P

    @property
    def Q(self):
        return self._Q

    def _set_PQ(self):
        if np.linalg.det(self._A) < 0:
            for i in range(3):
                if self._A[i, i] < 0:
                    self._flip_sign_row(i)
            self._Ps += self._L
            self._L = []

        P = np.eye(3, dtype='intc')
        for _P in self._Ps:
            P = np.dot(_P, P)
        Q = np.eye(3, dtype='intc')
        for _Q in self._Qs:
            Q = np.dot(Q, _Q.T)

        if np.linalg.det(P) < 0:
            P = -P
            Q = -Q

        self._P = P
        self._Q = Q
        self._D = self._A.copy()

    def _first(self):
        self._first_one_loop()
        A = self._A
        if A[1, 0] == 0 and A[2, 0] == 0:
            return True
        elif A[1, 0] % A[0, 0] == 0 and A[2, 0] % A[0, 0] == 0:
            self._first_finalize()
            self._Ps += self._L
            self._L = []
            return True
        else:
            return False

    def _first_one_loop(self):
        self._first_column()
        self._Ps += self._L
        self._L = []
        self._A = self._A.T
        self._first_column()
        self._Qs += self._L
        self._L = []
        self._A = self._A.T

    def _first_column(self):
        i = self._search_first_pivot()
        if i > 0:
            self._swap_rows(0, i)

        if self._A[1, 0] != 0:
            self._zero_first_column(1)
        if self._A[2, 0] != 0:
            self._zero_first_column(2)

    def _zero_first_column(self, j):
        if self._A[j, 0] < 0:
            self._flip_sign_row(j)
        A = self._A
        r, s, t = xgcd([A[0, 0], A[j, 0]])
        self._set_zero(0, j, A[0, 0], A[j, 0], r, s, t)

    def _search_first_pivot(self):
        A = self._A
        for i in range(3):  # column index
            if A[i, 0] != 0:
                return i

    def _first_finalize(self):
        """Set zeros along the first colomn except for A[0, 0]

        This is possible only when A[1,0] and A[2,0] are dividable by A[0,0].

        """

        A = self._A
        L = np.eye(3, dtype='intc')
        L[1, 0] = -A[1, 0] // A[0, 0]
        L[2, 0] = -A[2, 0] // A[0, 0]
        self._L.append(L.copy())
        self._A = np.dot(L, self._A)

    def _second(self):
        """Find Smith normal form for Right-low 2x2 matrix"""

        self._second_one_loop()
        A = self._A
        if A[2, 1] == 0:
            return True
        elif A[2, 1] % A[1, 1] == 0:
            self._second_finalize()
            self._Ps += self._L
            self._L = []
            return True
        else:
            return False

    def _second_one_loop(self):
        self._second_column()
        self._Ps += self._L
        self._L = []
        self._A = self._A.T
        self._second_column()
        self._Qs += self._L
        self._L = []
        self._A = self._A.T

    def _second_column(self):
        """Right-low 2x2 matrix

        Assume elements in first row and column are all zero except for A[0,0].

        """

        if self._A[1, 1] == 0 and self._A[2, 1] != 0:
            self._swap_rows(1, 2)

        if self._A[2, 1] != 0:
            self._zero_second_column()

    def _zero_second_column(self):
        if self._A[2, 1] < 0:
            self._flip_sign_row(2)
        A = self._A
        r, s, t = xgcd([A[1, 1], A[2, 1]])
        self._set_zero(1, 2, A[1, 1], A[2, 1], r, s, t)

    def _second_finalize(self):
        """Set zero at A[2, 1]

        This is possible only when A[2,1] is dividable by A[1,1].

        """

        A = self._A
        L = np.eye(3, dtype='intc')
        L[2, 1] = -A[2, 1] // A[1, 1]
        self._L.append(L.copy())
        self._A = np.dot(L, self._A)

    def _swap_rows(self, i, j):
        """Swap i and j rows

        As the side effect, determinant flips.

        """

        L = np.eye(3, dtype='intc')
        L[i, i] = 0
        L[j, j] = 0
        L[i, j] = 1
        L[j, i] = 1
        self._L.append(L.copy())
        self._A = np.dot(L, self._A)

    def _flip_sign_row(self, i):
        """Multiply -1 for all elements in row"""

        L = np.eye(3, dtype='intc')
        L[i, i] = -1
        self._L.append(L.copy())
        self._A = np.dot(L, self._A)

    def _set_zero(self, i, j, a, b, r, s, t):
        """Let A[i, j] be zero based on Bezout's identity

           [ii ij]
           [ji jj] is a (k,k) minor of original 3x3 matrix.

        """

        L = np.eye(3, dtype='intc')
        L[i, i] = s
        L[i, j] = t
        L[j, i] = -b // r
        L[j, j] = a // r
        self._L.append(L.copy())
        self._A = np.dot(L, self._A)

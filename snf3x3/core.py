import numpy as np
from snf3x3.xgcd import xgcd

class SNF3x3(object):
    def __init__(self, A):
        self._A_orig = np.array(A, dtype='intc')
        self._A = np.array(A, dtype='intc')
        self._P = []
        self._Q = []
        self._L = None
        self._R = None

    def run(self):
        self._first_column()

    def _first_column_and_row(self):
        i = self._search_first_pivot()
        if i > 0:
            self._swap_rows(0, i)

        A = self._A
        if A[1, 0] != 0:
            j = 1
        elif A[2, 0] != 0:
            j = 2
        else:
            return None

        r, s, t = xgcd([A[0, 0], A[j, 0]])
        self._zero_row(0, j, A[0, 0], A[j, 0], r, s, t)

        if j == 1:
            A = self._A
            r, s, t = xgcd([A[0, 0], A[2, 0]])
            self._zero_row(0, 2, A[0, 0], A[2, 0], r, s, t)

    def __str__(self):
        return str(self._A)

    def _search_first_pivot(self):
        A = self._A
        for i in range(3): # column index
            if A[i, 0] != 0:
                return i

    def _swap_rows(self, i, j):
        L = np.eye(3, dtype='intc')
        L[i, i] = 0
        L[j, j] = 0
        L[i, j] = 1
        L[j, i] = 1
        self._L = L
        self._P.append(L.copy())
        self._A = np.dot(L, self._A)

    def _swap_columns(self, i, j):
        R = np.eye(3, dtype='intc')
        R[i, i] = 0
        R[j, j] = 0
        R[i, j] = 1
        R[j, i] = 1
        self._R = R
        self._Q.append(R.copy())
        self._A = np.dot(self._A, R)

    def _zero_row(self, i, j, a, b, r, s, t):
        """ [ii ij]
            [ji jj] is a (k,k) minor of original 3x3 matrix.
        """

        L = np.eye(3, dtype='intc')
        L[i, i] = s
        L[i, j] = t
        L[j, i] = -b // r
        L[j, j] = a // r
        self._L = L
        self._P.append(L.copy())
        self._A = np.dot(L, self._A)

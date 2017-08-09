import numpy as np
from snf3x3.xgcd import xgcd

class SNF3x3(object):
    def __init__(self, A):
        self._A_orig = np.array(A, dtype='intc')
        self._A = np.array(A, dtype='intc')
        self._P = []
        self._Q = []
        self._L = []
        self._attempt = 0

    def run(self):
        for i in self:
            pass

    def __iter__(self):
        return self

    def __next__(self):
        self._attempt += 1
        if self._first():
            raise StopIteration
        return self._attempt

    def next(self):
        self.__next__()

    @property
    def A(self):
        return self._A

    @property
    def P(self):
        return self._P

    @property
    def Q(self):
        return self._Q

    def _first(self):
        print("attempt %d" % self._attempt)
        self._first_one_loop()
        A = self._A
        if A[1, 0] == 0 and A[2, 0] == 0:
            return True
        elif A[1, 0] % A[0, 0] == 0 and A[2, 0] % A[0, 0] == 0:
            self._first_finalize()
            self._P += self._L
            self._L = []
            return True
        else:
            return False

    def _first_one_loop(self):
        self._first_column()
        self._P += self._L
        self._L = []
        self._A = self._A.T
        self._first_column()
        self._Q += self._L
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
            self._flip_row(j)
        A = self._A
        r, s, t = xgcd([A[0, 0], A[j, 0]])
        self._zero_column(0, j, A[0, 0], A[j, 0], r, s, t)

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
        L[j, i] = -1
        self._L.append(L.copy())
        self._A = np.dot(L, self._A)

    def _flip_row(self, i):
        L = np.eye(3, dtype='intc')
        L[i, i] = -1
        self._L.append(L.copy())
        self._A = np.dot(L, self._A)

    def _zero_column(self, i, j, a, b, r, s, t):
        """ [ii ij]
            [ji jj] is a (k,k) minor of original 3x3 matrix.
        """
        L = np.eye(3, dtype='intc')
        L[i, i] = s
        L[i, j] = t
        L[j, i] = -b // r
        L[j, j] = a // r
        self._L.append(L.copy())
        self._A = np.dot(L, self._A)

    def _first_finalize(self):
        print("finalize")
        A = self._A
        L = np.eye(3, dtype='intc')
        L[1, 0] = -A[1, 0] // A[0, 0]
        L[2, 0] = -A[2, 0] // A[0, 0]
        self._L.append(L.copy())
        self._A = np.dot(L, self._A)

import numpy as np

def xgcd(vals):
    _xgcd = Xgcd(vals)
    return _xgcd.run()

class Xgcd(object):
    def __init__(self, vals):
        self._vals = np.array(vals, dtype='intc')

    def run(self):
        r0, r1 = self._vals
        s0 = 1
        s1 = 0
        t0 = 0
        t1 = 1
        for i in range(100):
            r0, r1, s0, s1, t0, t1 = self._step(r0, r1, s0, s1, t0, t1)
            if r1 == 0:
                break
        self._rst = np.array([r0, s0, t0], dtype='intc')
        return self._rst

    def _step(self, r0, r1, s0, s1, t0, t1):
        q, m = divmod(r0, r1)
        r2 = m
        s2 = s0 - q * s1
        t2 = t0 - q * t1
        return r1, r2, s1, s2, t1, t2

    def __str__(self):
        v = self._vals
        r, s, t = self._rst
        return "%d = %d * (%d) + %d * (%d)" % (r, v[0], s, v[1], t)

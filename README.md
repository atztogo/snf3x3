# snf3x3
Computing Smith normal form like 3x3 integer matrices.

This is an implementation of algorithm found at wikipedia,
https://en.wikipedia.org/wiki/Smith_normal_form. But this
implementation only works for 3x3 integer matricies.

An integer 3x3 matrix A is transformed to PDQ, where D is an integer
diagonal matrix of det(D) >= 0, and P and Q are unimodular matricies
of det(P)=1 and det(Q)=sgn(det(A)).

Python and C implementations are found in `python` and `c`
directories, respectively.
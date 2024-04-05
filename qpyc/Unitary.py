from qpyc.Device import Circuit, MZI
import numpy as np
from math import factorial

from jax import jit

def p2s(pat, width):
    '''
    Convert pattern number to state.
    eg [3,4] width 6 <=> [0,0,1,1,0,0]
    '''
    assert max(pat) <= width
    # return [1 if i in pat else 0 for i in range(1,width+1)]
    return [pat.count(i) for i in range(width)]


def s2p(state):
    '''
    Convert state tp pattern number.
    eg [3,4] width 6 <=> [0,0,1,1,0,0]
    '''
    ll = [[i]*state[i] for i in range(len(state)) if state[i] != 0]
    return [i for l in ll for i in l]

@jit
def nnperm(M):
    """
    Numpy code for computing the permanent of a matrix,
    from https://github.com/scipy/scipy/issues/7151.
    """
    n = M.shape[0]
    d = np.ones(n)
    j = 0
    s = 1
    f = np.arange(n)
    v = M.sum(axis=0)
    p = np.prod(v)
    while (j < n - 1):
        v -= 2 * d[j] * M[j]
        d[j] = -d[j]
        s = -s
        prod = np.prod(v)
        p += s * prod
        f[0] = 0
        f[j] = f[j + 1]
        f[j + 1] = j + 1
        j = f[0]
    return p / 2 ** (n - 1)

@jit
def chatnnperm(M):
    n = M.shape[0]
    p = np.prod(M.sum(axis=0))
    s = 1
    j = 0
    while j < n - 1:
        v = np.sum(M, axis=0) - 2 * s * M[j]
        s = -s
        p += s * np.prod(v)
        j = 0 if j == 0 else j + 1
    return p / 2 ** (n - 1)

def samp(mat, x, y):
    assert sum(x) == sum(y)
    matrix = mat[s2p(x)][:, s2p(y)]
    divisor = np.sqrt(np.prod([factorial(n) for n in x + y]))
    return nnperm(matrix) / divisor

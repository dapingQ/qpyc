from qpyc.Unitary import nnperm, samp, s2p, p2s
from qpyc.Unitary import square_decomposition_right
from scipy.stats import unitary_group



import numpy as np
from math import factorial

x = [1, 2, 0, 0]
y = [1, 1, 1, 0]


def test_perm():    
    uni = unitary_group.rvs(4)
    uni = np.arange(16).reshape(4,4)
    # print(samp(uni, [1, 1, 1, 0], [1, 1, 0, 1]))
    
    print(nnperm(uni))    


def test_decom():
    uni = unitary_group.rvs(6)
    # uni = np.eye(6)
    print(square_decomposition_right(uni))

if __name__ == '__main__':
    # test_perm()
    test_decom()
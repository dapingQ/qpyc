from qpyc.Unitary import nnperm, samp, s2p, p2s
from qpyc.Unitary import chatnnperm
from scipy.stats import unitary_group

import numpy as np
from math import factorial

x = [1, 2, 0, 0]
y = [1, 1, 1, 0]

if __name__ == '__main__':
    uni = unitary_group.rvs(4)
    uni = np.arange(16).reshape(4,4)
    # print(samp(uni, [1, 1, 1, 0], [1, 1, 0, 1]))
    
    print(nnperm(uni))    
    print(chatnnperm(uni))    

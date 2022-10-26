import numpy as np
from qpic.chip import Component, Circuit

def test_circuit():
    A = Component((0,0))
    B = Component((0,2))
    A.matrix =  np.array([
        [1,2],
        [3,4]
    ])
    B.matrix =  np.array([
        [1,2],
        [3,4]
    ])
    C = Circuit()
    C.add(A)
    C.add(B)
    print(C.matrix)

# C = Circuit()
# C.devices = [Component((4,0)), Component((0,2)), Component((1,1))]
# print(C.devices)

# if __name__ == "__main__":
#     test_circuit()